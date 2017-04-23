from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import views
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, render, redirect

##
from django.contrib.auth.decorators import login_required

from src.tasks.models import Task
from src.tasks.serializers import TaskSerializer, UserSerializer
from src.tasks.serializers import UserDetailSerializer


def index(request):
    if request.user.is_authenticated:
        return redirect("tasks")

    return render(request, 'tasks/index.html')


@login_required(login_url='/')
def tasks(request):
    return render(request, 'tasks/tasks.html')


class LogoutView(views.APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(views.APIView):
    """
    Use this endpoint to login user .
    """

    def post(self, request, *args, **kwargs):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        account = authenticate(username=username, password=password)

        if (account is not None) and account.is_active:
            login(request, account)
            session_key = request.session.session_key
            if not session_key:
                session_key = request.session.create()

            user = UserSerializer(account).data
            data = {
                "id": session_key,
                "user": user,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ViewSet):
    """
    Use this endpoint to get all username's .
    """
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Use this endpoint to manipulate width tasks.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = DjangoFilterBackend,
    filter_fields = ('status',)

    def perform_destroy(self, instance):
        user = instance.author
        if user is None or self.request.user.id == user.id:
            super().perform_destroy(instance)
        else:
            raise ValidationError("You can't delete not your task")

    def perform_update(self, serializer):
        user = serializer.instance.author

        if user and self.request.user.id != user.id:
            raise ValidationError("You can't update not your task")
        else:
            serializer.save()
