"""Views Auth extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from django.http import HttpResponseRedirect
from api.background_agent.oauth import (
    SESSION_STATE_KEY as BACKGROUND_AGENT_OAUTH_STATE_KEY,
    STATE_PREFIX as BACKGROUND_AGENT_STATE_PREFIX,
    exchange_and_store as store_background_agent_github,
    parse_state as parse_background_agent_state,
)
from .background_agent_auth import SESSION_KEY as BACKGROUND_AGENT_ADMIN_SESSION_KEY


class DeepLinkRedirect(HttpResponseRedirect):
    allowed_schemes = ["http", "https", "ftp", "nebians"]


def deep_link(url):
    return DeepLinkRedirect(url)

def login_page(request):
    if api.get_session_token(request):
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url and next_url.startswith('/') and not next_url.startswith('//'):
            return redirect(next_url)
        return redirect('web:home')
    stats = cache.get('login_stats')
    if stats is None:
        from django.db.models import Sum
        total_resources = Resource.objects.filter(approval_status='approved').count()
        total_users = User.objects.count()
        total_posts = Post.objects.filter(is_archived=False).count()
        recent_resources = list(Resource.objects.filter(approval_status='approved').select_related('uploaded_by').order_by('-added_at')[:3].values('title', 'subject', 'type', 'added_at'))
        for r in recent_resources:
            r['type_label'] = dict(Resource.EXAM_TYPES).get(r.get('type', ''), r.get('type', 'PDF'))
        stats = {
            'total_resources': total_resources,
            'total_users': total_users,
            'total_posts': total_posts,
            'recent_resources': recent_resources,
        }
        cache.set('login_stats', stats, 300)
    return render(request, 'web/login.html', _ctx(request, login_stats=stats))

@require_POST
def google_auth(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Check for email auth token (from email login flow)
    email_auth_token = data.get('emailAuthToken')
    if email_auth_token:
        try:
            user = get_user_by_auth_token(email_auth_token)
            token = email_auth_token
            user_data = _normalize_user_data(UserSerializer(user).data)
            user_data['isNewUser'] = data.get('emailUser', {}).get('isNewUser', False)
            profile_incomplete = not user.display_name or not user.gender or not user.class_level
            user_data['profileIncomplete'] = data.get('emailUser', {}).get('profileIncomplete', profile_incomplete)
            api.set_session_auth(request, token, user_data)
            return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': user_data.get('isNewUser', False), 'profileIncomplete': user_data.get('profileIncomplete', False)})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid auth token'}, status=401)

    id_token = data.get('idToken', '')
    if not id_token:
        logger.warning('google_auth: no idToken in request body. Keys: %s', list(data.keys()))
        return JsonResponse({'error': 'idToken is required'}, status=400)

    logger.info('google_auth: verifying token (length=%d)', len(id_token))
    google_info = verify_google_token(id_token)
    if not google_info:
        logger.warning('google_auth: Google token verification failed')
        return JsonResponse({'error': 'Invalid Google ID Token'}, status=401)
    user_id = google_info['userId']
    email = google_info.get('email') or ''
    display_name = google_info.get('displayName') or ''
    photo_url = google_info.get('photoUrl') or ''
    try:
        db_user = User.objects.get(pk=user_id)
        if getattr(db_user, 'is_banned', False):
            return JsonResponse({'error': 'This account has been banned'}, status=403)
        token = issue_auth_token(db_user)
        user_data = _normalize_user_data(UserSerializer(db_user).data)
        user_data['isNewUser'] = False
        api.set_session_auth(request, token, user_data)
        logger.info('google_auth: existing user signed in: %s', db_user.username or db_user.id)
        return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': False})
    except User.DoesNotExist:
        pass
    provider_verified = bool(google_info.get('email_verified', False))
    if email and provider_verified:
        try:
            existing = User.objects.get(email__iexact=email)
            if not existing.email_verified:
                logger.warning('google_auth: refusing link to unverified account (email=%s)', email)
                return JsonResponse({'error': 'An account with this email exists but is not verified. Please verify it or log in with your password first.'}, status=409)
            token = issue_auth_token(existing)
            user_data = _normalize_user_data(UserSerializer(existing).data)
            user_data['isNewUser'] = False
            api.set_session_auth(request, token, user_data)
            logger.info('google_auth: linked %s to existing user %s (email=%s)', user_id, existing.id, email)
            return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': False})
        except User.DoesNotExist:
            pass
    if email and User.objects.filter(email__iexact=email).exists():
        return JsonResponse({'error': 'An account with this email already exists. Please log in with your original sign-in method first.'}, status=409)
    auth_token = User.generate_token()
    temp_username = f"user_{user_id[:8]}"
    db_user = User(
        pk=user_id,
        username=temp_username,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        email_verified=provider_verified,
        created_at=now_ms()
    )
    db_user.auth_token = hash_auth_token(auth_token)
    db_user.save()
    token = auth_token
    user_data = _normalize_user_data(UserSerializer(db_user).data)
    user_data['isNewUser'] = True
    api.set_session_auth(request, token, user_data)
    logger.info('google_auth: new user created: %s (temp_username=%s)', user_id, temp_username)
    return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': True})

def google_login(request):
    """Kick off Google OAuth2 redirect flow — fully custom button, no GIS chrome."""
    client_id = settings.GOOGLE_CLIENT_ID
    if not client_id:
        return HttpResponse('Google OAuth is not configured.', status=501)
    redirect_uri = _https_redirect_uri(request, '/auth/google/callback/')
    state = request.GET.get('state', '')
    if not state:
        next_url = request.GET.get('next')
        if next_url and next_url.startswith('/') and not next_url.startswith('//'):
            state = f"next:{next_url}"
    authorize_url = (
        f'https://accounts.google.com/o/oauth2/v2/auth'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        f'&response_type=code'
        f'&scope=openid+email+profile'
        f'&prompt=select_account'
        f'&access_type=online'
    )
    if state:
        authorize_url += f'&state={state}'
    return redirect(authorize_url)

def google_oauth_callback(request):
    """Handle Google OAuth2 code → exchange for tokens → verify id_token → login/signup."""
    state = request.GET.get('state', '')
    is_mobile = state == 'mobile_google'
    next_url = None
    if state and state.startswith('next:'):
        next_url = state[5:]
    code = request.GET.get('code')
    if not code:
        if is_mobile:
            return deep_link('nebians://auth-callback?error=cancelled')
        messages.error(request, 'Google sign-in was cancelled.')
        return redirect('web:login')
    redirect_uri = _https_redirect_uri(request, '/auth/google/callback/')
    try:
        import requests as _req
        token_resp = _req.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            },
            timeout=10,
        )
        token_data = token_resp.json()
    except Exception as e:
        logger.error('google_oauth_callback: token exchange failed: %s', e)
        if is_mobile:
            return deep_link('nebians://auth-callback?error=token_exchange_failed')
        messages.error(request, 'Google sign-in failed. Please try again.')
        return redirect('web:login')
    id_token = token_data.get('id_token')
    if not id_token:
        logger.error('google_oauth_callback: no id_token in response: %s', token_data)
        if is_mobile:
            return deep_link('nebians://auth-callback?error=no_id_token')
        messages.error(request, 'Google sign-in failed. Please try again.')
        return redirect('web:login')
    google_info = verify_google_token(id_token)
    if not google_info:
        if is_mobile:
            return deep_link('nebians://auth-callback?error=token_verification_failed')
        messages.error(request, 'Google token verification failed.')
        return redirect('web:login')
    user_id = google_info['userId']
    email = google_info.get('email') or ''
    display_name = google_info.get('displayName') or ''
    photo_url = google_info.get('photoUrl') or ''
    try:
        db_user = User.objects.get(pk=user_id)
        if getattr(db_user, 'is_banned', False):
            messages.error(request, 'This account has been banned.')
            return redirect('web:login')
        token = issue_auth_token(db_user)
        user_data = _normalize_user_data(UserSerializer(db_user).data)
        user_data['isNewUser'] = False
        api.set_session_auth(request, token, user_data)
        logger.info('google_oauth_callback: existing user signed in: %s', db_user.username or db_user.id)
        if is_mobile:
            return deep_link(f'nebians://auth-callback?authToken={token}&isNewUser=false&username={db_user.username}')
        if next_url:
            return redirect(next_url)
        return redirect('web:home')
    except User.DoesNotExist:
        pass
    redirect_result, linked = _link_oauth_user(request, email, user_id, display_name, photo_url, 'google_oauth_callback', provider_verified=bool(google_info.get('email_verified', False)))
    if linked:
        if is_mobile:
            linked_token = api.get_session_token(request) or ''
            linked_user = User.objects.get(email__iexact=email)
            return deep_link(f'nebians://auth-callback?authToken={linked_token}&isNewUser=false&username={linked_user.username}')
        if next_url:
            return redirect(next_url)
        return redirect_result
    auth_token = User.generate_token()
    temp_username = f"user_{user_id[:8]}"
    if email and User.objects.filter(email__iexact=email).exists():
        messages.error(request, 'An account with this email already exists. Please log in with your original sign-in method first.')
        return redirect('web:login')
    db_user = User(
        pk=user_id,
        username=temp_username,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        email_verified=bool(google_info.get('email_verified', False)),
        created_at=now_ms()
    )
    db_user.auth_token = hash_auth_token(auth_token)
    db_user.save()
    token = auth_token
    user_data = _normalize_user_data(UserSerializer(db_user).data)
    user_data['isNewUser'] = True
    api.set_session_auth(request, token, user_data)
    logger.info('google_oauth_callback: new user created: %s (temp_username=%s)', user_id, temp_username)
    if is_mobile:
        return deep_link(f'nebians://auth-callback?authToken={auth_token}&isNewUser=true&username={temp_username}')
    if next_url:
        return redirect(f"{reverse('web:edit_profile')}?next={next_url}")
    return redirect('web:edit_profile')

def github_login(request):
    """Redirect user to GitHub OAuth authorization page."""
    client_id = settings.GITHUB_CLIENT_ID
    if not client_id:
        return HttpResponse('GitHub OAuth is not configured.', status=501)
    redirect_uri = _https_redirect_uri(request, '/auth/github/callback/')
    state = request.GET.get('mobile', '')
    if state == '1':
        state = 'mobile_github'
    else:
        next_url = request.GET.get('next')
        if next_url and next_url.startswith('/') and not next_url.startswith('//'):
            state = f"next:{next_url}"
        else:
            state = ''
    authorize_url = (
        f'https://github.com/login/oauth/authorize'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        f'&scope=read:user,user:email'
    )
    if state:
        authorize_url += f'&state={state}'
    return redirect(authorize_url)

@require_GET
def github_callback(request):
    """Handle GitHub OAuth callback — exchange code for token, fetch user, create/login."""
    state = request.GET.get('state', '')
    if state.startswith(BACKGROUND_AGENT_STATE_PREFIX):
        import secrets
        background_admin_id = parse_background_agent_state(state)
        expected_state = request.session.pop(BACKGROUND_AGENT_OAUTH_STATE_KEY, '')
        signed_in_admin_id = request.session.get(BACKGROUND_AGENT_ADMIN_SESSION_KEY)
        if (
            not background_admin_id
            or not expected_state
            or not secrets.compare_digest(str(state), str(expected_state))
            or str(signed_in_admin_id or '') != str(background_admin_id)
        ):
            return HttpResponse('Invalid or expired background-agent OAuth state.', status=403)
        code = request.GET.get('code')
        if not code:
            messages.error(request, 'GitHub authorization was cancelled.')
            return redirect('web:background_agent')
        try:
            admin_user = User.objects.get(pk=background_admin_id, is_admin=True, is_locked=False, is_bot=False)
        except User.DoesNotExist:
            return HttpResponse('Invalid background-agent administrator.', status=403)
        redirect_uri = _https_redirect_uri(request, '/auth/github/callback/')
        github_login, error = store_background_agent_github(admin_user, code=code, redirect_uri=redirect_uri)
        if error:
            messages.error(request, error)
        else:
            messages.success(request, f'GitHub connected as {github_login}.')
        return redirect('web:background_agent')
    is_mobile = state == 'mobile_github'
    next_url = None
    if state and state.startswith('next:'):
        next_url = state[5:]
    code = request.GET.get('code')
    if not code:
        if is_mobile:
            return deep_link('nebians://auth-callback?error=cancelled')
        return HttpResponse('Missing authorization code.', status=400)
    redirect_uri = _https_redirect_uri(request, '/auth/github/callback/')
    token_url = 'https://github.com/login/oauth/access_token'
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    try:
        import requests as _req
        resp = _req.post(token_url, json=data, headers=headers, timeout=10)
        token_data = resp.json()
    except Exception as e:
        logger.error('github_callback: token exchange failed: %s', e)
        if is_mobile:
            return deep_link('nebians://auth-callback?error=token_exchange_failed')
        return HttpResponse('Failed to exchange authorization code.', status=502)
    access_token = token_data.get('access_token')
    if not access_token:
        if is_mobile:
            return deep_link('nebians://auth-callback?error=no_access_token')
        return HttpResponse('Failed to get access token from GitHub.', status=502)
    try:
        user_resp = _req.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
            timeout=10,
        )
        github_user = user_resp.json()
    except Exception as e:
        logger.error('github_callback: user fetch failed: %s', e)
        if is_mobile:
            return deep_link('nebians://auth-callback?error=user_fetch_failed')
        return HttpResponse('Failed to fetch GitHub user info.', status=502)
    github_id = str(github_user.get('id', ''))
    if not github_id:
        if is_mobile:
            return deep_link('nebians://auth-callback?error=no_user_id')
        return HttpResponse('Could not retrieve GitHub user ID.', status=502)
    email = github_user.get('email') or ''
    github_email_verified = False
    if not email:
        try:
            emails_resp = _req.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
                timeout=10,
            )
            emails = emails_resp.json()
            for e in emails:
                if e.get('primary') and e.get('verified'):
                    email = e['email']
                    github_email_verified = True
                    break
            if not email:
                for e in emails:
                    if e.get('verified'):
                        email = e['email']
                        github_email_verified = True
                        break
        except Exception:
            pass
    display_name = github_user.get('name') or github_user.get('login', '')
    photo_url = github_user.get('avatar_url') or ''
    user_pk = f'github_{github_id}'
    try:
        db_user = User.objects.get(pk=user_pk)
        if getattr(db_user, 'is_banned', False):
            messages.error(request, 'This account has been banned.')
            return redirect('web:login')
        token = issue_auth_token(db_user)
        user_data = _normalize_user_data(UserSerializer(db_user).data)
        user_data['isNewUser'] = False
        api.set_session_auth(request, token, user_data)
        logger.info('github_callback: existing user signed in: %s', db_user.username or db_user.id)
        if is_mobile:
            return deep_link(f'nebians://auth-callback?authToken={token}&isNewUser=false&username={db_user.username}')
        if next_url:
            return redirect(next_url)
        return redirect('web:home')
    except User.DoesNotExist:
        pass
    redirect_result, linked = _link_oauth_user(request, email, user_pk, display_name, photo_url, 'github_callback', provider_verified=github_email_verified)
    if linked:
        if is_mobile:
            linked_token = api.get_session_token(request) or ''
            linked_user = User.objects.get(email__iexact=email)
            return deep_link(f'nebians://auth-callback?authToken={linked_token}&isNewUser=false&username={linked_user.username}')
        if next_url:
            return redirect(next_url)
        return redirect_result
    auth_token = User.generate_token()
    temp_username = f"github_{github_id[:8]}"
    base_username = temp_username
    suffix = 1
    while User.objects.filter(username=temp_username).exists():
        temp_username = f"{base_username}_{suffix}"
        suffix += 1
    if email and User.objects.filter(email__iexact=email).exists():
        messages.error(request, 'An account with this email already exists. Please log in with your original sign-in method first.')
        return redirect('web:login')
    db_user = User(
        pk=user_pk,
        username=temp_username,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        email_verified=github_email_verified,
        created_at=now_ms(),
    )
    db_user.auth_token = hash_auth_token(auth_token)
    db_user.save()
    token = auth_token
    user_data = _normalize_user_data(UserSerializer(db_user).data)
    user_data['isNewUser'] = True
    api.set_session_auth(request, token, user_data)
    logger.info('github_callback: new user created: %s', user_pk)
    if is_mobile:
        return deep_link(f'nebians://auth-callback?authToken={auth_token}&isNewUser=true&username={temp_username}')
    if next_url:
        return redirect(f"{reverse('web:edit_profile')}?next={next_url}")
    return redirect('web:edit_profile')

def logout(request):
    token = api.get_session_token(request)
    if token:
        revoke_auth_token(token)
    api.clear_session_auth(request)
    return redirect('web:home')

def email_signup_page(request):
    if api.get_session_token(request):
        return redirect('web:home')
    return redirect('/login/?panel=email-signup')

def email_login_page(request):
    if api.get_session_token(request):
        return redirect('web:home')
    return render(request, 'web/email_login.html', _ctx(request))

def email_verify_page(request):
    return render(request, 'web/email_verify.html', _ctx(request))

def email_forgot_page(request):
    return render(request, 'web/email_forgot.html', _ctx(request))

def password_page(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    user = api.get_session_user(request)
    has_password = False
    if user:
        try:
            db_user = User.objects.get(id=user.get('id'))
            has_password = bool(db_user.password_hash)
        except User.DoesNotExist:
            pass
    return render(request, 'web/password_set.html', _ctx(request, has_password=has_password))

def change_password_page(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    return render(request, 'web/password_change.html', _ctx(request))

def token_login(request):
    token = request.GET.get('token', '').strip()
    next_url = request.GET.get('next', '').strip()
    if not next_url or not next_url.startswith('/') or next_url.startswith('//'):
        next_url = reverse('web:home')
    if token:
        try:
            user = get_user_by_auth_token(token)
            user_data = UserSerializer(user).data
            api.set_session_auth(request, token, user_data)
            return redirect(next_url)
        except Exception:
            pass
    return redirect(f"{reverse('web:login')}?next={next_url}")

