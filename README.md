# Electric Shop Dashboard

A professional dashboard for managing an electric shop's inventory, built with Python and Streamlit.

## Features

- 📊 Interactive dashboard with key metrics and visualizations
- ➕ Add new products with unique product codes
- 📦 Manage stock levels (add/remove items)
- 🔍 Search and filter inventory
- ⚠️ Low stock alerts
- 📈 Stock value tracking
- 🗑️ Product deletion capability

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Usage

The dashboard has four main sections:

1. **Dashboard**: View key metrics, charts, and low stock alerts
2. **Add Product**: Add new products to the inventory
3. **Manage Stock**: Update stock levels for existing products
4. **Inventory**: View, search, and manage all products

## Database

The application uses SQLite for data storage. The database file (`electric_shop.db`) will be created automatically when you first run the application.

## Product Categories

- Lighting
- Power Tools
- Cables
- Switches
- Other

## Note

Make sure to keep your product codes unique when adding new products to the inventory. 