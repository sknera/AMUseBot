import json
from typing import Dict
from os import walk
import re
import random

import AMUseBotBackend.consts as c

class DST:
    def __init__(self, recipe_path, dialog_path):
        self.__recipe_path = recipe_path
        self.__dialog_path = dialog_path
        self.recipes = {}
        self.__set_all_recipes()
        self.__recipe_id = None
        self.__curr_step = None
        self.__ingredients = []
        self.__steps = {}
        self.__dialog_history = []

    def generate_state(self, key=None) -> Dict:
        state = {
            c.RECIPE_ID_KEY: self.__recipe_id,
            c.CURR_STEP_KEY: self.__curr_step,
            c.STEPS_KEY: self.__steps,
            c.INGREDIENTS_KEY: self.__ingredients,
            c.DIALOG_HISTORY_KEY: self.__dialog_history,
        }
        return state if not key else state.get(key, "")

    def set_recipe(self, recipe_id) -> Dict:
        self.__recipe_id = recipe_id
        self.__set_steps()
        self.__set_ingredients()
        return self.recipes[recipe_id]

    def set_next_step(self) -> bool:
        if (None == self.__curr_step):
            self.__curr_step = 0
            return True
        if (self.__curr_step < len(self.__steps) - 1):
            self.__curr_step += 1
            return True
        return False 

    def update_dialog_history(self, system_message, user_message, intents):
        obj = {}
        obj[c.SYSTEM_MESSAGE_KEY] = system_message
        obj[c.USER_MESSAGE_KEY] = user_message
        obj[c.INTENTS_KEY] = intents
        self.__dialog_history.append(obj)

    def add_intent(self, intent):
        self.__intents.append(intent)

    def restart(self):
        self.__init__(self.__recipe_path, self.__dialog_path)

    def __set_all_recipes(self) -> Dict:
        recipe_files = [] 
        for (_, _, filenames) in walk(self.__recipe_path):
            recipe_files.extend(filenames)
            break
        regex_pattern = re.compile(r'([0-9]{3})_(.+).json')
        recipe_dict = {}
        for recipe_title in recipe_files:
            result = re.search(regex_pattern, recipe_title)
            recipe_dict[int(result.group(1))] = result.group(2).replace("_", " ")
        self.recipes = recipe_dict


    def get_random_recipes(self, n):
        recipes_id = []
        while len(recipes_id) < n:
            random_id = random.randint(0, len(self.recipes) - 1)
            if random_id not in recipes_id: recipes_id.append(random_id)
        return [self.recipes[id] for id in recipes_id]

    def __set_steps(self):
        dialog_files = [] 
        steps = {}
        for (_, _, filenames) in walk(self.__dialog_path):
            dialog_files.extend(filenames)
            break
        for dialog_title in dialog_files:
            if dialog_title.startswith(f"{self.__recipe_id:03d}"):
                with open(self.__dialog_path + "/" + dialog_title) as f:
                    data = json.load(f)
                    for message in data["messages"]:
                        if "inform_instruction" in message["annotations"]:
                            steps[len(steps)] = message["utterance"]
        self.__steps = steps
    
    def __set_ingredients(self):
        dialog_files = []
        ingredients = []
        for (_, _, filenames) in walk(self.__recipe_path):
            dialog_files.extend(filenames)
            break
        for dialog_title in dialog_files:
            if dialog_title.startswith(f"{self.__recipe_id:03d}"):
                with open(self.__recipe_path + dialog_title) as f:
                    data = json.load(f)
                    for row in data['content']:
                        if row['type']=='ingredient':
                            ingredients.append(row['text'])
        self.__ingredients = ingredients
