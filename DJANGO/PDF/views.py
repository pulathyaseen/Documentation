from web.function import render_to_pdf

def convert_to_pdf(request):
	...
	# data calculations
	...
	context = {
		'data': data,
		...
	}
	return render_to_pdf(request,'path/to/template.html',context)
