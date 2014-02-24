# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from mspviz.models import MSP, Party, District

def index(request):

	context = RequestContext(request)
	context_dict = {'bmessage': "I am a message"}
	return render_to_response('mspviz/index.html', context_dict, context)

def listmsps(request):
	context = RequestContext(request)
	all_msps = MSP.objects.all().order_by('mspName')
	context_dict = {'all_msps':all_msps}
	return render_to_response('mspviz/listmsps.html',context_dict,context)

def msp(request,mspID):
	context = RequestContext(request)
	thisMSP = MSP.objects.get(mspID = mspID)
	context_dict = {'msp': thisMSP}
	return render_to_response('mspviz/msp.html',context_dict,context)

def party(request,partyID):
	context = RequestContext(request)
	thisParty = Party.objects.get(id = partyID)
	partyMSPs = MSP.objects.filter(mspParty = thisParty).order_by('mspName')
	context_dict = {'party':thisParty};
	context_dict['partyMSPs'] = partyMSPs
	return render_to_response('mspviz/party.html',context_dict,context)

def area(request,areaID):
	context = RequestContext(request)
	thisArea = District.objects.get(id = areaID)
	areaMSPs = MSP.objects.filter(mspDistrict = thisArea).order_by('mspParty')
	context_dict = {'district':thisArea}
	context_dict['districtMSPs'] = areaMSPs
	return render_to_response('mspviz/area.html',context_dict,context)

def listareas(request):
	context = RequestContext(request)
	districts = District.objects.all().order_by('districtName')
	context_dict = {'districts':districts}
	return render_to_response('mspviz/listareas.html',context_dict,context)