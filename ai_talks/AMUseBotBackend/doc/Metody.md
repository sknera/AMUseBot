# Metody użyte w prototypie

## NLU
 
Kacper

## DST 

Klasa zawierająca informacje o stanie dialogu. Przechowywane informacje to: 
- id przepisu
- numer obecnego kroku w przepisie
- wszystkie kroki wybranego przepisu
- potrzebne składniki
- historia dialogu

Przykład zapisu stanu dialogu:

    {'dialog_state': {'curr_step': 0,
            'inngredients': ['2 tablespoons canola oil', '1 large eggplant, peeled and sliced', '3 eggs, beaten', '2 cups dry bread crumbs'],
            'recipe_id': 61,
            'steps': {0: 'First heat 2 tablespoons canola oil in a large skillet over medium-high heat.',
                    1: 'Next dip 1 large eggplant, peeled and sliced in the egg. You should use 3 beaten eggs for this.',
                    2: 'Now dip the eggplant into the crumbles. You can use 2 cups dry bread crumbs for this.',
                    3: 'Next place the eggplant into the hot oil.',
                    4: 'Fry 2 to 3 minutes on each side.',
                    5: 'Drain the eggplant on paper towels.'},
            'user_messages': [{'intents': ['greeting', 'req_start'],
                                'system_message': "Hello! I'm AMUseBot, virtual cooking assistant, tell me the name of the recipe you would love to cook today?",
                                'user_message': 'Hello'},
                            {'intents': [], 'system_message': 'Hi! What do you want to cook today?', 'user_message': 'abc'},
                            {'intents': ['req_repeat'],
                                'system_message': 'You choose Easy Fried Eggplant lets get to work.\nFirst heat 2 tablespoons canola oil in a large skillet over medium-high heat.',
                                'user_message': "i don't understand could you repeat"}]}}

## DP

Regułowy moduł podejmujący decyzje na podstawie stanu dialogu oraz aktu mowy użytkownika.	

Przykład reguły polityki dialogu:

    if (None != self.dst_module.generate_state(c.RECIPE_ID_KEY) and "" != self.dst_module.generate_state(c.RECIPE_ID_KEY)):
        if ("req_ingredient_list" in intents
            or "req_ingredient" in intents):
            return NLG.MESSAGE_INGREDIENTS(self.dst_module.generate_state(c.INGREDIENTS_KEY))
 
## NLG 

Moduł oparty o gotowe odpowiedzi oraz szablony

Przykład szablonu:

    @staticmethod
    def MESSAGE_CHOOSEN_RECIPE(recipe_name):
        return "You choose " + recipe_name + " lets get to work."


# *Dodatkowe metody (Opcjonalne)*

##  Okapi BM25 

Wyszukiwarka przepisów - Adrian