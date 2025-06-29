import streamlit as st

def show_documentation():
    st.title("📚 ABC Kliima - Tootekataloogi Chat App Dokumentatsioon")
    
    st.markdown("""
    A Streamlit-based chat interface for querying ABC Kliima's air conditioning and ventilation equipment catalogue.
    """)
    
    # Features Section
    st.header("🚀 Funktsioonid")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - 💬 Interactive chat interface in Estonian
        - 🔍 Product search across all categories
        - 📊 Product statistics and filtering
        - 💡 Suggested queries for easy navigation
        """)
    
    with col2:
        st.markdown("""
        - 🏷️ Category-based filtering
        - 💰 Price range filtering
        - 📱 Responsive design
        """)
    
    # Product Categories Section
    st.header("📦 Tootekategooriad")
    st.markdown("The catalogue includes:")
    
    categories = [
        "Õhksoojuspumbad (Air heat pumps)",
        "Maasoojuspumbad (Ground heat pumps)",
        "Õhk-vesisoojuspumbad (Air-water heat pumps)",
        "Ventilatsioonisoojuspumbad (Ventilation heat pumps)",
        "Konditsioneerid (Air conditioners)",
        "Ventilatsioon (Ventilation)",
        "Kesktolmuimejad (Central vacuum cleaners)",
        "Päikesepaneelid (Solar panels)",
        "Küttejaotus (Heating distribution)",
        "Veeboilerid (Water boilers)",
        "Akumulatsioonipaagid (Accumulation tanks)",
        "Elektrikatlad, küttekehad (Electric boilers, heaters)",
        "Õhkkardinad (Air curtains)",
        "Õhukuivatid (Air dryers)",
        "Paigaldustarvikud (Installation accessories)",
        "Keemiakaubad (Chemical products)"
    ]
    
    for category in categories:
        st.markdown(f"- {category}")
    
    # Installation Section
    st.header("⚙️ Installatsioon")
    
    st.markdown("1. Clone this repository:")
    st.code("""
git clone <repository-url>
cd product-catalogue-ai
    """, language="bash")
    
    st.markdown("2. Install dependencies:")
    st.code("pip install -r requirements.txt", language="bash")
    
    st.markdown("3. Run the Streamlit app:")
    st.code("streamlit run app.py", language="bash")
    
    st.markdown("4. Open your browser and navigate to `http://localhost:8501`")
    
    # Usage Section
    st.header("📖 Kasutamine")
    
    usage_points = [
        "**Chat Interface**: Type your questions in Estonian about products",
        "**Quick Filters**: Use the sidebar to filter by price range or category",
        "**Suggestions**: Click on suggested queries for quick access",
        "**Product Details**: View detailed information including prices, power, energy class, and availability"
    ]
    
    for point in usage_points:
        st.markdown(f"- {point}")
    
    # Example Queries Section
    st.header("💡 Näidisküsimused")
    
    example_queries = [
        "Näita kõiki õhksoojuspumpasid",
        "Millised on kõige odavamad tooted?",
        "Näita A+++ energiaklassiga tooteid",
        "Millised on saadaval maasoojuspumbad?",
        "Näita tooteid alla 500 euro"
    ]
    
    for query in example_queries:
        st.markdown(f"- \"{query}\"")
    
    # Data Structure Section
    st.header("🗄️ Andmestruktuur")
    st.markdown("The app uses a CSV file (`products.csv`) with the following columns:")
    
    data_columns = [
        "`product_id`: Unique product identifier",
        "`product_name`: Product name in Estonian",
        "`category`: Product category",
        "`price_eur`: Price in euros",
        "`power_kw`: Power in kilowatts (if applicable)",
        "`energy_class`: Energy efficiency class",
        "`availability`: Stock availability",
        "`description`: Product description in Estonian"
    ]
    
    for column in data_columns:
        st.markdown(f"- {column}")
    
    # Technologies Section
    st.header("🛠️ Kasutatud tehnoloogiad")
    
    tech_stack = [
        "**Streamlit**: Web application framework",
        "**Pandas**: Data manipulation and analysis",
        "**Python**: Programming language"
    ]
    
    for tech in tech_stack:
        st.markdown(f"- {tech}")
    
    # Company Information Section
    st.header("🏢 Ettevõtte teave")
    
    st.markdown("**ABC Kliima** - Your trusted partner in air conditioning and ventilation solutions")
    
    contact_info = [
        "📞 +372 1234 5678",
        "📧 info@abckliima.ee",
        "🌐 www.abckliima.ee"
    ]
    
    for contact in contact_info:
        st.markdown(f"- {contact}")

if __name__ == "__main__":
    show_documentation()
