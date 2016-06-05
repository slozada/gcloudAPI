import webapp2
from google.appengine.ext import ndb
import db_models
import json


class Offer(webapp2.RequestHandler):
	def post(self):
	
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports JSON"
			return

		new_offer=db_models.Off()
		code=self.request.get('code',default_value=None)
		product=self.request.get('product',default_value=None)
		discountPer=self.request.get('discountPer',default_value=None)
		validUntil=self.request.get('validUntil',default_value=None)
		validWebsite=self.request.get('validWebsite',default_value=None)
		
		if code:
			new_offer.code=code
		else:
			self.response.status=400
			self.response.status_message="Invalid Request"
		if product:
			new_offer.product=product
		if discountPer:
			new_offer.discountPer=discountPer
		if validUntil:
			new_offer.validUntil=validUntil
		if validWebsite:
			new_offer.validWebsite=validWebsite

		key=new_offer.put()
		out=new_offer.to_dict()
		self.response.write(json.dumps(out))
		return 		

	def get(self,**kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports JSON"	
			return
		if 'id' in kwargs:
			out=ndb.Key(db_models.Off,int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))	
		else:
			q=db_models.Off.query()
			keys=q.fetch(keys_only=True)
			results={'keys':[x.id() for x in keys]}
			self.response.write(json.dumps(results))

class OffSearch(webapp2.RequestHandler):
	def post(self):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports JSON"
			return
		q=db_models.Off.query()
		if self.request.get('validWebsite',None):
			q=q.filter(db_models.Off.validWebsite==self.request.get('validWebsite'))
		if self.request.get('validUntil',None):
			q=q.filter(db_models.Off.validUntil==self.request.get('validUntil'))
		keys=q.fetch(keys_only=True)
		results={'keys':[x.id() for x in keys]}
		self.response.write(json.dumps(results)) 	

class EditOff(webapp2.RequestHandler):
	def put(self,**kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message = "Not acceptable, API only supports json calls"
		if 'id' in kwargs:
			print kwargs['id']
			offer=ndb.Key(db_models.Off, int (kwargs['id'])).get()
			if not offer:
				self.response.status=404
				self.response.status_message="User Not Found"
				return
			print offer.to_dict()	
			code=self.request.get('code',default_value=None)
			product=self.request.get('product',default_value=None)
			discountPer=self.request.get('discountPer',default_value=None)
			validUntil=self.request.get('validUntil',default_value=None)
			validWebsite=self.request.get('validWebsite',default_value=None)
			print product 	
			if code:
				offer.code=code
			if product:
				offer.product=product
			if discountPer:
				offer.discountPer=discountPer
			if validUntil:
				offer.validUntil=validUntil
			if validWebsite:
				offer.validWebsite=validWebsite
			
			print offer.to_dict()
			offer.put()
		self.response.write(json.dumps(offer.to_dict()))
		return

class OfferDelete(webapp2.RequestHandler):
	def delete(self,**kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports JSON"
			return
		if 'id' in kwargs:
			offer=ndb.Key(db_models.Off,int(kwargs['id'])).get()
			offer.key.delete()
			self.response.write("Deleted offer")
			return	
