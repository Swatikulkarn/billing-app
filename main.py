import sys
from PySide6.QtWidgets import QApplication
from billing_app import BillingApp
from db import create_tables

if __name__ == "__main__":
    create_tables()  # Ensure tables are created before starting the app

    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
