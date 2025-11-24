from django.contrib.auth import get_user_model
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skill(models.Model):
    FUNDAMENTAL = 'Fundamental'
    BASIC = 'Basic'
    LEVEL_CHOICES = [
        (FUNDAMENTAL, 'Fundamental'),
        (BASIC, 'Basic'),
    ]

    name = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=FUNDAMENTAL)
    proficiency = models.PositiveSmallIntegerField(default=60, help_text='0-100 percentage')
    icon = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.level})'


class Project(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('django', 'Django'),
        ('python', 'Python'),
        ('web', 'Web'),
        ('other', 'Others'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=600)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    demo_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class GalleryImage(TimeStampedModel):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='gallery/')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BlogPost(TimeStampedModel):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} by {self.name}'
