from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/',views.UserProfileView.as_view(), name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
