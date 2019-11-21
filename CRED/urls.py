from django.conf.urls import url,include
import views


urlpatterns = [
    url(r'^$', views.sales, name='sales'),
    url(r'^create/$', views.create_sale, name='create'),
    url(r'^view/(?P<pk>.*)$', views.sale_sale, name='sale'),
    url(r'^edit/(?P<pk>.*)$', views.edit_sale_sale, name='edit'),
    url(r'^delete/(?P<pk>.*)$', views.delete_sale, name='delete'),

    # available for autocomplete and to get customer data to another page
    url(r'^customer-autocomplete/$',views.CustomerAutocomplete.as_view(),name='customer-autocomplete',),
    url(r'^get-customer$', views.get_customer, name='get_customer'),
]

