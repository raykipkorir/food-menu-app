from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from PIL import Image


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField('email address', blank=True, unique=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ,
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class UserProfile(models.Model):
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    twitter = models.URLField(blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_pic:
            img = Image.open(self.profile_pic.path)

            def crop_center(pil_img, crop_width, crop_height):
                img_width, img_height = pil_img.size
                return pil_img.crop(
                    (
                        (img_width - crop_width) // 2,
                        (img_height - crop_height) // 2,
                        (img_width + crop_width) // 2,
                        (img_height + crop_height) // 2,
                    )
                )

            def crop_max_square(pil_img):
                return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

            im_thumb = crop_max_square(img).resize((300, 300), Image.LANCZOS)
            im_thumb.save(self.profile_pic.path, quality=95)