# -*- coding: utf-8 -*-
import pytest
from decimal import Decimal
from models import Flavour, FlavourQuantity, Order
from vm.tools import random_string


def test_tools_random_string():
    """
    Test the random_string tools to check if the render has the good length
    and is only [a-zA-Z]
    :return:
    """
    test = random_string(18)
    assert len(test) == 18
    assert test.isalpha() == True


@pytest.fixture()
def set_up_flavour():
    """
    Setup to declare flavour
    """
    Flavour.objects.create(name="Choco", picture_name="choco.png")
    Flavour.objects.create(name="Vanille des îles", picture_name="vanille.png", price=4.00, quantity=20)
    Flavour.objects.create(name="Caramel", picture_name="caramel.png")


@pytest.mark.django_db
def test_flavour_default_value(set_up_flavour):
    """
    Check the default values (price, quantity and capacity)  of a Flavour
    :param set_up_flavour: the setup
    """
    chocolate = Flavour.objects.get(name="Choco")
    assert chocolate.price == 2.00
    assert chocolate.quantity == 40
    assert chocolate.capacity == 40


@pytest.mark.django_db
def test_flavour_user_value(set_up_flavour):
    """
    Check the values with non default setting (price, quantity and capacity)
    of a Flavour
    :param set_up_flavour: the setup
    """
    vanilla = Flavour.objects.get(name="Vanille des îles")
    assert vanilla.price == 4.00
    assert vanilla.quantity == 20
    assert vanilla.capacity == 40


@pytest.fixture()
def set_up_flavour_quantity(set_up_flavour):
    """
    Setup to create an order with 4 Choco and 1 Vanilla flavour

    :param set_up_flavour: the setup for create 3 flavours
    :return: the ordet's code
    """
    flavour1 = Flavour.objects.get(name="Choco")
    flavour2 = Flavour.objects.get(name="Vanille des îles")

    order = Order.objects.create()
    flavour_quantity = FlavourQuantity(flavour=flavour1, order=order, quantity=4)
    flavour_quantity.save()
    flavour_quantity2 = FlavourQuantity(flavour=flavour2, order=order, quantity=1)
    flavour_quantity2.save()
    order.save()

    return order.code


@pytest.mark.django_db
def test_order_exist(set_up_flavour_quantity):
    """
    Check if the order is save
    :param set_up_flavour_quantity: creation of the order
    """
    assert Order.objects.filter(code=set_up_flavour_quantity).exists() == True


@pytest.mark.django_db
def test_order_dont_exist(set_up_flavour_quantity):
    """
    Check if a false order doesn't exist
    :param set_up_flavour_quantity: creation of the order
    """
    assert Order.objects.filter(code="a").exists() == False


@pytest.mark.django_db
def test_order_values(set_up_flavour_quantity):
    """
    Check value (price, quantity) after save the order
    :param set_up_flavour_quantity: creation of the order
    """
    order = Order.objects.get(code=set_up_flavour_quantity)

    flavour_quantity = order.flavour_quantity.all()
    assert flavour_quantity[0].total_price == Decimal('8.00')
    assert flavour_quantity[0].quantity == 4
    assert flavour_quantity[1].total_price == Decimal('4.00')
    assert flavour_quantity[1].quantity == 1

    assert order.final_price == Decimal('12.00')
    assert order.tag_value() == '12.00 €'.decode('utf-8')

    flavour1 = Flavour.objects.get(name="Choco")
    flavour2 = Flavour.objects.get(name="Vanille des îles")
    flavour3 = Flavour.objects.get(name="Caramel")
    assert flavour1.quantity == 36
    assert flavour2.quantity == 19
    assert flavour3.quantity == 40
