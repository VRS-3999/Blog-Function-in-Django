from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                          .filter(status='Published')

class Post(models.Model):
    objects=models.Manager()
    published=PublishedManager()
    STATUS_CHOICE = (
        ('draft','Draft'),
        ('published','Published'),
        )
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,
                          unique_for_date='publish')
    author=models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='My_Adventure_post')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,
                            choices=STATUS_CHOICE,
                            default='draft')
    tags=TaggableManager()
    
    def get_absolute_url(self):
        return reverse('My_Adventure:post_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
    class Meta:
        ordering=('-publish',)
        #db_table='Actuary'  for custum table name in database

    def __str__(self):
        return self.title
         
class Comment(models.Model):
    post=models.ForeignKey(Post,
                           on_delete=models.CASCADE,
                           related_name='comments')
    name=models.CharField(max_length=100)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)