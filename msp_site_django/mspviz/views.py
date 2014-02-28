# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from mspviz.models import MSP, Party, District


# navigation
navigation_main={
	'index' : {
				'id':'index',
				'title':'About', 
				'desc': "Your vote, your msp. Find out what's going on at Holyrood...",
	}, 
	'listmsps' : {
				'id':'listmsps',
				'title':'All MSPs', 
				'desc': 'This is just a sample text. More information about this subsite should follow. Browse all MSPs of the Scottish Parliament and find out more about their area, party and votes...',
	}, 
	'listareas': {
				'id': 'listareas',
				'title':'All areas', 
				'desc': 'This is just a sample text. More information about this subsite should follow. Browse all areas and get more information about corresponding msps...',
	}, 
	'listparties': {
				'id': 'listparties',
				'title':'All parties', 
				'desc': 'This is just a sample text. More information about this subsite should follow. Browse all parties and explore their members...'
	}
}
				

# gloabal config
context_dict={
	'title': "mspviz",
	'desc': "Your vote, your msp",
	'copyr': "mspviz 2014",
	'contact_name': "mspviz team 2014",
	'contact_email': "info@mspviz.co.uk",
	'navigation_main': navigation_main,
}


def index(request):
	context = RequestContext(request)
	context_dict['activesite'] = navigation_main['index']
	return render_to_response('mspviz/base.html', context_dict, context)


def listmsps(request):
	context = RequestContext(request)
	context_dict['activesite'] = navigation_main['listmsps']
	
	all_msps = MSP.objects.all().order_by('mspName')
	context_dict['all_msps'] = all_msps
	return render_to_response('mspviz/listmsps.html', context_dict, context)


def msp(request,mspID):
	context = RequestContext(request)
	context_dict['activesite'] = navigation_main['listmsps']
	
	thisMSP = MSP.objects.get(mspID = mspID)
	context_dict['msp'] = thisMSP
	return render_to_response('mspviz/msp.html', context_dict, context)


def listparties(request):
	context = RequestContext(request)
	context_dict['activesite'] = navigation_main['listparties']
	
	context_dict['parties'] = Party.objects.all().order_by('partyName')
	return render_to_response('mspviz/listparties.html', context_dict, context)


def party(request,partyID):
	context = RequestContext(request)
	context_dict['activesite'] = navigation_main['listparties']
	
	thisParty = Party.objects.get(id = partyID)
	partyMSPs = MSP.objects.filter(mspParty = thisParty).order_by('mspName')
	context_dict['party'] = thisParty
	context_dict['partyMSPs'] = partyMSPs
	return render_to_response('mspviz/party.html', context_dict, context)


def listareas(request):
	context = RequestContext(request)
	context_dict['activesite'] = navigation_main['listareas']
	
	context_dict['districts'] = District.objects.all().order_by('districtName')
	return render_to_response('mspviz/listareas.html', context_dict, context)


def area(request,areaID):
	context = RequestContext(request)
	context_dict['activesite'] = navigation_main['listareas']

	thisArea = District.objects.get(id = areaID)
	areaMSPs = MSP.objects.filter(mspDistrict = thisArea).order_by('mspParty')
	context_dict['district'] = thisArea
	context_dict['districtMSPs'] = areaMSPs
	return render_to_response('mspviz/area.html', context_dict, context)



