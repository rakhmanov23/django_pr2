from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, ManyToManyField, CharField, SlugField, CASCADE, Model, IntegerField, \
    SmallIntegerField, PositiveIntegerField, JSONField, ForeignKey, DateTimeField, CheckConstraint, Q
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class User(AbstractUser):
    image = ImageField(upload_to='users/', null=True, blank=True)
    carts = ManyToManyField('apps.Product', through='apps.Cart')


class Category(MPTTModel):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, editable=False)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    discount = SmallIntegerField()
    description = CKEditor5Field()
    quantity = PositiveIntegerField()
    shipping_cost = IntegerField()
    specifications = JSONField(default=dict, blank=True)
    author = ForeignKey('apps.User', CASCADE)
    category = ForeignKey('apps.Category', CASCADE)
    tags = ManyToManyField('apps.Tag', blank=True)
    created_at = DateTimeField(auto_now_add=True)

    @property
    def current_price(self):
        return self.price - self.price * self.discount / 100


class Review(Model):
    title = CharField(max_length=255)
    product = ForeignKey('apps.Product', CASCADE)
    author = ForeignKey('apps.User', CASCADE)
    rating = SmallIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(rating__range=(0, 10)), name="rating_range_0_10")
        ]


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    created_at = DateTimeField(auto_now_add=True)


class Tag(Model):
    name = CharField(max_length=255)


class Order(Model):
    user = ForeignKey('apps.User', CASCADE)
    created_at = DateTimeField(auto_now_add=True)


class Cart(Model):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)
    created_at = DateTimeField(auto_now_add=True)


class OrderItem(Model):
    order = ForeignKey('Order', CASCADE)
    quantity = PositiveIntegerField(default=1, db_default=1)


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE)


class Country(Model):
    name = CharField(max_length=255)
    code = CharField(max_length=5)
