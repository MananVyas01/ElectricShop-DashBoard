import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import ElectricShopDB
from datetime import datetime

# Initialize database
db = ElectricShopDB()

# Page config
st.set_page_config(
    page_title="Electric Shop Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Power BI-like styling with improved visibility
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
        padding: 2rem;
        color: #2c3e50;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        color: white;
    }
    .css-1d391kg .stRadio>label {
        color: white;
    }
    .css-1d391kg .stMarkdown h3 {
        color: white;
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #0056b3 0%, #003d82 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Title styling */
    h1, h2, h3 {
        color:rgb(0, 0, 0);
        font-weight: 700;
        background: linear-gradient(90deg, #2c3e50 0%, #3498db 100%);
        -webkit-background-clip: text;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        color: #2c3e50;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Form styling */
    .stForm {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        padding: 12px;
        color: #2c3e50;
        background-color: white;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
    }
    
    .stTextInput>label,
    .stNumberInput>label,
    .stSelectbox>label {
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.75rem;
        display: block;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Success alert */
    .element-container .stAlert[data-baseweb="notification"] {
        background: linear-gradient(145deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
    }
    
    /* Error alert */
    .element-container .stAlert[data-baseweb="notification"].stAlert-error {
        background: linear-gradient(145deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
    }
    
    /* Warning alert */
    .element-container .stAlert[data-baseweb="notification"].stAlert-warning {
        background: linear-gradient(145deg, #fff3cd 0%, #ffeeba 100%);
        border-left: 4px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.title("⚡ Electric Shop")
    st.markdown("---")
    page = st.radio("Navigation", ["Dashboard", "Add Product", "Manage Stock", "Inventory"])
    st.markdown("---")
    st.markdown("### Quick Stats")
    products = db.get_all_products()
    if products:
        df = pd.DataFrame(products, columns=['Product Code', 'Product Name', 'Category', 'Price', 'Stock', 'Last Updated'])
        st.metric("Total Products", len(df))
        st.metric("Total Value", f"${df['Price'].mul(df['Stock']).sum():,.2f}")
    
    st.markdown("---")
    st.markdown("### Demo Data")
    if st.button("Load Sample Data"):
        if db.add_sample_data():
            st.success("Sample data loaded successfully!")
            st.experimental_rerun()
        else:
            st.error("Failed to load sample data.")

# Dashboard Page
if page == "Dashboard":
    st.title("📊 Electric Shop Analytics")
    
    products = db.get_all_products() # Fetch products again for this page
    if products:
        df = pd.DataFrame(products, columns=['Product Code', 'Product Name', 'Category', 'Price', 'Stock', 'Last Updated'])
        
        # Add date range filter
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            date_range = st.date_input(
                "Select Date Range",
                value=(datetime.now().date(), datetime.now().date()),
                max_value=datetime.now().date()
            )
        with col2:
            category_filter = st.multiselect(
                "Filter by Category",
                options=df['Category'].unique(),
                default=df['Category'].unique()
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filter data based on selections
        filtered_df = df[df['Category'].isin(category_filter)]
        
        # Top metrics in a row with improved styling
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            total_products = len(filtered_df)
            in_stock = len(filtered_df[filtered_df['Stock'] > 0])
            st.metric("Total Products", total_products, f"{in_stock} in stock")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            total_value = filtered_df['Price'].mul(filtered_df['Stock']).sum()
            st.metric("Total Value", f"${total_value:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            low_stock = len(filtered_df[filtered_df['Stock'] < 10])
            st.metric("Low Stock Items", low_stock, "Need attention" if low_stock > 0 else "All good")
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            categories = filtered_df['Category'].nunique()
            st.metric("Categories", categories)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Charts in a grid layout with improved interactivity
        st.markdown("### 📈 Analytics Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            # Stock by Category (Pie Chart) with improved interactivity
            fig = px.pie(filtered_df, names='Category', values='Stock', 
                        title='Stock Distribution by Category',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4)  # Make it a donut chart
            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Price Distribution (Box Plot) with improved styling
            fig = px.box(filtered_df, x='Category', y='Price',
                        title='Price Distribution by Category',
                        color='Category',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(
                showlegend=False,
                xaxis_title="Category",
                yaxis_title="Price ($)",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Stock Value by Category (Bar Chart) with improved interactivity
            filtered_df['Stock Value'] = filtered_df['Price'] * filtered_df['Stock']
            fig = px.bar(filtered_df.groupby('Category')['Stock Value'].sum().reset_index(),
                        x='Category', y='Stock Value',
                        title='Total Stock Value by Category',
                        color='Category',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(
                showlegend=False,
                xaxis_title="Category",
                yaxis_title="Stock Value ($)",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Stock Level Gauge with improved styling
            total_stock = filtered_df['Stock'].sum()
            max_stock = filtered_df['Stock'].max() * len(filtered_df) if not filtered_df.empty else 100
            if max_stock == 0: max_stock = 100
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=total_stock,
                title={'text': "Total Stock Level", 'font': {'size': 24}},
                delta={'reference': max_stock * 0.7, 'relative': True},
                gauge={
                    'axis': {'range': [0, max_stock]},
                    'bar': {'color': "#3498db"},
                    'steps': [
                        {'range': [0, max_stock*0.3], 'color': "#e74c3c"},
                        {'range': [max_stock*0.3, max_stock*0.7], 'color': "#f39c12"},
                        {'range': [max_stock*0.7, max_stock], 'color': "#2ecc71"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_stock * 0.7
                    }
                }
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Low Stock Alert Section with improved styling
        st.markdown("### ⚠️ Low Stock Alerts")
        low_stock = filtered_df[filtered_df['Stock'] < 10]
        if not low_stock.empty:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            # Add color coding for stock levels
            def color_stock(val):
                color = 'red' if val < 5 else 'orange'
                return f'color: {color}'
            
            styled_df = low_stock[['Product Code', 'Product Name', 'Category', 'Stock', 'Price']].style.applymap(
                color_stock, subset=['Stock']
            )
            st.dataframe(styled_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("No low stock items!")
    else:
        st.info("No products in inventory yet. Add products using the 'Add Product' tab.")

# Add Product Page
elif page == "Add Product":
    st.title("➕ Add New Product")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_code = st.text_input("Product Code", placeholder="Enter unique product code (e.g., ELE-001)")
            product_name = st.text_input("Product Name", placeholder="Enter product name (e.g., LED Bulb 60W)")
            category = st.selectbox("Category", ["Lighting", "Power Tools", "Cables", "Switches", "Other"])
        with col2:
            price = st.number_input("Price ($)", min_value=0.0, step=0.01, placeholder="Enter price (e.g., 5.99)")
            stock_quantity = st.number_input("Initial Stock", min_value=0, step=1, placeholder="Enter initial stock quantity (e.g., 100)")
        
        submitted = st.form_submit_button("Add Product")
        if submitted:
            if product_code and product_name and price >= 0 and stock_quantity >= 0:
                if db.add_product(product_code, product_name, category, price, stock_quantity):
                    st.success(f"Product '{product_name}' added successfully!")
                    # Clear form fields (requires re-running app, not directly supported in Streamlit forms)
                    # A workaround would be to use st.session_state, but let\'s keep it simple for now.
                else:
                    st.error(f"Product code '{product_code}' already exists! Please use a unique code.")
            else:
                st.error("Please fill all required fields correctly! Price and Stock must be non-negative.")
    st.markdown('</div>', unsafe_allow_html=True)

# Manage Stock Page
elif page == "Manage Stock":
    st.title("📦 Stock Management")
    
    products = db.get_all_products()
    if products:
        df = pd.DataFrame(products, columns=['Product Code', 'Product Name', 'Category', 'Price', 'Stock', 'Last Updated'])
        
        # Create tabs for different sections
        tab1, tab2 = st.tabs(["Update Stock", "Sales History"])
        
        with tab1:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                with st.form("update_stock_form"):
                    product_codes = df['Product Code'].tolist()
                    display_codes = ["Select a product"] + product_codes
                    selected_product_code_display = st.selectbox("Select Product", display_codes)
                    
                    if selected_product_code_display != "Select a product":
                        selected_product_code = selected_product_code_display
                        product_info = df[df['Product Code'] == selected_product_code].iloc[0]
                        
                        # Display product details in a nice format
                        st.markdown("### Product Details")
                        st.markdown(f"""
                            - **Name:** {product_info['Product Name']}
                            - **Category:** {product_info['Category']}
                            - **Price:** ${product_info['Price']:.2f}
                            - **Current Stock:** {product_info['Stock']} units
                        """)
                        
                        st.markdown("### Update Stock")
                        col1, col2 = st.columns(2)
                        with col1:
                            add_stock = st.number_input("Add Stock", min_value=0, step=1, placeholder="Enter quantity to add")
                        with col2:
                            remove_stock = st.number_input("Remove Stock", min_value=0, step=1, placeholder="Enter quantity to remove")
                        
                        submitted = st.form_submit_button("Update Stock")
                        if submitted:
                            if add_stock > 0 or remove_stock > 0:
                                quantity_change = add_stock - remove_stock
                                if db.update_stock(selected_product_code, quantity_change):
                                    # If removing stock, record it as a sale
                                    if remove_stock > 0:
                                        total_price = remove_stock * product_info['Price']
                                        db.record_sale(selected_product_code, remove_stock, total_price)
                                    st.success(f"Stock for '{selected_product_code}' updated successfully!")
                                else:
                                    st.error(f"Failed to update stock for '{selected_product_code}'! Not enough stock available.")
                            else:
                                st.warning("Please enter a quantity to add or remove.")
                    else:
                        st.info("Please select a product first.")
                        if st.form_submit_button("Update Stock"):
                            st.warning("Please select a product first.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Current Stock Levels")
                updated_products = db.get_all_products()
                if updated_products:
                    updated_df = pd.DataFrame(updated_products, columns=['Product Code', 'Product Name', 'Category', 'Price', 'Stock', 'Last Updated'])
                    st.dataframe(updated_df[['Product Code', 'Product Name', 'Category', 'Stock', 'Last Updated']],
                                use_container_width=True)
                else:
                    st.info("No products available.")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Sales History")
            
            # Get sales history
            sales_history = db.get_sales_history()
            if sales_history:
                sales_df = pd.DataFrame(sales_history, 
                    columns=['ID', 'Product Code', 'Quantity', 'Total Price', 'Sale Date', 'Product Name', 'Category'])
                
                # Display sales summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Sales", len(sales_df))
                with col2:
                    st.metric("Total Revenue", f"${sales_df['Total Price'].sum():,.2f}")
                with col3:
                    st.metric("Total Items Sold", sales_df['Quantity'].sum())
                
                # Display recent sales
                st.markdown("### Recent Sales")
                st.dataframe(sales_df[['Product Name', 'Category', 'Quantity', 'Total Price', 'Sale Date']],
                            use_container_width=True)
                
                # Display sales summary by product
                st.markdown("### Sales Summary by Product")
                sales_summary = db.get_sales_summary()
                if sales_summary:
                    summary_df = pd.DataFrame(sales_summary,
                        columns=['Product Code', 'Product Name', 'Category', 'Total Sales', 'Total Quantity', 'Total Revenue'])
                    st.dataframe(summary_df, use_container_width=True)
            else:
                st.info("No sales history available yet.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No products in inventory yet. Add products using the 'Add Product' tab before managing stock.")

# Inventory Page
elif page == "Inventory":
    st.title("📋 Inventory Management")
    
    products = db.get_all_products() # Fetch products again for this page
    if products:
        df = pd.DataFrame(products, columns=['Product Code', 'Product Name', 'Category', 'Price', 'Stock', 'Last Updated'])
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # Search and filter
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Search by Product Code or Name", placeholder="Type to search product code or name...")
        with col2:
            category_filter = st.multiselect("Filter by Category", df['Category'].unique(), placeholder="Select categories to filter...")
        
        # Apply filters
        filtered_df = df.copy()
        if search:
            filtered_df = filtered_df[filtered_df['Product Code'].str.contains(search, case=False) | 
                                      filtered_df['Product Name'].str.contains(search, case=False)]
        if category_filter:
            filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]
        
        # Display inventory with enhanced styling
        st.dataframe(filtered_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Delete product section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🗑️ Delete Product")
        
        product_codes = df['Product Code'].tolist()
        if product_codes:
            with st.form("delete_product_form"):
                product_to_delete = st.selectbox("Select Product to Delete", product_codes)
                if st.form_submit_button("Delete Product"):
                    if db.delete_product(product_to_delete):
                        st.success(f"Product '{product_to_delete}' deleted successfully!")
                        # st.experimental_rerun() # Rerun to update the table immediately
                    else:
                        st.error(f"Failed to delete product '{product_to_delete}'!")
        else:
            st.info("No products available to delete.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No products in inventory yet.") 