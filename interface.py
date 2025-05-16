import mysql.connector
import pandas as pd
import streamlit as st
from datetime import datetime
import base64

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            print("Database connection established successfully.")
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            self.connection = None
            self.cursor = None

    def execute_proc(self, proc_name, params):
        try:
            if self.connection is None:
                raise Exception("Database connection is not established.")
            self.cursor.callproc(proc_name, params)
            self.connection.commit()
            print(f"Procedure {proc_name} executed successfully.")
        except mysql.connector.Error as err:
            print(f"Error executing procedure {proc_name}: {err}")
            self.connection.rollback()
        except Exception as e:
            print(f"Error: {e}")

    def fetch_results(self):
        results = []
        try:
            if self.connection is None:
                raise Exception("Database connection is not established.")
            for result in self.cursor.stored_results():
                results = result.fetchall()
        except Exception as e:
            print(f"Error fetching results: {e}")
        return results

class CustomerManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register_customer(self, name, address, phone):
        try:
            self.db_connection.execute_proc('RegisterCustomer', (name, address, phone))
            print(f"Customer {name} registered successfully.")
        except Exception as e:
            print(f"Error registering customer {name}: {e}")

    def update_customer(self, customer_id, name, address, phone):
        try:
            self.db_connection.execute_proc('UpdateCustomer', (customer_id, name, address, phone))
            print(f"Customer {customer_id} updated successfully.")
        except Exception as e:
            print(f"Error updating customer {customer_id}: {e}")

    def search_customer(self, customer_name):
        try:
            self.db_connection.execute_proc('SearchCustomer', (customer_name,))
            results = self.db_connection.fetch_results()
            print(f"Search result for customer '{customer_name}': {results}")
            return results
        except Exception as e:
            print(f"Error searching customer '{customer_name}': {e}")

    def show_customer(self):
        try:
            self.db_connection.execute_proc('ShowCustomer', ())
            results = self.db_connection.fetch_results()
            return results
        except Exception as e:
            print(f"Error showing customers: {e}")
            return []

class ProductManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_product(self, name, price, stock_quantity):
        try:
            self.db_connection.execute_proc('AddProduct', (name, price, stock_quantity))
            print(f"Product {name} added successfully.")
        except Exception as e:
            print(f"Error adding product {name}: {e}")

    def edit_product(self, product_id, name, price, stock_quantity):
        try:
            self.db_connection.execute_proc('EditProduct', (product_id, name, price, stock_quantity))
            print(f"Product {product_id} updated successfully.")
        except Exception as e:
            print(f"Error editing product {product_id}: {e}")

    def delete_product(self, product_id):
        try:
            self.db_connection.execute_proc('DeleteProduct', (product_id,))
            print(f"Product {product_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting product {product_id}: {e}")

    def show_product(self):
        try:
            self.db_connection.execute_proc('ShowProduct', ())
            results = self.db_connection.fetch_results()
            return results
        except Exception as e:
            print(f"Error showing products: {e}")
            return []

    def search_product(self, product_name):
        try:
            self.db_connection.execute_proc('SearchProduct', (product_name,))
            results = self.db_connection.fetch_results()
            print(f"Search result for product '{product_name}': {results}")
            return results
        except Exception as e:
            print(f"Error searching product '{product_name}': {e}")


class OrderManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_order(self, customer_id, order_date, employee_id):
        try:
            self.db_connection.execute_proc('CreateOrder', (customer_id, order_date, employee_id))
            print(f"Order for customer {customer_id} created successfully.")
        except Exception as e:
            print(f"Error creating order for customer {customer_id}: {e}")

    def update_order_status(self, order_id, status):
        try:
            self.db_connection.execute_proc('UpdateOrderStatus', (order_id, status))
            print(f"Order {order_id} status updated to {status}.")
        except Exception as e:
            print(f"Error updating status for order {order_id}: {e}")

    def track_order(self, order_id):
        try:
            self.db_connection.execute_proc('TrackOrder', (order_id,))
            results = self.db_connection.fetch_results()
            print(f"Order {order_id} status: {results}")
            return results
        except Exception as e:
            print(f"Error tracking order {order_id}: {e}")

    def search_order(self, search_term):
        try:
            self.db_connection.execute_proc('SearchOrder', (search_term,))
            results = self.db_connection.fetch_results()
            print(f"Search results for '{search_term}': {results}")
            return results
        except Exception as e:
            print(f"Error searching orders with term '{search_term}': {e}")
            return []

    def get_all_order_details(self):
        try:
            self.db_connection.execute_proc('AllOrderDetail', ())
            results = self.db_connection.fetch_results()
            print(f"All order details retrieved: {results}")
            return results
        except Exception as e:
            print(f"Error retrieving all order details: {e}")
            return []

class OrderDetailsManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_order_details(self, order_id, product_id, quantity):
        try:
            self.db_connection.execute_proc('AddOrderDetails', (order_id, product_id, quantity))
            print(f"Order details added for order {order_id}, product {product_id}.")
        except Exception as e:
            print(f"Error adding order details for order {order_id}, product {product_id}: {e}")

class EmployeeManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_employee(self, name, job_title):
        try:
            self.db_connection.execute_proc('AddEmployee', (name, job_title))
            print(f"Employee {name} added successfully.")
        except Exception as e:
            print(f"Error adding employee {name}: {e}")

    def update_employee(self, employee_id, name, job_title):
        try:
            self.db_connection.execute_proc('UpdateEmployee', (employee_id, name, job_title))
            print(f"Employee {employee_id} updated successfully.")
        except Exception as e:
            print(f"Error updating employee {employee_id}: {e}")

    def search_employee(self, employee_name):
        try:
            self.db_connection.execute_proc('SearchEmployee', (employee_name,))
            results = self.db_connection.fetch_results()
            print(f"Search result for customer '{employee_name}': {results}")
            return results
        except Exception as e:
            print(f"Error searching customer '{employee_name}': {e}")

    def show_employee(self):
        try:
            self.db_connection.execute_proc('ShowEmployee', ())
            results = self.db_connection.fetch_results()
            return results
        except Exception as e:
            print(f"Error showing employees: {e}")
            return []

class ReportManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_total_sales_report(self, start_date, end_date):
        try:
            # Truy vấn trực tiếp mà không cần stored procedure
            query = '''
                SELECT 
                    O.OrderID,
                    OD.ProductID,
                    OD.SalePrice,
                    O.OrderDate
                FROM Orders O
                JOIN OrderDetails OD ON O.OrderID = OD.OrderID
                WHERE O.OrderDate BETWEEN %s AND %s
                ORDER BY O.OrderDate;
            '''
            self.db_connection.cursor.execute(query, (start_date, end_date))
            return self.db_connection.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching total sales report: {e}")
            return []

    def get_sales_by_employee(self):
        try:
            query = "SELECT * FROM SalesReportByEmployee;"
            self.db_connection.cursor.execute(query)
            return self.db_connection.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching sales by employee: {e}")
            return []

    def get_sales_by_product(self):
        try:
            query = "SELECT * FROM SalesReportByProduct;"
            self.db_connection.cursor.execute(query)
            return self.db_connection.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching sales by product: {e}")
            return []

    def get_sales_by_customer(self):
        try:
            query = "SELECT * FROM SalesReportByCustomer;"
            self.db_connection.cursor.execute(query)
            return self.db_connection.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching sales by customer: {e}")
            return []

    def get_top_employees(self, top_n):
        try:
            query = "CALL GetTopEmployees(%s);"
            self.db_connection.cursor.execute(query, (top_n,))
            return self.db_connection.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching top employees: {e}")
            return []

    def get_top_selling_products(self, top_n):
        try:
            query = "CALL GetTopSellingProducts(%s);"
            self.db_connection.cursor.execute(query, (top_n,))
            return self.db_connection.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching top selling products: {e}")
            return []

    def get_top_customers(self, top_n):
        try:
            query = "CALL GetTopCustomers(%s);"
            self.db_connection.cursor.execute(query, (top_n,))
            return self.db_connection.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching top customers: {e}")
            return []


db = DatabaseConnection('localhost', 'root', '123456', 'sales_management')

customer_manager = CustomerManager(db)
product_manager = ProductManager(db)
order_manager = OrderManager(db)
order_details_manager = OrderDetailsManager(db)
employee_manager = EmployeeManager(db)
report_manager = ReportManager(db)


def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Gọi hàm để đặt ảnh nền
set_background("background.jpg")

# Menu chính
menu = [
    "Welcome", 
    "Customer Management", 
    "Product Management", 
    "Order Management", 
    "Employee Management", 
    "Sales Reports"
]
choice = st.sidebar.selectbox("Select a task", menu, index=0)

# Trang Welcome
if choice == "Welcome":
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: flex-start; height: 100vh; text-align: center; padding-top: 50px; white-space: nowrap;'>
            <div>
                <h1 style='font-size: 3em;'>Welcome to the Sales Management System!</h1>
                <p style='font-size: 1.5em;'>This is your all-in-one system for managing customers, products, orders, employees, and sales reports.</p>
                <p style='font-size: 1.5em;'>Please choose a task from the menu to get started.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif choice == "Customer Management":
    st.subheader("Customer Management")

    tab1, tab2, tab3, tab4 = st.tabs(["Register Customer", "Update Customer", "Search Customer", "All Customer"])

    with tab1:
        st.subheader("Register Customer")
        with st.form(key="register_customer_form"):
            name = st.text_input("Name", key="register_name")
            address = st.text_input("Address", key="register_address")
            phone = st.text_input("Phone", key="register_phone")
            submit_button = st.form_submit_button("Register Customer")
            if submit_button:
                customer_manager.register_customer(name, address, phone)
                st.success(f"Customer '{name}' registered successfully!")

    with tab2:
        st.subheader("Update Customer")
        with st.form(key="update_customer_form"):
            customer_id = st.text_input("Customer ID", key="update_id")
            name = st.text_input("New Name", key="update_name")
            address = st.text_input("New Address", key="update_address")
            phone = st.text_input("New Phone", key="update_phone")
            submit_button = st.form_submit_button("Update Customer")
            if submit_button:
                customer_manager.update_customer(customer_id, name, address, phone)
                st.success(f"Customer ID '{customer_id}' updated successfully!")

    with tab3:
        st.subheader("Search Customer")
        search_name = st.text_input("Enter Name to Search", key="search_customer")
        if st.button("Search Customer"):
            results = customer_manager.search_customer(search_name)
            if results:
                df = pd.DataFrame(results, columns=["CustomerID", "Name", "Address", "Phone"])
                st.dataframe(df)  # Hiển thị kết quả dưới dạng bảng
            else:
                st.warning("No matching customer found.")

    with tab4:
        st.subheader("All Customer")
        results = customer_manager.show_customer()
        if results:
            df = pd.DataFrame(results, columns=["Customer ID", "Customer Name", "Address", "Phone"])
            st.dataframe(df)
        else:
            st.info("No customers available.")

elif choice == "Product Management":
    st.subheader("Product Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add Product", "Edit Product", "Delete Product", "Search Product", "All Product"])

    with tab1:
        st.subheader("Add Product")
        with st.form(key="add_product_form"):
            name = st.text_input("Product Name", key="add_name")
            price = st.number_input("Price", min_value=0.0, key="add_price")
            stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1, key="add_stock")
            submit_button = st.form_submit_button("Add Product")
            if submit_button:
                product_manager.add_product(name, price, stock_quantity)
                st.success(f"Product '{name}' added successfully!")

    with tab2:
        st.subheader("Edit Product")
        with st.form(key="edit_product_form"):
            product_id = st.text_input("Product ID", key="edit_id")
            name = st.text_input("New Product Name", key="edit_name")
            price = st.number_input("New Price", min_value=0.0, key="edit_price")
            stock_quantity = st.number_input("New Stock Quantity", min_value=0, step=1, key="edit_stock")
            submit_button = st.form_submit_button("Update Product")
            if submit_button:
                product_manager.edit_product(product_id, name, price, stock_quantity)
                st.success(f"Product ID '{product_id}' updated successfully!")

    with tab3:
        st.subheader("Delete Product")
        with st.form(key="delete_product_form"):
            product_id = st.text_input("Product ID to delete", key="delete_id")
            submit_button = st.form_submit_button("Delete Product")
            if submit_button:
                product_manager.delete_product(product_id)
                st.success(f"Product ID '{product_id}' deleted successfully!")

    with tab4:
        st.subheader("Search Product")
        product_name = st.text_input("Enter Product Name to search", key="search_name")
        if st.button("Search Product"):
            results = product_manager.search_product(product_name)
            if results:
                df = pd.DataFrame(results, columns=["ProductID", "ProductName", "Price", "Stock", "Is Active"])
                st.dataframe(df)  # Hiển thị kết quả dưới dạng bảng
            else:
                st.warning("No matching product found.")

    with tab5:
        st.subheader("All Product")
        results = product_manager.show_product()
        if results:
            df = pd.DataFrame(results, columns=["Product ID", "Product Name", "Price", "Stock Quantity"])
            st.dataframe(df)
        else:
            st.info("No products available.")

elif choice == "Order Management":
    st.subheader("Order Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Create Order", "Update Order Status", "Add Order Details", "All Order Details", "Search Orders"])

    with tab1:
        st.subheader("Create Order")
        with st.form(key="create_order_form"):
            customer_id = st.text_input("Customer ID", key="create_customer_id")
            employee_id = st.text_input("Employee ID", key="create_employee_id")
            order_date = st.date_input("Order Date", value=datetime.today())
            submit_button = st.form_submit_button("Create Order")
            
            if submit_button:
                order_manager.create_order(customer_id, order_date, employee_id)
                st.success(f"Order for customer {customer_id} created successfully!")

    with tab2:
        st.subheader("Update Order Status")
        with st.form(key="update_order_status_form"):
            order_id = st.text_input("Order ID", key="update_order_id")
            status = st.selectbox("Order Status", ["Pending", "Completed", "Cancelled", "Shipped"])
            submit_button = st.form_submit_button("Update Order Status")
            
            if submit_button:
                order_manager.update_order_status(order_id, status)
                st.success(f"Order {order_id} status updated to {status}")

    with tab3:
        st.subheader("Add Order Details")
        with st.form(key="add_order_details_form"):
            order_id = st.text_input("Order ID", key="add_order_id")
            product_id = st.text_input("Product ID", key="add_product_id")
            quantity = st.number_input("Quantity", min_value=1, step=1, key="add_quantity")
            submit_button = st.form_submit_button("Add Order Details")
            
            if submit_button:
                try:
                    order_details_manager.add_order_details(order_id, product_id, quantity)
                    st.success(f"Order details added for order {order_id}, product {product_id}.")
                except Exception as e:
                    st.error(f"Error adding order details: {e}")

    with tab4:
        st.subheader("All Order Details")
        try:
            results = order_manager.get_all_order_details()
            if results:
                df = pd.DataFrame(results, columns=[
                    "Order Detail ID", "Order ID", "Product ID", "Quantity", "Sale Price"
                ])  
                st.dataframe(df)
            else:
                st.warning("No order details found.")
        except Exception as e:
            st.error(f"Error retrieving order details: {e}")

    with tab5:
        st.subheader("Search Orders")
        with st.form(key="search_order_form"):
            search_term = st.text_input("Customer Name", key="search_customer_name")
            submit_button = st.form_submit_button("Search")

            if submit_button:
                try:
                    results = order_manager.search_order(search_term)
                    if results:
                        df = pd.DataFrame(results, columns=["Order ID", "Customer Name", "Employee Name", "Order Date", "Status"])
                        st.dataframe(df)
                    else:
                        st.warning(f"No orders found for customer name containing '{search_term}'.")
                except Exception as e:
                    st.error(f"Error searching orders: {e}")

elif choice == "Employee Management":
    st.subheader("Employee Management")

    tab1, tab2, tab3, tab4 = st.tabs(["Add Employee", "Update Employee", "Search Employee", "All Employee"])

    with tab1:
        st.subheader("Add New Employee")
        with st.form(key="add_employee_form"):
            name = st.text_input("Employee Name")
            job_title = st.text_input("Job Title")
            submit_button = st.form_submit_button("Add Employee")
            
            if submit_button:
                employee_manager.add_employee(name, job_title)
                st.success(f"Employee {name} added successfully!")

    with tab2:
        st.subheader("Update Existing Employee")
        with st.form(key="update_employee_form"):
            employee_id = st.text_input("Employee ID")
            updated_name = st.text_input("Updated Name")
            updated_job_title = st.text_input("Updated Job Title")
            update_button = st.form_submit_button("Update Employee")

            if update_button:
                if employee_id and updated_name and updated_job_title:
                    try:
                        employee_manager.update_employee(employee_id, updated_name, updated_job_title)
                        st.success(f"Employee {employee_id} updated successfully!")
                    except Exception as e:
                        st.error(f"Error updating employee: {e}")
                else:
                    st.warning("Please fill in all fields for update.")

    with tab3:
        st.subheader("Search Employee")
        search_name = st.text_input("Enter Name to Search", key="search_employee")
        if st.button("Search Employee"):
            results = employee_manager.search_employee(search_name)
            if results:
                df = pd.DataFrame(results, columns=["Employee ID", "Name", "Job Title"])
                st.dataframe(df)  
            else:
                st.warning("No matching employee found.")

    with tab4:
        st.subheader("All Employee")
        results = employee_manager.show_employee()
        if results:
            df = pd.DataFrame(results, columns=["Employee ID", "Employee Name", "Job Title"])
            st.dataframe(df)
        else:
            st.info("No customers available.")

elif choice == "Sales Reports":
    st.subheader("Sales Reports")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Total Sales by Date", 
        "Sales by Employee",
        "Sales by Product", 
        "Sales by Customer", 
        "Top Employees", 
        "Top Selling Products",
        "Top Customers"
    ])

    with tab1:
        st.subheader("Total Sales by Date")
        start_date = st.date_input("Start Date", key="total_sales_start")
        end_date = st.date_input("End Date", key="total_sales_end")
        if st.button("Get Total Sales Report"):
            results = report_manager.get_total_sales_report(start_date, end_date)
            df = pd.DataFrame(results, columns=["OrderID", "ProductID", "SalePrice", "OrderDate"])
            st.dataframe(df)

    with tab2:
        st.subheader("Sales by Employee")
        results = report_manager.get_sales_by_employee()
        df = pd.DataFrame(results, columns=["EmployeeID", "EmployeeName", "TotalSales"])
        st.dataframe(df)

    with tab3:
        st.subheader("Sales by Product")
        results = report_manager.get_sales_by_product()
        df = pd.DataFrame(results, columns=["ProductID", "ProductName", "TotalSales"])
        st.dataframe(df)

    with tab4:
        st.subheader("Sales by Customer")
        results = report_manager.get_sales_by_customer()
        df = pd.DataFrame(results, columns=["CustomerID", "CustomerName", "TotalSales"])
        st.dataframe(df)

    with tab5:
        st.subheader("Top Employees")
        top_n = st.number_input("Number of Top Employees", min_value=1, value=5)
        if st.button("Get Top Employees"):
            results = report_manager.get_top_employees(top_n)
            df = pd.DataFrame(results, columns=["EmployeeID", "EmployeeName", "TotalSales"])
            st.dataframe(df)

    with tab6:
        st.subheader("Top Selling Products")
        top_n = st.number_input("Number of Top Products", min_value=1, value=5, key="top_products")
        if st.button("Get Top Selling Products"):
            results = report_manager.get_top_selling_products(top_n)
            df = pd.DataFrame(results, columns=["ProductID", "ProductName", "TotalSales"])
            st.dataframe(df)

    with tab7:
        st.subheader("Top Customers")
        top_n = st.number_input("Number of Top Customers", min_value=1, value=5, key="top_customers")
        if st.button("Get Top Customers"):
            results = report_manager.get_top_customers(top_n)
            df = pd.DataFrame(results, columns=["CustomerID", "CustomerName", "TotalSales"])
            st.dataframe(df)
