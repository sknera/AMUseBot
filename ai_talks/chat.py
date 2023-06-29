from pathlib import Path
from random import randrange

from AMUseBotBackend.src.DP.dp import DP
from AMUseBotBackend.src.DST.dst import DST

import graphviz
import streamlit as st
from PIL import Image
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation
from src.utils.lang import en
import openai
import copy
import json
import string
import streamlit.components.v1 as components
import re
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    
    # --- PATH SETTINGS ---
    current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    css_file: Path = current_dir / "src/styles/.css"
    assets_dir: Path = current_dir / "assets"
    icons_dir: Path = assets_dir / "icons"
    img_dir: Path = assets_dir / "img"
    tg_svg: Path = icons_dir / "tg.svg"
    favicon: Path = icons_dir / "favicons/0.png"
    # --- GENERAL SETTINGS ---
    LANG_PL: str = "Pl"

    CONFIG = {"page_title": "AMUsebot", "page_icon": Image.open(favicon)}

    st.set_page_config(**CONFIG)

    # --- LOAD CSS ---
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    load_dotenv('.env_template')

    DIALOG_PATH = os.getenv('DIALOG_PATH')
    RECIPE_PATH = os.getenv('RECIPE_PATH')
    CHARACTERS_DICT = os.getenv('CHARACTERS_DICT')
    API_KEY = os.getenv('API_KEY')

    # Storing The Context
    if "locale" not in st.session_state:
        st.session_state.locale = en
    if "generated" not in st.session_state:
        st.session_state.generated = ["Hello! I'm AMUseBot, a virtual cooking assistant. Please tell me the name of the dish that you'd like to prepare today."]
    if "past" not in st.session_state:
        st.session_state.past = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_text" not in st.session_state:
        st.session_state.user_text = ""
    if "seed" not in st.session_state:
        st.session_state.seed = randrange(10 ** 3)  # noqa: S311
    if "costs" not in st.session_state:
        st.session_state.costs = []
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = []
    if "dst" not in st.session_state:
        st.session_state.dst = DST(recipe_path=RECIPE_PATH, dialog_path=DIALOG_PATH)
    if "dp" not in st.session_state:
        st.session_state.dp = DP(dst=st.session_state.dst)
    if "openai" not in st.session_state:
        st.session_state.openai = openai
        st.session_state.openai.api_key = API_KEY
    if "characters_dict" not in st.session_state:
        with open(CHARACTERS_DICT) as f:
            st.session_state.characters_dict = json.load(f)
        
def mermaid(code: str) -> None:
    components.html(
        f"""
        <pre class="mermaid">
            %%{{init: {{'themeVariables': {{ 'edgeLabelBackground': 'transparent'}}}}}}%%
            flowchart TD;
            {code}
            linkStyle default fill:white,color:white,stroke-width:2px,background-color:lime;
        </pre>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """, height=1000
    )

def graph():
    # Create a graphlib graph object
    if st.session_state.generated:
        system = [utterance for utterance in st.session_state.generated][-3:]
        user = [utterance for utterance in st.session_state.past][-2:]
        graph = ""
        for i, utterance in enumerate(system):
            utterance = utterance.strip('\n')
            utterance = " ".join([word + '<br>' if i % 5 == 0 and i > 0 else word for i, word in enumerate(utterance.split(" "))])
            utterance = utterance.replace('\"', '')
            if i < len(user):
                user[i] = user[i].strip('\n')
                user[i] = user[i].replace('\"', '')
                user[i] = " ".join([word + '<br>' if i % 5 == 0 and i > 0 else word for i, word in enumerate(user[i].split(' '))])
                graph += f"{string.ascii_uppercase[i]}(\"{utterance}\") --> |{user[i]}| {string.ascii_uppercase[i+1]};"
            else:
                graph += f"{string.ascii_uppercase[i]}(\"{utterance}\") --> {string.ascii_uppercase[i+1]}(...);style {string.ascii_uppercase[i+1]} fill:none,color:white;"
    graph = graph.replace('\n', ' ')#replace(')','').replace('(','')
    #print(graph)
    return graph


def main() -> None:
    c1, c2 = st.columns(2)
    with c1, c2:
        character_type = c1.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                         options=st.session_state.locale.ai_role_options)
        st.session_state.dp.character = character_type
        if character_type == 'default':
            st.session_state.dp.llm_rephrasing = False
        else:
            st.session_state.dp.llm_rephrasing = True
        
    get_user_input()
    show_chat_buttons()
    
    show_conversation()
    with st.sidebar:
        mermaid(graph())
        #show_graph()


if __name__ == "__main__":
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    main()
