import sirius_db as db

# creating tables for schema design
def create_schema_tables():

    store_table = """
        CREATE TABLE if not exists branch_sales(
            Store_Name VARCHAR(250),
            Average_Spend DECIMAL(10,2),
            Total_Spend DECIMAL(10,2)
        );
        """
    db.cursor.execute(store_table)

    transactions = """
        CREATE TABLE if not exists transactions(
            Transaction_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            Transaction_Date_Time DATETIME,
            Store_Name VARCHAR(50),
            Total_price DECIMAL(10,2),
            Payment_Type VARCHAR(50)
        );
    """ 
    db.cursor.execute(transactions)

    basket_items_table = """
        CREATE TABLE if not exists basket_items(
            Transaction_Id INT NOT NULL,
            Item_Name VARCHAR(250),
            Item_Size VARCHAR(50),
            Item_Price DECIMAL(6,2),
            Quantity INT NOT NULL,
            FOREIGN KEY (Transaction_Id) REFERENCES transactions(Transaction_Id) ON DELETE CASCADE
        );
        """
    db.cursor.execute(basket_items_table)

    print("Schema tables created!.")

create_schema_tables()
db.connection.commit()
db.cursor.close()
db.connection.close()