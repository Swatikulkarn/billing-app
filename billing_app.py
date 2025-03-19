import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                               QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox)
from db import connect_db

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing System")
        self.setGeometry(100, 100, 400, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Customer Name Input
        self.name_label = QLabel("Customer Name:")
        self.name_input = QLineEdit()

        # Bill Amount Input
        self.amount_label = QLabel("Total Amount:")
        self.amount_input = QLineEdit()

        # Buttons
        self.save_button = QPushButton("Save Bill")
        self.save_button.clicked.connect(self.save_bill)

        self.view_button = QPushButton("View Bills")
        self.view_button.clicked.connect(self.view_bills)

        # Table for Displaying Bills
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Bill ID", "Customer Name", "Total Amount"])

        # Adding Widgets to Layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.view_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def save_bill(self):
        name = self.name_input.text()
        amount = self.amount_input.text()

        if not name or not amount:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Insert Customer
            cursor.execute("INSERT INTO customers (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name", (name,))
            conn.commit()

            # Get Customer ID
            cursor.execute("SELECT id FROM customers WHERE name=%s", (name,))
            customer_id = cursor.fetchone()[0]

            # Insert Bill
            cursor.execute("INSERT INTO bills (customer_id, total_amount) VALUES (%s, %s)", (customer_id, amount))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Bill Saved Successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def view_bills(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.id, c.name, b.total_amount FROM bills b
                JOIN customers c ON b.customer_id = c.id
            """)
            results = cursor.fetchall()
            conn.close()

            self.table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, item in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))