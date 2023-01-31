import pandas as pd

def extract():
    df = pd.read_csv("data/chesterfield_25-08-2021_09-00-00.csv")
        
    headerList = ["Timestamp of Purchase", 
                    "Store Name", 
                    "Customer Name", 
                    "Basket Items (Name, Size & Price)", 
                    "Total Price", 
                    "Cash/Card", 
                    "Card Number (Empty if Cash)"]
    # Extracting the file
    df.to_csv("data/chesterfield_25-08-2021_09-00-00.csv", header=headerList, index=False)
    df2 = pd.read_csv("data/chesterfield_25-08-2021_09-00-00.csv")
    print(df2)

extract()