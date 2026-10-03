from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudentProfileViewSet,
    DocumentViewSet,
    create_conversation,
    conversation_ask
)

router = DefaultRouter()

router.register('profile', StudentProfileViewSet, basename='profile')
router.register('documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('', include(router.urls)),

    path(
        'conversation/',
        create_conversation,
        name='create-conversation'
    ),

    path(
        'conversation/ask/',
        conversation_ask,
        name='conversation-ask'
    ),
]