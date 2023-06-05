import os
import sys

import numpy as np
from rank_bm25 import BM25Okapi


def weighted_search(tokenized_query, bm25_recipes, bm25_ingredients,
                    tok_text_recipes, tok_text_ingredients, weight_recipe=10, weight_ingredient=1):
    d_ingredients = np.sum(sorted(bm25_ingredients.get_scores(tokenized_query), reverse=True)[:10])
    d_recipes = np.sum(sorted(bm25_recipes.get_scores(tokenized_query), reverse=True)[:10])
    d = d_ingredients + d_recipes

    weighted_scores_ingredients = bm25_ingredients.get_scores(tokenized_query) * weight_ingredient
    weighted_scores_recipes = bm25_recipes.get_scores(tokenized_query) * weight_recipe


    ingredients_recipes_scores = weighted_scores_ingredients + weighted_scores_recipes

    if np.max(ingredients_recipes_scores / d) if d else 0 > 1.00:  # can be set to other value
        result = np.argmax(ingredients_recipes_scores)
        return int(tok_text_recipes[result][1])
    else:
        return None


def search_recipe(query):
    tokenized_query = query.lower().split(" ")

    tok_text_ingredients = []
    tok_text_recipes = []
    with open('AMUseBotFront/ai_talks/AMUseBotBackend/utils/tools/ingredients_recipes_merged.csv', 'r') as file:
        for line in file:
            line = line.split(',  ')
            ingredients_splitted = [x for x in line[1].split(',')]
            tok_text_ingredients.append(ingredients_splitted)
            tok_text_recipes.append([ingredients_splitted[0]] + [x.lower() for x in line[0].split(',')])


    bm25_recipes = BM25Okapi([recipe[2:] for recipe in tok_text_recipes])
    bm25_ingredients = BM25Okapi([ingredient[1:] for ingredient in tok_text_ingredients])

    result = weighted_search(
        tokenized_query, bm25_recipes, bm25_ingredients, tok_text_recipes, tok_text_ingredients, weight_recipe=10,
        weight_ingredient=1
        # word in recipe title is 10 times more important than in ingredients list
    )
    return result
