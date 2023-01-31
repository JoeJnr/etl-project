import pandas as pd
from unittest.mock import patch

def extract():
    df = pd.read_csv("chesterfield_25-08-2021_09-00-00.csv")
    headerList = ["Timestamp of Purchase", 
    "Store Name", 
    "Customer Name", 
    "Basket Items (Name, Size & Price)", 
    "Total Price", 
    "Cash/Card", 
    "Card Number (Empty if Cash)"]
    df.to_csv("chesterfield_25-08-2021_09-00-00.csv", header=headerList, index=False)
    df2 = pd.read_csv("chesterfield_25-08-2021_09-00-00.csv")
    print(df2)
    return df2

@patch('builtins.print')
def test_extract(mock_print):
    df2 = extract()
    mock_print.assert_called_with(df2)