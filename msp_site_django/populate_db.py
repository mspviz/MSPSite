import os,json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msp_site_django.settings")

from django.db import connection
from django.core import management
from StringIO import StringIO 
import re
import hashlib

from mspviz import models



def clearDatabase():
	''' clear whole database and delete alls data and tables '''
	
	print "Clearing database..."
	management.call_command('flush')
	content = StringIO()
	clearcommands = management.call_command('sqlclear',  'mspviz', stdout=content)
	content.seek(0)
	cleararr = content.read().split(';')
	cursor = connection.cursor()
	
	for id, clearcomm in enumerate(cleararr):
		if (not 'BEGIN' in clearcomm and not 'COMMIT' in clearcomm):
			print "execute database command: ", clearcomm
			cursor.execute(clearcomm)
	
	management.call_command('syncdb')


def populateVotes():
	''' read votes json and populate Division and Vote '''
	print 'populate votes...'
	data = []
	with open('static/data/models/votes.json') as f:
		for line in f:
			data.append(json.loads(line))
		
	missed = 0;	
	falty = []
	for vote in data:
		# match division id
		regexmatch = re.search('S\dM-[\d]{1,7}(.\d)?', vote['detail'])
		if(regexmatch):
			divisionid = regexmatch.group(0)
		else:
			# hash description if no division id found
			divisionid = hashlib.md5(vote['detail'])
			missed+=1
			falty.append(vote['detail'])
		
		# create division
		d = add_division(divisionid, vote['detail'], vote['result'])
		m = models.MSP.objects.get(foreignid=vote['mspid'])
		v = add_vote(m, d, vote['MSPVote'])
		
	print 'missed', missed, falty
		

def populateMSPs():
	''' read msp json and populate MSP, Party and District '''
	print 'populate msps...'
	data = []
	with open('static/data/models/msps.json') as f:
		for line in f:
			data.append(json.loads(line))
	
	for msp in data:
		p = add_party(msp['party'])
		
		if('parentregion' in msp):
			pd = msp['parentregion']
		else:
			pd = None
		d = add_district(msp['area'], pd)
		
		name = msp['name'].split(',')
		m = add_msp(name[0], name[1], p, msp['mspid'], msp['imguri'], d)
		
		

def add_msp(inputlastname, inputfirstname, inputparty, mspid, imguri, inputdistrict):
	m = models.MSP.objects.get_or_create(lastname = inputlastname, firstname = inputfirstname,foreignid = mspid, party = inputparty, image = imguri, district=inputdistrict)[0]
	return m

def add_party(inputname):
	p = models.Party.objects.get_or_create(name = inputname)[0]
	return p

def add_district(inputname, parentdistrict):
	if(parentdistrict):
		pd = models.District.objects.get_or_create(name = parentdistrict)[0]
		d = models.District.objects.get_or_create(name = inputname, parent = pd)[0]
	else:
		d = models.District.objects.get_or_create(name = inputname)[0]
	return d

def add_division(divisionid, text, inputresult):
	res = 0
	if(inputresult == 'Carried'):
		res = models.Division.CARRIED
	elif(inputresult == 'Defeated'):
		res = models.Division.DEFEATED
	d = models.Division.objects.get_or_create(identifier = divisionid, teasertext=text, result=res)[0]
	return d

def add_vote(inputmsp, inputdiv, inputvote):
	res = 0
	if(inputvote == 'Yes'):
		res = models.Vote.YES
	elif(inputvote == 'No'):
		res = models.Vote.NO
	elif(inputvote == 'Abstain'):
		res = models.Vote.ABSTAIN
	v = models.Vote.objects.get_or_create(msp = inputmsp, division=inputdiv, vote=res)[0]
	return v


if __name__ == '__main__':
	# clear database and delete everything
	clearDatabase()
	
	# read json files
	populateMSPs()
	# populate votes takes a long time since sqllite can only do 12 transactions per sec - combining inserts into one transaction is difficult because the many-to-many realationship and dublicate entries.
	populateVotes() 
    