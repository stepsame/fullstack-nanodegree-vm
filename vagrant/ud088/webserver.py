from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

## import CRUD Operations from Lesson 1 ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

#Create session and connect to DB
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
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>&#161Hola	<a href = '/hello'>Back to Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurants = session.query(Restaurant).all()

				output = ""
				output += "<html><body>"
				for restaurant in restaurants:
					output += "%s <br>" % restaurant.name
					output += "<a href='/restaurants/%s/edit'>EDIT</a><br>" % restaurant.id
					output += "<a href='/restaurants/%s/delete'>DELETE</a><br>" % restaurant.id
					output += "<hr>"

				output += "<a href='/restaurants/new'>Create New Restaurant</a>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return	

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='name' type='text' placeholder='New Restaurant Name'>"
				output += "<input type='submit' value='Create'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]
				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

				if restaurant != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "<h1>Edit a Restaurant</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
					output += "<input name='name' type='text' placeholder='%s'>" % restaurant.name
					output += "<input type='submit' value='Rename'></form>"
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]
				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

				if restaurant != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "<h1>Are you sure you want to delete %s ?</h1>" % restaurant.name
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
					output += "<input type='submit' value='Delete'></form>"
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return


		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)
	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('name')

				#Create new Restaurant class
				restaurant = Restaurant(name = messagecontent[0])
				session.add(restaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

				return

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('name')

				restaurantIDPath = self.path.split("/")[2]

				#Edit new Restaurant class
				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if restaurant != []:
					restaurant.name = messagecontent[0]
					session.add(restaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

				return

			if self.path.endswith("/delete"):
				# ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				# if ctype == 'multipart/form-data':
				# 	fields = cgi.parse_multipart(self.rfile, pdict)
				# 	messagecontent = fields.get('name')

				restaurantIDPath = self.path.split("/")[2]

				#Delete Restaurant class
				restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if restaurant != []:
					session.delete(restaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

				return

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print("Web server running on port %s" % port)
		server.serve_forever()

	except KeyboardInterrupt:
		print " ^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()