# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return f"<Ingredient {self.name}>"

class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Recipe {self.title}>"

class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)
    quantity = db.Column(db.String(64), nullable=True)

    recipe = db.relationship("Recipe", backref=db.backref("recipe_ingredients", cascade="all,delete-orphan"))
    ingredient = db.relationship("Ingredient")

class Substitution(db.Model):
    __tablename__ = "substitution"
    id = db.Column(db.Integer, primary_key=True)
    from_ing_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), nullable=False)
    to_ing_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), nullable=False)
    cost = db.Column(db.Float, default=1.0)  # smaller = better substitute

    from_ing = db.relationship("Ingredient", foreign_keys=[from_ing_id])
    to_ing = db.relationship("Ingredient", foreign_keys=[to_ing_id])

    def __repr__(self):
        return f"<Sub {self.from_ing.name} -> {self.to_ing.name} cost={self.cost}>"
