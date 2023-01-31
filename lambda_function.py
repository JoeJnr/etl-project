import psycopg2
import os

def lambda_handler(event, context):
    print("event collected is {}".format(event))
    
    dbname = os.getenv('dbname')
    host = os.getenv('host')
    user = os.getenv('user')
    password = os.getenv('password')
    iam_role = os.getenv('iam_role')
    port = 5439
    
    # Define connection string
    conn_string = "postgresql://{}:{}@{}:{}/{}".format(
         user,
         password,
         host,
         port,
         dbname
    )
  
    # Test connection
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    print('connected')
    
    store_table = """
         CREATE TABLE if not exists branch_sales(
            Transaction_Dates DATE,
            Store_Name VARCHAR(250),
            Average_Spend DECIMAL(10,2),
            Total_Spend DECIMAL(10,2)
         );
         """
    cur.execute(store_table)
  
    transactions = """
        CREATE TABLE if not exists transactions(
            Transaction_id INT NOT NULL PRIMARY KEY,
            Transaction_Date_Time TIMESTAMP,
            Store_Name VARCHAR(50),
            Total_price DECIMAL(10,2),
            Payment_Type VARCHAR(50)
        );
    """ 
    cur.execute(transactions)
    
    basket_items_table = """
        CREATE TABLE if not exists basket_items(
            Transaction_Id INT NOT NULL,
            Transaction_Date_Time TIMESTAMP,
            Item_Name VARCHAR(250),
            Item_Size VARCHAR(50),
            Item_Price DECIMAL(6,2),
            Store_Name VARCHAR(250),
            FOREIGN KEY (Transaction_Id) REFERENCES transactions(Transaction_Id)
        );
        """
    cur.execute(basket_items_table)
    conn.commit()
    print('print successfully created table')
    
    file_path = "s3://deman4-group3/transformed/branch_sales_extracted/"
    file_path2 = "s3://deman4-group3/transformed/transaction_extracted/"
    file_path3 = "s3://deman4-group3/transformed/basket_items_extracted/"
    
  
    # Copy data
    sql_query = """
         COPY branch_sales
         FROM '{}'
         iam_role '{}'
         csv
         IGNOREHEADER 1 
         ;
    """.format(file_path, iam_role)
    
    cur.execute(sql_query)
  
    sql_query2 = """
         COPY transactions
         FROM '{}'
         iam_role '{}'
         csv
         IGNOREHEADER 1
         ;
    """.format(file_path2, iam_role)
    
    cur.execute(sql_query2)
    
    sql_query3 = """
         COPY basket_items
         FROM '{}'
         iam_role '{}'
         csv
         IGNOREHEADER 1 
         ;
    """.format(file_path3, iam_role)
    
    cur.execute(sql_query3)
    print('successfully loaded')
    conn.commit()
    cur.close()
    conn.close()
    print('done')