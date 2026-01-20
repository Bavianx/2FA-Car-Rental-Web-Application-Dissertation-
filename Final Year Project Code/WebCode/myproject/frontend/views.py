import re
import pyotp, qrcode, base64
from io import BytesIO
from .models import Booking
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.password_validation import validate_password

@login_required
def index_view(request):
    """
    Main application page - requires authentication.
    Users must complete login + OTP verification to access.
    """
    return render(request, 'frontend/index.html')



# AUTHENTICATION VIEWS


def sign_up_view(request):
    """
    User registration view.
    Validates email uniqueness and password complexity before account creation.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check all fields are provided
        if not all([username, email, password]):
            messages.error(request, "All fields are required.")
            return render(request, 'frontend/login.html', {
                'username': username, 
                'email': email
            })
    
        # Check email isn't already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'frontend/login.html', {
                'username': username, 
                'email': email
            })

        # Validate password (uses all validators including custom one)
        try: 
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ", ".join(e.messages))
            return render(request, 'frontend/login.html', {
                'username': username, 
                'email': email
            })

        # Create user account
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )
        user.save()
        
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'frontend/login.html')


def login_view(request):
    """
    User login view.
    Authenticates credentials then redirects to OTP verification.
    Does NOT create session until OTP is verified (Zero Trust).
    """
    if request.method == 'POST':
        username_or_email = request.POST.get('email')
        password = request.POST.get('password')

        # Find username from email
        try:
            user_obj = User.objects.get(email=username_or_email)
            username = user_obj.username  
        except User.DoesNotExist:
            username = username_or_email

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Store user ID in session for OTP verification
            # Don't call login() yet - that happens after OTP verification
            request.session['pre_otp_user_id'] = user.id
            return redirect('otp_verify')
        else:
            messages.error(request, "Incorrect email or password. Please try again.")
            return render(request, 'frontend/login.html')

    return render(request, 'frontend/login.html')


def logout_view(request):
    """
    Logs out user and redirects to login page.
    Displays farewell message with username.
    """
    username = request.user.username if request.user.is_authenticated else None
    logout(request)
    
    if username:
        messages.success(request, f"Goodbye, {username}! You've been logged out.")
    
    return redirect('login')


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view for email-based password recovery.
    Note: Email backend set to console for development.
    """
    template_name = 'frontend/password_reset.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save(
            request=self.request,
            domain_override='127.0.0.1:8000',  # Local development only
            use_https=False 
        )
        messages.success(
            self.request,
            "A password reset link has been sent to your email."
        )
        return super().form_valid(form)



# TWO-FACTOR AUTHENTICATION (OTP)


def generate_qr_code(provisioning_uri):
    """
    Generates QR code image from TOTP provisioning URI.
    Returns base64-encoded PNG for embedding in HTML.
    
    Source: https://github.com/getsentry/sentry-auth-google
    """
    qr_image = BytesIO()
    qrcode.make(provisioning_uri).save(qr_image, format='PNG')
    qr_image.seek(0)
    return base64.b64encode(qr_image.getvalue()).decode()


@login_required
def otp_view(request):
    """
    OTP device setup view.
    First-time users: Displays QR code for Google Authenticator linking.
    Returning users: Redirects to OTP verification (device already linked).
    """
    device = TOTPDevice.objects.filter(user=request.user).first()

    if not device:
        # First-time setup - generate new TOTP secret
        secret_key = pyotp.random_base32()
        provisioning_uri = pyotp.TOTP(secret_key).provisioning_uri(
            name=request.user.email,
            issuer_name="FYP_WebApp"
        )
        
        # Save device and generate QR code
        TOTPDevice.objects.create(
            user=request.user, 
            name='Google Authenticator', 
            key=secret_key
        )
        qr_code = generate_qr_code(provisioning_uri)
        
        return render(request, 'frontend/otp_verify.html', {'qr_code': qr_code})

    # Device already exists - go to verification
    return redirect('otp_verify')


def otp_verify_view(request):
    """
    OTP verification view - the final authentication step.
    Verifies TOTP code before granting application access (Zero Trust).
    """
    # Get user from session (set during login_view)
    user_id = request.session.get('pre_otp_user_id')
    
    if not user_id:
        messages.error(request, "Please log in first.")
        return redirect('login')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid session. Please log in again.")
        return redirect('login')
    
    # Check if user has TOTP device
    device = TOTPDevice.objects.filter(user=user).first()
    
    if not device:
        messages.error(request, "No OTP device found. Please set up OTP first.")
        # Log them in temporarily to access OTP setup
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('otp')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        totp = pyotp.TOTP(device.key)

        if totp.verify(otp):
            # OTP verified - NOW we actually log them in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Clear the pre-OTP session data
            del request.session['pre_otp_user_id']
            
            messages.success(request, "Login successful!")
            return redirect('index')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'frontend/otp_verify.html')



# BOOKING FUNCTIONALITY


@login_required
def submit_booking(request):
    """
    Handles booking form submissions.
    Validates input and stores booking in database.
    """
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        date = request.POST.get('date')
        phone = request.POST.get('phone', '').strip()
        time = request.POST.get('time')
        message = request.POST.get('message', '').strip()
        
        # Validate required fields
        if not all([name, email, date, phone, time]):
            messages.error(request, "All fields except message are required.")
            return redirect('index')
        
        # Validate phone number (simple check)
        if not phone.isdigit() or len(phone) != 11:
            messages.error(request, "Phone number must be 11 digits.")
            return redirect('index')
        
        # Create and save booking
        try:
            booking = Booking(
                user=request.user,  # Link to logged-in user
                name=name,
                email=email,
                date=date,
                phone=phone,
                time=time,
                message=message,
            )
            booking.save()
            
            messages.success(request, "Booking submitted successfully!")
        except Exception as e:
            messages.error(request, "An error occurred while submitting your booking. Please try again.")
        
        return redirect('index')
    
    # GET request - just show the page
    return redirect('index')
