from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Owns(db.Model):
    owns_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.itinerary_id'), nullable=False)
    preference = db.Column(db.String(120))

    def __repr__(self):
        return f'<Owns {self.user_id} - {self.itinerary_id}>'

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.itinerary_id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.attraction_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(120))

    def __repr__(self):
        return f'<Feedback {self.user_id} - {self.itinerary_id}>'

class Itinerary(db.Model):
    itinerary_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Itinerary {self.itinerary_id}>'

class Includes(db.Model):
    includes_id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.itinerary_id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.attraction_id'), nullable=False)

    def __repr__(self):
        return f'<Includes {self.itinerary_id} - {self.attraction_id}>'

class Attraction(db.Model):
    attraction_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    operating_hours = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Attraction {self.name}>'

class Restaurant(db.Model):
    restaurant_id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.attraction_id'), nullable=False)
    specialty = db.Column(db.String(120), nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Restaurant {self.restaurant_id}>'
