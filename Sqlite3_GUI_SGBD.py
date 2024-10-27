"""Anass El Amrany | group 1 IDAA"""

import re
from datetime import datetime
import sqlite3
import csv
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox

# Database creation
def create_database():
    conn = sqlite3.connect('ventes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ventes_clean (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date DATE,
                Product TEXT,
                Price REAL,
                Quantity INTEGER,
                Region TEXT
            )''')
    conn.commit()
    conn.close()
    messagebox.showinfo("Information", "Database created successfully")

# Add entry
def add_entry():
    if not verify_fields():
        return
    conn = sqlite3.connect('ventes.db')
    c = conn.cursor()
    c.execute("INSERT INTO ventes_clean (Date, Product, Price, Quantity, Region) VALUES (?, ?, ?, ?, ?)",
              (entry_date.get(), entry_produit.get(), entry_prix.get(), entry_quantite.get(), entry_region.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Information", "Data added successfully")
    clear_entries()
    load_data()

# Field verification
def verify_fields():
    if not all([entry_date.get(), entry_produit.get(), entry_prix.get(), entry_quantite.get(), entry_region.get()]):
        messagebox.showerror("Error", "All fields must be filled")
        return False

    try:
        float(entry_prix.get())
    except ValueError:
        messagebox.showerror("Error", "Price must be a real number")
        return False

    try:
        int(entry_quantite.get())
    except ValueError:
        messagebox.showerror("Error", "Quantity must be an integer")
        return False

    try:
        datetime.strptime(entry_date.get(), "%d-%m-%Y")
    except ValueError:
        messagebox.showerror("Error", "Date must be in DD-MM-YYYY format")
        return False

    if not re.match("^[A-Za-z ]+$", entry_produit.get()):
        messagebox.showerror("Error", "Product name should not contain numbers")
        return False

    if not re.match("^[A-Za-z ]+$", entry_region.get()):
        messagebox.showerror("Error", "Region should not contain numbers")
        return False

    return True

# Load data from database
def load_data():
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect('ventes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ventes_clean")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        tree.insert('', 'end', values=row)

# Delete entry
def delete_entry():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No entry selected")
        return
    item_id = tree.item(selected_item, 'values')[0]
    conn = sqlite3.connect('ventes.db')
    c = conn.cursor()
    c.execute("DELETE FROM ventes_clean WHERE ID=?", (item_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Information", "Data deleted successfully")
    load_data()

# Select item for editing
def select_item(event):
    try:
        selected_item = tree.selection()[0]
        item = tree.item(selected_item, 'values')
        clear_entries()
        entry_date.insert(tk.END, item[1])
        entry_produit.insert(tk.END, item[2])
        entry_prix.insert(tk.END, item[3])
        entry_quantite.insert(tk.END, item[4])
        entry_region.insert(tk.END, item[5])
    except IndexError:
        pass

# Update entry
def update_entry():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No entry selected")
        return
    item_id = tree.item(selected_item, 'values')[0]
    conn = sqlite3.connect('ventes.db')
    c = conn.cursor()
    c.execute("UPDATE ventes_clean SET Date=?, Product=?, Price=?, Quantity=?, Region=? WHERE ID=?",
              (entry_date.get(), entry_produit.get(), entry_prix.get(), entry_quantite.get(), entry_region.get(), item_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Information", "Data updated successfully")
    load_data()

# Export data to CSV
def export_data():
    conn = sqlite3.connect('ventes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ventes_clean")
    rows = c.fetchall()
    conn.close()

    with open('ventes_export.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Date', 'Product', 'Price', 'Quantity', 'Region'])
        writer.writerows(rows)
    messagebox.showinfo("Information", "Data exported successfully to ventes_export.csv")

# Clear entries
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_produit.delete(0, tk.END)
    entry_prix.delete(0, tk.END)
    entry_quantite.delete(0, tk.END)
    entry_region.delete(0, tk.END)


# GUI setup
root = tk.Tk()
style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

root.title("Sales Management")

# Main frame
frame = ttk.Frame(root)
frame.pack(padx=20, pady=10)

# Widgets frame
widgets_frame = ttk.LabelFrame(frame, text="Insert Row")
widgets_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Treeview frame
treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

# Scrollbar for the Treeview
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

# Treeview widget with columns and headings
cols = ('ID', 'Date', 'Product', 'Price', 'Quantity', 'Region')
tree = ttk.Treeview(treeFrame, show='headings', yscrollcommand=treeScroll.set, columns=cols, height=13)
tree.heading('ID', text='ID')
tree.heading('Date', text='Date')
tree.heading('Product', text='Product')
tree.heading('Price', text='Price')
tree.heading('Quantity', text='Quantity')
tree.heading('Region', text='Region')

# Set column widths
tree.column('ID', width=50)
tree.column('Date', width=100)
tree.column('Product', width=150)
tree.column('Price', width=100)
tree.column('Quantity', width=80)
tree.column('Region', width=100)

tree.pack(side='left', fill='both', expand=True)
treeScroll.config(command=tree.yview)

# Labels and entry fields using grid
date_label = ttk.Label(widgets_frame, text="Date (DD-MM-YYYY) : ")
date_label.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
entry_date = ttk.Entry(widgets_frame)  
entry_date.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))

product_label = ttk.Label(widgets_frame, text="Product : ")
product_label.grid(row=2, column=0, sticky="ew", padx=5, pady=(5, 0))
entry_produit = ttk.Entry(widgets_frame)
entry_produit.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 5))

price_label = ttk.Label(widgets_frame, text="Price : ")
price_label.grid(row=4, column=0, sticky="ew", padx=5, pady=(5, 0))
entry_prix = ttk.Entry(widgets_frame)
entry_prix.grid(row=5, column=0, sticky="ew", padx=5, pady=(0, 5))

qte_label = ttk.Label(widgets_frame, text="Quantity : ")
qte_label.grid(row=6, column=0, sticky="ew", padx=5, pady=(5, 0))
entry_quantite = ttk.Entry(widgets_frame)
entry_quantite.grid(row=7, column=0, sticky="ew", padx=5, pady=(0, 5))

region_label = ttk.Label(widgets_frame, text="Region :")
region_label.grid(row=8, column=0, sticky="ew", padx=5, pady=(5, 0))
entry_region = ttk.Entry(widgets_frame)
entry_region.grid(row=9, column=0, sticky="ew", padx=5, pady=(0, 5))

# Buttons frame
buttons_frame = ttk.LabelFrame(frame, text="Click button")
buttons_frame.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

# Buttons using grid
btn_create_db = ttk.Button(buttons_frame, text="Create Database", command=create_database)
btn_create_db.grid(row=0, column=1, padx=10, pady=10)

btn_add = ttk.Button(buttons_frame, text="Add", command=add_entry)
btn_add.grid(row=0, column=2, padx=10, pady=10)

btn_update = ttk.Button(buttons_frame, text="Update", command=update_entry)
btn_update.grid(row=0, column=3, padx=10, pady=10)

btn_delete = ttk.Button(buttons_frame, text="Delete", command=delete_entry)
btn_delete.grid(row=0, column=4, padx=10, pady=10)

btn_clear = ttk.Button(buttons_frame, text="Clear", command=clear_entries)
btn_clear.grid(row=0, column=5, padx=10, pady=10)

btn_export = ttk.Button(buttons_frame, text="Export to CSV", command=export_data)
btn_export.grid(row=0, column=6, columnspan=4, padx=10, pady=10)

# Load data initially
load_data()
root.mainloop()