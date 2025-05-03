import mysql.connector

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

class OrderManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_order(self, customer_id, order_date, status, employee_id):
        try:
            self.db_connection.execute_proc('CreateOrder', (customer_id, order_date, status, employee_id))
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

class ReportManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_sales_report_today(self):
        try:
            self.db_connection.cursor.execute("SELECT * FROM SalesReportToday")
            results = self.db_connection.cursor.fetchall()
            print(f"Sales report for today: {results}")
            return results
        except Exception as e:
            print(f"Error fetching sales report for today: {e}")

    def get_sales_report_by_employee(self):
        try:
            self.db_connection.cursor.execute("SELECT * FROM SalesReportByEmployee")
            results = self.db_connection.cursor.fetchall()
            print(f"Sales report by employee: {results}")
            return results
        except Exception as e:
            print(f"Error fetching sales report by employee: {e}")

    def get_total_sales_report(self, start_date, end_date):
        try:
            # Câu lệnh SQL lấy tổng doanh thu từ view với điều kiện ngày bắt đầu và kết thúc
            query = """
            SELECT SUM(TotalSales) AS TotalSales, OrderDate
            FROM TotalSalesReport
            WHERE OrderDate BETWEEN %s AND %s
            GROUP BY OrderDate
            ORDER BY OrderDate;
            """
        
            # Thực thi câu lệnh với các tham số ngày bắt đầu và kết thúc
            self.db_connection.cursor.execute(query, (start_date, end_date))
            
            # Lấy kết quả
            results = self.db_connection.cursor.fetchall()
            
            if not results:
                print("No data found for the specified date range.")
            else:
                for row in results:
                    print(f"Date: {row[1]}, Total Sales: {row[0]}")
        
            return results
        except Exception as e:
            print(f"Error fetching total sales report: {e}")



    def get_total_sales_report(self, start_date, end_date):
        try:
            # Câu lệnh SQL lấy tổng doanh thu từng ngày từ view với điều kiện ngày bắt đầu và kết thúc
            query = """
            SELECT SUM(TotalSales) AS TotalSales, OrderDate
            FROM TotalSalesReport
            WHERE OrderDate BETWEEN %s AND %s
            GROUP BY OrderDate
            ORDER BY OrderDate;
            """
        
            # Thực thi câu lệnh với các tham số ngày bắt đầu và kết thúc
            self.db_connection.cursor.execute(query, (start_date, end_date))
        
            # Lấy kết quả
            results = self.db_connection.cursor.fetchall()
        
            # Kiểm tra và hiển thị kết quả từng ngày
            if not results:
                print("No data found for the specified date range.")
            else:
                total_sales_all_days = 0
                print("Sales Report by Date:")
                for row in results:
                    print(f"Date: {row[1]}, Total Sales: {row[0]}")
                    total_sales_all_days += row[0]  # Cộng dồn tổng doanh thu tất cả các ngày
                
                # In ra tổng doanh thu tất cả các ngày
                print(f"\nTotal Sales from {start_date} to {end_date}: {total_sales_all_days}")
        
            return results
        except Exception as e:
            print(f"Error fetching total sales report: {e}")

    def calculate_discount(self, product_id, discount_rate):
        try:
            self.db_connection.cursor.callproc('CalculateDiscount', (product_id, discount_rate))
            results = self.db_connection.fetch_results()
            if not results:
                print(f"No discount calculated for product {product_id}.")
            else:
                print(f"Discounted price for product {product_id} with {discount_rate}% discount: {results}")
            return results
        except Exception as e:
            print(f"Error calculating discount for product {product_id}: {e}")


# Example usage:
db = DatabaseConnection('localhost', 'root', '123456', 'sales_management')

customer_manager = CustomerManager(db)
product_manager = ProductManager(db)
order_manager = OrderManager(db)
order_details_manager = OrderDetailsManager(db)
employee_manager = EmployeeManager(db)
report_manager = ReportManager(db)