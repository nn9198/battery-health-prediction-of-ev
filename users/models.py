from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class UserPredictModel(models.Model):
    Current = models.FloatField()  # or appropriate field type
    Voltage = models.FloatField()  # or appropriate field type
    Speed = models.FloatField()    # or appropriate field type
    Temperature = models.FloatField()  # or appropriate field type
    Range = models.FloatField()    # or appropriate field type
    SOC = models.FloatField()
    Label = models.FloatField() # this is output

    def __str__(self):
        return f"Prediction: {self. Label}"
    


