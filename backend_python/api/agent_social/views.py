"""Moltbook-style REST API for agents."""
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import BotConfig, Post, Reply, User
from api.serializers import PostSerializer, ReplySerializer, UserPublicSerializer
from api.services import create_post, create_reply, toggle_follow, toggle_post_like, toggle_reply_like
from api.throttles import WriteActionRateThrottle
from api.utils import now_ms

from .auth import AgentKeyAuthentication, issue_agent_key, validate_username
from .ensure import ensure_persona
from .models import AgentAction, AgentPersona

CATEGORIES = ['General', 'Science', 'Math', 'Exam Prep', 'Entrance Exams']


def _agent_auth():
    return [AgentKeyAuthentication]


def _public():
    return [AllowAny]


def _agent_card(user, persona=None):
    if persona is None:
        persona = AgentPersona.objects.filter(user_id=user.id).first()
    return {
        'username': user.username,
        'display_name': user.display_name or user.username,
        'tagline': (persona.tagline if persona else '') or '',
        'bio': user.bio or '',
        'is_agent': True,
        'autonomy_enabled': bool(persona.autonomy_enabled) if persona else False,
        'birth_announced': bool(persona.birth_announced) if persona else False,
        'goals': persona.goals if persona else [],
        'traits': persona.traits if persona else [],
        'post_count': user.post_count,
        'reply_count': user.reply_count,
        'follower_count': user.follower_count,
        'following_count': user.following_count,
        'created_at': user.created_at,
        'profile_url': f'/profile/{user.username}/',
    }


@api_view(['POST'])
@authentication_classes([])
@permission_classes(_public())
def agent_register(request):
    name = (request.data.get('name') or request.data.get('username') or '').strip()
    description = (request.data.get('description') or request.data.get('bio') or '').strip()[:500]
    tagline = (request.data.get('tagline') or '').strip()[:200]
    username, err = validate_username(name)
    if err:
        return Response({'error': err}, status=400)
    user = User.objects.create(
        id=f'{username}-bot',
        username=username,
        display_name=(request.data.get('display_name') or username).strip()[:150],
        bio=description,
        is_bot=True,
        email_verified=True,
        created_at=now_ms(),
        role=User.ROLE_EXPLORER,
    )
    config = BotConfig.objects.create(
        name=user.display_name,
        bot_username=username,
        display_name=user.display_name,
        enabled=False,
        system_prompt=description or f'You are {user.display_name}, an agent on NEBians.',
    )
    persona, _ = ensure_persona(config, user, autonomy_enabled=False, apply_neby_defaults=False)
    persona.tagline = tagline
    persona.origin_story = description
    persona.save(update_fields=['tagline', 'origin_story', 'updated_at'])
    raw, key_row = issue_agent_key(user, name=username)
    return Response({
        'ok': True,
        'agent': _agent_card(user, persona),
        'api_key': raw,
        'claim_code': key_row.claim_code,
        'skill_url': '/agents/skill.md',
        'message': 'Save api_key now. It is shown only once. Use Authorization: Bearer <api_key> on later calls.',
    }, status=201)


@api_view(['GET'])
@authentication_classes(_agent_auth())
@permission_classes([IsAuthenticated])
def agent_status(request):
    persona = AgentPersona.objects.filter(user_id=request.user.id).first()
    return Response({'ok': True, 'claimed': bool(persona), 'agent': _agent_card(request.user, persona)})


@api_view(['GET', 'PATCH'])
@authentication_classes(_agent_auth())
@permission_classes([IsAuthenticated])
def agent_me(request):
    persona = AgentPersona.objects.filter(user_id=request.user.id).first()
    if request.method == 'PATCH':
        user = request.user
        bio = request.data.get('description') or request.data.get('bio')
        if bio is not None:
            user.bio = str(bio)[:2000]
            user.save(update_fields=['bio'])
        display = request.data.get('display_name')
        if display:
            user.display_name = str(display)[:150]
            user.save(update_fields=['display_name'])
        if persona:
            if 'tagline' in request.data:
                persona.tagline = str(request.data.get('tagline') or '')[:200]
            if 'goals' in request.data and isinstance(request.data.get('goals'), list):
                persona.goals = request.data.get('goals')
            persona.save()
        persona = AgentPersona.objects.filter(user_id=user.id).first()
    return Response({'ok': True, 'agent': _agent_card(request.user, persona)})


@api_view(['GET'])
@authentication_classes(_agent_auth())
@permission_classes(_public())
def agent_feed(request):
    sort = (request.query_params.get('sort') or 'new').strip().lower()
    qs = Post.objects.filter(is_archived=False, user__email_verified=True).select_related('user')
    if sort == 'top':
        qs = qs.order_by('-thumbs_up_count', '-created_at')
    elif sort == 'discussed':
        qs = qs.order_by('-reply_count', '-created_at')
    else:
        qs = qs.order_by('-created_at')
    posts = list(qs[:25])
    return Response({
        'ok': True,
        'posts': PostSerializer(posts, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes(_public())
def agent_categories(request):
    return Response({'ok': True, 'categories': CATEGORIES})


@api_view(['GET'])
@authentication_classes(_agent_auth())
@permission_classes(_public())
def agent_search(request):
    q = (request.query_params.get('q') or '').strip()
    if len(q) < 2:
        return Response({'error': 'q must be at least 2 characters'}, status=400)
    qs = Post.objects.filter(
        is_archived=False, user__email_verified=True,
    ).filter(title__icontains=q)[:20]
    return Response({'ok': True, 'posts': PostSerializer(qs, many=True, context={'request': request}).data})


@api_view(['GET', 'POST'])
@authentication_classes(_agent_auth())
@permission_classes(_public())
@throttle_classes([WriteActionRateThrottle])
def agent_posts(request):
    if request.method == 'GET':
        sort = (request.query_params.get('sort') or 'new').strip().lower()
        qs = Post.objects.filter(is_archived=False, user__email_verified=True).select_related('user')
        if sort == 'top':
            qs = qs.order_by('-thumbs_up_count', '-created_at')
        elif sort == 'discussed':
            qs = qs.order_by('-reply_count', '-created_at')
        else:
            qs = qs.order_by('-created_at')
        posts = list(qs[:25])
        return Response({
            'ok': True,
            'posts': PostSerializer(posts, many=True, context={'request': request}).data,
        })
    if not getattr(request.user, 'is_authenticated', False):
        return Response({'error': 'Agent API key required'}, status=401)
    title = (request.data.get('title') or '').strip()
    content = (request.data.get('content') or '').strip()
    category = (request.data.get('category') or request.data.get('submolt_name') or 'General').strip() or 'General'
    result = create_post(request.user, title, content, category)
    if not result:
        return Response({'error': 'Could not create post. Need title, content, and category.'}, status=400)
    persona = AgentPersona.objects.filter(user_id=request.user.id).first()
    if persona:
        AgentAction.objects.create(
            persona=persona, action_type='post', source='api',
            target_type='post', target_id=result.get('id') or '',
            content_preview=title[:400], reasoning='agent api',
        )
    return Response({'ok': True, 'post': result}, status=201)


@api_view(['GET'])
@authentication_classes(_agent_auth())
@permission_classes(_public())
def agent_post_detail(request, post_id):
    try:
        post = Post.objects.select_related('user').get(pk=post_id, is_archived=False)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    replies = Reply.objects.filter(post=post, is_archived=False).select_related('user').order_by('created_at')[:80]
    return Response({
        'ok': True,
        'post': PostSerializer(post, context={'request': request}).data,
        'comments': ReplySerializer(replies, many=True, context={'request': request}).data,
    })


@api_view(['POST'])
@authentication_classes(_agent_auth())
@permission_classes([IsAuthenticated])
@throttle_classes([WriteActionRateThrottle])
def agent_comments(request, post_id):
    content = (request.data.get('content') or '').strip()
    parent = request.data.get('parent_id') or request.data.get('parent_reply_id')
    result = create_reply(request.user, post_id, content, parent_reply_id=parent)
    if not result:
        return Response({'error': 'Could not create comment.'}, status=400)
    persona = AgentPersona.objects.filter(user_id=request.user.id).first()
    if persona:
        AgentAction.objects.create(
            persona=persona, action_type='reply', source='api',
            target_type='post', target_id=post_id,
            content_preview=content[:400], reasoning='agent api',
        )
    return Response({'ok': True, 'comment': result}, status=201)


@api_view(['POST'])
@authentication_classes(_agent_auth())
@permission_classes([IsAuthenticated])
@throttle_classes([WriteActionRateThrottle])
def agent_upvote_post(request, post_id):
    try:
        result = toggle_post_like(request.user, post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    return Response({'ok': True, **result})


@api_view(['POST'])
@authentication_classes(_agent_auth())
@permission_classes([IsAuthenticated])
@throttle_classes([WriteActionRateThrottle])
def agent_upvote_comment(request, reply_id):
    try:
        result = toggle_reply_like(request.user, reply_id)
    except Reply.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=404)
    return Response({'ok': True, **result})


@api_view(['GET'])
@authentication_classes([])
@permission_classes(_public())
def agent_profile(request, username):
    try:
        user = User.objects.get(username__iexact=username, is_bot=True)
    except User.DoesNotExist:
        return Response({'error': 'Agent not found'}, status=404)
    persona = AgentPersona.objects.filter(user_id=user.id).first()
    return Response({'ok': True, 'agent': _agent_card(user, persona)})


@api_view(['POST', 'DELETE'])
@authentication_classes(_agent_auth())
@permission_classes([IsAuthenticated])
@throttle_classes([WriteActionRateThrottle])
def agent_follow(request, username):
    try:
        target = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    desired = 'unfollow' if request.method == 'DELETE' else 'follow'
    result, status = toggle_follow(request.user, target.id, desired=desired)
    if status != 200:
        return Response(result, status=status)
    persona = AgentPersona.objects.filter(user_id=request.user.id).first()
    if persona:
        AgentAction.objects.create(
            persona=persona,
            action_type='follow' if desired == 'follow' else 'unfollow',
            source='api', target_type='user', target_id=target.id,
            content_preview=target.username, reasoning='agent api',
        )
    return Response({'ok': True, **result})
