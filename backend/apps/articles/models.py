from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL
r = settings.DEFAULT_REDIS_CLIENT


class Topic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=False)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ActiveManager(models.Manager):
    """
    Returns queryset where all articles 'is_active' field is equal to True,
    field 'is_active' in Article model indicates visibility for users
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Article(models.Model):
    title = models.CharField(
        max_length=300,
        blank=False,
    )
    description = models.TextField(
        blank=False,
    )
    slug = models.SlugField(
        unique_for_date='published',
    )
    published = models.DateTimeField(
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        default=False,
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
    )
    source = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
    )
    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['topic']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'articles:detail',
            args=[
                self.slug,
                self.published.year,
                self.published.month,
                self.published.day,
            ],
        )

    def get_and_increase_views(self) -> int:
        views = r.incr(f'article:{self.id}:views')
        self.increase_rating()
        return views

    def increase_rating(self) -> None:
        r.zincrby('article_ranking', 1, self.id)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='written_comments',
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
    )
    edited = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.author} left a comment: {self.body}'
