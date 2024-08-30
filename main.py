import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy.orm import sessionmaker
import sys
import os
import datetime

# Add the project root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from models import engine, ItemInventory, CustomerContact, SalesOrder, PurchaseOrder, SalesOrderItem, PurchaseOrderItem
from data_import import import_all_data
from config.config import DATABASE_URI
from pdf_generator import generate_pdf

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

class MRPERPApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MRP/ERP Application")
        self.master.geometry("1024x768")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.inventory_tab = ttk.Frame(self.notebook)
        self.customers_tab = ttk.Frame(self.notebook)
        self.sales_tab = ttk.Frame(self.notebook)
        self.purchasing_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)
        self.query_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.inventory_tab, text="Inventory")
        self.notebook.add(self.customers_tab, text="Customers")
        self.notebook.add(self.sales_tab, text="Sales")
        self.notebook.add(self.purchasing_tab, text="Purchasing")
        self.notebook.add(self.reports_tab, text="Reports")
        self.notebook.add(self.query_tab, text="Query")

        # Set up tabs
        self.setup_inventory_tab()
        self.setup_customers_tab()
        self.setup_sales_tab()
        self.setup_purchasing_tab()
        self.setup_reports_tab()
        self.setup_query_tab()

        # Add a menu bar
        self.setup_menu()

    def setup_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

    def import_data(self):
        import_all_data()
        messagebox.showinfo("Import Complete", "All data has been imported successfully.")
        self.refresh_all_data()

    def refresh_all_data(self):
        self.refresh_inventory()
        self.refresh_customers()
        self.refresh_sales()
        self.refresh_purchasing()

    def setup_inventory_tab(self):
        # Create a treeview to display inventory data
        self.inventory_tree = ttk.Treeview(self.inventory_tab, columns=("Item Number", "Description", "In Stock", "Last Purchase Price"), show="headings")
        self.inventory_tree.heading("Item Number", text="Item Number")
        self.inventory_tree.heading("Description", text="Description")
        self.inventory_tree.heading("In Stock", text="In Stock")
        self.inventory_tree.heading("Last Purchase Price", text="Last Purchase Price")
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons
        button_frame = ttk.Frame(self.inventory_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Refresh", command=self.refresh_inventory).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Item", command=self.add_inventory_item).pack(side=tk.LEFT, padx=5)

    def setup_customers_tab(self):
        # Create a treeview to display customer data
        self.customer_tree = ttk.Treeview(self.customers_tab, columns=("BP Code", "Contact Name", "Title", "Telephone"), show="headings")
        self.customer_tree.heading("BP Code", text="BP Code")
        self.customer_tree.heading("Contact Name", text="Contact Name")
        self.customer_tree.heading("Title", text="Title")
        self.customer_tree.heading("Telephone", text="Telephone")
        self.customer_tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons
        button_frame = ttk.Frame(self.customers_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Refresh", command=self.refresh_customers).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Customer", command=self.add_customer).pack(side=tk.LEFT, padx=5)

    def setup_sales_tab(self):
        # Create a treeview to display sales order data
        self.sales_tree = ttk.Treeview(self.sales_tab, columns=("Order Number", "Customer", "Status", "Total", "Order Date", "Due Date"), show="headings")
        self.sales_tree.heading("Order Number", text="Order Number")
        self.sales_tree.heading("Customer", text="Customer")
        self.sales_tree.heading("Status", text="Status")
        self.sales_tree.heading("Total", text="Total")
        self.sales_tree.heading("Order Date", text="Order Date")
        self.sales_tree.heading("Due Date", text="Due Date")
        self.sales_tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons
        button_frame = ttk.Frame(self.sales_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Refresh", command=self.refresh_sales).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="New Sale", command=self.create_new_sale).pack(side=tk.LEFT, padx=5)

    def setup_purchasing_tab(self):
        # Create a treeview to display purchase order data
        self.purchase_tree = ttk.Treeview(self.purchasing_tab, columns=("Order Number", "Supplier", "Status", "Total", "Order Date"), show="headings")
        self.purchase_tree.heading("Order Number", text="Order Number")
        self.purchase_tree.heading("Supplier", text="Supplier")
        self.purchase_tree.heading("Status", text="Status")
        self.purchase_tree.heading("Total", text="Total")
        self.purchase_tree.heading("Order Date", text="Order Date")
        self.purchase_tree.pack(fill=tk.BOTH, expand=True)

        # Add buttons
        button_frame = ttk.Frame(self.purchasing_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Refresh", command=self.refresh_purchasing).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="New Purchase Order", command=self.create_new_purchase_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Confirm Receipt", command=self.confirm_purchase_receipt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export PDF", command=self.export_purchase_order_pdf).pack(side=tk.LEFT, padx=5)

    def setup_reports_tab(self):
        report_buttons = [
            ("Inventory Report", self.generate_inventory_report),
            ("Sales Report", self.generate_sales_report),
            ("Reorder Report", self.generate_reorder_report),
            ("Low Stock Items", self.view_low_stock_items),
            ("Top 10 Customers", self.view_top_customers),
            ("Monthly Sales", self.view_monthly_sales)
        ]

        for text, command in report_buttons:
            ttk.Button(self.reports_tab, text=text, command=command).pack(pady=5)

    def setup_query_tab(self):
        # Create a text widget for SQL input
        self.query_input = tk.Text(self.query_tab, height=10)
        self.query_input.pack(fill=tk.X, padx=5, pady=5)

        # Add an execute button
        ttk.Button(self.query_tab, text="Execute Query", command=self.execute_query).pack(pady=5)

        # Create a treeview for query results
        self.query_tree = ttk.Treeview(self.query_tab)
        self.query_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def refresh_inventory(self):
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)
        
        inventory_data = session.query(ItemInventory).all()
        for item in inventory_data:
            self.inventory_tree.insert("", "end", values=(item.item_number, item.description, item.in_stock, item.last_purchase_price))

    def refresh_customers(self):
        for i in self.customer_tree.get_children():
            self.customer_tree.delete(i)
        
        customer_data = session.query(CustomerContact).all()
        for customer in customer_data:
            self.customer_tree.insert("", "end", values=(customer.bp_code, customer.contact_name, customer.title, customer.telephone))

    def refresh_sales(self):
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)
        
        sales_data = session.query(SalesOrder).all()
        for order in sales_data:
            self.sales_tree.insert("", "end", values=(order.sales_order_number, order.bp_code, order.status_code, order.document_total, order.posting_date, order.due_date))

    def refresh_purchasing(self):
        for i in self.purchase_tree.get_children():
            self.purchase_tree.delete(i)
        
        purchase_data = session.query(PurchaseOrder).all()
        for order in purchase_data:
            self.purchase_tree.insert("", "end", values=(order.purchase_order_number, order.supplier, order.status, order.total, order.order_date))

    def add_inventory_item(self):
        # Create a new window for adding inventory item
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Inventory Item")

        # Create and place widgets
        ttk.Label(add_window, text="Item Number:").grid(row=0, column=0, padx=5, pady=5)
        item_number_entry = ttk.Entry(add_window)
        item_number_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        description_entry = ttk.Entry(add_window)
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="In Stock:").grid(row=2, column=0, padx=5, pady=5)
        in_stock_entry = ttk.Entry(add_window)
        in_stock_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Last Purchase Price:").grid(row=3, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(add_window)
        price_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_item():
            new_item = ItemInventory(
                item_number=item_number_entry.get(),
                description=description_entry.get(),
                in_stock=float(in_stock_entry.get()),
                last_purchase_price=float(price_entry.get())
            )
            session.add(new_item)
            session.commit()
            messagebox.showinfo("Success", "New item added successfully!")
            add_window.destroy()
            self.refresh_inventory()

        ttk.Button(add_window, text="Save", command=save_item).grid(row=4, column=1, padx=5, pady=5)

    def add_customer(self):
        # Create a new window for adding customer
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Customer")

        # Create and place widgets
        ttk.Label(add_window, text="BP Code:").grid(row=0, column=0, padx=5, pady=5)
        bp_code_entry = ttk.Entry(add_window)
        bp_code_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Contact Name:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Title:").grid(row=2, column=0, padx=5, pady=5)
        title_entry = ttk.Entry(add_window)
        title_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Telephone:").grid(row=3, column=0, padx=5, pady=5)
        telephone_entry = ttk.Entry(add_window)
        telephone_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_customer():
            new_customer = CustomerContact(
                bp_code=bp_code_entry.get(),
                contact_name=name_entry.get(),
                title=title_entry.get(),
                telephone=telephone_entry.get()
            )
            session.add(new_customer)
            session.commit()
            messagebox.showinfo("Success", "New customer added successfully!")
            add_window.destroy()
            self.refresh_customers()

        ttk.Button(add_window, text="Save", command=save_customer).grid(row=4, column=1, padx=5, pady=5)

    def create_new_sale(self):
        # Create a new window for creating a sale
        sale_window = tk.Toplevel(self.master)
        sale_window.title("Create New Sale")

        # Create and place widgets
        ttk.Label(sale_window, text="Customer:").grid(row=0, column=0, padx=5, pady=5)
        customer_entry = ttk.Entry(sale_window)
        customer_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(sale_window, text="Item Number:").grid(row=1, column=0, padx=5, pady=5)
        item_entry = ttk.Entry(sale_window)
        item_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(sale_window, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(sale_window)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(sale_window, text="Due Date:").grid(row=3, column=0, padx=5, pady=5)
        due_date_entry = ttk.Entry(sale_window)
        due_date_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_sale():
            new_sale = SalesOrder(
                bp_code=customer_entry.get(),
                status_code='Open',
                posting_date=datetime.date.today(),
                due_date=datetime.datetime.strptime(due_date_entry.get(), '%Y-%m-%d').date(),
                currency='USD',
                document_total=0  # This should be calculated based on the item price and quantity
            )
            session.add(new_sale)
            session.commit()

            # Add sales order item
            item = session.query(ItemInventory).filter_by(item_number=item_entry.get()).first()
            if item:
                new_sale_item = SalesOrderItem(
                    sales_order_number=new_sale.sales_order_number,
                    item_number=item.item_number,
                    quantity=float(quantity_entry.get()),
                    unit_price=item.last_purchase_price,
                    total_price=float(quantity_entry.get()) * item.last_purchase_price
                )
                session.add(new_sale_item)
                session.commit()

            messagebox.showinfo("Success", "New sale created successfully!")
            sale_window.destroy()
            self.refresh_sales()

        ttk.Button(sale_window, text="Save", command=save_sale).grid(row=4, column=1, padx=5, pady=5)

    def create_new_purchase_order(self):
        # Create a new window for creating a purchase order
        po_window = tk.Toplevel(self.master)
        po_window.title("Create New Purchase Order")

        # Create and place widgets
        ttk.Label(po_window, text="Supplier:").grid(row=0, column=0, padx=5, pady=5)
        supplier_entry = ttk.Entry(po_window)
        supplier_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(po_window, text="Item Number:").grid(row=1, column=0, padx=5, pady=5)
        item_entry = ttk.Entry(po_window)
        item_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(po_window, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(po_window)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_po():
            new_po = PurchaseOrder(
                supplier=supplier_entry.get(),
                status='Open',
                total=0,  # This should be calculated based on the item price and quantity
                order_date=datetime.date.today()
            )
            session.add(new_po)
            session.commit()

            # Add purchase order item
            item = session.query(ItemInventory).filter_by(item_number=item_entry.get()).first()
            if item:
                new_po_item = PurchaseOrderItem(
                    purchase_order_number=new_po.purchase_order_number,
                    item_number=item.item_number,
                    quantity=float(quantity_entry.get()),
                    unit_price=item.last_purchase_price,
                    total_price=float(quantity_entry.get()) * item.last_purchase_price
                )
                session.add(new_po_item)
                session.commit()

            messagebox.showinfo("Success", "New purchase order created successfully!")
            po_window.destroy()
            self.refresh_purchasing()

        ttk.Button(po_window, text="Save", command=save_po).grid(row=3, column=1, padx=5, pady=5)

    def confirm_purchase_receipt(self):
        selected_item = self.purchase_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a purchase order to confirm receipt.")
            return

        order_number = self.purchase_tree.item(selected_item[0])['values'][0]
        order = session.query(PurchaseOrder).filter_by(purchase_order_number=order_number).first()
        
        if order:
            order.status = 'Received'
            order.receipt_date = datetime.date.today()
            session.commit()
            messagebox.showinfo("Success", f"Purchase Order {order_number} marked as received.")
            self.refresh_purchasing()
        else:
            messagebox.showerror("Error", "Selected order not found.")

    def export_purchase_order_pdf(self):
        selected_item = self.purchase_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a purchase order to export.")
            return

        order_number = self.purchase_tree.item(selected_item[0])['values'][0]
        order = session.query(PurchaseOrder).filter_by(purchase_order_number=order_number).first()
        
        if order:
            filename = filedialog.asksaveasfilename(defaultextension=".pdf")
            if filename:
                generate_pdf(order, filename)
                messagebox.showinfo("Success", f"Purchase Order exported to {filename}")
        else:
            messagebox.showerror("Error", "Selected order not found.")

    def generate_inventory_report(self):
        inventory_data = session.query(ItemInventory).all()
        df = pd.DataFrame([(item.item_number, item.in_stock) for item in inventory_data], columns=['Item Number', 'In Stock'])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(kind='bar', x='Item Number', y='In Stock', ax=ax)
        ax.set_title('Inventory Levels')
        ax.set_xlabel('Item Number')
        ax.set_ylabel('In Stock')
        plt.xticks(rotation=45)
        
        self.show_plot(fig)

    def generate_sales_report(self):
        sales_data = session.query(SalesOrder).all()
        df = pd.DataFrame([(order.sales_order_number, order.document_total, order.posting_date) for order in sales_data], 
                          columns=['Order Number', 'Total', 'Date'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(kind='line', x='Date', y='Total', ax=ax)
        ax.set_title('Sales Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Sales')
        
        self.show_plot(fig)

    def generate_reorder_report(self):
        inventory_data = session.query(ItemInventory).all()
        df = pd.DataFrame([(item.item_number, item.in_stock, item.qty_ordered_by_customers) for item in inventory_data], 
                          columns=['Item Number', 'In Stock', 'Ordered by Customers'])
        
        df['Needs Reorder'] = df['In Stock'] < df['Ordered by Customers']
        reorder_items = df[df['Needs Reorder']]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        reorder_items.plot(kind='bar', x='Item Number', y=['In Stock', 'Ordered by Customers'], ax=ax)
        ax.set_title('Items Needing Reorder')
        ax.set_xlabel('Item Number')
        ax.set_ylabel('Quantity')
        plt.xticks(rotation=45)
        
        self.show_plot(fig)

    def view_low_stock_items(self):
        inventory_data = session.query(ItemInventory).filter(ItemInventory.in_stock < 10).all()
        df = pd.DataFrame([(item.item_number, item.description, item.in_stock) for item in inventory_data], 
                          columns=['Item Number', 'Description', 'In Stock'])
        self.show_dataframe(df, "Low Stock Items")

    def view_top_customers(self):
        sales_data = session.query(SalesOrder).all()
        df = pd.DataFrame([(order.bp_code, order.document_total) for order in sales_data], 
                          columns=['Customer', 'Total'])
        df = df.groupby('Customer').sum().sort_values('Total', ascending=False).head(10)
        self.show_dataframe(df, "Top 10 Customers by Sales")

    def view_monthly_sales(self):
        sales_data = session.query(SalesOrder).all()
        df = pd.DataFrame([(order.posting_date, order.document_total) for order in sales_data], 
                          columns=['Date', 'Total'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        monthly_sales = df.resample('M').sum()
        self.show_dataframe(monthly_sales, "Monthly Sales Report")

    def show_plot(self, fig):
        for widget in self.reports_tab.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.reports_tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_dataframe(self, df, title):
        df_window = tk.Toplevel(self.master)
        df_window.title(title)

        text_widget = tk.Text(df_window)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, df.to_string())

    def execute_query(self):
        query = self.query_input.get("1.0", tk.END).strip()
        try:
            result = session.execute(query)
            self.display_query_results(result)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))

    def display_query_results(self, result):
        for i in self.query_tree.get_children():
            self.query_tree.delete(i)

        columns = result.keys()
        self.query_tree["columns"] = columns
        for col in columns:
            self.query_tree.heading(col, text=col)
            self.query_tree.column(col, width=100)

        for row in result:
            self.query_tree.insert("", "end", values=tuple(row))

if __name__ == "__main__":
    root = tk.Tk()
    app = MRPERPApp(root)
    root.mainloop()