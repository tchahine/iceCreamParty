# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.dispatch import receiver
from decimal import Decimal
from django.db.models.signals import post_save
from tools import random_string
from django.core.mail import send_mail


class Flavour(models.Model):
    """
    Flavour model for each ice cream
    """
    name = models.CharField('Name', max_length=250)
    picture_name = models.CharField('Picture', max_length=250)
    price = models.DecimalField('Price', default=2.00, decimal_places=2, max_digits=20)
    quantity = models.PositiveIntegerField('Quantity', default=40)
    capacity = models.PositiveIntegerField('Capacity', default=40)
    order = models.ManyToManyField('Order', through='FlavourQuantity', related_name='orders')

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        super(Flavour, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Parfum'
        verbose_name_plural = 'Parfums'


class Order(models.Model):
    """
    Order model
    """
    date = models.DateTimeField(auto_now_add=True)
    code = models.CharField('Code', max_length=250, unique=True)
    final_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    def __unicode__(self):
        return unicode(self.code) if self.code else 'New Order'

    class Meta:
        ordering = ['-date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def save(self, *args, **kwargs):
        """
        We create a random code of 8 characters for the order.
        We update the sum of all FlavourQuantity of the order to define the final price
        """
        random_code = random_string(8)
        while Order.objects.filter(code=random_code).exists():
            random_code = random_string(8)
        self.code = random_code
        flavour_quantity = self.flavour_quantity.all()
        self.final_price = flavour_quantity.aggregate(Sum('total_price'))['total_price__sum'] if flavour_quantity.exists() else 0.00
        super(Order, self).save(*args, **kwargs)

    def tag_value(self):
        return '{value} {currency}'.format(value=self.final_price, currency=settings.CURRENCY.decode('utf-8'))


class FlavourQuantity(models.Model):
    """
    Class to connect the flavour and the order
    """
    flavour = models.ForeignKey(Flavour, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='flavour_quantity')
    quantity = models.PositiveIntegerField('Quantity')
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    def __unicode__(self):
        return '{value} - {quantity}'.format(value=self.self.flavour.name, quantity=self.quantity)

    def save(self, *args, **kwargs):
        """
        Before the save, we update the total price : quantity x price
        """
        self.total_price = Decimal(self.quantity) * Decimal(self.flavour.price)
        super(FlavourQuantity, self).save(*args, **kwargs)

    def tag_total_price(self):
        return '{price} {currency}'.format(price=self.total_price, currency=settings.CURRENCY.decode('utf-8'))


@receiver(post_save, sender=FlavourQuantity)
def update_quantity(sender, instance, **kwargs):
    """
    After save the flavourQuantity, the quantity is updated on Flavour, and an email is send if the quantity equal 0
    """
    try:
        # flavour = Flavour.objects.get(
        #    id=instance.flavour.id
        # )
        flavour = instance.flavour
        flavour.quantity -= instance.quantity
        if flavour.quantity == 0:
            print('Attention la glace {0} est vide'.format(flavour.name))
            # send_mail('Attention la glace {0} est vide'.format(flavour.name),
            #           'Allez vite dans l\'interface pour la remplir',
            #           settings.ADMIN_MAIL,
            #           ['theo.chahine+dev@gmail.com'],
            #           fail_silently=False, )
        flavour.save()
    except Exception, e:
        print e
