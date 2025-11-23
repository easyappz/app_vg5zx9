from django.urls import path
from .views import (
    HelloView,
    RegisterView,
    LoginView,
    CurrentUserView,
    ProfileView,
    MessagesListView,
    MessageCreateView,
    OnlineUsersView,
    HeartbeatView
)

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", CurrentUserView.as_view(), name="current-user"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("messages/", MessagesListView.as_view(), name="messages-list"),
    path("users/online/", OnlineUsersView.as_view(), name="users-online"),
    path("users/heartbeat/", HeartbeatView.as_view(), name="users-heartbeat"),
]
