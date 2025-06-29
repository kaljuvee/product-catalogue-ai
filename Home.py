import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
import re

# --- LOAD ENVIRONMENT ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY puudub .env failis. Palun lisa see ja taaskäivita rakendus.")
    st.stop()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# --- CONFIG ---
st.set_page_config(page_title="ABC Kliima - Tootekataloogi Chat", page_icon="❄️", layout="centered")

# --- ESTONIAN WORD VARIATIONS ---
def get_estonian_variations(word):
    """Generate Estonian word variations for better matching"""
    word = word.lower().strip()
    variations = {word}
    
    # Common Estonian word variations
    estonian_variations = {
        # Õhksoojuspumbad variations
        'õhksoojuspumbad': ['õhksoojuspump', 'õhksoojuspumpa', 'õhksoojuspumpasid', 'õhksoojuspumpade', 'õhksoojuspumpadel'],
        'õhksoojuspump': ['õhksoojuspumbad', 'õhksoojuspumpa', 'õhksoojuspumpasid', 'õhksoojuspumpade', 'õhksoojuspumpadel'],
        
        # Maasoojuspumbad variations
        'maasoojuspumbad': ['maasoojuspump', 'maasoojuspumpa', 'maasoojuspumpasid', 'maasoojuspumpade', 'maasoojuspumpadel'],
        'maasoojuspump': ['maasoojuspumbad', 'maasoojuspumpa', 'maasoojuspumpasid', 'maasoojuspumpade', 'maasoojuspumpadel'],
        
        # Õhk-vesisoojuspumbad variations
        'õhk-vesisoojuspumbad': ['õhk-vesisoojuspump', 'õhk-vesisoojuspumpa', 'õhk-vesisoojuspumpasid'],
        'õhk-vesisoojuspump': ['õhk-vesisoojuspumbad', 'õhk-vesisoojuspumpa', 'õhk-vesisoojuspumpasid'],
        
        # Ventilatsioonisoojuspumbad variations
        'ventilatsioonisoojuspumbad': ['ventilatsioonisoojuspump', 'ventilatsioonisoojuspumpa', 'ventilatsioonisoojuspumpasid'],
        'ventilatsioonisoojuspump': ['ventilatsioonisoojuspumbad', 'ventilatsioonisoojuspumpa', 'ventilatsioonisoojuspumpasid'],
        
        # Konditsioneerid variations
        'konditsioneerid': ['konditsioneer', 'konditsioneeri', 'konditsioneere', 'konditsioneeride'],
        'konditsioneer': ['konditsioneerid', 'konditsioneeri', 'konditsioneere', 'konditsioneeride'],
        
        # Ventilatsioon variations
        'ventilatsioon': ['ventilatsiooniseadmed', 'ventilatsiooniseade', 'ventilatsiooniseadet'],
        'ventilatsiooniseadmed': ['ventilatsioon', 'ventilatsiooniseade', 'ventilatsiooniseadet'],
        
        # Kesktolmuimejad variations
        'kesktolmuimejad': ['kesktolmuimeja', 'kesktolmuimejat', 'kesktolmuimejate'],
        'kesktolmuimeja': ['kesktolmuimejad', 'kesktolmuimejat', 'kesktolmuimejate'],
        
        # Päikesepaneelid variations
        'päikesepaneelid': ['päikesepaneel', 'päikesepaneeli', 'päikesepaneelid', 'päikesepaneelide'],
        'päikesepaneel': ['päikesepaneelid', 'päikesepaneeli', 'päikesepaneelid', 'päikesepaneelide'],
        
        # Paigaldustarvikud variations
        'paigaldustarvikud': ['paigaldustarvik', 'paigaldustarvikut', 'paigaldustarvikute'],
        'paigaldustarvik': ['paigaldustarvikud', 'paigaldustarvikut', 'paigaldustarvikute'],
        
        # Küttejaotus variations
        'küttejaotus': ['küttejaotuse', 'küttejaotust', 'küttejaotused'],
        
        # Veeboilerid variations
        'veeboilerid': ['veeboiler', 'veeboileri', 'veeboilerit', 'veeboilerite'],
        'veeboiler': ['veeboilerid', 'veeboileri', 'veeboilerit', 'veeboilerite'],
        
        # Akumulatsioonipaagid variations
        'akumulatsioonipaagid': ['akumulatsioonipaak', 'akumulatsioonipaagi', 'akumulatsioonipaaki'],
        'akumulatsioonipaak': ['akumulatsioonipaagid', 'akumulatsioonipaagi', 'akumulatsioonipaaki'],
        
        # Elektrikatlad variations
        'elektrikatlad': ['elektrikatel', 'elektrikatla', 'elektrikatlat', 'elektrikatlate'],
        'elektrikatel': ['elektrikatlad', 'elektrikatla', 'elektrikatlat', 'elektrikatlate'],
        
        # Küttekehad variations
        'küttekehad': ['küttekeha', 'küttekeha', 'küttekehi', 'küttekehade'],
        'küttekeha': ['küttekehad', 'küttekeha', 'küttekehi', 'küttekehade'],
        
        # Õhkkardinad variations
        'õhkkardinad': ['õhkkardin', 'õhkkardina', 'õhkkardinat', 'õhkkardinade'],
        'õhkkardin': ['õhkkardinad', 'õhkkardina', 'õhkkardinat', 'õhkkardinade'],
        
        # Õhukuivatid variations
        'õhukuivatid': ['õhukuivati', 'õhukuivati', 'õhukuivatit', 'õhukuivatite'],
        'õhukuivati': ['õhukuivatid', 'õhukuivati', 'õhukuivatit', 'õhukuivatite'],
        
        # Keemiakaubad variations
        'keemiakaubad': ['keemiakaup', 'keemiakauba', 'keemiakaubat', 'keemiakaubade'],
        'keemiakaup': ['keemiakaubad', 'keemiakauba', 'keemiakaubat', 'keemiakaubade'],
    }
    
    # Add variations if word exists in our dictionary
    if word in estonian_variations:
        variations.update(estonian_variations[word])
    
    # Also add the original word and common suffixes
    variations.add(word)
    variations.add(word.replace('id', ''))  # Remove plural ending
    variations.add(word.replace('ad', ''))  # Remove plural ending
    variations.add(word.replace('ud', ''))  # Remove plural ending
    
    return variations

def find_matching_category(query, categories):
    """Find matching category using Estonian word variations"""
    query_lower = query.lower()
    query_variations = get_estonian_variations(query)
    
    for category in categories:
        category_lower = str(category).lower()
        category_variations = get_estonian_variations(category_lower)
        
        # Check if any variation matches
        for query_var in query_variations:
            for cat_var in category_variations:
                if query_var in cat_var or cat_var in query_var:
                    return category
    
    return None

# --- LOAD DATA ---
@st.cache_data
def load_products():
    return pd.read_csv("products.csv")

df = load_products()

# --- LANGCHAIN AGENT ---
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    allow_dangerous_code=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

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

# Sidebar
with st.sidebar:
    st.header("⚙️ Seaded")
    
    # Refresh button
    if st.button("🔄 Puhasta vestlus", type="primary"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Show data button
    if st.button("📊 Näita andmeid"):
        st.session_state.show_data = not st.session_state.get('show_data', False)
        st.rerun()
    
    st.markdown("---")
    
    # Company Information
    st.subheader("🏢 Ettevõtte teave")
    st.markdown("**ABC Kliima** - Teie usaldusväärne partner kliimaseadmete ja ventilatsioonilahenduste valdkonnas")
    
    st.markdown("📞 **Telefon:** +372 1234 5678")
    st.markdown("📧 **E-post:** info@abckliima.ee")
    st.markdown("🌐 **Veebileht:** www.abckliima.ee")
    
    st.markdown("---")
    st.markdown("**❄️ Kvaliteetsed kliimaseadmed ja ventilatsioonilahendused**")

# Show data if requested
if st.session_state.get('show_data', False):
    st.header("📊 Tootekataloogi andmed")
    st.markdown("**Kõik tooted kataloogis:**")
    
    # Add some statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tooteid kokku", len(df))
    with col2:
        st.metric("Kategooriaid", len(df['category'].unique()))
    with col3:
        st.metric("Keskmine hind", f"{df['price_eur'].mean():.0f} €")
    with col4:
        st.metric("Kõige kallim", f"{df['price_eur'].max():.0f} €")
    
    # Show the dataframe with options
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "product_id": st.column_config.NumberColumn("ID", width="small"),
            "product_name": st.column_config.TextColumn("Toote nimi", width="medium"),
            "category": st.column_config.SelectboxColumn("Kategooria", options=df['category'].unique()),
            "price_eur": st.column_config.NumberColumn("Hind (€)", format="%.2f €"),
            "power_kw": st.column_config.NumberColumn("Võimsus (kW)", format="%.1f"),
            "energy_class": st.column_config.SelectboxColumn("Energiaklass", options=df['energy_class'].unique()),
            "availability": st.column_config.SelectboxColumn("Saadavus", options=df['availability'].unique()),
            "description": st.column_config.TextColumn("Kirjeldus", width="large")
        }
    )
    
    # Add download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Lae alla CSV failina",
        data=csv,
        file_name="abckliima_tooted.csv",
        mime="text/csv"
    )
    
    st.markdown("---")

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
        response = None
        
        # --- IMPROVED SEARCH LOGIC WITH ESTONIAN VARIATIONS ---
        
        # Price filter: e.g. "tooteid alla 500 euro"
        price_match = re.search(r"alla (\d+)[\s-]*euro", query.lower())
        if price_match:
            price_limit = float(price_match.group(1))
            filtered = df[df['price_eur'] < price_limit]
            if not filtered.empty:
                response = f"Leidsin {len(filtered)} toodet alla {int(price_limit)} euro:\n\n"
                for _, row in filtered.iterrows():
                    response += f"**{row['product_name']}** — {row['price_eur']} €\n"
            else:
                response = f"Alla {int(price_limit)} euro tooteid ei leitud."
        
        # Category filter with Estonian variations
        elif "näita" in query.lower() or "millised" in query.lower():
            # Extract potential category words from query
            query_words = query.lower().split()
            matched_category = None
            
            # Try to find matching category
            for word in query_words:
                if len(word) > 3:  # Only check words longer than 3 characters
                    matched_category = find_matching_category(word, df['category'].unique())
                    if matched_category:
                        break
            
            if matched_category:
                filtered = df[df['category'] == matched_category]
                if not filtered.empty:
                    response = f"Leidsin {len(filtered)} toodet kategooriast '{matched_category}':\n\n"
                    for _, row in filtered.iterrows():
                        response += f"**{row['product_name']}** — {row['price_eur']} €"
                        if pd.notna(row['power_kw']) and row['power_kw'] > 0:
                            response += f" ({row['power_kw']} kW)"
                        if pd.notna(row['energy_class']):
                            response += f" — {row['energy_class']}"
                        response += "\n"
                else:
                    response = f"Kategoorias '{matched_category}' tooteid ei leitud."
            else:
                # Check for specific product types in product names
                for word in query_words:
                    if len(word) > 3:
                        # Search in product names
                        name_matches = df[df['product_name'].str.lower().str.contains(word, na=False)]
                        if not name_matches.empty:
                            response = f"Leidsin {len(name_matches)} toodet, mis sisaldavad '{word}':\n\n"
                            for _, row in name_matches.iterrows():
                                response += f"**{row['product_name']}** — {row['price_eur']} €\n"
                            break
        
        # Energy class filter
        elif "a+++" in query.lower() or "a++" in query.lower() or "a+" in query.lower():
            energy_class = None
            if "a+++" in query.lower():
                energy_class = "A+++"
            elif "a++" in query.lower():
                energy_class = "A++"
            elif "a+" in query.lower():
                energy_class = "A+"
            
            if energy_class:
                filtered = df[df['energy_class'] == energy_class]
                if not filtered.empty:
                    response = f"Leidsin {len(filtered)} {energy_class} energiaklassiga toodet:\n\n"
                    for _, row in filtered.iterrows():
                        response += f"**{row['product_name']}** — {row['price_eur']} €\n"
                else:
                    response = f"{energy_class} energiaklassiga tooteid ei leitud."
        
        # Cheapest products
        elif "odavamad" in query.lower() or "kõige odavam" in query.lower():
            cheapest = df.nsmallest(5, 'price_eur')
            response = "Kõige odavamad tooted:\n\n"
            for _, row in cheapest.iterrows():
                response += f"**{row['product_name']}** — {row['price_eur']} €\n"
        
        # Most powerful products
        elif "võimsamad" in query.lower() or "kõige võimsam" in query.lower():
            powerful = df[df['power_kw'] > 0].nlargest(5, 'power_kw')
            if not powerful.empty:
                response = "Kõige võimsamad tooted:\n\n"
                for _, row in powerful.iterrows():
                    response += f"**{row['product_name']}** — {row['power_kw']} kW — {row['price_eur']} €\n"
            else:
                response = "Võimsusega tooteid ei leitud."
        
        # Otherwise, use the agent
        if not response:
            with st.spinner("Otsin vastust..."):
                try:
                    response = agent.invoke(f"Vasta eesti keeles: {query}")
                except Exception as e:
                    response = f"Vabandust, tekkis viga: {e}"
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# Input placeholder
st.markdown("<div style='color: #888;'>Küsi näiteks: 'Millised on kõige odavamad tooted?'</div>", unsafe_allow_html=True) 