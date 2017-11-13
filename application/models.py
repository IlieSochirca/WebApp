from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models import Count
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    birth_date = models.DateField(null=True, blank=False)  #the below fields are added as desired
    current_project = models.CharField(max_length=50, blank=False)
    hobby = models.TextField(max_length=150, blank=False, null=True)
    phone = models.CharField(max_length=20,blank=False, null=True)
    city = models.CharField(max_length=50, blank=False, null=True)
    image = models.ImageField(upload_to='media/images')
    is_admin = models.BooleanField(default=False)

    def create_profile(sender, **kwargs):  # this part is helping us syncronize to create the user in the User table and in our Profile table too in the DB
        user = kwargs['instance']
        if kwargs['created']:
            user_profile=Profile(user=user)
            user_profile.save()
    post_save.connect(create_profile, sender=User)

    def __str__(self):
        return "%s" %self.user

class GroupCategory(models.Model):
    name = models.CharField(max_length=30, default=None, blank=False, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return "%s" % self.name


class Group(models.Model):
    name = models.CharField(max_length=30, blank=False, null=True, default=None)
    category = models.ForeignKey(GroupCategory, blank=False, null=True, default=None)
    description = models.CharField(max_length=50, blank=False, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, related_name='follow', default=None)
    followers = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=True, auto_now=False)
    added_by = models.ForeignKey(User, blank=False, null=True, default=None)


    def get_absolute_url(self):
        return reverse('application:group_detail', kwargs={'group_pk': self.pk}) # this function helps redirect the user to detail page after he created a new group

    def __str__(self):
        return "%s" %self.name
    class Meta:
        ordering = ["-created"]

class Post(models.Model):
    name = models.CharField(max_length=30, blank=False, null=True, default=None)
    group_post = models.ForeignKey(Group, blank=False, null=True, default=None)
    image = models.FileField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)
    post_user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    description = models.TextField(blank=False, null=True, default=None)
    posted_by = models.ForeignKey(User, null=True, default=None, related_name='posts_create')    # posted by who?
    updated_by =models.ForeignKey(User, null=True, default=None, related_name="posts_update")
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=True, auto_now=False)

    @property
    def get_total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('application:post_detail', kwargs={'pk':self.pk, 'group_pk': self.group_post.pk})

    def __str__(self):   #the string representation of the object
        return "%s" % self.name

    class Meta:
        ordering = ["-created"]   # the "-' before meants we want it to show in reverse way

class Comment(models.Model):
    description = models.TextField(blank=False, null=True, default=None)
    comment_post = models.ForeignKey(Post, blank=False, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/images',null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    comment_user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="comment_likes")
    added_by = models.ForeignKey(User, null=True)

    @property
    def get_total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('application:post_detail',  kwargs={"pk":self.comment_post.pk, "group_pk":self.comment_post.group_post.pk})

    def __str__(self):
        return "%s" %self.comment_post