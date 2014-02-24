import os,json

def populate():
	data = []
	with open('static/data/msps.json') as f:
		for line in f:
			data.append(json.loads(line))

	for msp in data:
		p = add_party(msp['party'])
		d = add_district(msp['area'])
		m = add_msp(msp['name'],p,msp['mspid'],msp['imguri'],d)

def add_msp(name,party,mspid,imguri,district):
	m = MSP.objects.get_or_create(mspName = name,mspID = mspid,mspParty = party,mspImg = imguri,mspDistrict=district)[0]
	return m

def add_party(name):
	p = Party.objects.get_or_create(partyName = name)[0]
	return p

def add_district(name):
	d = District.objects.get_or_create(districtName = name)[0]
	return d

if __name__ == '__main__':
    print "Starting msp population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msp_site_django.settings')
    from mspviz.models import Party, MSP, District
    populate()