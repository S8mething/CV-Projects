# <p align="center">Containers, Database and Visualization</p>

<p align="center">
  <img width="800" height00" src="https://user-images.githubusercontent.com/99510843/191127263-6ebf06ce-4c42-4e87-8e16-56223b445e6c.png">
</p>

## Tools used:

- AWS VPC 
- AWS RDS  
- AWS EFS
- AWS ECS
- AWS EC2
- AWS Cloudformation                                                                                                                                        
- Docker
- Docker images phpMyAdmin and Metabase
                                                                                                                                      
                                                                                                                                        
## Steps:
                                                                                                                                        
- Create Parameter in Parameter store for Administrator RDS Database password
                                                                                                                                        
![image](https://user-images.githubusercontent.com/99510843/191348660-7a74c5ae-d82f-491f-b0f8-28c92ca25b1a.png)                                                                                                                                     
- Create Cloudformation stack with ```cloudformation-stack.yaml``` template. Parameters:
  - ```AdminMySQLName``` ***Admin RDS MYSQL Name***
  - ```AmiECSId``` - ***Referense for image id from AWS Parameter Store for ECS EC2 Instances***
  - ```DBInstanceType``` - ***RDS Instance type***
  - ```ECSInstanceType``` - ***ECS EC2 Instance type***
  - ```KeyNameECSEC2``` ***KeyPair name for SSH connection to ECS EC2 Instances***
  - ```LogGroupName``` ***Name of LogGroup for petclinic app containers***
  - ```MySQLAdminPassParameterName``` ***Parameter Name from Parameter Store for Administrator RDS Database password***
  - ```MyIp```- ***Ip or CIDR Range for connection to ECS Containers and Instances***
                                                                                                                                        
![image](https://user-images.githubusercontent.com/99510843/191347355-ac771309-6a86-4934-b6b3-1f2cff5f0c8a.png)

- Connect to Metabase web page
                                                                                                                                        
![image](https://user-images.githubusercontent.com/99510843/191347756-9847f606-ce56-4fb5-bd6a-036bcd3cc699.png)                                                                                                                                    
![image](https://user-images.githubusercontent.com/99510843/177016198-3068196f-ae41-4f40-bbe4-f36a4e1940ba.png)

- Configure Metabase:
   - Choose the default language;
   - Create a Metabase Administrator account;
   - Link the database to Metabase.
   - Host = RDS Endpoint

![image](https://user-images.githubusercontent.com/99510843/177016280-1a6e018d-ea30-469f-9492-c30a0510b71f.png)

- Create database structure with phpMyAdmin

![image](https://user-images.githubusercontent.com/99510843/177016321-0a098261-87d8-45c5-b01e-edc3792d46d5.png)

![image](https://user-images.githubusercontent.com/99510843/177016329-31ed973b-ddde-4929-82df-9295aaab7d66.png)

###### Create Products Table

```
CREATE TABLE products
(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    category VARCHAR(100),
    price DOUBLE,
    stock INT
);
```
###### Adding data to ```products```

```
INSERT INTO products(name, category, price, stock)
VALUES
    ('Superkey 84', 'keyboard', 50, 7),
    ('MX Click', 'mouse', 39, 2),
    ('Type Pro 2022', 'keyboard', 115, 4),
    ('GL Zoom', 'webcam', 70, 13),
    ('LEDD Future 5K', 'monitor', 450, 1);
```

###### Create Customers Table

```
CREATE TABLE customers
(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    age INT,
    email VARCHAR(100)
);
```
###### Adding data to ```customers```

```
INSERT INTO customers(first_name, last_name, age, email)
VALUES 
    ('James', 'Cooper', 27, 'james.cooper@mail.com'),
    ('Ruth', 'Dugan', 45, 'ruth.dugan@mail.com'),
    ('Victor', 'Jackson', 14, 'victor.jackson@mail.com'),
    ('Elizabeth', 'Sullivan', 27, 'elizabeth.sullivan@mail.com'),
    ('Connie', 'Jackson', 33, 'connie.jackson@mail.com');
```

###### Create Orders Table

```
CREATE TABLE orders
(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    order_date DATE,
    cost DOUBLE
);
```
###### Adding data to ```orders```

```
INSERT INTO orders(customer_id, product_id, order_date, cost)
VALUES
    (1, 3, '2022-01-02', 115),
    (1, 5, '2022-01-02', 450),
    (3, 4, '2022-01-12', 70),
    (2, 4, '2022-01-17', 70),
    (1, 1, '2022-02-01', 50),
    (4, 2, '2022-02-14', 39),
    (4, 3, '2022-02-27', 115),
    (5, 3, '2022-02-28', 115),
    (1, 3, '2022-03-03', 115),
    (2, 1, '2022-03-18', 50);
```

- Create dashboards with Metabase. 4 statistics will be made from the data recently added in the database:
```The most purchased products```
```The most purchased categories of products```
```The best customers```
cThe sales revenues```

- Add the newly created database (computer_store), to do this go to Admin settings, then Databases and select Add database

![image](https://user-images.githubusercontent.com/99510843/177016531-0e6d4a76-c97d-474b-92d4-681b2764ed2b.png)


![image](https://user-images.githubusercontent.com/99510843/177016521-9a197a7f-0dc2-4da6-9072-53aa12379f08.png)

- Open the SQL Query menu, then select the Computer Store database

![image](https://user-images.githubusercontent.com/99510843/177016584-2ca5e173-d01f-45f2-b4f1-e5bda36e2c9b.png)

###### Most purchased products

```
SELECT products.name, COUNT(*) AS purchased
FROM products, orders
WHERE products.id=orders.product_id
GROUP BY products.name
ORDER BY COUNT(*) DESC
```

###### Most purchased categories of products

```
SELECT products.category, COUNT(*) AS purchased
FROM products, orders
WHERE products.id=orders.product_id
GROUP BY products.category
ORDER BY COUNT(*) DESC
```

###### Best customers

```
SELECT CONCAT(customers.first_name,' ',customers.last_name) AS customer, COUNT(*) AS purchases
FROM customers, orders
WHERE customers.id=orders.customer_id
GROUP BY customer
ORDER BY COUNT(*) DESC
```

###### Sales revenues

```
SELECT SUM(orders.cost)
FROM orders
```
- Create a Dashboard

![image](https://user-images.githubusercontent.com/99510843/177016690-1132c5e1-6969-43a2-92ed-6bebd58b09bd.png)

![image](https://user-images.githubusercontent.com/99510843/177016724-cd10fac5-bf1a-46cb-a3e2-c0a630b2ab35.png)

![image](https://user-images.githubusercontent.com/99510843/177016727-63db51fa-cb80-4af4-a712-acb6bbc68836.png)












                                                                                                                                        

