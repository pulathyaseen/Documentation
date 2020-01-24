def short_tb_filter(request): 
    instances = PackageAppointment.objects.filter(is_deleted=False,visited=True)

    title = "Previous Package Appointments : "
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    date_error = "no"
    filter_date_period = False
    filter_date = False  # to check if user needs datas of one day only (if user enters from_date only)

    if from_date and to_date:
        try:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date() # + datetime.timedelta(days=1)            
        except ValueError:
            date_error = "yes"  
        filter_date_period = True

    elif from_date:
        try:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        except ValueError:
            date_error = "yes"  
        filter_date = True

    if filter_date_period:
        try:
            title = "Appointments : From %s to %s " %(str(from_date),str(to_date))
            if PackageAppointment.objects.filter(is_deleted=False,visited=True, date__range=[from_date, to_date]).exists():
                instances = PackageAppointment.objects.filter(is_deleted=False,visited=True, date__range=[from_date, to_date])
            else:
                instances = None
        except ValueError:
            date_error = "yes"

    elif filter_date:
        try:
            title = "Appointments On %s : " %(str(from_date),str(to_date))
            if PackageAppointment.objects.filter(is_deleted=False,visited=True, date=from_date).exists():
                instances = PackageAppointment.objects.filter(is_deleted=False,visited=True, date=from_date)
            else:
                instances = None
        except ValueError:
            date_error = "yes"

    context = {
        "title" : title,
        "instances" : instances,
        "app_title" : "Wellphy",
    }
    return render(request,'patients/appointment_history_for_staffs.html',context)
