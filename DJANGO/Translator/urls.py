from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^switch-language/$', general_views.switch_language, name='switch_language'),
    ...
]    

urlpatterns += i18n_patterns(
    path('', include(('web.urls', 'web'), namespace='web')),
    path('app/', general_views.app, name='app'),
    path('app/dashboard/', general_views.dashboard, name='dashboard'),
    path('app/main/', include('main.urls')), 

)
