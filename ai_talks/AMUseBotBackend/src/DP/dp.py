from typing import List
from AMUseBotBackend.src.DST.dst import DST
from AMUseBotBackend.src.NLG.nlg import NLG
from AMUseBotBackend.src.tools.search import search_recipe

import AMUseBotBackend.consts as c


class DP:

    def __init__(self, dst: DST):
        self.dst_module = dst



    def generate_response(self, intents: List[str]) -> str:

        # Prompt
        if (None == intents):
            return NLG.MESSAGE_PROMPT

        # No recipe is choosen
        if ((None == self.dst_module.generate_state(c.RECIPE_ID_KEY)) or (
                "" == self.dst_module.generate_state(c.RECIPE_ID_KEY))):
            if ("greeting" in intents):
                return NLG.MESSAGE_HI

            if ("choose_recipe" in intents):
                found_recipe = search_recipe(self.dst_module.generate_state(c.DIALOG_HISTORY_KEY)[-1][
                                                      c.USER_MESSAGE_KEY])  # change this line for user utterance
                if found_recipe:
                    recipe_name = self.dst_module.set_recipe(found_recipe)
                    self.dst_module.set_next_step()
                    return NLG.MESSAGE_CHOOSEN_RECIPE(recipe_name=recipe_name) + "\n" \
                        + self.dst_module.generate_state(c.STEPS_KEY)[self.dst_module.generate_state(c.CURR_STEP_KEY)]
                if not found_recipe:
                    return NLG.MESSAGE_NOT_UNDERSTAND_SUGGEST_RECIPE(self.dst_module.get_random_recipes(3))
            # not understand ask recipe
            return NLG.MESSAGE_ASK_RECIPE

        # Recipe choosen
        if (None != self.dst_module.generate_state(c.RECIPE_ID_KEY) and "" != self.dst_module.generate_state(
                c.RECIPE_ID_KEY)):
            if ("req_ingredient_list" in intents
                    or "req_ingredient" in intents):
                return NLG.MESSAGE_INGREDIENTS(self.dst_module.generate_state(c.INGREDIENTS_KEY))
            if ("confirm" in intents
                    or "affirm" in intents
                    or "req_start" in intents
                    or "thank" in intents
                    or "req_instruction" in intents):
                next_step = self.dst_module.set_next_step()
                if (next_step):
                    return self.dst_module.generate_state(c.STEPS_KEY)[self.dst_module.generate_state(c.CURR_STEP_KEY)]
                if (not next_step):
                    self.dst_module.restart()
                    return NLG.RECIPE_OVER_ANSWER
            if ("req_repeat" in intents):
                return self.dst_module.generate_state(c.STEPS_KEY)[self.dst_module.generate_state(c.CURR_STEP_KEY)]

        # other
        return NLG.NOT_UNDERSTAND_ANSWER
