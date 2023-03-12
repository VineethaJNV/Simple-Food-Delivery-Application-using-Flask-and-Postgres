from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:postgres@localhost:5432/menu_details')
Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu_details'

    menu_id = Column(Integer, primary_key = True)
    food_items = Column(String(length = 60))

    def __repr__(self):
        return "<Menu(menu_id ='{0}', food_items = '{1}'>".format(self.menu_id, self.food_items)

class Food(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key = True)
    menu_id = Column(Integer, ForeignKey('menu_details.menu_id'))
    description = Column(String(length =60))

    menu = relationship("Menu")

    def __repr__(self):
        return "<Food(description = '{0}')>".format(self.description)

Base.metadata.create_all(engine)

def create_session():
    session = sessionmaker(bind = engine)
    return session()

if __name__ == "__main__":
    session = create_session()

    adding_to_menu = Menu(food_items = "Sandwich")
    session.add(adding_to_menu)
    session.commit()

    adding_to_food = Food(description = "Veg_Cheese", menu_id =adding_to_menu.menu_id )
    session.add(adding_to_food)
    session.commit()

