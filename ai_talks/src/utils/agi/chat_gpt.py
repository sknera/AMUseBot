import logging
from typing import List  # NOQA: UP035

import openai
import streamlit as st


@st.cache_data()
def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
    #logging.info(f"{messages=}")
    # completion = openai.ChatCompletion.create(
    #     model=ai_model,
    #     messages=messages,
    #     # stream=True,
    #     # temperature=0.7,
    # )
    #logging.info(f"{completion=}")
   # return completion
   pass
