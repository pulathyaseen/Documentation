#modules for urls.py in project

    from django.conf.urls import url, include
    from django.contrib import admin
    from django.conf import settings
    from registration.backends.default.views import RegistrationView
    from django.views.static import serve
    

#modules for urls.py in app
    #python2 -->
        from django.conf.urls import url,include
        import views
    
    # python3 -->
        from django.urls import path, re_path
        from . import views
    

#modules for views.py (especially for erp)

    from django.core.urlresolvers import reverse
    from django.http.response import HttpResponseRedirect, HttpResponse
    import json
    import datetime
    from django.views.decorators.http import require_GET, require_POST
    from django.contrib.auth.decorators import login_required
    from django.shortcuts import resolve_url, render, get_object_or_404
    from django.views.decorators.csrf import csrf_protect
    from django.contrib.auth.tokens import default_token_generator
    from django.template.response import TemplateResponse
    from django.forms.models import formset_factory
    from django.forms.models import inlineformset_factory
    from django.forms.widgets import TextInput, Textarea, Select
    from django.contrib.auth.models import User, Group
    from django.core.mail import send_mail
    from django.contrib.auth.forms import PasswordChangeForm
    from django.db.models import Q
    from dal import autocomplete
    
    
#modules for models.py

    from __future__ import unicode_literals
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from decimal import Decimal
    from django.core.validators import MinValueValidator
    
    
#modules for forms.py

    from django import forms
    from django.forms.widgets import TextInput, Textarea, Select
    from django.utils.translation import ugettext_lazy as _
    from dal import autocomplete
