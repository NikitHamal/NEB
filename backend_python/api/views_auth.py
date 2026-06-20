"""Views Auth extracted from views.py."""
import uuid
from .view_helpers import *  # noqa: F401,F403

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def auth_github(request):
    """
    Sign-in or Register via GitHub OAuth authorization code (for mobile apps).
    Body: { "code": "<github_oauth_authorization_code>" }
    Returns: { "status": "success", "isNewUser": bool, "authToken": "...", "user": {...} }
    """
    code = request.data.get('code')
    if not code:
        return Response({'error': 'code is required'}, status=400)

    from django.conf import settings
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_CLIENT_SECRET
    if not client_id or not client_secret:
        return Response({'error': 'GitHub OAuth is not configured'}, status=501)

    redirect_uri = request.data.get('redirectUri', '')

    token_url = 'https://github.com/login/oauth/access_token'
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }
    if redirect_uri:
        data['redirect_uri'] = redirect_uri

    try:
        import requests as _req
        resp = _req.post(token_url, json=data, headers=headers, timeout=10)
        token_data = resp.json()
    except Exception as e:
        logger.error('auth_github: token exchange failed: %s', e)
        return Response({'error': 'Failed to exchange authorization code.'}, status=502)

    access_token = token_data.get('access_token')
    if not access_token:
        error_desc = token_data.get('error_description', token_data.get('error', 'Unknown error'))
        logger.warning('auth_github: no access token: %s', error_desc)
        return Response({'error': 'Failed to get access token from GitHub.'}, status=401)

    try:
        user_resp = _req.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
            timeout=10,
        )
        github_user = user_resp.json()
    except Exception as e:
        logger.error('auth_github: user fetch failed: %s', e)
        return Response({'error': 'Failed to fetch GitHub user info.'}, status=502)

    github_id = str(github_user.get('id', ''))
    if not github_id:
        return Response({'error': 'Could not retrieve GitHub user ID.'}, status=502)

    email = github_user.get('email') or ''
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
                    break
            if not email:
                for e in emails:
                    if e.get('verified'):
                        email = e['email']
                        break
        except Exception:
            pass

    display_name = github_user.get('name') or github_user.get('login', '')
    photo_url = github_user.get('avatar_url') or ''
    user_pk = f'github_{github_id}'

    try:
        user = User.objects.get(pk=user_pk)
        auth_token = issue_auth_token(user)
        logger.info('auth_github: existing user signed in: %s', user.username or user.id)
        return Response({
            'status': 'success',
            'isNewUser': False,
            'authToken': auth_token,
            'user': UserSerializer(user).data
        })
    except User.DoesNotExist:
        pass

    linked = _link_oauth_user_model(email, user_pk, display_name, photo_url)
    if linked:
        auth_token = issue_auth_token(linked)
        logger.info('auth_github: linked existing user by email: %s', email)
        return Response({
            'status': 'success',
            'isNewUser': False,
            'authToken': auth_token,
            'user': UserSerializer(linked).data
        })

    auth_token = User.generate_token()
    temp_username = f"github_{github_id[:8]}"
    base_username = temp_username
    suffix = 1
    while User.objects.filter(username=temp_username).exists():
        temp_username = f"{base_username}_{suffix}"
        suffix += 1
    user = User(
        pk=user_pk,
        username=temp_username,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        created_at=_now_ms()
    )
    user.auth_token = hash_auth_token(auth_token)
    user.save()
    logger.info('auth_github: new user created: %s', user_pk)
    return Response({
        'status': 'success',
        'isNewUser': True,
        'authToken': auth_token,
        'user': UserSerializer(user).data
    })

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
@authentication_classes([])
@permission_classes([AllowAny])
def auth_google(request):
    """
    Sign-in or Register via Google ID Token.
    Body: { "idToken": "<google_id_token>" }
    Returns: { "status": "success", "isNewUser": bool, "authToken": "...", "user": {...} }
    """
    id_token = request.data.get('idToken')
    if not id_token:
        logger.warning("auth_google: missing idToken")
        return Response({'error': 'idToken is required'}, status=400)

    google_info = verify_google_token(id_token)
    if not google_info:
        logger.warning("auth_google: Google token verification failed")
        return Response({'error': 'Invalid Google ID Token'}, status=401)

    user_id = google_info['userId']
    email = google_info.get('email') or ''
    display_name = google_info.get('displayName') or ''
    photo_url = google_info.get('photoUrl') or ''

    try:
        user = User.objects.get(pk=user_id)
        auth_token = issue_auth_token(user)
        logger.info("auth_google: existing user signed in: %s", user.username or user.id)
        return Response({
            'status': 'success',
            'isNewUser': False,
            'authToken': auth_token,
            'user': UserSerializer(user).data
        })
    except User.DoesNotExist:
        # New user — create with auth token, temporary username placeholder
        auth_token = User.generate_token()
        temp_username = f"user_{user_id[:8]}"
        user = User(
            pk=user_id,
            username=temp_username,
            email=email,
            display_name=display_name,
            photo_url=photo_url,
            created_at=_now_ms()
        )
        user.auth_token = hash_auth_token(auth_token)
        user.save()
        logger.info("auth_google: new user created: %s (temp_username=%s)", user_id, temp_username)
        return Response({
            'status': 'success',
            'isNewUser': True,
            'authToken': auth_token,
            'user': UserSerializer(user).data
        })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([SignupRateThrottle])
def auth_email_signup(request):
    """
    POST /api/auth/email/signup
    Body: { "email": "...", "password": "...", "username": "..." }
    Creates user with email, sends 6-digit verification code.
    """
    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '')
    username = request.data.get('username', '').strip()
    role = request.data.get('role', 'student').strip().lower()

    if not email or not password or not username:
        return Response({'error': 'Email, password, and username are required'}, status=400)

    if role not in ('student', 'teacher', 'institution', 'explorer'):
        role = 'student'

    password_error = _validate_password_strength(password)
    if password_error:
        return password_error

    if len(username) < 3:
        return Response({'error': 'Username must be at least 3 characters'}, status=400)

    if not username.replace('_', '').isalnum():
        return Response({'error': 'Username can only contain letters, numbers, and underscores'}, status=400)

    if User.objects.filter(email__iexact=email).exists():
        return Response({'error': 'An account with this email already exists'}, status=409)

    if User.objects.filter(username__iexact=username).exists():
        return Response({'error': 'This username is already taken'}, status=409)

    user = User(
        pk=str(uuid.uuid4()),
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=role,
        email_verified=False,
        created_at=_now_ms()
    )
    user.save()
    code = _issue_verification_code(user, 'signup')

    send_verification_email(email, code, username)

    logger.info("auth_email_signup: new user %s (email=%s), verification code sent", username, email)
    return Response({
        'status': 'success',
        'message': 'Verification code sent to your email',
        'userId': user.id,
        'email': email,
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VerificationRateThrottle])
def auth_email_verify(request):
    """
    POST /api/auth/email/verify
    Body: { "email": "...", "code": "123456" }
    Verifies the 6-digit code. On success, returns auth token + user.
    """
    email = request.data.get('email', '').strip().lower()
    code = request.data.get('code', '').strip()

    if not email or not code:
        return Response({'error': 'Email and verification code are required'}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'error': 'No account found with this email'}, status=404)

    if user.email_verified:
        return Response({'error': 'Email is already verified. Please log in.'}, status=400)

    ok, error_response = _verify_user_code(user, code, 'signup')
    if not ok:
        return error_response

    user.email_verified = True
    _clear_verification_code(user)
    auth_token = issue_auth_token(user, save=False)
    user.save()

    logger.info("auth_email_verify: email verified for user %s", user.username)
    return Response({
        'status': 'success',
        'isNewUser': True,
        'profileIncomplete': _profile_incomplete(user),
        'authToken': auth_token,
        'user': UserSerializer(user).data,
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VerificationRateThrottle])
def auth_email_resend(request):
    """
    POST /api/auth/email/resend
    Body: { "email": "..." }
    Resends verification code. Rate-limited to prevent abuse.
    """
    email = request.data.get('email', '').strip().lower()

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'error': 'No account found with this email'}, status=404)

    if user.email_verified:
        return Response({'error': 'Email is already verified. Please log in.'}, status=400)

    if _verification_resend_blocked(user):
        return Response({'error': 'Please wait 60 seconds before requesting a new code'}, status=429)

    code = _issue_verification_code(user, 'signup')

    send_verification_email(email, code, user.username)

    logger.info("auth_email_resend: new code sent to %s", email)
    return Response({'status': 'success', 'message': 'New verification code sent'})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def auth_email_login(request):
    """
    POST /api/auth/email/login
    Body: { "email": "...", "password": "..." }
    The email field accepts either an email or a username.
    Logs in with email/username + password. Requires email_verified=True.
    """
    login_id = request.data.get('email', '').strip()
    password = request.data.get('password', '')

    if not login_id or not password:
        return Response({'error': 'Email/username and password are required'}, status=400)

    # Look up by email or username
    try:
        if '@' in login_id:
            user = User.objects.get(email__iexact=login_id)
        else:
            user = User.objects.get(username__iexact=login_id)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email/username or password'}, status=401)
    except User.MultipleObjectsReturned:
        return Response({'error': 'Multiple accounts found. Please use your email address.'}, status=400)

    if not user.email_verified:
        if not _verification_resend_blocked(user):
            code = _issue_verification_code(user, 'signup')
            send_verification_email(user.email, code, user.username)
        return Response({'error': 'Please verify your email first', 'needsVerification': True, 'email': user.email}, status=403)

    if not user.password_hash:
        return Response({'error': 'This account uses Google sign-in. Use "Forgot password?" to set a password for email login.', 'needsSetPassword': True, 'email': user.email}, status=400)

    password_ok, needs_rehash = verify_password(password, user.password_hash)
    if not password_ok:
        return Response({'error': 'Invalid email/username or password'}, status=401)

    auth_token = issue_auth_token(user, save=False)
    update_fields = ['auth_token']
    if needs_rehash:
        user.password_hash = hash_password(password)
        update_fields.append('password_hash')
    if update_fields:
        user.save(update_fields=update_fields)

    logger.info("auth_email_login: user %s logged in", user.username)
    return Response({
        'status': 'success',
        'isNewUser': False,
        'profileIncomplete': _profile_incomplete(user),
        'authToken': auth_token,
        'user': UserSerializer(user).data,
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VerificationRateThrottle])
def auth_email_forgot(request):
    """
    POST /api/auth/email/forgot
    Body: { "email": "..." }
    Sends a verification code to reset or set a password.
    For Google-only accounts (no password), returns needsSetPassword: true
    so the frontend can show an appropriate UI.
    """
    email = request.data.get('email', '').strip().lower()

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'status': 'success', 'message': 'If an account exists with this email, a verification code has been sent'})

    needs_set_password = not bool(user.password_hash)
    purpose = 'set_password' if needs_set_password else 'password_reset'

    if _verification_resend_blocked(user):
        return Response({
            'status': 'success',
            'message': 'If an account exists with this email, a verification code has been sent',
            'needsSetPassword': needs_set_password,
        })

    code = _issue_verification_code(user, purpose)
    send_verification_email(email, code, user.username)

    logger.info("auth_email_forgot: %s code sent to %s", purpose, email)
    return Response({
        'status': 'success',
        'message': 'If an account exists with this email, a verification code has been sent',
        'needsSetPassword': needs_set_password,
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VerificationRateThrottle])
def auth_email_reset_password(request):
    """
    POST /api/auth/email/reset-password
    Body: { "email": "...", "code": "123456", "newPassword": "...", "confirmPassword": "..." }
    Resets or sets a password using verification code.
    Works for both password_reset and set_password purposes.
    """
    email = request.data.get('email', '').strip().lower()
    code = request.data.get('code', '').strip()
    new_password = request.data.get('newPassword', '')
    confirm_password = request.data.get('confirmPassword', '')

    if not email or not code or not new_password:
        return Response({'error': 'Email, code, and new password are required'}, status=400)

    if confirm_password and new_password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=400)

    password_error = _validate_password_strength(new_password)
    if password_error:
        return password_error

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid or expired verification code'}, status=400)

    ok, error_response = _verify_user_code(user, code, None)
    if not ok:
        return error_response

    user.password_hash = hash_password(new_password)
    user.email_verified = True
    _clear_verification_code(user)
    auth_token = issue_auth_token(user, save=False)
    user.save()

    logger.info("auth_email_reset_password: password set/reset for %s", user.username)
    return Response({
        'status': 'success',
        'profileIncomplete': _profile_incomplete(user),
        'authToken': auth_token,
        'user': UserSerializer(user).data,
    })

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def auth_set_password(request):
    """
    POST /api/auth/set-password
    Body: { "password": "..." }
    Sets a password for a Google-only account so they can also log in with email/username.
    Requires authentication. Also sets email_verified=True since Google already verified it.
    """
    user, err = _require_user(request)
    if err:
        return err

    password = request.data.get('password', '')
    if not password:
        return Response({'error': 'Password is required'}, status=400)

    password_error = _validate_password_strength(password)
    if password_error:
        return password_error

    if user.password_hash:
        return Response({'error': 'Password already set. Use change-password instead.'}, status=400)

    user.password_hash = hash_password(password)
    user.email_verified = True
    user.save(update_fields=['password_hash', 'email_verified'])

    logger.info("auth_set_password: password set for user %s", user.username)
    return Response({
        'status': 'success',
        'message': 'Password set successfully',
        'user': UserSerializer(user).data,
    })

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def auth_change_password(request):
    """
    POST /api/auth/change-password
    Body: { "currentPassword": "...", "newPassword": "..." }
    Changes password for an account that already has one.
    Requires authentication.
    """
    user, err = _require_user(request)
    if err:
        return err

    current_password = request.data.get('currentPassword', '')
    new_password = request.data.get('newPassword', '')

    if not current_password or not new_password:
        return Response({'error': 'Current password and new password are required'}, status=400)

    password_error = _validate_password_strength(new_password)
    if password_error:
        return password_error

    if not user.password_hash:
        return Response({'error': 'No password set. Use set-password instead.'}, status=400)

    password_ok, _needs_rehash = verify_password(current_password, user.password_hash)
    if not password_ok:
        return Response({'error': 'Current password is incorrect'}, status=401)

    user.password_hash = hash_password(new_password)
    auth_token = issue_auth_token(user, save=False)
    user.save(update_fields=['password_hash', 'auth_token'])

    logger.info("auth_change_password: password changed for user %s", user.username)
    return Response({
        'status': 'success',
        'message': 'Password changed successfully',
        'authToken': auth_token,
        'user': UserSerializer(user).data,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_logout(request):
    """POST /api/auth/logout — revoke the current auth token so it cannot be reused."""
    raw_token = request.META.get('HTTP_AUTHORIZATION', '')
    if raw_token.startswith('Bearer '):
        raw_token = raw_token[7:].strip()
    if raw_token:
        revoke_auth_token(raw_token)
    return Response({'status': 'success', 'message': 'Logged out'})
