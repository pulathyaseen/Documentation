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
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from users.models import Notification
from main.functions import get_auto_id,get_a_id,generate_form_errors
from main.decorators import check_mode,ajax_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from customers.models import Customer
from customers.forms import CustomersForm
from dal import autocomplete


class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Customer.objects.none()

        items = Customer.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query))
        return items


@login_required
def create_customer(request):
    if request.method=='POST':
        form = CustomersForm(request.POST,request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Customer)
            data.save()

            # response_data = {
            #     'status' : 'true',
            #     'title' : 'successfully Created',
            #     'message' : "Successfully Created new Customer",
            #     'redirect' : 'true',
            #     'redirect_url' : reverse('customers:customer',kwargs={"pk":data.pk})
            # }
            return HttpResponseRedirect(reverse('customers:view_customer',kwargs={"pk":data.pk}))

        else:
            # message = generate_form_errors(form,formset=False)
            # responsive_data = {
            #     'status' : 'false',
            #     'stable' : 'true',
            #     'title' : 'Form Validation Error Occured',
            #     'message' : message,
            # }
            form = CustomersForm(request.POST)
            context = {
                "form" : form,
                "title" : "Create Customer",
                "redirect": True,

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

            return render(request,'customers/entry.html',context)
        # return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = CustomersForm()
        context = {
            "form" : form,
            "title" : "Create Customer",
            "redirect": True,

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

        return render(request,'customers/entry.html',context)


def customers(request):
    instances = Customer.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query))
    context = {
        'title': "customers :",
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
    return render(request,'customers/customers.html',context)


def view_customer(request,pk):
    instance = get_object_or_404(Customer.objects.filter(pk=pk))
    context = {
        'title': "customer : " + instance.name,
        'instance' : instance,

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
    return render(request,'customers/customer.html',context)


@login_required
def edit_customer(request,pk):
    instance = get_object_or_404(Customer.objects.filter(pk=pk))

    if request.method=='POST':
        form = CustomersForm(request.POST,request.FILES,instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.updater = request.user
            data.date_updated = datetime.datetime.now()
            data.save()

            # response_data = {
            #     'status' : 'true',
            #     'title' : 'successfully Updated',
            #     'message' : "Successfully Updated Customer",
            #     'redirect' : 'true',
            #     'redirect_url' : reverse('customers:customer',kwargs={"pk":data.pk})
            # }

            return HttpResponseRedirect(reverse('customers:view_customer',kwargs={"pk":data.pk}))

        else:
        #     message = generate_form_errors(form,formset=False)
        #     responsive_data = {
        #         'status' : 'false',
        #         'stable' : 'true',
        #         'title' : 'Form Validation Error Occured',
        #         'message' : message,
        #     }
        #
            form = CustomersForm(requets.POST)
            context = {
                "form" : form,
                "title" : "Update Customer",
                "redirect": True,

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

            return render(request,'customers/entry.html',context)
        # return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = CustomersForm(instance=instance)
        context = {
            "form" : form,
            "title" : "Update Customer",
            "redirect": True,

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

        return render(request,'customers/entry.html',context)


@login_required
@ajax_required
def delete_customer(request,pk):
    Customer.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "true",
        "title" : "Successfully Deleted",
        "message" : "Customer Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('customers:customers')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def get_customer(request):
    pk = request.GET.get('id')
    if Customer.objects.filter(pk=pk).exists:
        customer = Customer.objects.get(pk=pk)
        response_data = {
            'status' : 'true',
            'email' : customer.email,
            'phone' : customer.phone,
            'address' : customer.address,
        }

    else:
        response_data = {
            'status' : 'false',
            'message' : 'Customer does not exist',
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
