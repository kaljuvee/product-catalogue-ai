# ABC Kliima - Tootekataloogi Chat App

A Streamlit-based chat interface for querying ABC Kliima's air conditioning and ventilation equipment catalogue.

## Features

- 💬 Interactive chat interface in Estonian
- 🔍 Product search across all categories
- 📊 Product statistics and filtering
- 💡 Suggested queries for easy navigation
- 🏷️ Category-based filtering
- 💰 Price range filtering
- 📱 Responsive design

## Product Categories

The catalogue includes:
- Õhksoojuspumbad (Air heat pumps)
- Maasoojuspumbad (Ground heat pumps)
- Õhk-vesisoojuspumbad (Air-water heat pumps)
- Ventilatsioonisoojuspumbad (Ventilation heat pumps)
- Konditsioneerid (Air conditioners)
- Ventilatsioon (Ventilation)
- Kesktolmuimejad (Central vacuum cleaners)
- Päikesepaneelid (Solar panels)
- Küttejaotus (Heating distribution)
- Veeboilerid (Water boilers)
- Akumulatsioonipaagid (Accumulation tanks)
- Elektrikatlad, küttekehad (Electric boilers, heaters)
- Õhkkardinad (Air curtains)
- Õhukuivatid (Air dryers)
- Paigaldustarvikud (Installation accessories)
- Keemiakaubad (Chemical products)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd product-catalogue-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## Usage

1. **Chat Interface**: Type your questions in Estonian about products
2. **Quick Filters**: Use the sidebar to filter by price range or category
3. **Suggestions**: Click on suggested queries for quick access
4. **Product Details**: View detailed information including prices, power, energy class, and availability

## Example Queries

- "Näita kõiki õhksoojuspumpasid"
- "Millised on kõige odavamad tooted?"
- "Näita A+++ energiaklassiga tooteid"
- "Millised on saadaval maasoojuspumbad?"
- "Näita tooteid alla 500 euro"

## Data Structure

The app uses a CSV file (`products.csv`) with the following columns:
- `product_id`: Unique product identifier
- `product_name`: Product name in Estonian
- `category`: Product category
- `price_eur`: Price in euros
- `power_kw`: Power in kilowatts (if applicable)
- `energy_class`: Energy efficiency class
- `availability`: Stock availability
- `description`: Product description in Estonian

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Python**: Programming language

## Company Information

**ABC Kliima** - Your trusted partner in air conditioning and ventilation solutions
- 📞 +372 1234 5678
- 📧 info@abckliima.ee
- 🌐 www.abckliima.ee