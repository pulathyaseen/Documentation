
    # install
        pip install django-versatileimagefield
		
    #settings.py -> add in installed apps
		'versatileimagefield',
		
	#to be added in settings.py
		VERSATILEIMAGEFIELD_SETTINGS = {
    		'cache_length': 2592000,
    		'cache_name': 'versatileimagefield_cache',
    		'jpeg_resize_quality': 70,
    		'sized_directory_name': '__sized__',
    		'filtered_directory_name': '__filtered__',
    		'placeholder_directory_name': '__placeholder__',
    		'create_images_on_demand': True,
    		'image_key_post_processor': None,
    		'progressive_jpeg': False
		}
		
    # models.py 
        from versatileimagefield.fields import VersatileImageField
		
        photo = VersatileImageField('image', blank=True, null=True, upload_to='customers/') 
		# image is the common name given to the files uploaded
	
	# changes in template.html -> where the image is displayed
		<img class="img-responsive" src="{{instance.photo.crop.600x600}}" alt="{{instance.name}}" />
		<img class="img-responsive" src="{{instance.photo.thumbnail.600x600}}" alt="{{instance.name}}" /> 

#thumbnail is better becouse it doesn't force to be on the size specified. it automatically adjusts height(if width is bigger than height)



# adding ImageField in django
	
		
		
		
