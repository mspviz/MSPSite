from django.db import models
from datetime import datetime


class Party(models.Model):
	'''
	Represents parties
	'''
	name = models.CharField(max_length=128, unique=True)
	image = models.CharField(max_length=256)
	
	def __unicode__(self):
		return self.name



class District(models.Model):
	'''
	Represents electoral districts
	'''
	parent = models.ForeignKey('self', default=0)
	name = models.CharField(max_length=128, unique=True)

	def __unicode__(self):
		return self.name
	


class MSP(models.Model):
	'''
	Represents msps
	'''
	foreignid = models.PositiveIntegerField(max_length=8, unique=True)
	district = models.ForeignKey(District)
	party = models.ForeignKey(Party)
	firstname = models.CharField(max_length=128)
	lastname = models.CharField(max_length=128)
	image = models.CharField(max_length=256)

	def __unicode__(self):
		return self.name



class Division(models.Model):
	'''
	Represents divisions - can be motions, questions or amendments
	'''
	CARRIED = 1
	DEFEATED = 2
	RESULTS = (
	    (CARRIED, 'Carried'),
	    (DEFEATED, 'Defeated')
	)
	
	parent = models.ForeignKey('self', default=0)
	identifier = models.CharField(max_length=128)
	date = models.DateTimeField(default=datetime.now())
	keywords = models.CharField(max_length=512)
	teasertext = models.CharField(max_length=512)
	result = models.PositiveIntegerField(max_length=2, choices=RESULTS)
	votes = models.ManyToManyField(MSP, through='Vote')
	


class Vote(models.Model):
	'''
	Represents votes of the MSPs concerning divisions
	'''
	YES = 1
	NO = 2
	ABSTAIN = 3
	ABSENT = 4
	VOTES = (
	    (YES, 'Yes'),
	    (NO, 'No'),
	    (ABSTAIN, 'Abstain'),
	    (ABSENT, 'Absent')
	)
	
	msp = models.ForeignKey(MSP)
	division = models.ForeignKey(Division)
	vote = models.PositiveIntegerField(max_length=2, choices=VOTES)
	
	
