from flask import Flask, render_template, request, url_for, redirect, jsonify, flash

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'id':'1'}

# API Endpoints with JSON
@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [entry.serialize for entry in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def itemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem = item.serialize)

@app.route('/')
@app.route('/restaurant')
def showRestaurants():
	#return "This page will show all my restaurants"
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
	# return "This page will be for making a new restaurant"
	if request.method == 'GET':
		return render_template('newrestaurant.html')
	else:
		restaurant = Restaurant(name = request.form['restaurant_name'])
		session.add(restaurant)
		session.commit()
		flash("New Restaurant Created")
		return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	# return "This page will be for editing restaurant %s" % restaurant_id
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'GET':
		return render_template('editrestaurant.html', restaurant = restaurant)
	else:
		restaurant.name = request.form['restaurant_name']
		session.add(restaurant)
		session.commit()
		flash("Restaurant Successfully Edited")
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	# return "This page will be for deleting restaurant %s" % restaurant_id
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'GET':
		return render_template('deleterestaurant.html', restaurant = restaurant)
	else:
		session.delete(restaurant)
		session.commit()
		flash("Restaurant Successfully Deleted")
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	# return "This page is the menu for restaurant %s" % restaurant_id
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	# return "This page is for making a new menu item for restaurant %s" % restaurant_id
	if request.method == 'GET':
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		return render_template('newmenuitem.html', restaurant = restaurant)
	else:
		item = MenuItem(name = request.form['item_name'], restaurant_id = restaurant_id)
		session.add(item)
		session.commit()
		flash("Menu Item Created")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	# return "This page is for editing menu item %s" % menu_id
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'GET':
		return render_template('editmenuitem.html', restaurant = restaurant, item = item)
	else:
		item.name = request.form['item_name']
		session.add(item)
		session.commit()
		flash("Menu Item Successfully Edited")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	# return "This page is for deleting menu item %s" % menu_id
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'GET':
		return render_template('deletemenuitem.html', restaurant = restaurant, item = item)
	else:
		session.delete(item)
		session.commit()
		flash("Menu Item Successfully Deleted")
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)