from django.conf.urls import url
from rest_framework import routers

from src.tasks.views import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'tasks', TaskViewSet, 'tasks')

urlpatterns = router.urls + [
    url(r'^auth/login/$', LoginView.as_view(), name='login'),
    url(r'^auth/logout/$', LogoutView.as_view(), name='logout'),
]
