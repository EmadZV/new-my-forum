from django.core.validators import MinValueValidator, MaxValueValidator
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
    # rating = models.DecimalField(decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    #
    # def ratingcalclulator(self):
    #

    def __str__(self):
        return self.user.username
