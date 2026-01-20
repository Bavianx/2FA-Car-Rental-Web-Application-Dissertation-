
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from frontend import views
from frontend.views import CustomPasswordResetView


urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    
    # GOOGLE SSO (OAuth 2.0)
    path('accounts/', include('allauth.urls')),
    
    # AUTHENTICATION
    path('signup/', views.sign_up_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # TWO-FACTOR AUTHENTICATION (OTP)
    path('otp/', views.otp_view, name='otp'),
    path('otp/verify/', views.otp_verify_view, name='otp_verify'),
    
    # PASSWORD RESET
    path('password_reset/', 
         CustomPasswordResetView.as_view(), 
         name='password_reset'),
    
    path('password_reset_done/', 
         auth_views.PasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    
    path('password_reset_confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    
    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),

    # MAIN APPLICATION
    path('', views.index_view, name='index'),
    path('submit-booking/', views.submit_booking, name='submit_booking'),
]