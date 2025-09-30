# graphs.py
import networkx as nx
from models import Ingredient, RecipeIngredient, Substitution

def build_substitution_graph(session):
    """Directed graph: A -> B means A can be substituted by B (edge weight = cost)."""
    G = nx.DiGraph()
    for ing in session.query(Ingredient).all():
        G.add_node(ing.id, name=ing.name)
    for s in session.query(Substitution).all():
        # edge weight = cost
        G.add_edge(s.from_ing_id, s.to_ing_id, weight=s.cost)
    return G

def build_inverted_index(session):
    """Return dict: ingredient_id -> set(recipe_id)."""
    inv = {}
    for ri in session.query(RecipeIngredient).all():
        inv.setdefault(ri.ingredient_id, set()).add(ri.recipe_id)
    return inv
