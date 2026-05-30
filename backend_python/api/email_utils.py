"""
Email sending utility for NEBians.
Uses Django's email backend (configurable via settings).
Supports both SMTP and console backend for development.
"""
import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_verification_email(email, code, username=None):
    """
    Send a 6-digit verification code to the user's email.
    Returns True if sent successfully, False otherwise.
    """
    subject = "NEBians - Verify Your Email"
    greeting = f"Hi {username}," if username else "Hi,"
    body = (
        f"{greeting}\n\n"
        f"Your NEBians verification code is: {code}\n\n"
        f"This code expires in 10 minutes.\n\n"
        f"If you didn't create an account on NEBians, you can ignore this email.\n\n"
        f"— NEBians Team"
    )
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        logger.info("send_verification_email: sent to %s", email)
        return True
    except Exception as e:
        logger.error("send_verification_email: failed for %s: %s", email, e)
        return False


def send_welcome_email(email, username=None):
    """
    Send a welcome email after successful verification.
    """
    subject = "Welcome to NEBians!"
    greeting = f"Hi {username}," if username else "Hi,"
    body = (
        f"{greeting}\n\n"
        f"Welcome to NEBians — your unified platform for NEB study resources, "
        f"forum discussions, and collaborative learning.\n\n"
        f"Get started by exploring resources, joining discussions, and completing your profile.\n\n"
        f"— NEBians Team"
    )
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        logger.info("send_welcome_email: sent to %s", email)
        return True
    except Exception as e:
        logger.error("send_welcome_email: failed for %s: %s", email, e)
        return False