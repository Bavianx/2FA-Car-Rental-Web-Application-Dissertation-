# Two-Factor Authentication Web Application

**BSc Cyber Security Final Year Project - 2025**  
**Nottingham Trent University**

A Django-based web application demonstrating secure authentication practices including Two-Factor Authentication (2FA), Multi-Factor Authentication (MFA), and Single Sign-On (SSO) for the car rental industry.

##  Project Overview

This project addresses security gaps in the car rental industry by implementing modern authentication methods. Research showed that major rental companies (Hertz, Budget, Thrifty, etc.) rely solely on traditional password authentication, leaving users vulnerable to common attacks.

### Key Features

-  **Traditional Authentication** - Secure password-based login with complexity requirements
-  **Two-Factor Authentication (2FA)** - TOTP-based verification via Google Authenticator
-  **Google Single Sign-On (SSO)** - OAuth 2.0 integration for seamless access
-  **QR Code Device Linking** - One-time device pairing for ongoing authentication
-  **Zero Trust Security Model** - Continuous verification, no implicit trust
-  **Encrypted Database** - MySQL with AES encryption, password hashing & salting

##  Technologies Used

- **Backend:** Django 5.1.1 (Python)
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** 
  - django-allauth (OAuth 2.0)
  - django-otp (TOTP)
  - PyOTP (QR code generation)
  - Google Authenticator App
- **Security:** CSRF protection, XSS prevention, SQL injection mitigation

##  Research Findings

Primary research on top UK car rental services revealed:
- 50% use only email + password authentication
- 0% implement 2FA or MFA
- Password reset vulnerabilities in 83% of services
- No adherence to OWASP Top 10 guidelines

This project demonstrates how modern authentication can close these security gaps.


### Known Limitations
- Email backend set to console (password reset emails print to terminal)
- Google OAuth requires public callback URL (limited to localhost testing)
- No biometric authentication (considered out of scope for project)
- No native mobile app (web-responsive only)
- Designed for demonstration purposes, not production scale

##  Future Enhancements

Potential additions for future development:
- **Biometric Authentication** - Fingerprint/facial recognition for mobile devices
- **AI-Powered Anomaly Detection** - Machine learning to detect suspicious login patterns
- **Additional SSO Providers** - Facebook, Apple, Microsoft login options
- **SMS Backup Codes** - Alternative 2FA method if device is lost
- **Rate Limiting** - Prevent brute force attacks more effectively
- **Session Management** - Advanced timeout and multi-device handling
- **Cloud Deployment** - AWS, Azure, or Google Cloud hosting
- **WebAuthn/FIDO2** - Passwordless authentication support


##  Related Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [django-otp Documentation](https://django-otp-official.readthedocs.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Authenticator](https://support.google.com/accounts/answer/1066447)