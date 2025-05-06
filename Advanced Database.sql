USE sales_management;
DELIMITER //
CREATE PROCEDURE RegisterCustomer(IN p_CustomerName VARCHAR(100), IN p_Address VARCHAR(100), IN p_Phone VARCHAR(10))
BEGIN
    INSERT INTO Customers (CustomerName, Address, Phone)
    VALUES (p_CustomerName, p_Address, p_Phone);
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE UpdateCustomer(IN p_CustomerID VARCHAR(10), IN p_CustomerName VARCHAR(100), IN p_Address VARCHAR(100), IN p_Phone VARCHAR(10))
BEGIN
    UPDATE Customers
    SET CustomerName = p_CustomerName, Address = p_Address, Phone = p_Phone
    WHERE CustomerID = p_CustomerID;
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE SearchCustomer(IN p_CustomerName VARCHAR(100))
BEGIN
    SELECT * FROM Customers WHERE CustomerName LIKE CONCAT('%', p_CustomerName, '%');
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AddProduct(IN p_ProductName VARCHAR(100), IN p_Price DECIMAL(10,2), IN p_StockQuantity INT)
BEGIN
    INSERT INTO Products (ProductName, Price, StockQuantity)
    VALUES (p_ProductName, p_Price, p_StockQuantity);
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE EditProduct(IN p_ProductID VARCHAR(10), IN p_ProductName VARCHAR(100), IN p_Price DECIMAL(10,2), IN p_StockQuantity INT)
BEGIN
    UPDATE Products
    SET ProductName = p_ProductName, Price = p_Price, StockQuantity = p_StockQuantity
    WHERE ProductID = p_ProductID;
END; //
DELIMITER ;


ALTER TABLE Products ADD COLUMN IsActive BOOLEAN DEFAULT TRUE;
DELIMITER //
CREATE PROCEDURE DeleteProduct(IN p_ProductID VARCHAR(10))
BEGIN
    UPDATE Products
    SET IsActive = FALSE
    WHERE ProductID = p_ProductID;
END;
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE SearchProduct(IN p_ProductName VARCHAR(100))
BEGIN
    SELECT * FROM Products
    WHERE ProductName LIKE CONCAT('%', p_ProductName, '%');
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CreateOrder(IN p_CustomerID VARCHAR(10), IN p_OrderDate DATE, IN p_EmployeeID VARCHAR(10))
BEGIN
    INSERT INTO Orders (CustomerID, OrderDate, Status, EmployeeID)
    VALUES (p_CustomerID, p_OrderDate, 'Pending', p_EmployeeID);
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE UpdateOrderStatus(IN p_OrderID VARCHAR(10), IN p_Status VARCHAR(20))
BEGIN
    UPDATE Orders
    SET Status = p_Status
    WHERE OrderID = p_OrderID;
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE TrackOrder(IN p_OrderID VARCHAR(10))
BEGIN
    SELECT O.OrderID, O.CustomerID, O.OrderDate, O.Status, O.EmployeeID
    FROM Orders O
    WHERE O.OrderID = p_OrderID;
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AddOrderDetails(IN p_OrderID VARCHAR(10), IN p_ProductID VARCHAR(10), IN p_Quantity INT)
BEGIN
    INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
    VALUES (p_OrderID, p_ProductID, p_Quantity);
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AddEmployee(IN p_EmployeeName VARCHAR(100), IN p_JobTitle VARCHAR(50))
BEGIN
    INSERT INTO Employees (EmployeeName, JobTitle)
    VALUES (p_EmployeeName, p_JobTitle);
END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE UpdateEmployee(IN p_EmployeeID VARCHAR(10), IN p_EmployeeName VARCHAR(100), IN p_JobTitle VARCHAR(50))
BEGIN
    UPDATE Employees
    SET EmployeeName = p_EmployeeName, JobTitle = p_JobTitle
    WHERE EmployeeID = p_EmployeeID;
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SearchEmployee(IN p_EmployeeName VARCHAR(100))
BEGIN
    SELECT * FROM Employees WHERE EmployeeName LIKE CONCAT('%', p_EmployeeName, '%');
END; //
DELIMITER ;


CREATE OR REPLACE VIEW SalesReportByEmployee AS
SELECT 
    E.EmployeeID, 
    E.EmployeeName, 
    SUM(OD.SalePrice) AS TotalSales
FROM OrderDetails OD
JOIN Orders O ON OD.OrderID = O.OrderID
JOIN Employees E ON O.EmployeeID = E.EmployeeID
GROUP BY E.EmployeeID, E.EmployeeName;


DELIMITER $$
CREATE PROCEDURE GetTopEmployees(IN top_n INT)
BEGIN
    SELECT 
        EmployeeID,
        EmployeeName,
        TotalSales
    FROM SalesReportByEmployee
    ORDER BY TotalSales DESC
    LIMIT top_n;
END $$
DELIMITER ;


CREATE OR REPLACE VIEW SalesReportByCustomer AS
SELECT 
    C.CustomerID,
    C.CustomerName,
    SUM(OD.SalePrice) AS TotalSales
FROM OrderDetails OD
JOIN Orders O ON OD.OrderID = O.OrderID
JOIN Customers C ON O.CustomerID = C.CustomerID
GROUP BY C.CustomerID, C.CustomerName;


DELIMITER $$

CREATE PROCEDURE GetTopCustomers(IN top_n INT)
BEGIN
    SELECT 
        CustomerID,
        CustomerName,
        TotalSales
    FROM SalesReportByCustomer
    ORDER BY TotalSales DESC
    LIMIT top_n;
END $$

DELIMITER ;


CREATE OR REPLACE VIEW SalesReportByProduct AS
SELECT 
    P.ProductID,
    P.ProductName,
    SUM(OD.SalePrice) AS TotalSales
FROM OrderDetails OD
JOIN Products P ON OD.ProductID = P.ProductID
GROUP BY P.ProductID, P.ProductName;


DELIMITER $$
CREATE PROCEDURE GetTopSellingProducts(IN top_n INT)
BEGIN
    SELECT 
        ProductID,
        ProductName,
        TotalSales
    FROM SalesReportByProduct
    ORDER BY TotalSales DESC
    LIMIT top_n;
END $$
DELIMITER ;


DELIMITER //
CREATE TRIGGER UpdateInventoryAfterOrder
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Products
    SET StockQuantity = StockQuantity - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END; //
DELIMITER ;


DELIMITER //
CREATE TRIGGER UpdateInventoryAfterCancel
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
    IF OLD.Status = 'Pending' AND NEW.Status = 'Cancelled' THEN
        UPDATE Products
        SET StockQuantity = StockQuantity + (SELECT Quantity FROM OrderDetails WHERE OrderID = OLD.OrderID)
        WHERE ProductID IN (SELECT ProductID FROM OrderDetails WHERE OrderID = OLD.OrderID);
    END IF;
END; //
DELIMITER ;

CREATE INDEX idx_customer_name ON Customers(CustomerName);
CREATE INDEX idx_product_name ON Products(ProductName);
CREATE INDEX idx_order_date ON Orders(OrderDate);

CREATE INDEX idx_employee_name ON Employees(EmployeeName);
CREATE INDEX idx_orderdetails_orderid ON OrderDetails(OrderID);




