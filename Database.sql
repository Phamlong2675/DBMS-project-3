drop database if exists sales_management;
CREATE DATABASE sales_management;
USE sales_management;
-- Tạo bảng Customers
CREATE TABLE Customers (
    CustomerID VARCHAR(10) PRIMARY KEY,  -- CustomerID là khóa chính
    CustomerName VARCHAR(100) NOT NULL,
    Address VARCHAR(100),
    Phone VARCHAR(10)
);

DELIMITER //
CREATE TRIGGER before_insert_customers
BEFORE INSERT ON Customers
FOR EACH ROW
BEGIN
    DECLARE max_id INT DEFAULT 0;
    SELECT COALESCE(MAX(CAST(SUBSTRING(CustomerID, 2) AS UNSIGNED)), 0) INTO max_id FROM Customers;
    SET NEW.CustomerID = CONCAT('C', LPAD(max_id + 1, 3, '0'));
END; //
DELIMITER ;

INSERT INTO Customers (CustomerName, Address, Phone) VALUES
('Nguyen Van A', '23 Tran Duy Hung, Hanoi', '0912345678'),
('Le Thi B', '46 Nguyen Trai, Hanoi', '0901234567'),
('Tran Van C', '60 Doi Can, Hanoi', '0987654321'),
('Pham Thi D', '12 Le Duan, Da Nang', '0934567890'),
('Hoang Van E', '78 Le Loi, Hue', '0943216789'),
('Vu Thi F', '89 Phan Chau Trinh, Da Nang', '0976543210'),
('Dang Van G', '9 Vo Van Tan, HCMC', '0909090909'),
('Bui Thi H', '101 Hai Ba Trung, HCMC', '0922334455'),
('Ngo Van I', '35 Tran Phu, Nha Trang', '0933123456'),
('Do Thi K', '55 Le Thanh Ton, HCMC', '0955667788');

-- Tạo bảng Employees
CREATE TABLE Employees (
    EmployeeID VARCHAR(10) PRIMARY KEY,
    EmployeeName VARCHAR(100) NOT NULL,
    JobTitle VARCHAR(50)
);

DELIMITER //
CREATE TRIGGER before_insert_employees
BEFORE INSERT ON Employees
FOR EACH ROW
BEGIN
    DECLARE max_id INT DEFAULT 0;
    SELECT COALESCE(MAX(CAST(SUBSTRING(EmployeeID, 2) AS UNSIGNED)), 0) INTO max_id FROM Employees;
    SET NEW.EmployeeID = CONCAT('E', LPAD(max_id + 1, 3, '0'));
END; //
DELIMITER ;

INSERT INTO Employees (EmployeeName, JobTitle) VALUES
('Nguyen Minh', 'Sales Representative'),
('Tran Anh', 'Manager'),
('Le Tuan', 'Sales Representative'),
('Hoang Hoa', 'Sales Representative'),
('Pham Long', 'Sales Assistant'),
('Doan Khoa', 'Manager'),
('Bui Hien', 'Sales Assistant'),
('Ngo Linh', 'Sales Representative'),
('Dinh Phuc', 'Sales Assistant'),
('Nguyen Hanh', 'Sales Representative');


-- Tạo bảng Products
CREATE TABLE Products (
    ProductID VARCHAR(10) PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2),
    StockQuantity INT,
	IsActive BOOLEAN DEFAULT TRUE
);

DELIMITER //
CREATE TRIGGER before_insert_products
BEFORE INSERT ON Products
FOR EACH ROW
BEGIN
    DECLARE max_id INT DEFAULT 0;
    SELECT COALESCE(MAX(CAST(SUBSTRING(ProductID, 2) AS UNSIGNED)), 0) INTO max_id FROM Products;
    SET NEW.ProductID = CONCAT('P', LPAD(max_id + 1, 3, '0'));
END; //
DELIMITER ;

INSERT INTO Products (ProductName, Price, StockQuantity) VALUES
('Laptop Dell XPS 13', 25000000, 15),
('iPhone 14 Pro', 29000000, 20),
('Samsung Galaxy S22', 24000000, 18),
('Apple Watch Series 8', 12000000, 25),
('AirPods Pro', 6000000, 40),
('Logitech MX Master 3', 2500000, 30),
('Kindle Paperwhite', 3000000, 22),
('MacBook Air M2', 32000000, 12),
('Sony WH-1000XM5', 8500000, 10),
('Asus ROG Laptop', 45000000, 5);

-- Tạo bảng Orders
CREATE TABLE Orders (
    OrderID VARCHAR(10) PRIMARY KEY,
    CustomerID VARCHAR(10) NOT NULL,
    OrderDate DATE,
    Status VARCHAR(20),
    EmployeeID VARCHAR(10) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

DELIMITER //
CREATE TRIGGER before_insert_orders
BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
    DECLARE max_id INT DEFAULT 0;
    SELECT COALESCE(MAX(CAST(SUBSTRING(OrderID, 2) AS UNSIGNED)), 0) INTO max_id FROM Orders;
    SET NEW.OrderID = CONCAT('O', LPAD(max_id + 1, 3, '0'));
END; //
DELIMITER ;

INSERT INTO Orders (CustomerID, OrderDate, Status, EmployeeID) VALUES
('C004', '2024-12-01', 'Completed', 'E005'),
('C007', '2025-01-15', 'Pending', 'E009'),
('C010', '2025-02-20', 'Shipped', 'E004'),
('C009', '2025-03-10', 'Completed', 'E001'),
('C003', '2025-03-15', 'Pending', 'E010'),
('C005', '2025-03-20', 'Cancelled', 'E003'),
('C001', '2025-03-25', 'Completed', 'E007'),
('C008', '2025-04-01', 'Pending', 'E004'),
('C002', '2025-04-10', 'Shipped', 'E001'),
('C006', '2025-04-20', 'Completed', 'E008');




-- Tạo bảng OrderDetails
CREATE TABLE OrderDetails (
    OrderDetailID VARCHAR(10) PRIMARY KEY,
    OrderID VARCHAR(10) NOT NULL,
    ProductID VARCHAR(10) NOT NULL,
    Quantity INT,
    SalePrice DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

DELIMITER //
CREATE TRIGGER before_insert_orderdetails
BEFORE INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    DECLARE max_id INT DEFAULT 0;
    DECLARE unit_price DECIMAL(10,2) DEFAULT 0;

    -- Lấy ID lớn nhất hiện tại
    SELECT COALESCE(MAX(CAST(SUBSTRING(OrderDetailID, 3) AS UNSIGNED)), 0)
    INTO max_id FROM OrderDetails;

    -- Sinh OrderDetailID mới
    SET NEW.OrderDetailID = CONCAT('OD', LPAD(max_id + 1, 3, '0'));

    -- Lấy đơn giá từ bảng Products
    SELECT Price INTO unit_price FROM Products WHERE ProductID = NEW.ProductID;

    -- Tính SalePrice = Quantity * unit_price
    SET NEW.SalePrice = NEW.Quantity * unit_price;
END;
//
DELIMITER ;


INSERT INTO OrderDetails (OrderID, ProductID, Quantity) VALUES
('O008', 'P001', 1),
('O004', 'P002', 2),
('O005', 'P003', 1),
('O003', 'P004', 1),
('O007', 'P005', 3),
('O010', 'P006', 2),
('O006', 'P007', 1),
('O001', 'P008', 1),
('O002', 'P009', 1),
('O009', 'P010', 1);
