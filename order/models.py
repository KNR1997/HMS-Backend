import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Customer
from common.models import AuditableModel, BaseModel
from products.models import Product, ProductVariation, Batch

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+94719999999'. Up to 15 digits allowed."
)


class Order(BaseModel, AuditableModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    order_number = models.IntegerField(null=True, unique=True)
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), on_delete=models.CASCADE)
    customer_contact = models.CharField(max_length=15, null=True, blank=True, validators=[phone_regex])
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    language = models.CharField(max_length=10, default='en', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    percentage_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    percentage_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    note = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(verbose_name=_('Status'), max_length=20, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Customer-{self.customer} - O#-{self.order_number}"


class OrderItem(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    batch_number = models.CharField(max_length=50, blank=True, null=True)  # Added batch number
    item_name = models.CharField(max_length=200, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    percentage_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    sale_price_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    percentage_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    flat_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    quantity = models.IntegerField(blank=True, default=1)
    return_quantity = models.IntegerField(default=0)
    item_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    order = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)
    product_variant = models.ForeignKey(ProductVariation, blank=True, null=True, on_delete=models.SET_NULL)
    batch = models.ForeignKey(Batch, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Order-{self.order}"


class OrderAddress(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    order = models.ForeignKey(Order, blank=False, null=True, on_delete=models.CASCADE, related_name='order_addresses')
    title = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    delivery_contact = models.CharField(max_length=15, blank=True, null=True, validators=[phone_regex])
    delivery_note = models.CharField(max_length=200, blank=True, null=True)
    delivery_time = models.CharField(max_length=100, null=True, blank=True)
    delivery_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Id-{self.id} Order-{self.order.order_number}"
