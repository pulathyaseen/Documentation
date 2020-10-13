from django.utils.translation import activate

def switch_language(request):
    lang = request.GET.get('language')
    next = request.GET.get('next')
    if lang == "en":
        activate('en')
    elif lang == "ml":
        activate('ml')
    
    return HttpResponseRedirect(next)
