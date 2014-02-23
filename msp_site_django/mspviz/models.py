from django.db import models

class Party(models.Model):
	partyName = models.CharField(max_length=128,unique=True)

	def __unicode__(self):
		return self.name

class MSP(models.Model):
	mspID = models.CharField(max_length=8,unique=True)
	mspName = models.CharField(max_length=128)
	mspParty = models.ForeignKey(Party)

	def __unicode__(self):
		return self.name

