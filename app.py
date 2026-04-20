import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database Path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')

def init_db():
    """Create Database And Table"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL, 
                  category TEXT, 
                  quantity INTEGER, 
                  price REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Show All Item In Dashboard"""
    search_query = request.args.get('search', '')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    if search_query:
        # Name OR Category search by SQL LIKE 
        query = "SELECT * FROM inventory WHERE name LIKE ? OR category LIKE ?"
        c.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        c.execute("SELECT * FROM inventory")
        
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items, last_search=search_query)

@app.route('/add', methods=['POST'])
def add_item():
    """Add New Item"""
    name = request.form['name']
    category = request.form['category']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, category, quantity, price) VALUES (?, ?, ?, ?)",
              (name, category, quantity, price))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_item():
    """Edit Item"""
    item_id = request.form['id']
    name = request.form['name']
    category = request.form['category']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""UPDATE inventory 
                 SET name = ?, category = ?, quantity = ?, price = ? 
                 WHERE id = ?""",
              (name, category, quantity, price, item_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_item(id):
    """Item Delete"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)