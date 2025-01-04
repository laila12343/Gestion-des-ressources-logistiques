import sqlite3
import matplotlib.pyplot as plt

def get_top_selling_products():
    conn = sqlite3.connect('db/store_analysis.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.name, SUM(s.quantity) AS total_sales
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.name
    ORDER BY total_sales DESC
    LIMIT 5
    """)
    top_products = cursor.fetchall()
    conn.close()
    return top_products

def generate_sales_graph(sales_data):
    dates = [item[0] for item in sales_data]
    sales = [item[1] for item in sales_data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, sales, marker='o', color='b')
    plt.title("Ventes par jour")
    plt.xlabel("Date")
    plt.ylabel("Quantité vendue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()