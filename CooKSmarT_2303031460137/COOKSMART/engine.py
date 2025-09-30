# engine.py
import networkx as nx
from models import Ingredient, Recipe

def normalize(name: str) -> str:
    return name.strip().lower()

def suggest_recipes(session, sub_graph, inv_index, available_names,
                    max_missing=2, max_sub_hops=2, top_n=10):
    """
    session: db.session
    sub_graph: networkx DiGraph (from graphs.build_substitution_graph)
    inv_index: ingredient_id -> set(recipe_id)
    available_names: list[str] (free text names)
    """
    # normalize
    available_norm = [normalize(x) for x in available_names if x and x.strip()]
    if not available_norm:
        return []

    # map names to ingredient ids
    ing_objs = session.query(Ingredient).filter(Ingredient.name.in_(available_norm)).all()
    avail_ids = {i.id for i in ing_objs}
    # if none matched, return empty
    if not avail_ids:
        return []

    # candidate recipes via inverted index
    candidate_recipe_ids = set()
    for aid in avail_ids:
        candidate_recipe_ids |= inv_index.get(aid, set())

    results = []
    for rid in candidate_recipe_ids:
        recipe = session.get(Recipe, rid) or Recipe.query.get(rid)
        # gather ingredient ids for recipe
        recipe_ing_ids = {ri.ingredient_id for ri in recipe.recipe_ingredients}
        direct_matches = recipe_ing_ids & avail_ids
        missing = list(recipe_ing_ids - avail_ids)

        substitution_plan = {}   # missing_id -> substitute_available_id
        unmet = []
        substitution_cost = 0.0

        for m in missing:
            best = None
            # try shortest path from missing -> any available ing
            for a in avail_ids:
                try:
                    # compute shortest path length in hops (ignore weights for hop limit)
                    hops = nx.shortest_path_length(sub_graph, m, a)
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    continue
                if hops <= max_sub_hops and (best is None or hops < best[0]):
                    best = (hops, a)
            if best:
                hops, a = best
                # compute substitution cost along shortest weighted path
                try:
                    path = nx.shortest_path(sub_graph, m, a, weight='weight')
                    # sum edge weights
                    path_cost = 0.0
                    for i in range(len(path)-1):
                        edge_w = sub_graph[path[i]][path[i+1]].get('weight', 1.0)
                        path_cost += edge_w
                except Exception:
                    path_cost = hops * 1.0
                substitution_plan[m] = a
                substitution_cost += path_cost
            else:
                unmet.append(m)

        if len(unmet) > max_missing:
            continue

        used_count = len(direct_matches) + len(substitution_plan)
        total_ings = len(recipe_ing_ids) if recipe_ing_ids else 1

        # scoring formula (tweak if desired)
        score = (used_count / total_ings) - (len(unmet) * 0.4) - (substitution_cost * 0.05)

        # map ids -> names
        def name_of(iid):
            ing = session.get(Ingredient, iid) or Ingredient.query.get(iid)
            return ing.name if ing else str(iid)

        results.append({
            "recipe_id": rid,
            "title": recipe.title,
            "score": round(score, 3),
            "ingredients": [name_of(ri.ingredient_id) for ri in recipe.recipe_ingredients],
            "missing": [name_of(mid) for mid in unmet],
            "substitutions": {name_of(k): name_of(v) for k, v in substitution_plan.items()}
        })

    # sort and return top_n
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_n]
