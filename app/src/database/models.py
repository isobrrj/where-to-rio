from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, event
from sqlalchemy.ext.declarative import declarative_base
from hashlib import sha256
import hashlib
import uuid


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

    @staticmethod
    def hash_password(password):
        """
        Gera um hash SHA256 da senha.
        """
        return sha256(password.encode()).hexdigest()
    
# Listener para hash da senha
@event.listens_for(User, "before_insert")
def hash_password_before_insert(mapper, connection, target):
    """
    Garante que a senha seja hashada antes de uma inserção.
    """
    target.password = User.hash_password(target.password)

@event.listens_for(User, "before_update")
def hash_password_before_update(mapper, connection, target):
    """
    Garante que a senha seja hashada antes de uma atualização.
    """
    # Apenas faça hash se a senha foi modificada
    if "password" in target.__dict__ and target.__dict__["password"] != target.password:
        target.password = User.hash_password(target.password)

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
    rating = Column(Integer, nullable=True)
    comment = Column(String(120))

    def __repr__(self):
        return f"<Feedback {self.user_id} - {self.itinerary_id}>"

class Itinerary(Base):
    __tablename__ = "itinerary"
    itinerary_id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Itinerary {self.itinerary_id}>"

class Includes(Base):
    __tablename__ = "includes"
    includes_id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey("itinerary.itinerary_id"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attraction.attraction_id"), nullable=False)
    time_of_day = Column(String(120), nullable=False)
    date = Column(Date, nullable=False)  # Nova coluna para armazenar a data da atividade

    def __repr__(self):
        return f"<Includes {self.itinerary_id} - {self.attraction_id} - {self.date}>"


class Attraction(Base):
    __tablename__ = "attraction"
    attraction_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    operating_hours = Column(String(120), nullable=True)
    description = Column(String(120), nullable=True)
    photo = Column(String(120), nullable=True)
    attraction_type = Column(Integer, ForeignKey("attraction_type.attraction_type_id"), nullable=False)
    time_of_day = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<Attraction {self.name}>"

class Restaurant(Base):
    __tablename__ = "restaurant"
    restaurant_id = Column(Integer, primary_key=True)
    attraction_id = Column(Integer, ForeignKey("attraction.attraction_id"), nullable=False)
    restaurant_type = Column(Integer, ForeignKey("attraction_type.attraction_type_id"), nullable=False)
    vegetarian = Column(Boolean, nullable=True)
    price = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Restaurant {self.restaurant_id}>"

class AttractionType(Base):
    __tablename__ = "attraction_type"
    attraction_type_id = Column(Integer, primary_key=True)
    attraction_type = Column(String(120), nullable=True)
    restaurant_type = Column(String(120), nullable=True)

    def __repr__(self):
        return f"<AttractionType {self.name}>"
