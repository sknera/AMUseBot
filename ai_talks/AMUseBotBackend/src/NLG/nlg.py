import streamlit as st
class NLG:
    MESSAGE_PROMPT = "Hello! I'm AMUseBot, a virtual cooking assistant. Please tell me the name of the dish that you'd like to prepare today."
    MESSAGE_HI   = "Hi! What do you want to make today?"
    MESSAGE_ASK_RECIPE = "Please tell me the name of the recipe."
    BYE_ANSWER    = "Bye, hope to see you soon!"
    RECIPE_OVER_ANSWER    = "Congratulations! You finished preparing the dish, bon appetit!"
    NOT_UNDERSTAND_ANSWER = "I'm sorry, I don't understand. Could you rephrase?"
    CANNOT_HELP_ANSWER = "I'm sorry I can't help you with that."

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

    
    def llm_create_response(character, input):
        model = st.session_state.characters_dict['model']
        prompt = st.session_state.characters_dict['characters'][character]['prompt']

        message = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': input}]

        response = st.session_state.openai.ChatCompletion.create(
            model=model, messages=message, temperature=1, max_tokens=128
        )
        rephrased_response = response.choices[0].message.content

        return rephrased_response
    
    def llm_rephrase_recipe(character, response):

        input = st.session_state.characters_dict['task_paraphrase'] + f'"{response}".' + st.session_state.characters_dict['characters'][character]['task_specification']
        try:
            return NLG.llm_create_response(character, input)
        except:
            print('OpenAI API call failed during response paraphrasing! Returning input response')
            return response

    def llm_substitute_product(character, user_message):

        input = st.session_state.characters_dict['task_substitute'] + f'"{user_message}".' + st.session_state.characters_dict['characters'][character]['task_specification']

        try:
            return NLG.llm_create_response(character, input)
        except:
            print('OpenAI API call failed during response paraphrasing! Returning input response')
            return NLG.CANNOT_HELP_ANSWER


