import logging
import boto3
import pandas as pd
import numpy as np
import io

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket('deman4-group3')

headerList = ["Timestamp of Purchase", 
                    "Store Name", 
                    "Customer Name", 
                    "Basket Items (Name, Size & Price)", 
                    "Total Price", 
                    "Cash/Card", 
                    "Card Number (Empty if Cash)"]
    
def handler(event, context):
  LOGGER.info(f'Event structure: {event}')
  extract()
  transform()
  normalize_transaction()
  normalize_branch_sales()
      
def extract():
  prefix_objs = bucket.objects.filter(Prefix="2022/") and bucket.objects.filter(Prefix="2023/")
  for obj in prefix_objs:
    key = obj.key
    response = s3_client.get_object(Bucket="deman4-group3", Key=key)
    df = pd.read_csv(response.get("Body"))
    
    with io.StringIO() as csv_buffer:
      df.to_csv(csv_buffer, header=headerList, index=False)
      response2 = s3_client.put_object(Bucket="deman4-group3", Key="extracted/{}".format(key), Body=csv_buffer.getvalue())
    print("\nSuccessful\n")

def transform():
  prefix_objs = bucket.objects.filter(Prefix="extracted/")
  for obj in prefix_objs:
    key = obj.key
    response3 = s3_client.get_object(Bucket="deman4-group3", Key=key)
    df = pd.read_csv(response3.get("Body"))
    print('\nTransform Basket Item\n')
    to_drop = ["Customer Name", "Card Number (Empty if Cash)", "Total Price", "Cash/Card"]
    df.drop(columns=to_drop, inplace=True)
    df['Timestamp of Purchase'] = pd.to_datetime(df['Timestamp of Purchase'])
  
    df.index = np.arange(1, len(df) + 1)
    df = df.reset_index()
    df.rename(columns = {'index':'Customer_Id'}, inplace = True)
    df = df.set_index(['Customer_Id']).astype(str).apply(lambda x:x.str.split(',').explode()).reset_index()
    
    new = df["Basket Items (Name, Size & Price)"].str.split("-", n=2, expand = True)
    df["item_size_name"]= new[0]
    df["item_name_price"]= new[1]
    df["item_price"]= new[2]
    df.drop(columns =["Basket Items (Name, Size & Price)"], inplace = True)   
    new = df["item_size_name"].str.split(" ", n=2, expand = True)
    df["item_size"]= new[0]
    df["item_name2"]= new[1]
    df["item_name1"]= new[2]
    df.drop(columns =["item_size_name"], inplace = True)  
    df["item_price"].fillna(df.item_name_price, inplace = True)   
    df.loc[df["item_size"] == '', 'item_size'] = df['item_name2']   
    df["item_name"] = df["item_name2"] + ' ' + df["item_name1"] + df["item_name_price"]
    df.drop(columns =["item_name_price", "item_name1", "item_name2"], inplace = True)

    df["item_name"] = df["item_name"].str.replace('\d+', '')
    df["item_name"] = df["item_name"].str.replace('Regular+', '')
    df["item_name"] = df["item_name"].str.replace('Large+', '')
    df["item_name"] = df["item_name"].str.replace('\.', '')
    df["item_name"] = df["item_name"].str.strip(' ')
    df["item_price"] = df["item_price"].str.strip(' ')
    
    df.rename(columns = {'item_name':'Item_Name'}, inplace = True)
    df.rename(columns = {'item_size':'Item_Size'}, inplace = True)
    df.rename(columns = {'item_price':'Item_Price'}, inplace = True)
    df.rename(columns = {'Customer_Id':'Transaction_Id'}, inplace = True)
    df.rename(columns = {'Timestamp of Purchase':'Transaction_Date_Time'}, inplace = True)
    df.rename(columns = {'Store Name':'Store_Name'}, inplace = True)
    items_df = df.iloc[:, [0,1,5,4,3,2,]]
    
    with io.StringIO() as csv_buffer:
      items_df.to_csv(csv_buffer, index=False)
      response1 = s3_client.put_object(Bucket="deman4-group3", Key="transformed/basket_items_{}".format(key), Body=csv_buffer.getvalue())
  print("Uploaded Basket items")

def normalize_transaction():
  prefix_objs = bucket.objects.filter(Prefix="extracted/")
  for obj in prefix_objs:
    key = obj.key
    response3 = s3_client.get_object(Bucket="deman4-group3", Key=key)
    df = pd.read_csv(response3.get("Body"))
    print('\nNormalize Transaction\n')
    to_drop = ["Basket Items (Name, Size & Price)", "Customer Name", "Card Number (Empty if Cash)"]
    df.drop(columns=to_drop, inplace=True)
    df['Timestamp of Purchase'] = pd.to_datetime(df['Timestamp of Purchase'])
    df.index = np.arange(1, len(df) + 1)
    df = df.reset_index()
    df.rename(columns = {'index':'Transaction_Id'}, inplace = True)
    df.rename(columns = {'Cash/Card':'Payment_Type'}, inplace = True)
    df.rename(columns = {'Store Name':'Store_Name'}, inplace = True)
    df.rename(columns = {'Timestamp of Purchase':'Transaction_Date_Time'}, inplace = True)
    df.rename(columns = {'Total Price':'Total_Price'}, inplace = True)
    transaction_df = df.iloc[:,  [0,1,2,3,4]]
    
    with io.StringIO() as csv_buffer:
      transaction_df.to_csv(csv_buffer, index=False)
      response2 = s3_client.put_object(Bucket="deman4-group3", Key="transformed/transaction_{}".format(key), Body=csv_buffer.getvalue())
    print("Uploaded Transaction")

def normalize_branch_sales():
  prefix_objs = bucket.objects.filter(Prefix="extracted/")
  for obj in prefix_objs:
    key = obj.key
    response3 = s3_client.get_object(Bucket="deman4-group3", Key=key)
    df = pd.read_csv(response3.get("Body"))
    print('\nNormalize Branch Sales\n')
    to_drop = ["Basket Items (Name, Size & Price)", "Cash/Card", "Customer Name", "Card Number (Empty if Cash)"]
    df.drop(columns=to_drop, inplace=True)
    df.rename(columns = {'Store Name':'Store_Name'}, inplace = True)
    df['Timestamp of Purchase'] = pd.to_datetime(df['Timestamp of Purchase']).dt.date
    df.rename(columns = {'Timestamp of Purchase':'Transaction_Dates'}, inplace = True)
    
    total_spend = df.groupby(['Transaction_Dates']).sum().rename(columns={"Total Price": "Total_Spend"})
    avg_spend = df.groupby(['Transaction_Dates']).mean().rename(columns={"Total Price": "Average_Spend"})
    avg = avg_spend.round(2)
    customer_spend = avg.merge(total_spend, on='Transaction_Dates')
    
    df1 = customer_spend.merge(df, on='Transaction_Dates')
    to_drop = ["Total Price"]
    df1.drop(columns=to_drop, inplace=True)
    df = df1.drop_duplicates()
    df_branch = df.iloc[:, [0,3,1,2]]
  
    with io.StringIO() as csv_buffer:
      df_branch.to_csv(csv_buffer, index=False)
      response3 = s3_client.put_object(Bucket="deman4-group3", Key="transformed/branch_sales_{}".format(key), Body=csv_buffer.getvalue())
    print('Successfully Uploaded!')