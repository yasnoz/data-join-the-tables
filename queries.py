# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    query ="""SELECT Customers.ContactName AS CustomerContactName, Employees.FirstName AS EmployeeFirstName, Orders.OrderID AS Order_ID
           FROM Orders
           JOIN Customers ON Orders.CustomerID = Customers.CustomerID
           JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
           ORDER BY Orders.OrderID
           """
    results = db.execute(query)
    results = results.fetchall()
    return [(order_id, contact_name, employee_name) for contact_name, employee_name, order_id in results]


def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query ="""SELECT
    C.ContactName,
    ROUND(SUM(OD.UnitPrice * OD.Quantity), 2) AS total_spent
FROM
    Customers C
JOIN
    Orders O ON C.CustomerID = O.CustomerID
JOIN
    OrderDetails OD ON O.OrderID = OD.OrderID
GROUP BY
    C.ContactName
ORDER BY
    total_spent ASC"""
    results = db.execute(query)
    results = results.fetchall()
    return results

def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee! By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like: ('FirstName', 'LastName', 6000 (the sum of all purchase)). The order of the information is irrelevant'''
    query ="""SELECT
    E.FirstName,
    E.LastName,
    ROUND(SUM(OD.UnitPrice * OD.Quantity), 2) AS total_sales
FROM
    Employees E
JOIN
    Orders O ON E.EmployeeID = O.EmployeeID
JOIN
    OrderDetails OD ON O.OrderID = OD.OrderID
GROUP BY
    E.EmployeeID
ORDER BY
    total_sales DESC
LIMIT 1"""
    results = db.execute(query)
    results = results.fetchone()
    return results

def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    query ="""SELECT C.ContactName , COALESCE(COUNT(O.OrderID), 0) AS order_count
           FROM Customers C
           LEFT JOIN
           Orders O ON C.CustomerID = O.CustomerID
           GROUP BY C.CustomerID, C.CompanyName
           ORDER BY order_count ASC"""
    results = db.execute(query)
    results = results.fetchall()
    return results
