import pandas as pd
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the project root directory to the Python path
desktop_path = os.path.expanduser("~/Desktop")
project_root = os.path.join(desktop_path, "MRP_ERP_App")
sys.path.append(project_root)

from src.models import engine, ItemInventory, CustomerContact, SalesOrder, PurchaseOrder
from config.config import ITEM_MASTER_FILE, BP_CONTACT_FILE, SALES_ORDER_FILE, PURCHASE_ORDER_FILE

Session = sessionmaker(bind=engine)
session = Session()

def import_item_inventory():
    try:
        df = pd.read_csv(ITEM_MASTER_FILE, sep='\t', header=None, names=[
            'item_number', 'description', 'manufacturer_number', 'in_stock',
            'qty_ordered_by_customers', 'qty_ordered_from_vendors', 'last_purchase_price'
        ])

        for _, row in df.iterrows():
            item = ItemInventory(
                item_number=row['item_number'],
                description=row['description'],
                manufacturer=row['manufacturer_number'],
                in_stock=row['in_stock'],
                qty_ordered_by_customers=row['qty_ordered_by_customers'],
                qty_ordered_from_vendors=row['qty_ordered_from_vendors'],
                last_purchase_price=row['last_purchase_price']
            )
            session.merge(item)

        session.commit()
        print("Item inventory data imported successfully.")
    except Exception as e:
        print(f"Error importing item inventory data: {str(e)}")
        session.rollback()

def import_customer_contacts():
    try:
        df = pd.read_csv(BP_CONTACT_FILE, sep='\t', header=None, names=[
            'bp_code', 'contact_name', 'title', 'address', 'telephone', 'mobile_phone', 'fax', 'email'
        ])

        for _, row in df.iterrows():
            contact = CustomerContact(
                bp_code=row['bp_code'],
                contact_name=row['contact_name'],
                title=row['title'],
                address=row['address'],
                telephone=row['telephone'],
                email=row['email']
            )
            session.merge(contact)

        session.commit()
        print("Customer contact data imported successfully.")
    except Exception as e:
        print(f"Error importing customer contact data: {str(e)}")
        session.rollback()

def import_sales_orders():
    try:
        df = pd.read_csv(SALES_ORDER_FILE, sep='\t', header=None, names=[
            'sales_order_number', 'bp_code', 'status_code', 'posting_date', 'due_date',
            'promise_date', 'currency', 'document_total', 'total_tax', 'discount_percent',
            'total_discount', 'gross_profit', 'paid_to_date', 'remarks'
        ])

        for _, row in df.iterrows():
            order = SalesOrder(
                sales_order_number=row['sales_order_number'],
                bp_code=row['bp_code'],
                status_code=row['status_code'],
                posting_date=pd.to_datetime(row['posting_date']),
                due_date=pd.to_datetime(row['due_date']),
                promise_date=pd.to_datetime(row['promise_date']),
                currency=row['currency'],
                document_total=row['document_total'],
                total_tax=row['total_tax'],
                discount_percent=row['discount_percent'],
                total_discount=row['total_discount'],
                gross_profit=row['gross_profit'],
                paid_to_date=row['paid_to_date'],
                remarks=row['remarks']
            )
            session.merge(order)

        session.commit()
        print("Sales order data imported successfully.")
    except Exception as e:
        print(f"Error importing sales order data: {str(e)}")
        session.rollback()

def import_purchase_orders():
    try:
        df = pd.read_csv(PURCHASE_ORDER_FILE, sep='\t', header=None, names=[
            'purchase_order_number', 'supplier', 'status', 'total', 'order_date', 'receipt_date'
        ])

        for _, row in df.iterrows():
            order = PurchaseOrder(
                purchase_order_number=row['purchase_order_number'],
                supplier=row['supplier'],
                status=row['status'],
                total=row['total'],
                order_date=pd.to_datetime(row['order_date']),
                receipt_date=pd.to_datetime(row['receipt_date']) if pd.notna(row['receipt_date']) else None
            )
            session.merge(order)

        session.commit()
        print("Purchase order data imported successfully.")
    except Exception as e:
        print(f"Error importing purchase order data: {str(e)}")
        session.rollback()

def import_all_data():
    print("Starting data import process...")
    import_item_inventory()
    import_customer_contacts()
    import_sales_orders()
    import_purchase_orders()
    print("All data imported successfully.")

if __name__ == "__main__":
    import_all_data()
