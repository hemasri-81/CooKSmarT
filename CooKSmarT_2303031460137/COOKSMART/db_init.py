# db_init.py
from app import create_app
from models import db, Ingredient, Recipe, RecipeIngredient, Substitution

def normalize(s: str) -> str:
    return s.strip().lower()

SAMPLE_RECIPES = [
    {
        "title": "Pancakes",
        "instructions": "Mix flour, milk, egg, sugar and fry.",
        "ingredients": [("flour","1 cup"), ("milk","3/4 cup"), ("egg","1"), ("sugar","1 tbsp"), ("butter","1 tbsp")]
    },
    {
        "title": "Omelette",
        "instructions": "Beat eggs with milk, fry with salt & pepper and onion.",
        "ingredients": [("egg","2"), ("milk","2 tbsp"), ("salt","to taste"), ("pepper","to taste"), ("onion","1/4 cup")]
    },
    {
        "title": "Grilled Cheese",
        "instructions": "Place cheese between bread and grill with butter.",
        "ingredients": [("bread","2 slices"), ("cheese","2 slices"), ("butter","1 tbsp")]
    },
    {
        "title": "Pasta Alfredo",
        "instructions": "Cook pasta and mix with butter, garlic, milk and cheese.",
        "ingredients": [("pasta","200 g"), ("butter","2 tbsp"), ("garlic","2 cloves"), ("cheese","1/2 cup"), ("milk","1/2 cup")]
    },
    {
        "title": "Simple Salad",
        "instructions": "Chop lettuce, tomato and cucumber and toss with olive oil & salt.",
        "ingredients": [("lettuce","1 head"), ("tomato","1"), ("cucumber","1/2"), ("olive oil","1 tbsp"), ("salt","to taste")]
    },
    {
        "title": "French Toast",
        "instructions": "Dip bread in beaten egg and milk, fry with butter.",
        "ingredients": [("bread","2 slices"), ("egg","1"), ("milk","1/4 cup"), ("butter","1 tbsp"), ("sugar","1 tsp")]
    },
    {
        "title": "Tomato Soup",
        "instructions": "Cook tomatoes with onion, garlic, and blend with butter.",
        "ingredients": [("tomato","3"), ("onion","1/2"), ("garlic","2 cloves"), ("butter","1 tbsp"), ("salt","to taste")]
    },
    {
        "title": "Scrambled Eggs",
        "instructions": "Beat eggs, cook with butter, season with salt and pepper.",
        "ingredients": [("egg","2"), ("butter","1 tbsp"), ("salt","to taste"), ("pepper","to taste")]
    },
    {
        "title": "Mashed Potatoes",
        "instructions": "Boil potatoes, mash with butter and milk, season with salt.",
        "ingredients": [("potato","2"), ("butter","2 tbsp"), ("milk","1/4 cup"), ("salt","to taste")]
    },
    {
        "title": "Garlic Bread",
        "instructions": "Spread garlic butter on bread slices and bake.",
        "ingredients": [("bread","2 slices"), ("garlic","2 cloves"), ("butter","2 tbsp")]
    },
    {
        "title": "Fruit Salad",
        "instructions": "Chop apple, banana, and orange, mix with honey.",
        "ingredients": [("apple","1"), ("banana","1"), ("orange","1"), ("honey","1 tbsp")]
    },
    {
        "title": "Veggie Stir Fry",
        "instructions": "Stir fry carrot, beans, and capsicum with soy sauce.",
        "ingredients": [("carrot","1"), ("beans","1/2 cup"), ("capsicum","1"), ("soy sauce","1 tbsp"), ("oil","1 tbsp")]
    },
    {
        "title": "Rice Pulao",
        "instructions": "Cook rice with peas, carrot, onion, and spices.",
        "ingredients": [("rice","1 cup"), ("peas","1/2 cup"), ("carrot","1"), ("onion","1"), ("oil","1 tbsp"), ("salt","to taste")]
    },
    {
        "title": "Chicken Curry",
        "instructions": "Cook chicken with onion, tomato, garlic, ginger, and spices.",
        "ingredients": [("chicken","200 g"), ("onion","1"), ("tomato","1"), ("garlic","2 cloves"), ("ginger","1 tsp"), ("oil","2 tbsp")]
    },
    {
        "title": "Fried Rice",
        "instructions": "Stir fry cooked rice with egg, carrot, beans, and soy sauce.",
        "ingredients": [("rice","1 cup"), ("egg","1"), ("carrot","1/2"), ("beans","1/2 cup"), ("soy sauce","1 tbsp"), ("oil","1 tbsp")]
    },
    {
        "title": "Paratha",
        "instructions": "Roll out dough with flour, fry with oil or ghee.",
        "ingredients": [("flour","1 cup"), ("water","1/2 cup"), ("salt","pinch"), ("oil","1 tbsp")]
    },
    {
        "title": "Poha",
        "instructions": "Cook poha with onion, curry leaves, turmeric, and peanuts.",
        "ingredients": [("poha","1 cup"), ("onion","1/2"), ("curry leaves","5"), ("turmeric","1/4 tsp"), ("peanuts","2 tbsp")]
    },
    {
        "title": "Upma",
        "instructions": "Roast semolina, cook with onion, carrot, beans, and spices.",
        "ingredients": [("semolina","1 cup"), ("onion","1/2"), ("carrot","1/2"), ("beans","1/4 cup"), ("oil","1 tbsp")]
    },
    {
        "title": "Sandwich",
        "instructions": "Layer bread with tomato, cucumber, cheese, and lettuce.",
        "ingredients": [("bread","2 slices"), ("tomato","1"), ("cucumber","1/2"), ("cheese","1 slice"), ("lettuce","2 leaves")]
    },
    {
        "title": "Banana Smoothie",
        "instructions": "Blend banana with milk, sugar, and ice.",
        "ingredients": [("banana","1"), ("milk","1 cup"), ("sugar","1 tsp"), ("ice","3 cubes")]
    },
    {
        "title": "Idli",
        "instructions": "Soak rice and urad dal, grind to batter, ferment overnight, and steam in idli molds.",
        "ingredients": [("rice","2 cups"), ("urad dal","1 cup"), ("fenugreek seeds","1 tsp"), ("salt","to taste"), ("water","as needed")]
    },
    {
        "title": "Dosa",
        "instructions": "Prepare fermented batter, spread thin on hot tawa, cook until crisp, serve with chutney.",
        "ingredients": [("rice","2 cups"), ("urad dal","1 cup"), ("salt","to taste"), ("oil","2 tbsp"), ("water","as needed")]
    },
    {
        "title": "Sambar",
        "instructions": "Cook dal, mix with tamarind water, add vegetables, sambar powder, and temper with spices.",
        "ingredients": [("toor dal","1 cup"), ("tamarind","small lemon size"), ("sambar powder","2 tbsp"), ("drumstick","1"), ("curry leaves","few")]
    },
    {
        "title": "Rasam",
        "instructions": "Boil tamarind water with rasam powder, tomatoes, dal water, and temper with mustard & curry leaves.",
        "ingredients": [("tamarind","small lemon size"), ("rasam powder","1 tbsp"), ("tomato","1"), ("toor dal","1/4 cup"), ("mustard seeds","1 tsp")]
    },
    {
        "title": "Upma",
        "instructions": "Roast rava, fry onions & green chili in ghee, add water, salt, cook until fluffy.",
        "ingredients": [("rava/sooji","1 cup"), ("onion","1"), ("green chili","2"), ("ghee","2 tbsp"), ("salt","to taste")]
    },
    {
        "title": "Pongal",
        "instructions": "Cook rice and moong dal with pepper, cumin, ginger, and ghee until soft.",
        "ingredients": [("rice","1 cup"), ("moong dal","1/2 cup"), ("pepper","1 tsp"), ("cumin","1 tsp"), ("ghee","2 tbsp")]
    },
    {
        "title": "Vada",
        "instructions": "Soak urad dal, grind smooth, shape into rings, deep fry until golden.",
        "ingredients": [("urad dal","1 cup"), ("onion","1 small"), ("green chili","2"), ("ginger","1 tsp"), ("salt","to taste")]
    },
    {
        "title": "Curd Rice",
        "instructions": "Mix cooked rice with curd, add salt, temper with mustard & curry leaves.",
        "ingredients": [("rice","1 cup"), ("curd","1 cup"), ("mustard seeds","1 tsp"), ("curry leaves","few"), ("salt","to taste")]
    },
    {
        "title": "Lemon Rice",
        "instructions": "Mix cooked rice with lemon juice, turmeric, tempered mustard seeds & chilies.",
        "ingredients": [("rice","2 cups"), ("lemon juice","2 tbsp"), ("turmeric","1/2 tsp"), ("mustard seeds","1 tsp"), ("green chili","2")]
    },
    {
        "title": "Tamarind Rice",
        "instructions": "Cook tamarind pulp with jaggery & spices, mix with rice.",
        "ingredients": [("rice","2 cups"), ("tamarind","small lemon size"), ("jaggery","1 tsp"), ("red chili","2"), ("curry leaves","few")]
    },

    # ---------- NORTH INDIAN ----------
    {
        "title": "Chole",
        "instructions": "Cook soaked chickpeas with onion, tomato, ginger-garlic paste, and chole masala.",
        "ingredients": [("chickpeas","2 cups"), ("onion","2"), ("tomato","2"), ("chole masala","2 tbsp"), ("ginger-garlic paste","1 tbsp")]
    },
    {
        "title": "Paneer Butter Masala",
        "instructions": "Cook paneer cubes in a creamy tomato-onion gravy with butter and spices.",
        "ingredients": [("paneer","200 g"), ("butter","2 tbsp"), ("onion","1"), ("tomato puree","1 cup"), ("cream","1/4 cup")]
    },
    {
        "title": "Rajma",
        "instructions": "Cook soaked rajma with onion-tomato masala until soft and flavorful.",
        "ingredients": [("rajma","2 cups"), ("onion","2"), ("tomato","2"), ("ginger-garlic paste","1 tbsp"), ("garam masala","1 tsp")]
    },
    {
        "title": "Aloo Paratha",
        "instructions": "Stuff wheat dough with spiced mashed potato, roll and roast with ghee.",
        "ingredients": [("wheat flour","2 cups"), ("potato","2"), ("green chili","2"), ("ghee","2 tbsp"), ("salt","to taste")]
    },
    {
        "title": "Palak Paneer",
        "instructions": "Blend spinach, cook with masala and add paneer cubes.",
        "ingredients": [("spinach","2 cups"), ("paneer","200 g"), ("onion","1"), ("ginger-garlic paste","1 tsp"), ("cream","2 tbsp")]
    },
    {
        "title": "Baingan Bharta",
        "instructions": "Roast brinjal, mash, cook with onion, tomato, and spices.",
        "ingredients": [("brinjal","1 large"), ("onion","1"), ("tomato","1"), ("green chili","2"), ("oil","2 tbsp")]
    },
    {
        "title": "Dal Makhani",
        "instructions": "Cook urad dal & rajma with butter, cream, and slow simmer for rich flavor.",
        "ingredients": [("urad dal","1 cup"), ("rajma","1/4 cup"), ("butter","2 tbsp"), ("cream","1/4 cup"), ("ginger-garlic paste","1 tbsp")]
    },
    {
        "title": "Kadai Paneer",
        "instructions": "Cook paneer with onion, capsicum, tomato, and kadai masala.",
        "ingredients": [("paneer","200 g"), ("capsicum","1"), ("onion","1"), ("tomato","1"), ("kadai masala","1 tbsp")]
    },
    {
        "title": "Poori Bhaji",
        "instructions": "Make wheat dough, roll into pooris, deep fry, serve with potato curry.",
        "ingredients": [("wheat flour","2 cups"), ("potato","2"), ("green chili","2"), ("turmeric","1/2 tsp"), ("oil","for frying")]
    },
    {
        "title": "Chicken Curry (North Indian)",
        "instructions": "Cook chicken with onion-tomato gravy, spices, and simmer until tender.",
        "ingredients": [("chicken","500 g"), ("onion","2"), ("tomato","2"), ("ginger-garlic paste","2 tbsp"), ("garam masala","1 tsp")]
    }
]

# sample substitutions (from -> to, cost)
SAMPLE_SUBS = [
    ("butter", "olive oil", 1.0),
    ("butter", "vegetable oil", 1.2),
    ("milk", "almond milk", 1.5),
    ("cheese", "vegan cheese", 2.0),
    ("bread", "tortilla", 1.3),
    ("egg", "flax meal", 2.5)
]

def seed_db():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # collect unique ingredient names
        all_ing_names = set()
        for r in SAMPLE_RECIPES:
            for n, _ in r['ingredients']:
                all_ing_names.add(normalize(n))
        for a,b,_ in SAMPLE_SUBS:
            all_ing_names.add(normalize(a)); all_ing_names.add(normalize(b))

        # create Ingredient objects and map name->obj
        name_map = {}
        for name in sorted(all_ing_names):
            ing = Ingredient(name=name)
            db.session.add(ing)
            db.session.flush()
            name_map[name] = ing

        # create recipes and recipe_ingredients
        for r in SAMPLE_RECIPES:
            rec = Recipe(title=r['title'], instructions=r.get('instructions',''))
            db.session.add(rec)
            db.session.flush()
            for ing_name, qty in r['ingredients']:
                n = normalize(ing_name)
                ri = RecipeIngredient(recipe_id=rec.id, ingredient_id=name_map[n].id, quantity=qty)
                db.session.add(ri)

        # create substitutions
        for frm, to, cost in SAMPLE_SUBS:
            s = Substitution(from_ing_id=name_map[normalize(frm)].id,
                             to_ing_id=name_map[normalize(to)].id,
                             cost=cost)
            db.session.add(s)

        db.session.commit()
        print("Seeded DB with sample recipes and substitutions.")

if __name__ == "__main__":
    seed_db()
