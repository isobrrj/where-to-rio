from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

class Owns(Base):
    __tablename__ = "owns"
    owns_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itinerary.itinerary_id"), nullable=False)
    preference = Column(String(120))

    def __repr__(self):
        return f"<Owns {self.user_id} - {self.itinerary_id}>"

class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itinerary.itinerary_id"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attraction.attraction_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(120))

    def __repr__(self):
        return f"<Feedback {self.user_id} - {self.itinerary_id}>"

class Itinerary(Base):
    __tablename__ = "itinerary"
    itinerary_id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Itinerary {self.itinerary_id}>"

class Includes(Base):
    __tablename__ = "includes"
    includes_id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey("itinerary.itinerary_id"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attraction.attraction_id"), nullable=False)

    def __repr__(self):
        return f"<Includes {self.itinerary_id} - {self.attraction_id}>"

class Attraction(Base):
    __tablename__ = "attraction"
    attraction_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    operating_hours = Column(String(120), nullable=False)
    description = Column(String(120), nullable=False)
    photo = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<Attraction {self.name}>"

class Restaurant(Base):
    __tablename__ = "restaurant"
    restaurant_id = Column(Integer, primary_key=True)
    attraction_id = Column(Integer, ForeignKey("attraction.attraction_id"), nullable=False)
    specialty = Column(String(120), nullable=False)
    vegetarian = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Restaurant {self.restaurant_id}>"
