import sys #provides functions & vars

from sqlalchemy import Column, ForeignKey, Integer, String #for writing mapper code

from sqlalchemy.ext.declarative import declarative_base #config & class code

from sqlalchemy.orm import relationship #foreign key relationship

from sqlalchemy import create_engine #use at end of file

Base = declarative_base() #classes are SQLalchemy classes

#rep of table as a py class
#extends Base class
class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

#end
engine = create_engine('sqlite:///restaurantmenu.db') #instance connects to DB

Base.metadata.create_all(engine) #goes to DB and adds classes as new tables in the DB

