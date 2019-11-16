#   PYTHON-2

    virtualenv venv
    source venv/bin/activate

    pip install django==1.11.15
    pip install psycopg2

    cd src
    django-admin.py startproject `project_name`
    cd project_name
    mkdir static media templates


#   PYTHON-3

    virtualenv venv -p python-3

    ''''''''''''''


#setup database
    sudo su postgres
    createdb `dbname`
    createuser `user` -P
# enter password for new user
    psql
    	grant all privileges on database `dbname` to `user`;
    \q
    exit #exit from postgres


#start a new app
    python manage.py startapp `web`

#then register in INSTALLED_APPS
    'web'


#define DATABASES
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '`dbname`',
            'USER': '`user`',
            'PASSWORD': '`password`',
            'HOST':'localhost',
            'PORT': '',
        }
    }


#set URLs
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATIC_URL = '/static/'
    STATIC_FILE_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )


#define urlpatterns in project/urls.py  --> python 2
    from django.conf.urls import url ,include
    from django.contrib import admin
    from django.views.static import serve
    from django.conf import settings

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^',include('`web`.urls',namespace="`web`")),

        url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_FILE_ROOT}),
    ]
	
	# --> python 3
	
	from django.contrib import admin
	from django.urls import path, include
	from django.conf import settings
	from django.conf.urls.static import static


	urlpatterns = [
   		path('admin/', admin.site.urls),
   		path('', include('web.urls', namespace='web')),
    
	] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	
	
#create web/urls.py and paste the following --> python2
    from django.conf.urls import url
    import views


    urlpatterns = [
        url(r'^$', views.index,name="index"),
        url(r'^about/$', views.about,name="about"),
    ]

	
#  --> python3
	from django.contrib import admin
	from django.urls import path
	from . import views


	app_name = 'web'

	urlpatterns = [
   		path('', views.index, name='index'),
    	path('academics/', views.academics, name='academics'),
	]
	
	
	
#django models
    from django.utils.translation import ugettext_lazy as _
    from django.db import models
    from decimal import Decimal
    from django.core.validators import MinValueValidator

    class Blog(models.Model):
        auto_id = models.PositiveIntegerField(db_index=True,unique=True)  #for id as unique
        heading = models.CharField(max_length=128)
        content = models.TextField()
        adult = models.BooleanField(default=False)
        email = models.EmailField()
        date = models.DateField()
        main_content = RichTextUploadingField()  #will be like text editor
        price = models.DecimalField(default=0.0,decimal_places=2,max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
        college = models.ForeignKey('web.Colleges') #there is another model named Colleges in the web app
        image = models.ImageField(upload_to='images/blog')
        time = models.DateTimeField()
        video_url = models.URLField()

        class Meta:
            db_table = 'web_blog' #name of table to be created in the database
            verbose_name = ('Blog')
            verbose_name_plural = ('Blogs')
            ordering = ('-date')  #to show newest at first

        def __unicode__(self):
            return str(self.pk)


# Import model and define list display in admin.py
from __future__ import unicode_literals
    from django.contrib import admin
    from web.models import Blog

    class BlogAdmin(admin.ModelAdmin):
        list_display = ('heading','content','image','time','video_url')

    admin.site.register(Blog,BlogAdmin)


#to change admin header add these tags to change admin page tags
    admin.site.site_header = "PROJECT Admininistration"
    admin.site.site_title = "PROJECT Admin Portal"
    admin.site.index_title = "Welcome to PROJECT Researcher Portal"


# migrate changes into app and database
    python manage.py makemigrations
    python manage.py migrate


# Add superuser
    python manage.py createsuperuser
    # enter username, email(if needed) and password.


#change view into render, pass context,get objects in web/views.py
    from web.models import Blog

    def index(request):
        blog_datas = Blog.objects.all()

        context = {
            "title" : "HOME",
            "caption" : "The ultimate solution provider",
            "blog_datas" : blog_datas,
            "is_home" : True
        }
        return render(request, 'web/index.html',context)

# pass context and data into template
    	<title>{{title}} | {{caption}}</title>

# with for condition
	{% for blog in blog_datas %}
    <li>
        {{blog.image.url}}
        {{blog.title}}
        {{blog.content}}
    </li>
    {% endfor %}

# with if condition
        {% if blog_datas %}
            <p>content here</p>
        {% else %}
            <p>Nothing Found</p>
        {% endif %}

# Current year update(this tag will automatically add the current year at the place)
        {% now 'Y' %}


#template extending

    # create base.html
        #-------- header here --------
        {% block content %}
        	# ------- content of index should appear here -------
        {% endblock%}
        #------- footer here --------

    # index.html
        {% extends 'web/base.html' %}
        {% load static %}
        {% block content %}

        #-------- content of index here --------

        {% endblock%}

    # Fix hyperlinks
        href="{% url 'web:index' %}"
        href="{% url 'web:about' %}"
        href="{% url 'web:index' %}#features"


#database export and import
    python manage.py dumpdata > database.json
    python manage.py loaddata database.json


#delete migrations
    find . -path "*/migrations/*.pyc"  -delete
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete


# Use an existing project load this command after migrete in terminal
    python manage.py loaddata initial_data user_groups permissions notification
