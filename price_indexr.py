import sqlalchemy as alch
import requests
import json
from csv import writer, DictWriter
from bs4 import BeautifulSoup
from path import isfile
from sys import argv


# DEFINE CONSTANTS
DB_CON = argv[1]

SEARCH_FIELD = argv[2]
SEARCH_KEYWORDS = SEARCH_FIELD.split(" ")
SEARCH_HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
SEARCH_PARAMS = {
    "q" : SEARCH_FIELD,
    "tbm" : "shop"
}
SEARCH_RESPONSE = requests.get(
    "https://www.google.com/search",
    params = SEARCH_PARAMS,
    headers = SEARCH_HEADERS
)

TABLE_NAME = "price_indexr-" + "_".join(SEARCH_KEYWORDS)

# SETUP PLACE TO SAVE THE DATA 
if DB_CON.upper() == ".CSV":
    CSV_FILENAME = TABLE_NAME + ".csv"

    def write_results_csv(results):
        # 'results' must be a list ordered as 'fields' in this next line:
        fields = [Date, Currency, Price, Name, Store, Url]
        with open(CSV_FILENAME, 'a+', newline='', encoding = "UTF8") as write_file:
            for row in results:
                DictWriter(write_file, fieldnames=fields).writerow(row)

else:
    DB_DECBASE = declarative_base()
    DB_ENGINE = alch.create_engine(DB_CON)
    DB_SESSION = sessionmaker(bind = DB_ENGINE)
    DB_MSESSION = DB_SESSION()

    class prices_table(DB_DECBASE):
        __tablename__ = TABLE_NAME
        Id = alch.Column(alch.Integer, primary_key = True)
        Date = alch.Column(alch.Date)
        Currency = alch.Column(alch.String)
        Price = alch.Column(alch.Float)
        Name = alch.Column(alch.String)
        Store = alch.Column(alch.String)
        Url = alch.Column(alch.String)

        def __repr__(self):
            return "<entry(Date={}, Currency={}, Price={}, Name={}, Store={}, Url={})>".format(
            self.Date, self.Currency, self.Price, self.Name, self.Store, self.Url)
    
    def write_results_db(results):
        for row in results:
            trow_line = prices_table(
                Date = row[0],
                Currency = row[1],
                Price = row[2],
                Name = row[3],
                Store = row[4],
                Url = row[5]
            )
            DB_MSESSION.add(trow_line)
            DB_MSESSION.commit()
    
# COLLECT DATA

# SAVE

print( BeautifulSoup(SEARCH_RESPONSE.text, 'lxml') )
