import cherrypy
from ipay import app

if __name__ == '__main__':
    cherrypy.tree.graft(app, '/ipay')
    
    cherrypy.server.unsubscribe()
    
    server = cherrypy._cpserver.Server()
    
    server.socket_host = "0.0.0.0"
    server.socket_port = 8086
    server.thread_pool = 50
    
    server.subscribe()

    server2 = cherrypy._cpserver.Server()
   
    server2.socket_host = "0.0.0.0"
    server2.socket_port = 8087
    server2.thread_pool = 50
      
    server2.subscribe()
    
    cherrypy.engine.start()
    cherrypy.engine.block()