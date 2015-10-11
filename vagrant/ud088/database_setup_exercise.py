import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):

	__tablename__ = 'shelter'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	address = Column(String(250))
	city = Column(String(80))
	state = Column(String(20))
	zipCode = Column(String(10))
	website = Column(String)
	capacity = Column(Integer)
	occupancy = Column(Integer)
	

class Puppy(Base):

	__tablename__ = 'puppy'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	gender = Column(String(10), nullable = False)
	dateOfBirth = Column(Date)
	#breed = Column(String(20))
	picture = Column(String)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)
	weight = Column(Numeric(10))

class Profile(Base):

	__tablename__ = 'profile'

	id = Column(Integer, primary_key = True)
	photo = Column(String)
	description = Column(String(250))
	breed = Column(String(20))
	puppy_id = Column(Integer, ForeignKey('puppy.id'))

	puppy = relationship("Puppy", uselist=False, backref="profile")

association_table = Table('association', Base.metadata,
	Column('puppy_id', Integer, ForeignKey('puppy.id')),
	Column('adopter_id', Integer, ForeignKey('adopter.id'))
)

class Adopter(Base):

	__tablename__ = 'adopter'

	id = Column(Integer, primary_key = True)
	name = Column(String(20))
	puppy = relationship("Puppy", secondary=association_table, backref="adopter")



engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)