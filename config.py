import os

# Get the absolute path of the project root directory
desktop_path = os.path.expanduser("~/Desktop")
PROJECT_ROOT = os.path.join(desktop_path, "MRP_ERP_App_v2")

# Database configuration
DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'mrp_erp.db')

# Application configuration
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

# File paths
DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data')
ITEM_MASTER_FILE = os.path.join(DATA_FOLDER, 'Item+Master.txt')
BP_CONTACT_FILE = os.path.join(DATA_FOLDER, 'BP+Contact+Person.txt')
SALES_ORDER_FILE = os.path.join(DATA_FOLDER, 'Sales+Order.txt')
PURCHASE_ORDER_FILE = os.path.join(DATA_FOLDER, 'Purchase+Order.txt')
