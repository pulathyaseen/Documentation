from django.utils.translation import activate
from django.utils import translation


def switch_language(request):
    lang = request.GET.get('language') # accepting value choosen by client
    next = request.GET.get('next')
    language = translation.get_language() # this will return current active language

    if lang == "en":
        activate('en')
    elif lang == "ml":
        activate('ml')
    
    return HttpResponseRedirect(next)
