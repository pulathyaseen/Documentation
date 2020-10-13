
urlpatterns += i18n_patterns(
    path('', include(('web.urls', 'web'), namespace='web')),
    path('app/', general_views.app, name='app'),
    path('app/dashboard/', general_views.dashboard, name='dashboard'),
    path('app/main/', include('main.urls')), 

)
