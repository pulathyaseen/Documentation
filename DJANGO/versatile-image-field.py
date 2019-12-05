# to create a versatile image field

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
		
        photo = VersatileImageField('image', blank=True, null=True, upload_to='customers/') # image is the common name given to the files uploaded
	
	# changes in views.py -> chnages are to be made becouse ajax won't work on image field......... same edits are required in edit function
		def create(request):
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
            		return HttpResponseRedirect(reverse('customers:customer',kwargs={"pk":data.pk}))

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

    		else: .....# part is same as old
			
	
	# changes in template.html -> where the image is displayed
	# Remove form classes 
		class ="ajax reset redirect skip_empty_row not_allowed_without_formset" #remove these classes from form tag
		<img class="img-responsive" src="{{instance.photo.crop.600x600}}" alt="{{instance.name}}" />
		<img class="img-responsive" src="{{instance.photo.thumbnail.600x600}}" alt="{{instance.name}}" /> 

#thumbnail is better becouse it doesn't force to be on the size specified. it automatically adjusts height(if width is bigger than height)



# adding ImageField in django
	
		
		
		
