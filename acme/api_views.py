from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Q
from .models import Ticket, TicketComment
from .serializers import (
    TicketSerializer, 
    TicketDetailSerializer, 
    TicketCommentSerializer
)
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ticket_list(request):
    if request.method == 'GET':
        status_filter = request.query_params.get('status', None)
        priority_filter = request.query_params.get('priority', None)
        
        tickets = Ticket.objects.all()
        
        if status_filter:
            tickets = tickets.filter(status=status_filter)
        if priority_filter:
            tickets = tickets.filter(priority=priority_filter)
            
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def ticket_detail(request, ticket_id):
    try:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TicketDetailSerializer(ticket)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_stats(request):
    today = timezone.now().date()
    
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.exclude(status='Closed').count()
    closed_today = Ticket.objects.filter(
        status='Closed', 
        last_updated__date=today
    ).count()
    high_priority_open = Ticket.objects.filter(
        priority='High'
    ).exclude(status='Closed').count()
    
    stats = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'closed_today_tickets': closed_today,
        'high_priority_open_tickets': high_priority_open,
    }
    
    return Response(stats)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ticket_comments(request, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        comments = ticket.comments.all()
        serializer = TicketCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TicketCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([AllowAny])
def api_signin(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid credentials'}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):
    data = json.loads(request.body)
    
    required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return Response({'error': f'{field} is required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user exists
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    is_staff = data.get('is_staff', False)
    is_superuser = data.get('is_superuser', False)
    
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
        return Response({'success': 'User logged out successfully'}, 
                       status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)