from django.db import models
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.crypto import get_random_string


# Create your models here.

class BlogInfo(models.Model):
    site_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=60, null=True,blank=True)
    details = models.TextField(max_length=200)
    logo = models.ImageField(upload_to='media')
    facebook_url = models.CharField(max_length=150, null=True,blank=True)
    twitter_url = models.CharField(max_length=150, null=True,blank=True)
    youtube_url = models.CharField(max_length=150, null=True,blank=True)
    pinterest_url = models.CharField(max_length=150, null=True,blank=True)
    instagram_url = models.CharField(max_length=150, null=True,blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name_plural = '1. Blog Info'

class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category)
            while Category.objects.filter(slug = self.slug).exists():
                self.slug = f'{slugify(self.category)}-{get_random_string(2)}'
        super().save(*args,**kwargs)

    def __str__(self):
        return self.category
    
    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = '2. Category'

    
class BlogPost(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('publish', 'Publish')
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, null=True,blank=True)
    feature_img = models.ImageField(upload_to='media')
    featured_post = models.BooleanField(default=False)
    content = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,blank=True)
    tags = TaggableManager(blank=True)
    # for seo
    seo_title = models.CharField(max_length=70, null=True,blank=True, help_text='Enter Optimized SEO Title(max length: 70 chars)')
    seo_description = models.TextField(max_length=160, null=True,blank=True, help_text='Enter Optimized SEO Description(max length: 160 chars)')
    # seo ends here
    status = models.CharField(max_length=50, choices=STATUS, default='draft')
    publish_on = models.DateTimeField(auto_now_add=True)
    modify_on = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0, null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while BlogPost.objects.filter(slug = self.slug).exists():
                self.slug = f'{slugify(self.title)}-{get_random_string(2)}'
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish_on']
        verbose_name_plural = '3. All Posts'

# comment system
class Comment(models.Model):
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)