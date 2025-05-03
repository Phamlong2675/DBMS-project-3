CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminPassword123!';
CREATE USER 'sales_manager'@'localhost' IDENTIFIED BY 'salesManagerPassword123!';
CREATE USER 'inventory_manager'@'localhost' IDENTIFIED BY 'inventoryManagerPassword123!';
CREATE USER 'sales_staff'@'localhost' IDENTIFIED BY 'salesStaffPassword123!';

GRANT ALL PRIVILEGES ON sales_management.* TO 'admin'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE ON sales_management.orders TO 'sales_manager'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON sales_management.customers TO 'sales_manager'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON sales_management.products TO 'sales_manager'@'localhost';
GRANT SELECT ON sales_management.employees TO 'sales_manager'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE ON sales_management.products TO 'inventory_manager'@'localhost';
GRANT SELECT ON sales_management.orders TO 'inventory_manager'@'localhost';

GRANT SELECT, INSERT, UPDATE ON sales_management.orders TO 'sales_staff'@'localhost';
GRANT SELECT ON sales_management.customers TO 'sales_staff'@'localhost';
GRANT SELECT ON sales_management.products TO 'sales_staff'@'localhost';
FLUSH PRIVILEGES;


