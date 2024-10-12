import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("name")
    def validate_name(self, key, value):
        authors_names = [author.name for author in Author.query.all()]
        if not value or value in authors_names:
            raise ValueError("An author must have a name")
        return value

    @validates("phone_number")
    def validate_phone_number(self, key, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must be 10 digits")
        return value

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("content")
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return value

    @validates("summary")
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("A post summary must be at most 250 characters long")
        return value

    @validates("title")
    def validate_title(self, key, value):
        if not value:
            raise ValueError("A post must have a title")
        required_strings = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(required_string in value for required_string in required_strings):
            raise ValueError(
                "A post title must contain either Won't Believe or Secret or Top or Guess"
            )
        return value

    @validates("category")
    def validate_category(self, key, value):
        if not value in ["Fiction", "Non-Fiction"]:
            raise ValueError("Post category must either be Fiction or Non-Fiction")
        return value

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"