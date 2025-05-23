import sqlite3
from datetime import datetime

class ElectricShopDB:
    def __init__(self):
        self.conn = sqlite3.connect('electric_shop.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_code TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock_quantity INTEGER NOT NULL,
                last_updated TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                sale_date TIMESTAMP,
                FOREIGN KEY (product_code) REFERENCES products(product_code)
            )
        ''')
        self.conn.commit()
    
    def add_product(self, product_code, product_name, category, price, stock_quantity):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (product_code, product_name, category, price, stock_quantity, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_code, product_name, category, price, stock_quantity, datetime.now()))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_stock(self, product_code, quantity_change):
        cursor = self.conn.cursor()
        # First check if we have enough stock for negative changes
        if quantity_change < 0:
            cursor.execute('SELECT stock_quantity FROM products WHERE product_code = ?', (product_code,))
            current_stock = cursor.fetchone()[0]
            if current_stock + quantity_change < 0:
                return False  # Not enough stock
        
        cursor.execute('''
            UPDATE products 
            SET stock_quantity = stock_quantity + ?,
                last_updated = ?
            WHERE product_code = ?
        ''', (quantity_change, datetime.now(), product_code))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_product(self, product_code):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_code = ?', (product_code,))
        return cursor.fetchone()
    
    def get_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products')
        return cursor.fetchall()
    
    def delete_product(self, product_code):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM products WHERE product_code = ?', (product_code,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_low_stock_products(self, threshold=10):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE stock_quantity < ?', (threshold,))
        return cursor.fetchall()
    
    def record_sale(self, product_code, quantity, total_price):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO sales_history (product_code, quantity, total_price, sale_date)
                VALUES (?, ?, ?, ?)
            ''', (product_code, quantity, total_price, datetime.now()))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False
    
    def get_sales_history(self, limit=50):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT s.*, p.product_name, p.category
            FROM sales_history s
            JOIN products p ON s.product_code = p.product_code
            ORDER BY s.sale_date DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def get_sales_summary(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                p.product_code,
                p.product_name,
                p.category,
                COUNT(s.id) as total_sales,
                SUM(s.quantity) as total_quantity,
                SUM(s.total_price) as total_revenue
            FROM products p
            LEFT JOIN sales_history s ON p.product_code = s.product_code
            GROUP BY p.product_code
            ORDER BY total_revenue DESC
        ''')
        return cursor.fetchall()
    
    def add_sample_data(self):
        # Sample products
        sample_products = [
            ("ELE-001", "LED Bulb 60W", "Lighting", 4.99, 150),
            ("ELE-002", "LED Bulb 100W", "Lighting", 6.99, 120),
            ("ELE-003", "Power Drill 800W", "Power Tools", 89.99, 25),
            ("ELE-004", "Circular Saw", "Power Tools", 129.99, 15),
            ("ELE-005", "HDMI Cable 2m", "Cables", 12.99, 200),
            ("ELE-006", "USB-C Cable 1m", "Cables", 8.99, 300),
            ("ELE-007", "Smart Switch", "Switches", 24.99, 80),
            ("ELE-008", "Dimmer Switch", "Switches", 19.99, 60),
            ("ELE-009", "Extension Cord 5m", "Other", 15.99, 100),
            ("ELE-010", "Power Strip 6 Outlets", "Other", 29.99, 75)
        ]
        
        # Add products
        cursor = self.conn.cursor()
        for product in sample_products:
            try:
                cursor.execute('''
                    INSERT INTO products (product_code, product_name, category, price, stock_quantity, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (*product, datetime.now()))
            except sqlite3.IntegrityError:
                continue  # Skip if product already exists
        
        # Sample sales history
        from datetime import timedelta
        import random
        
        # Generate sales for the last 30 days
        for _ in range(100):  # Generate 100 sales
            product = random.choice(sample_products)
            quantity = random.randint(1, 5)
            total_price = quantity * product[3]
            sale_date = datetime.now() - timedelta(days=random.randint(0, 30))
            
            cursor.execute('''
                INSERT INTO sales_history (product_code, quantity, total_price, sale_date)
                VALUES (?, ?, ?, ?)
            ''', (product[0], quantity, total_price, sale_date))
        
        self.conn.commit()
        return True
    
    def __del__(self):
        self.conn.close() 