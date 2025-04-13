from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(_('Category Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    datetime_created = models.DateTimeField(_('Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Category')
    )
    title = models.CharField(_('Title'), max_length=100)
    description = RichTextField()
    short_description = models.TextField(_('Short Description'), blank=True)
    price = models.PositiveIntegerField(_('Price'), default=0)
    active = models.BooleanField(_('Active'), default=True)
    image = models.ImageField(_('Product Image'), upload_to='product/product_cover/', blank=True,)

    datetime_created = models.DateTimeField(_('Date Time of Creation'), default=timezone.now)
    datetime_modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


class ActiveCommentsManger(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManger, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]

    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name=_('Product')
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Comment author')
    )
    body = models.TextField(verbose_name=_('Comment Text'))
    stars = models.CharField(
        max_length=10, 
        choices=PRODUCT_STARS, 
        verbose_name=_('What is your score?')
    )

    datetime_created = models.DateTimeField(_('Created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(_('Modified'), auto_now=True)

    active = models.BooleanField(_('Active'), default=True)

    # Manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManger()

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return f'{self.author}: {self.body[:50]}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])