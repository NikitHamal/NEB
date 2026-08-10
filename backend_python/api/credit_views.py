import time
import uuid
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .authentication import AuthTokenAuthentication
from .models import User, NebyCreditTransaction
from .throttles import AuthRateThrottle

WHATSAPP_CONTACT = {
    'name': 'Nikit Hamal',
    'phone': '+9779765324034',
    'url': 'https://wa.me/9779765324034?text=Hi%20Nikit,%20I%20need%20more%20Neby%20Credits%20for%20NEBians.'
}


def check_and_reset_monthly_credits(user: User) -> User:
    """Ensure user has their free 10 monthly credits granted for the current month."""
    current_month = time.strftime('%Y-%m')
    if user.free_credits_month != current_month:
        user.free_credits = 10
        user.free_credits_month = current_month
        user.save(update_fields=['free_credits', 'free_credits_month'])
        
        NebyCreditTransaction.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            transaction_type='monthly_grant',
            amount=10,
            description=f'Monthly 10 Free Credits for {current_month}',
            created_at=int(time.time() * 1000)
        )
    return user


@api_view(['GET'])
@authentication_classes([AuthTokenAuthentication])
def credit_balance(request):
    user = getattr(request, 'user', None)
    if not isinstance(user, User) or user.is_locked:
        return Response({'error': 'Please sign in'}, status=status.HTTP_401_UNAUTHORIZED)
    
    user = check_and_reset_monthly_credits(user)
    
    return Response({
        'free_credits': user.free_credits,
        'ai_credits': user.ai_credits,
        'total_credits': user.free_credits + user.ai_credits,
        'nebians_points': user.nebians_points,
        'free_credits_month': user.free_credits_month,
        'conversion_rate': {'points_per_credit': 2},
        'whatsapp_contact': WHATSAPP_CONTACT
    })


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([AuthRateThrottle])
def convert_points_to_credits(request):
    user = getattr(request, 'user', None)
    if not isinstance(user, User) or user.is_locked:
        return Response({'error': 'Please sign in'}, status=status.HTTP_401_UNAUTHORIZED)
    
    user = check_and_reset_monthly_credits(user)
    
    try:
        points = int(request.data.get('points') or 0)
    except (ValueError, TypeError):
        return Response({'error': 'Invalid points amount'}, status=status.HTTP_400_BAD_REQUEST)
    
    if points < 2:
        return Response({'error': 'Minimum conversion is 2 points for 1 credit'}, status=status.HTTP_400_BAD_REQUEST)
    
    if points % 2 != 0:
        return Response({'error': 'Points must be an even number (2 points = 1 credit)'}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.nebians_points < points:
        return Response({
            'error': f'Insufficient points balance. You have {user.nebians_points} points, but requested {points}.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    credits_to_add = points // 2
    
    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user.pk)
        if user.nebians_points < points:
            return Response({'error': 'Insufficient points balance'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.nebians_points -= points
        user.ai_credits += credits_to_add
        user.save(update_fields=['nebians_points', 'ai_credits'])
        
        NebyCreditTransaction.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            transaction_type='conversion',
            amount=credits_to_add,
            points_spent=points,
            description=f'Converted {points} points to {credits_to_add} Neby Credits',
            created_at=int(time.time() * 1000)
        )
    
    return Response({
        'message': f'Successfully converted {points} points to {credits_to_add} Neby Credits!',
        'credits_added': credits_to_add,
        'free_credits': user.free_credits,
        'ai_credits': user.ai_credits,
        'total_credits': user.free_credits + user.ai_credits,
        'nebians_points': user.nebians_points
    })


@api_view(['GET'])
@authentication_classes([AuthTokenAuthentication])
def credit_history(request):
    user = getattr(request, 'user', None)
    if not isinstance(user, User) or user.is_locked:
        return Response({'error': 'Please sign in'}, status=status.HTTP_401_UNAUTHORIZED)
    
    transactions = NebyCreditTransaction.objects.filter(user=user).order_by('-created_at')[:50]
    data = [
        {
            'id': tx.id,
            'transaction_type': tx.transaction_type,
            'amount': tx.amount,
            'points_spent': tx.points_spent,
            'description': tx.description,
            'created_at': tx.created_at
        }
        for tx in transactions
    ]
    return Response({'transactions': data})
