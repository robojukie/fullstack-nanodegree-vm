from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import cgi
import urlparse, re
#hello
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("/hello"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ""
        output += "<html><body>Hello!"
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
        output += "</body></html>"
        self.wfile.write(output)
        print output
        return

      if self.path.endswith("/restaurants"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ""
        output += "<html><body>"
        output += "<ul>"
        restaurants = session.query(Restaurant).all()
        restaurant_id = ""
        for restaurant in restaurants:
          output += "<li>"
          output += restaurant.name
          output += " "
          output += "</br><a href='/restaurants/%s" % restaurant.id
          output += "/edit'>Edit</a>"
          output += "</br><a href='/restaurants/%s" % restaurant.id 
          output += "/delete'>Delete</a></li>"
        output += "</ul>"
        output += "<a href='/restaurants/new'>Make a New Restaurant</a>"
        output += "</body></html>"
        
        self.wfile.write(output)
#        print output
        return
        
      if self.path.endswith("/restaurants/new"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        output = "" 
        output += "<html><body>"
        output += "<form method='POST' enctype='multipart/form-data'><h2>Make a New Restaurant</h2><input name='newRestaurantName' type='text' ><input type='submit' value='Submit'> </form>"
        output += "</body></html>"

        self.wfile.write(output)
        print output
        return
  

      if self.path.endswith("/edit"):
        path = str(self.path)
        restaurant_id = re.findall(r'\d+', path)[0]

        restaurant = session.query(Restaurant).get(restaurant_id) 
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = "" 
        output += "<html><body>"
        output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % path
        output += "<h2>Edit %s</h2>" % restaurant.name
        output += "<input name='restaurant' type='text' ><input type='submit' value='Edit'> </form>"

        output += "</br><h2>ID: %s" % restaurant.id
        output += "</h2>"
        output += "</body></html>"
        self.wfile.write(output)
        print output
        return

      if self.path.endswith("/delete"): 
        path = str(self.path)
        restaurant_id = re.findall(r'\d+', path)[0]
 
        restaurant = session.query(Restaurant).get(restaurant_id)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ""
        output += "<html><body>"
        output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % path
        output += "Are you sure you want to delete %s?" % restaurant.name
        output += "<input type='submit' value='Delete'> </form>"
        output += "</body></html>"

        self.wfile.write(output)
        print output
        return


    except IOError:
      self.send_error(404, "File Not Found %s" % self.path)


  def do_POST(self):
    try:
      if self.path.endswith("/hello"):
        self.send_response(301)
        self.end_headers()
        
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('message')[0]
          output = ""
          output += "<html><body>"
          output += " <h2> ok, how about this: <h1> %s </h1> </h2>" % messagecontent
          output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2>"
          output += "<input name='message' type='text' ><input type='submit' value='Submit'> </form>"
          output += "</body></html>"
          self.wfile.write(output)
          #print output

      if self.path.endswith("/restaurants/new"):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        print ctype
        print pdict
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
        contentMessage = fields.get('newRestaurantName')[0]
        newRestaurant = Restaurant(name = contentMessage)
        session.add(newRestaurant)
        session.commit() 
      
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()


      if self.path.endswith("/edit"):
        path = str(self.path)

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('restaurant')[0]

        restaurant_id = re.findall(r'\d+', path)[0]
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one() 
        old_restaurant = restaurant.name
        restaurant.name = messagecontent
        session.add(restaurant)
        session.commit()

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()
       
        print restaurant.name
        output = ""
        output += "<html><body>"
        output += " <h2>%s changed to: <h1> %s </h1> </h2>" %old_restaurant % restaurant.name
        output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % path 
        output += "<h2>Edit %s</h2>" % messagecontent
        output += "<input name='message' type='text' ><input type='submit' value='Edit'> </form>"
        output += "</body></html>"
        self.wfile.write(output)


      if self.path.endswith("/delete"):
        path = str(self.path)
        r_id = re.findall(r'\d+', path)
        restaurant_id = r_id[0]
        
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one() 
        old_restaurant = restaurant.name
        session.delete(restaurant)
        session.commit()

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

 
    except:
      pass


def main():
  try:
    port = 8080
    server = HTTPServer(('',port), webserverHandler)
    print "Web server running on port %s" % port
    server.serve_forever()

  except KeyboardInterrupt:
    print "^C entered, stopping web server..."
    server.socket.close()

if __name__ == '__main__':
  main()
