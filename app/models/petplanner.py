from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    pets = db.relationship("Pet", backref="owner", cascade="all, delete-orphan")
    centers = db.relationship("Center", backref="user", cascade="all, delete-orphan")
    articles = db.relationship("Article", backref="author", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    physical_characteristics = db.Column(db.Text)
    health_conditions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    allergies = db.relationship("Allergy", secondary="pet_allergies", back_populates="pets")
    medical_events = db.relationship("MedicalEvent", backref="pet", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "breed": self.breed,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "physical_characteristics": self.physical_characteristics,
            "health_conditions": self.health_conditions,
            "created_at": self.created_at.isoformat()
        }

class Allergy(db.Model):
    __tablename__ = 'allergies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    pets = db.relationship("Pet", secondary="pet_allergies", back_populates="allergies")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

class PetAllergy(db.Model):
    __tablename__ = 'pet_allergies'

    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), primary_key=True)
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergies.id'), primary_key=True)
    def to_json(self):
        return {
            "pet_id": self.pet_id,
            "allergy_id": self.allergy_id,
        }

class MedicalEvent(db.Model):
    __tablename__ = 'medical_events'

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    is_completed = db.Column(db.Boolean)
    recurrence = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notifications = db.relationship("Notification", backref="event", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat(),
            "is_completed": self.is_completed,
            "recurrence": self.recurrence,
            "created_at": self.created_at.isoformat()
        }

class Center(db.Model):
    __tablename__ = 'centers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    hours = db.Column(db.String(255))
    services = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "address": self.address,
            "hours": self.hours,
            "services": self.services,
            "type": self.type
        }

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('medical_events.id'))
    scheduled_at = db.Column(db.DateTime)
    sent = db.Column(db.Boolean)

    def to_json(self):
        return {
            "id": self.id,
            "event_id": self.event_id,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "sent": self.sent
        }