# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):

	context = RequestContext(request)
	context_dict = {'bmessage': "I am a message"}
	return render_to_response('mspviz/index.html', context_dict, context)