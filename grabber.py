import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

url = 'https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a'
response = requests.get(url)
html_string = response.text

soup = BeautifulSoup(html_string, 'lxml')
table = soup.find_all('table')[1]

data = []
row_counter = 0
col_counter = 0

headers = ["State", "Col1","Col2","Col3","Col4","Col5","Col6","Col7","Col8","Col9","Col10"]

rows = table.find_all('tr')
for row in rows:
    if row_counter > 1:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    row_counter += 1

new_table = pd.DataFrame(columns=range(0, 11), index=range(0, 62))
new_table.columns = headers

row_marker = 0

for row in data:
    column_marker = 0
    delim_row = csv.reader(row)
    for ele in delim_row:
        for item in ele:
            if row_marker > 0:
                if column_marker > 0:
                    if item == "--":
                        new_table.iat[row_marker, column_marker] = 0
                    else:
                        new_table.iat[row_marker, column_marker] = float(item)
                else:
                    new_table.iat[row_marker, column_marker] = item
            else:
                new_table.iat[row_marker, column_marker] = item
        column_marker += 1
    row_marker += 1

# Convert to float if possible
for col in new_table:
    try:
        new_table[col] = new_table[col].astype(float)
    except ValueError:
        pass

new_table[['Col1']].plot(kind='hist',bins=[0,5,10,15,20,60],rwidth=0.8)
plt.show()
