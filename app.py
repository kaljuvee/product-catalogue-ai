import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv

# --- LOAD ENVIRONMENT ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY puudub .env failis. Palun lisa see ja taaskäivita rakendus.")
    st.stop()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# --- CONFIG ---
st.set_page_config(page_title="ABC Kliima - Tootekataloogi Chat", page_icon="❄️", layout="centered")

# --- LOAD DATA ---
@st.cache_data
def load_products():
    return pd.read_csv("products.csv")

df = load_products()

# --- LANGCHAIN AGENT ---
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)

# --- SUGGESTIONS ---
def get_suggestions():
    return [
        "Näita kõiki õhksoojuspumpasid",
        "Millised on kõige odavamad tooted?",
        "Näita A+++ energiaklassiga tooteid",
        "Millised on saadaval maasoojuspumbad?",
        "Näita tooteid alla 500 euro",
        "Millised on kõige võimsamad tooted?",
        "Näita konditsioneere",
        "Millised on ventilatsiooniseadmed?",
        "Näita päikesepaneelid",
        "Millised on paigaldustarvikud?"
    ]

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- MAIN UI ---
st.title("❄️ ABC Kliima - Tootekataloogi Chat")
st.markdown("Küsi tootekataloogi kohta. Vastused põhinevad andmetabelil. Kõik küsimused ja vastused on eesti keeles.")

# Show chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**Teie:** {msg['content']}")
    else:
        st.markdown(f"**ABC Kliima:** {msg['content']}")

# Suggestion buttons
st.markdown("**Soovitused:**")
sugg_cols = st.columns(2)
suggestions = get_suggestions()
clicked_suggestion = None
for i, suggestion in enumerate(suggestions):
    if sugg_cols[i % 2].button(suggestion, key=f"sugg_{i}"):
        clicked_suggestion = suggestion

# Input box
user_input = st.text_input(
    "Küsi midagi kataloogi kohta:",
    value=clicked_suggestion if clicked_suggestion else "",
    key="user_input_box"
)

# On submit
if st.button("Saada") or clicked_suggestion:
    query = user_input.strip() if not clicked_suggestion else clicked_suggestion
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.spinner("Otsin vastust..."):
            try:
                response = agent.run(f"Vasta eesti keeles: {query}")
            except Exception as e:
                response = f"Vabandust, tekkis viga: {e}"
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# Input placeholder
st.markdown("<div style='color: #888;'>Küsi näiteks: 'Millised on kõige odavamad tooted?'</div>", unsafe_allow_html=True) 