import pandas as pd
import sirius_db as db

# inserting into tables
def insert_into_branch():
    # inserting branch
    data1 = pd.read_csv ('data/branch.csv')   
    df1 = pd.DataFrame(data1)
    for row in df1.itertuples():
        sql = """
            INSERT INTO branch_sales (
                Store_Name, Average_Spend, Total_Spend) 
                VALUES (%s,%s,%s)
        """ 
        val = (row.Store_Name, row.Average_Spend, row.Total_Spend)
        db.cursor.execute(sql, val)
    print("Branch Sales Rows Inserted!.")

def insert_into_transaction():    
    # inserting transaction
    data3 = pd.read_csv ('data/transaction.csv')   
    df3 = pd.DataFrame(data3)
    for row in df3.itertuples():
        sql = """
        INSERT INTO transactions (
            Transaction_Id, Transaction_Date_Time,
            Store_Name, Total_Price, Payment_Type) 
            VALUES (%s,%s,%s,%s,%s)
        """ 
        val = (row.Transaction_Id, row.Transaction_Date_Time, 
        row.Store_Name, row.Total_Price, row.Payment_Type)
        db.cursor.execute(sql, val)
    print("Transaction Rows Inserted!.")

def insert_into_basket():
    # inserting basket_items
    data2 = pd.read_csv ('data/basket_items.csv')   
    df2 = pd.DataFrame(data2)
    for row in df2.itertuples():
        sql = """
        INSERT INTO basket_items (
            Transaction_Id, Item_Name, 
            Item_Size, Item_Price, Quantity)
            VALUES (%s,%s,%s,%s,%s)
        """ 
        val = (row.Transaction_Id, row.Item_Name, 
        row.Item_Size, row.Item_Price, row.Quantity)
        db.cursor.execute(sql, val)
    print("Basket Items Rows Inserted!.")


insert_into_branch()
insert_into_transaction()
insert_into_basket()
db.connection.commit()
db.cursor.close()
db.connection.close()