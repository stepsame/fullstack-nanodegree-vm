from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup_exercise import Base, Shelter, Puppy

import datetime

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#1. Query all of the puppies and return the results in ascending alphabetical order
# puppies = session.query(Puppy).order_by(Puppy.name)
# for puppy in puppies:
# 	print(puppy.id)
# 	print(puppy.name)
# 	print(puppy.gender)
# 	print('\n')

#2. Query all of the puppies that are less than 6 months old organized by the youngest first
# before = datetime.date.today() - datetime.timedelta(days=6 * 365/12)
# puppies = session.query(Puppy).filter(Puppy.dateOfBirth >= before).order_by(Puppy.dateOfBirth.desc())
# for puppy in puppies:
# 	print(puppy.id)
# 	print(puppy.name)
# 	print(puppy.dateOfBirth)
# 	print('\n')

#3. Query all puppies by ascending weight
# puppies = session.query(Puppy).order_by(Puppy.weight)
# for puppy in puppies:
# 	print(puppy.id)
# 	print(puppy.name)
# 	print(puppy.weight)
#4. Query all puppies grouped by the shelter in which they are staying
# puppies = session.query(Puppy).group_by(Puppy.shelter_id)
# for puppy in puppies:
# 	print(puppy.shelter_id)

def check(shelter_name):
	shelter = session.query(Shelter).one
	if shelter.occupancy < shelter.capacity:
		return "OK"
	return "Try a different"

def adopt(puppy_id, *adopters):
	#empty shelter_id

	#create adopter

	#add relationship of adopter and puppy
