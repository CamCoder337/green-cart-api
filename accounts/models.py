"""
Models for user management.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    Uses email as the main identifier instead of username.
    """

    # Basic fields
    email = models.EmailField(
        'Email Address',
        unique=True,
        error_messages={
            'unique': "A user with this email already exists.",
        },
    )

    first_name = models.CharField(
        'First Name',
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        'Last Name',
        max_length=150,
        blank=True
    )

    # Phone number with Cameroon format validation
    phone_regex = RegexValidator(
        regex=r'^(\+237|237)?[2368]\d{7,8}'
        ,
        message="Phone number must be in Cameroon format. Example: +237677123456 or 677123456"
    )
    phone_number = models.CharField(
        'Phone Number',
        validators=[phone_regex],
        max_length=15,
        blank=True,
        help_text='Cameroon phone number format: +237677123456'
    )

    # Avatar
    avatar = models.ImageField(
        'Profile Picture',
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        null=True
    )

    # Status fields
    is_verified = models.BooleanField(
        'Email Verified',
        default=False,
        help_text='Designates whether the user has verified their email address.'
    )

    # Timestamps
    created_at = models.DateTimeField(
        'Created At',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Updated At',
        auto_now=True
    )

    # Authentication settings
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active', 'is_verified']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        """String representation of the user."""
        return self.email

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def short_name(self):
        """Returns the first name or username if no first name."""
        return self.first_name or self.username

    @property
    def avatar_url(self):
        """Returns the avatar URL or a default URL."""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/images/default-avatar.png'

    def get_absolute_url(self):
        """Returns the URL for the user's profile."""
        return f"/users/{self.pk}/"

    def format_phone_number(self):
        """Returns formatted phone number with +237 prefix."""
        if not self.phone_number:
            return ""

        # Remove any existing prefix and spaces
        number = self.phone_number.replace('+237', '').replace('237', '').replace(' ', '')

        # Add +237 prefix if it's a valid Cameroon number
        if len(number) >= 8:
            return f"+237{number}"
        return self.phone_number


# Signals for automatic profile management
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Handle post-save operations for User model."""
    if created:
        # You can add any post-creation logic here
        # For example, sending welcome email, creating related objects, etc.
        pass