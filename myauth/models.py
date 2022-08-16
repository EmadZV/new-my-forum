from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserModel(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(choices=GENDER, max_length=6)
    phone_number = PhoneNumberField(default='0')
    last_seen = models.DateTimeField(default=None)
    profile_image = models.ImageField(upload_to='forum/images')

    def __str__(self):
        return self.user.username
