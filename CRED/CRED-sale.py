from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
import json
import datetime
from users.forms import UserForm
from users.models import Notification, Permission
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from main.decorators import ajax_required,check_mode
from django.shortcuts import resolve_url, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.template.response import TemplateResponse
from django.forms.models import formset_factory
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput, Textarea, Select
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from main.functions import get_auto_id,get_a_id,generate_form_errors
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from sales.models import Sale,SaleItem
from sales.forms import SaleForm,SaleItemForm
from products.functions import update_stock
from products.models import Product
from dal import autocomplete


@login_required
def create_sale(request):
    SaleItemFormset = formset_factory(SaleItemForm,extra=3)
    if request.method=='POST':
        form = SaleForm(request.POST)
        sale_item_formset = SaleItemFormset(request.POST,prefix="sale_item_formset")
        if form.is_valid() and sale_item_formset.is_valid():

            items = {}
            for f in sale_item_formset:
                product = f.cleaned_data['product']
                qty = f.cleaned_data['qty']
                if str(product.pk) in items:
                    q = items[str(product.pk)]["qty"]
                    items[str(product.pk)]["qty"] = q + qty
                else:
                    dic = {
                        "qty" : qty,
                    }
                    items[str(product.pk)] = dic

            stock_ok = True
            error_message =""
            for key, value in items.iteritems():
                product = Product.objects.get(pk=key)
                stock = product.stock
                qty = value['qty']
                if qty > stock:
                    stock_ok = False
                    error_message +="%s has only %s in stocks, " %(product.name,str(stock))

            if stock_ok:
                discount = form.cleaned_data['discount']

                data = form.save(commit=False)
                data.creator = request.user
                data.updater = request.user
                data.auto_id = get_auto_id(Sale)
                data.save()

                subtotal = 0
                for item in sale_item_formset:
                    product = item.cleaned_data['product']
                    qty = item.cleaned_data['qty']
                    price = product.price
                    sub = qty * price
                    subtotal += sub

                    SaleItem.objects.create(
                        product = product,
                        qty = qty,
                        sale = data
                    )

                    update_stock(product.pk,qty,"decrease")

                total = subtotal-discount
                data.subtotal = subtotal
                data.total = total
                data.save()

                response_data ={
                    "status": "true",
                    "title": 'Successfully created',
                    'message': "sale successfully created",
                    "redirect": "true",
                    "redirect_url": reverse('sales:view_sale',kwargs={'pk':data.pk})
                }
            else:
                response_data ={
                    "status": "False",
                    "stable": "True",
                    "title": 'Out Of Stock',
                    'message': error_message,
                }

        else:
            message = generate_form_errors(form,formset=False)
            message += generate_form_errors(sale_item_formset,formset=True)
            response_data = {
                "status" : "False",
                "stable": "true",
                'title': "form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        sale_form = SaleForm()
        sale_item_formset = SaleItemFormset(prefix="sale_item_formset")
        context = {
            "form" : sale_form,
            "title" : "Create Sale",
            "sale_item_formset": sale_item_formset,
            'is_create_page':True,
            'url':reverse('sales:create'),
            'redierct':True,

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
            "is_need_animations": True,
        }

        return render(request,'sales/entry.html',context)


@login_required
def edit_sale(request,pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk,is_deleted=False))

    if SaleItem.objects.filter(sale=instance).exists:
        extra = 0
    else:
        extra = 1

    SaleItemFormset = inlineformset_factory(
        Sale,
        SaleItem,
        can_delete = True,
        extra = extra,
        exclude = ('sale',),
        widgets = {
            'product': autocomplete.ModelSelect2(url='products:product-autocomplete',attrs={'data-placeholder': 'Product','data-minimum-input-length':1}),
            'qty': TextInput(attrs={'class': 'required number form-control','placeholder':'Qty'}),
        }
    )

    if request.method == 'POST':
        form = SaleForm(request.POST,instance=instance)
        sale_item_formset = SaleItemFormset(request.POST,prefix='sale_item_formset',instance=instance)

        if form.is_valid() and sale_item_formset.is_valid():
            items = {}
            stock_ok = True
            error_message = ''

            for f in sale_item_formset:
                if f not in sale_item_formset.deleted_forms:
                    product = f.cleaned_data['product']
                    qty = f.cleaned_data['qty']
                    if str(product.pk) in items:
                        q = items[str(product.pk)]['qty']
                        items[str(product.pk)]['qty'] = q+qty
                    else:
                        dic = {
                            "qty": qty
                        }
                        items[str(product.pk)] = dic

            for key, value in items.iteritems():
                product = Product.objects.get(pk=key)
                prev_qty = 0

                if SaleItem.objects.filter(sale=instance,product=product).exists():
                    prev_qty = SaleItem.objects.get(sale=instance,product=product).qty

                stock = product.stock + prev_qty

                product_qty =value['qty']
                if product_qty > stock:
                    stock_ok =False
                    error_message += "%s has only %s in stock, " %(product.name,str(stock))

            if stock_ok:

                discount = form.cleaned_data['discount']

                data = form.save(commit=False)
                data.updater = request.user
                data.date_updated = datetime.datetime.now()
                data.save()

                all_subtotal = 0

                previous_sale_item = SaleItem.objects.filter(sale=instance)
                for p in previous_sale_item:
                    prev_qty = p.qty
                    update_stock(p.product.pk,prev_qty,"increase")
                previous_sale_item.delete()

                for key, value in items.iteritems():
                    product = Product.objects.get(pk=key)
                    qty = value['qty']
                    price = product.price
                    subtotal = (qty * price)
                    all_subtotal += subtotal
                    SaleItem(
                        sale = data,
                        product = product,
                        qty = qty,
                    ).save()

                    update_stock(product.pk,qty,"decrease")

                subtotal = all_subtotal
                data.subtotal = subtotal
                data.total = subtotal  - discount
                data.save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Updated",
                    "message": "Sale Successfully updated",
                    "redirect": "true",
                    "redirect_url": reverse('sales:view_sale',kwargs={'pk':data.pk})
                }

            else:
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "Out of Stock",
                    "message": error_message,
                }
        else:
            message = generate_form_errors(form,formset=False)
            message += generate_form_errors(sale_item_formset,formset=True)
            esponse_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message,
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = SaleForm(instance=instance)
        sale_item_formset = SaleItemFormset(prefix='sale_item_formset',instance=instance)
        context = {
            "form": form,
            "title": "Edit sale #: "+str(instance.auto_id),
            "instance": instance,
            "url": reverse('sales:edit',kwargs={'pk':instance.pk}),
            "sale_item_formset": sale_item_formset,
            "redirect": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
        }
        return render(request, 'sales/entry.html', context)


def sales(request):
    instances = Sale.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(Q(customer__name__icontains=query) | Q(customer__email__icontains=query) | Q(customer__phone__icontains=query) | Q(customer__address__icontains=query))
    context = {
        'title': "Sales : ",
        'instances' : instances,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_chosen_select" : True,
        "is_need_grid_system" : True,
        "is_need_datetime_picker" : True,
        "is_need_animations": True,
    }
    return render(request,'sales/sales.html',context)


def view_sale(request,pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))
    sale_items = SaleItem.objects.filter(sale=instance)
    context = {
        'title': "sale : " + str(instance.auto_id),
        'instance' : instance,
        'sale_items': sale_items,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_chosen_select" : True,
        "is_need_grid_system" : True,
        "is_need_datetime_picker" : True,
        "is_need_animations": True,
    }
    return render(request,'sales/sale.html',context)


@login_required
@ajax_required
def delete_sale(request,pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))

    #stock updation
    sale_item = SaleItem.objects.filter(sale=instance) #sale_item is an array of items that are bought
    for p in sale_item:
        qty = p.qty
        update_stock(p.product.pk,qty,"increase")

    #setting sale as deleted
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status" : "true",
        "title" : "Successfully Deleted",
        "message" : "Sale Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('sales:sales')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
