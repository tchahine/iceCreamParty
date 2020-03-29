# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.serializers import json
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponseForbidden

from .models import Order, Flavour, FlavourQuantity


# TEMPLATES
def homepage(request, template_name='vm/index.html'):
    """ Homepage template render """
    context = {}
    return render(request, template_name, context)


def order(request, template_name='vm/order.html'):
    """ Render list of all flavour available """
    flavours_list = Flavour.objects.filter(quantity__gt=0).order_by('name')
    context = {'flavours_list': flavours_list}
    return render(request, template_name, context)


def search_order(request, template_name='vm/search_order.html'):
    """ Order search template render"""
    orders_list = Order.objects.all()[:5]
    context = {'orders_list': orders_list}
    return render(request, template_name, context)


@staff_member_required
def administration(request, template_name='vm/administration.html'):
    """
    Administration template to display all flavour to fill them.
    Available only if the user is connected in admin.
    """
    flavours = Flavour.objects.all()
    context = {
        'flavours': flavours,
    }

    return render(request, template_name, context)


# API
@staff_member_required
def ajax_fill_flavour(request, pk):
    """ Ajax call to fill the ice cream flavour """
    flavour = get_object_or_404(Flavour, id=pk)
    flavour.quantity = flavour.capacity
    flavour.save()
    data = dict()
    data['flavour'] = render_to_string(template_name='include/capacity.html',
                                        request=request,
                                        context={
                                            'flavour': flavour,
                                        })
    data['flavour_id'] = flavour.id
    return JsonResponse(data)


def ajax_search_order(request, code):
    """
    This is an ajax api to find an order from its code
    :param code: the order's code (string{8})
    :return: template of order if find it and a list of ice cream ball pictures (flavours),
        if not 404 error if code doesn't exist,
    """
    order = get_object_or_404(Order, code=code)
    data = dict()
    flavours = []
    flavour_quantity = order.flavour_quantity.all()
    for fq in flavour_quantity:
        for i in range(fq.quantity):
            flavours.append(fq.flavour.picture_name)

    data['order'] = render_to_string(template_name='include/order_container.html',
                                        request=request,
                                        context={
                                            'order': order,
                                            'flavours': flavours,
                                        })
    return JsonResponse(data)


def ajax_save_order(request):
    """
    Save order.
    Get all ids and quantity of these ids.
    Check if the quantity is number, and if the quantity asked is possible
        with the quantity of the flavour

    :return: template of order created and a list of ice cream ball pictures (flavours)
    """
    if request.POST:
        allQty = 0
        order = Order();
        ids = request.POST.getlist('id')

        for i in range(len(ids)):
            qty = request.POST.getlist('quantity')[i]
            id = ids[i]
            try:
                """ Check if quantity is number """
                qty = int(qty)
                if qty > 0:
                    allQty += int(qty)
                    flavour = Flavour.objects.get(pk=id)
                    if int(qty) > flavour.quantity:
                        """ Check if the quantity is possible"""
                        return HttpResponseForbidden()
                    else:
                        order.save()
                        flavour_quantity = FlavourQuantity(flavour=flavour, order=order, quantity=int(qty))
                        flavour_quantity.save()

            except ValueError:
                # it's not a number
                allQty += 0 # "nothing to do"

        data = dict()
        if allQty > 0:
            order.save()
            flavours = []
            flavour_quantity = order.flavour_quantity.all()
            for fq in flavour_quantity:
                for i in range(fq.quantity):
                    flavours.append(fq.flavour.picture_name)

            data['order'] = render_to_string(template_name='include/order_container.html',
                                             request=request,
                                             context={
                                                 'order': order,
                                                 'flavours': flavours,
                                             })

        else:
            #data["error"] = "Commande vide"
            return HttpResponseForbidden()

        return JsonResponse(data)
    else:
        return {}
