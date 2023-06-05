class NLG:
    MESSAGE_PROMPT = "Hello! I'm AMUseBot, a virtual cooking assistant. Please tell me the name of the dish that you'd like to prepare today."
    MESSAGE_HI   = "Hi! What do you want to make today?"
    MESSAGE_ASK_RECIPE = "Please tell me the name of the recipe."
    BYE_ANSWER    = "Bye, hope to see you soon!"
    RECIPE_OVER_ANSWER    = "Congratulations! You finished preparing the dish, bon appetit!"
    NOT_UNDERSTAND_ANSWER = "I'm sorry, I don't understand. Could you rephrase?"

    @staticmethod
    def MESSAGE_INGREDIENTS(ingr_list):
        return ", ".join(ingr_list)

    @staticmethod
    def MESSAGE_CHOOSEN_RECIPE(recipe_name):
        return f"You've chosen {recipe_name}. Let's get busy!"

    @staticmethod
    def MESSAGE_NOT_UNDERSTAND_SUGGEST_RECIPE(recipes_list):
        suggestions = ""
        if len(recipes_list) <= 2:
            suggestions = " or ".join(recipes_list)

        if len(recipes_list) > 2:
            suggestions = ", ".join(recipes_list[0:-1]) + f" or {recipes_list[-1]}"

        return f"I'm sorry, I don't know a recipe like that. Instead, I can suggest you {suggestions}."
