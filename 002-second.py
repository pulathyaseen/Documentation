# CONTEXT PROCESSORS
    # Create a new file web/context_processors.py
        def main_context(request):
            return {
                "caption" : "Femme Caption"
            }
    # Add to settings.py (TEMPLATES/OPTIONS)
        'web.context_processors.main_context',

    <title>caption</title>  #this has to be Replaced with
    <title>{{caption}}</title>



# sample model
    class About(models.Model):
        title = models.CharField(max_length=128)
        content = models.TextField()
        image = models.ImageField(upload_to="web/about/")

        class Meta:
            db_table = 'web_about'
            verbose_name = "about"
            verbose_name_plural = "about"

        def __unicode__(self):
            return self.title

    #after every model creation/edit it should be migrated to database


# Import About model in admin.py to add data by admin
    from __future__ import unicode_literals
    from django.contrib import admin
    from web.models import About


    class AboutAdmin(admin.ModelAdmin):
        list_display = ('title','content','image')

    admin.site.register(About,AboutAdmin)


#importand things to be imported in views.py
    from __future__ import unicode_literals
    from django.shortcuts import render
    from django.http.response import HttpResponse, HttpResponseRedirect
    from django.core.urlresolvers import reverse


# Define a new views.py entry
    def about(request):
        context = {
            "title" : "Femme",
            "caption" : "Femme Caption",
        }
        return render(request, 'web/about.html',context)
    # Specify in url patterns (web/views.py)
        url(r'^about$', views.about,name="about"),

    # update link in index 
        href = "{% url 'web:about' %}"
    # Create a new page about.html and load http://localhost:8000/about
    
    # filter() returns a queryset eg:
        product.filter(id=pk) #if pk = 1 then it will show elements that has id = 1
        product.filter(name='sam') #it will show only if the name is "sam" none other(SAM,Sam,..)
        product.filter(name__contains='sam') # it will return every names that contain sam eg:(samuel, ...) case sensitive
        product.filter(name__icontains='sam') # it will return every names that contain sam eg:(Sam, Samuel,...), not case sensitive.


# forms.py # sample
    from django import forms
    from django.forms.widgets import TextInput, Textarea, Select
    from django.utils.translation import ugettext_lazy as _
    from customers.models import Customer


    class CustomersForm(forms.ModelForm):
        class Meta:
            model = Customer
            exclude = ['is_deleted',]
            widgets  = {
                'name': TextInput(attrs={'class':'required form-control','placeholder': 'NAME'}),
                'email': TextInput(attrs={'class':'email required form-control','placeholder': 'E-MAIL'}),

            }
            error_messages = {
                'name' : {
                    'required' : _("Name Field is required."),
                },
                'email' : {
                    'required' : _("E-mail Field is required."),
                },
            }
