from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from project_name.settings import STATIC_FILE_ROOT
from django.template.loader import get_template


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, default_css=open(STATIC_FILE_ROOT + '/css/pdf/page.css','r').read())
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
