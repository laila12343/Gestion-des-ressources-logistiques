def get_product_returns():
    conn = sqlite3.connect('store_analysis.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.name, r.reason, r.condition, r.action, r.return_date
    FROM returns r
    JOIN sales s ON r.sale_id = s.sale_id
    JOIN products p ON s.product_id = p.product_id
    """)
    returns = cursor.fetchall()
    conn.close()

    return returns