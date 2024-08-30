from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os
import sys

# Add the project root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from config.config import DATABASE_URI

Base = declarative_base()

class ItemInventory(Base):
    __tablename__ = 'item_inventory'
    
    item_number = Column(String, primary_key=True)
    description = Column(String)
    manufacturer = Column(String)
    in_stock = Column(Float)
    qty_ordered_by_customers = Column(Float)
    qty_ordered_from_vendors = Column(Float)
    last_purchase_price = Column(Float)

class CustomerContact(Base):
    __tablename__ = 'customer_contact'
    
    bp_code = Column(String, primary_key=True)
    contact_name = Column(String)
    title = Column(String)
    address = Column(String)
    telephone = Column(String)
    email = Column(String)

class SalesOrder(Base):
    __tablename__ = 'sales_order'
    
    sales_order_number = Column(Integer, primary_key=True)
    bp_code = Column(String, ForeignKey('customer_contact.bp_code'))
    status_code = Column(String)
    posting_date = Column(Date)
    due_date = Column(Date)
    promise_date = Column(Date)
    currency = Column(String)
    document_total = Column(Float)
    total_tax = Column(Float)
    discount_percent = Column(Float)
    total_discount = Column(Float)
    gross_profit = Column(Float)
    paid_to_date = Column(Float)
    remarks = Column(String)

    customer = relationship("CustomerContact")
    items = relationship("SalesOrderItem", back_populates="sales_order")

class SalesOrderItem(Base):
    __tablename__ = 'sales_order_item'
    
    id = Column(Integer, primary_key=True)
    sales_order_number = Column(Integer, ForeignKey('sales_order.sales_order_number'))
    item_number = Column(String, ForeignKey('item_inventory.item_number'))
    quantity = Column(Float)
    unit_price = Column(Float)
    total_price = Column(Float)

    sales_order = relationship("SalesOrder", back_populates="items")
    item = relationship("ItemInventory")

class PurchaseOrder(Base):
    __tablename__ = 'purchase_order'
    
    purchase_order_number = Column(Integer, primary_key=True)
    supplier = Column(String)
    status = Column(String)
    total = Column(Float)
    order_date = Column(Date)
    receipt_date = Column(Date)

    items = relationship("PurchaseOrderItem", back_populates="purchase_order")

class PurchaseOrderItem(Base):
    __tablename__ = 'purchase_order_item'
    
    id = Column(Integer, primary_key=True)
    purchase_order_number = Column(Integer, ForeignKey('purchase_order.purchase_order_number'))
    item_number = Column(String, ForeignKey('item_inventory.item_number'))
    quantity = Column(Float)
    unit_price = Column(Float)
    total_price = Column(Float)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    item = relationship("ItemInventory")

# Create database engine
engine = create_engine(DATABASE_URI)

# Create all tables
Base.metadata.create_all(engine)