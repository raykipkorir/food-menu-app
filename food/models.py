from django.conf import settings
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "Categories"


class Food(models.Model):
    name = models.CharField(max_length=50)
    food_pic = models.ImageField(upload_to="food_images", blank=True, null=True)
    price = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now = True)
    tags = TaggableManager()
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-date_updated"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("food", kwargs={"pk": self.pk})

    @property
    def food_price(self):
        currency = "Ksh."
        return f"{currency}{self.price}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
