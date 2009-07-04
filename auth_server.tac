# Authentication server for Skule.ca
# Copyright James Cash 2009

from twisted.web import server, resource
from twisted.internet import reactor


class AuthSite(resource.Resource):
    """The root authentication server object
    """

    
      
        
        


site = server.Site(AuthSite())
reactor.listenTCP(8080, site)
reactor.run()
