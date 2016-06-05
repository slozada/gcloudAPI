import webapp2
from google.appengine.api import oauth 


app = webapp2.WSGIApplication([
    ('/offer', 'offer.Offer'),
], debug=True)

app.router.add(webapp2.Route(r'/offer/<id:[0-9]+><:/?>','offer.Offer'))
app.router.add(webapp2.Route(r'/user/<id:[0-9]+><:/?>','user.User'))
app.router.add(webapp2.Route(r'/user/search','user.UserSearch'))
app.router.add(webapp2.Route(r'/offeredit/<id:[0-9]+><:/?>','offer.EditOff'))
app.router.add(webapp2.Route(r'/user','user.User'))
app.router.add(webapp2.Route(r'/product/delete/<id:[0-9]+><:/?>','product.ProductDelete'))
app.router.add(webapp2.Route(r'/offer/delete/<id:[0-9]+><:/?>','offer.OfferDelete'))
app.router.add(webapp2.Route(r'/user/<pid:[0-9]+>/offer/<oid:[0-9]+><:/?>','user.UserOff'))

