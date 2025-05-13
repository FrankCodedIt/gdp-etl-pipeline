# Code for ETL operations on Country-GDP data

# Importing the required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

# -----------------------Initialization-----------------------------#

# Initialize all the known entities
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ["Country", "GDP_USD_millions"]
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'
log_file = './etl_project_log.txt'

# -------------------------Log Function ---------------------------- #
##record a message, along with its timestamp, in the log_file
''' This function logs the mentioned message at a given stage of the 
    code execution to a log file. Function returns nothing'''
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 

# -----------------------Extraction-----------------------------#
''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
def extract(url, table_attribs):
    # Log the start of the Extraction process of the ETL pipeline 
    log_progress("Logging...... Extraction Process Started")
    # Loading the webpage for Webscraping
    html_page = requests.get(url).text
    #Parse the text into an HTML object
    data = BeautifulSoup(html_page, 'html.parser')
    #Create an empty pandas DataFrame named df with columns as the table_attribs
    df = pd.DataFrame(columns=table_attribs)
    #Extract all 'tbody' attributes of the HTML object and then extract all the rows of the index 2 table using the 'tr' attribute.
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')

    '''Check the contents of each row, having attribute ‘td’, for the following conditions.
        a. The row should not be empty.
        b. The first column should contain a hyperlink.
        c. The third column should not be '—'.'''
    for row in rows:
        col = row.find_all('td')
        if len(col) !=0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0], "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)

    # Log the end of the Extraction process of the ETL pipeline 
    log_progress("Logging...... Extraction Process Complete")
    return df

# -----------------------Transformation-----------------------------#
''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
def transform(df):
    # Log the start of the Transformation process of the ETL pipeline 
    log_progress("Logging...... Transformation Process Started")
    # Convert the contents of the 'GDP_USD_millions' column of df dataframe from currency format to floating numbers.
    GDP_list = df["GDP_USD_millions"].tolist()
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]

    # Divide all these values by 1000 and round it to 2 decimal places.
    GDP_list = [np.round(x/1000,2) for x in GDP_list]
    df["GDP_USD_millions"] = GDP_list

    # Modify the name of the column from 'GDP_USD_millions' to 'GDP_USD_billions'.
    df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})

    # Log the end of the Transformation process of the ETL pipeline 
    log_progress("Logging...... Transformation Process Completed")
    return df

# -----------------------Load-----------------------------#
''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
def load_to_csv(df, csv_path):
    df.to_csv(csv_path)
    # Log the load to CSV process of the ETL pipeline 
    log_progress("Logging...... Load to CSV Process Completed")
    
''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    # Log the load to SQL Database process of the ETL pipeline 
    log_progress("Logging...... Load to SQL Database Process Completed")

# -----------------------Query the database-----------------------------#

''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attribs)

log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df)

log_progress('Data transformation complete. Initiating loading process')

load_to_csv(df, csv_path)

log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect('World_Economies.db')

log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')

query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
run_query(query_statement, sql_connection)

log_progress('Process Complete.')

sql_connection.close()