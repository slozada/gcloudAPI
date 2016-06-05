import webapp2
from google.appengine.ext import ndb
import db_models
import json

class User(webapp2.RequestHandler):
	def post(self):

		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not acceptable, API only supports json calls"
			return 
		new_user=db_models.User()
		fname=self.request.get('fname',default_value=None)
		lname=self.request.get('lname',default_value=None)	
		email=self.request.get('email',default_value=None)
		password=self.request.get('password',default_value=None)
		offers=self.request.get_all('offers[]',default_value=None)
		
		if email:
			new_user.email=email
		else:
			self.response.status=400
			self.response.status_message="Invalud request"
		
		if password:
			new_user.password=password
		else:
			self.response.status=400
			self.response.status_message="Invalud request"

		if fname:
			new_user.fname=fname
		else:
			self.response.status=400
			self.response.status_message="Invalud request"
		
		if lname:
			new_user.lname=lname
		else:
			self.response.status=400
			self.response.status_message="Invalud request"

		if offers:
			for offer in offers:
				new_user.offers.append(ndb.Key(db_models.Off, int(offer)))

		key=new_user.put()
		out=new_user.to_dict()
		print out
		self.response.write(json.dumps(out))
		return

	def get(self,**kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports JSON"	
			return
		if 'id' in kwargs:
			out=ndb.Key(db_models.User,int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))	
		else:
			q=db_models.User.query()
			keys=q.fetch(keys_only=True)
			results={'keys':[x.id() for x in keys]}
			self.response.write(json.dumps(results))

class UserOff(webapp2.RequestHandler):
	def put(self,**kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message = "Not acceptable, API only supports json calls"
		if 'pid' in kwargs:
			user=ndb.Key(db_models.User, int (kwargs['pid'])).get()
			if not user:
				self.response.status=404
				self.response.status_message="User Not Found"
				return
		if 'oid' in kwargs:
			offer=ndb.Key(db_models.Off,int(kwargs['oid']))
			if not offer:
				self.response.status=404
				self.response.status_message="Offer Not Found"
				return
		if offer not in user.offers:
			user.offers.append(offer)
			user.put()
		self.response.write(json.dumps(user.to_dict()))
		return


class UserSearch(webapp2.RequestHandler):
	def post(self):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports JSON"
			return
		q=db_models.User.query()
		if self.request.get('email',None):
			q=q.filter(db_models.User.email==self.request.get('email'))
		keys=q.fetch(keys_only=True)
		results={'keys':[x.id() for x in keys]}
		self.response.write(json.dumps(results)) 	

class ProductDelete(webapp2.RequestHandler):
	def delete(self,**kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports JSON"
			return
		if 'id' in kwargs:
			product=ndb.Key(db_models.Product,int(kwargs['id'])).get()
			product.key.delete()
			self.response.write("Deleted product")
			return	
