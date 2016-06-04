from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d=super(Model,self).to_dict()
		d['key']=self.key.id()
		return d

class User(Model):
	fname=ndb.StringProperty(required=True)
	lname=ndb.StringProperty(required=True)
	email=ndb.StringProperty(required=True)
	password=ndb.StringProperty(required=True)
	offers=ndb.KeyProperty(repeated=True)
	
	def to_dict(self):
		d=super(User,self).to_dict()
		d['offers']=[m.id() for m in d['offers']]
		return d

class Off(Model):
	code=ndb.StringProperty(required=True)
	product=ndb.StringProperty()
	discountPer=ndb.StringProperty()
	validUntil=ndb.StringProperty()
	validWebsite=ndb.StringProperty()
