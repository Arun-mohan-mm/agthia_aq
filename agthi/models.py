from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings


class Registration(models.Model):
    password = models.CharField(max_length=200, null=True)
    user_role = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Job_recruitment(models.Model):
    restaurant = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    salary_range = models.CharField(max_length=200, null=True)
    age_limit = models.CharField(max_length=200, null=True)
    employment_type = models.CharField(max_length=200, null=True)
    place = models.CharField(max_length=200, null=True)


class Job_application(models.Model):
    full_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    resume = models.FileField(null=True)
    apl_rec = models.ForeignKey(Job_recruitment, on_delete=models.CASCADE, null=True)

    def delete(self, *args, **kwargs):
        if self.resume:
            resume_path = os.path.join(settings.MEDIA_ROOT, self.resume.path)
            if os.path.isfile(resume_path):
                os.remove(resume_path)
        super().delete(*args, **kwargs)


class Restaurants(models.Model):
    logo = models.ImageField(null=True)
    image = models.ImageField(null=True)
    name = models.CharField(max_length=200, null=True)
    local_international = models.CharField(max_length=200, null=True)
    brand_paragraph = models.TextField(null=True)
    brand_paragraph1 = models.TextField(null=True)
    url = models.URLField(max_length=200, null=True)
    instagram_link = models.URLField(max_length=200, default="https://www.instagram.com/", null=True)
    facebook_link = models.URLField(max_length=200, default="https://www.facebook.com/", null=True)
    twitter_link = models.URLField(max_length=200, default="https://www.twitter.com/", null=True)


class Aboutt(models.Model):
    description = models.TextField(null=True)
    description1 = models.TextField(null=True)


class Our_people(models.Model):
    description = models.TextField(null=True)


class Mission(models.Model):
    description = models.TextField(null=True)


class Vision(models.Model):
    description = models.TextField(null=True)


class Word_from_CEO(models.Model):
    description = models.TextField(null=True)


class Latest_news(models.Model):
    news_title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)


class Restaurant_images(models.Model):
    image = models.ImageField(null=True)
    img_resta = models.ForeignKey(Restaurants, on_delete=models.CASCADE, null=True)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.path)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)


class Subscriptions(models.Model):
    email = models.CharField(max_length=200, null=True)


class Contact_uss(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    place = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    instagram_link = models.URLField(max_length=200, default="https://www.instagram.com/", null=True)
    facebook_link = models.URLField(max_length=200, default="https://www.facebook.com/", null=True)
    twitter_link = models.URLField(max_length=200, default="https://www.twitter.com/", null=True)
    pinterest_link = models.CharField(max_length=200, default="https://www.pinterest.com/", null=True)
    contact_email = models.CharField(max_length=200, null=True)