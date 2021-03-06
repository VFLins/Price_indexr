import sqlalchemy as alch
from sqlalchemy.ext.declarative import declarative_base
import requests
import re
#import json
from csv import writer, DictWriter
from datetime import date, datetime
from bs4 import BeautifulSoup
from os.path import isfile
from sys import argv

# ERROR MANAGEMENT AND RESULTS FILTERING
def filtered_by_name(name_to_filter: str, pos_filters: list, neg_filters: list) -> bool:
    """
    Checks if the product title has every keyword it is supposed to have,
    and if it does NOT have the keywords it isn't supposed to have,
    with every test passed, return 'True'.
    """
    checks_up = False
    for word in pos_filters:
        if bool( re.search(word.lower(), name_to_filter.lower()) ): checks_up = True
        else: checks_up = False
        if not checks_up: break
    
    if len(neg_filters) > 0 and checks_up:
        for word in neg_filters:
            if not bool( re.search(word.lower(), name_to_filter.lower()) ): checks_up = True
            else: checks_up = False
            if not checks_up: break
    
    return checks_up

def write_message_log(error, message: str):
    # write 4 lines on the error message.
    with open("exec_log.txt", 'a+', newline='', encoding = "UTF8") as log_file:
        # 1. Time and table name
        log_file.write(
            f"[{str(datetime.now())}] {TABLE_NAME}\n")
        # 2 and 3. Message and Exception
        log_file.write(f"{message}:\n{error}\n")
        # 4. Blank line
        log_file.write("\n")

def write_sucess_log(results: list):
    with open("exec_log.txt", 'a+', newline='', encoding = "UTF8") as log_file:
        # 1. Success message with time
        log_file.write(f"{TABLE_NAME} Successfully executed at: " + str(datetime.now()))
        # 2. Number of entries added
        log_file.write(f"\n{str( len(results) )} entries added")
        # 3. Blank line
        log_file.write("\n")

# DEFINE CONSTANTS
DB_CON = argv[1]
SEARCH_FIELD = argv[2].lower()
if len(argv) >= 4:
    LOCATION_CODE = argv[3]

# SORT FILTERS
try:
    # raise error if doesn't start with a positive filter
    if bool(re.match("-", SEARCH_FIELD)): raise TypeError

    SEARCH_KEYWORDS = {}
    SEARCH_KEYWORDS["negative"] = re.split(" -", SEARCH_FIELD)[1:]
    SEARCH_KEYWORDS["positive"] = re.split(" ", re.split(" -", SEARCH_FIELD)[0])
except TypeError as input_error:
    write_message_log(
        input_error, 
        "Your search should start with at least one positive filter and end with negative filters, if any"
    )

POS_KEYWORDS_LOWER = [keyword.lower() for keyword in SEARCH_KEYWORDS["positive"]]
NEG_KEYWORDS_LOWER = [keyword.lower() for keyword in SEARCH_KEYWORDS["negative"]]
TABLE_NAME = f"price_indexr-{'_'.join(POS_KEYWORDS_LOWER)}"

# SETUP PLACE TO SAVE THE DATA 
if DB_CON.upper() == ".CSV":
    CSV_FILENAME = f"{TABLE_NAME}.csv"

    def write_results_csv(results):
        # 'results' must be a list of lists that are ordered as 'fields' in this next line:
        fields = ["Date", "Currency", "Price", "Name", "Store", "Url"]
        # write results
        with open(CSV_FILENAME, "a+", newline="", encoding = "UTF8") as write_file:
            for row in results:
                DictWriter(write_file, fieldnames=fields).writerow(row)

else:
    
    DB_DECBASE = declarative_base()
    DB_ENGINE = alch.create_engine(DB_CON)
    DB_SESSION = alch.orm.sessionmaker(bind = DB_ENGINE)
    DB_MSESSION = DB_SESSION()

    
    DB_METADATA = alch.MetaData()
    current_table = alch.Table(
        TABLE_NAME, DB_METADATA,
        
        alch.Column("Id", alch.Integer, primary_key = True),
        alch.Column("Date", alch.Date),
        alch.Column("Currency", alch.String),
        alch.Column("Price", alch.Float),
        alch.Column("Name", alch.String),
        alch.Column("Store", alch.String),
        alch.Column("Url", alch.String)
    )

    DB_METADATA.create_all(DB_ENGINE, checkfirst = True)
    
    """
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
    """

    def write_results_db(results):
        DB_ENGINE.connect().execute(
            current_table.insert(), results
        )
        """
        trow_line = current_table(
            Date = row["Date"],
            Currency = row["Currency"],
            Price = row["Price"],
            Name = row["Name"],
            Store = row["Store"],
            Url = row["Url"]
        )
        DB_MSESSION.add(trow_line)
        DB_MSESSION.commit()
        """

# COLLECT DATA

SEARCH_HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.121 Safari/537.36"
}
SEARCH_PARAMS = {"q" : SEARCH_FIELD, "tbm" : "shop"}
if len(argv) >= 4: SEARCH_PARAMS["hl"] = LOCATION_CODE

SEARCH_RESPONSE = requests.get(
    "https://www.google.com/search",
    params = SEARCH_PARAMS,
    headers = SEARCH_HEADERS
)

### Ensure data was collected
try:
    try_con = 1
    maximum_try_con = 10
    while try_con <= maximum_try_con:
        
        soup = BeautifulSoup(SEARCH_RESPONSE.text, "lxml")
        soup_grid = soup.find_all("div", {"class": "sh-dgr__gr-auto sh-dgr__grid-result"})
        soup_inline = soup.find_all("a", {"class": "shntl sh-np__click-target"})

        if len(soup_grid) + len(soup_inline) > 0:
            write_message_log(
                f"Connection was successful after trying {try_con} times!",
                f"Using {len(soup_grid)} grid, and {len(soup_inline)} inline results"
            )
            break
        
        try_con = try_con + 1
        if try_con > maximum_try_con: raise ConnectionError(
            "Maximum number of connection tries exceeded"
        )
except TimeoutError as connection_error:
    write_message_log(
        connection_error, 
        "Couldn't obtain data, check your internet connection or User-Agent used on the source code."
    )
    quit()
except Exception as unexpected_error:
    write_message_log(
        unexpected_error, 
        "Unexpected error, closing connection...")
    quit()

### Structure results into a list of dictionaries
output_data = []

for result in soup_grid:
    Name = result.find("h4").get_text()
    if not filtered_by_name(Name, SEARCH_KEYWORDS["positive"], SEARCH_KEYWORDS["negative"]): continue

    Date = date.today()
    Price = result.find("span", {"class" : "a8Pemb OFFNJ"}).get_text().split("\xa0")
    Store = result.find("div", {"class" : "aULzUe IuHnof"}).get_text()
    #Store = result.find("div", {"data-mr" : True})["data-mr"]
    Url = f"https://www.google.com{result.find('a', {'class' : 'xCpuod'})['href']}"

    try:
        current_result = {
            "Date":Date, 
            "Currency":Price[0], 
            "Price":float( Price[1].replace(".", "").replace(",", ".") ), 
            "Name":Name, 
            "Store":Store, 
            "Url":Url}
        output_data.append(current_result)
    except IndexError:
        current_result = {
            "Date":Date, 
            "Currency":None, 
            "Price":float( Price[0].replace(".", "").replace(",", ".") ), 
            "Name":Name, 
            "Store":Store, 
            "Url":Url}
        output_data.append(current_result)
    except Exception as collect_error:
        write_message_log(collect_error, "Unexpected error collecting inline results:")

for result in soup_inline:
    Name = result.find("div", {"class" : "sh-np__product-title translate-content"}).get_text()
    if not filtered_by_name(Name, SEARCH_KEYWORDS["positive"], SEARCH_KEYWORDS["negative"]): continue

    Date = date.today()
    Price = result.find("b", {"class" : "translate-content"}).get_text().split("\xa0")
    Store = result.find("span", {"class" : "E5ocAb"}).get_text()
    Url = f"https://google.com{result['href']}"

    try:
        current_result = {
            "Date":Date, 
            "Currency":Price[0], 
            "Price":float( Price[1].replace(".", "").replace(",", ".") ), 
            "Name":Name, 
            "Store":Store, 
            "Url":Url}
        output_data.append(current_result)
    except IndexError:
        current_result = {
            "Date":Date, 
            "Currency":None, 
            "Price":float( Price[0].replace(".", "").replace(",", ".") ), 
            "Name":Name, 
            "Store":Store, 
            "Url":Url}
        output_data.append(current_result)
    except Exception as collect_error:
        write_message_log(collect_error, "Unexpected error collecting inline results:")

# SAVE

try:
    if DB_CON.lower() == ".csv":
        write_results_csv(output_data)
    else:
        write_results_db(output_data)
    write_sucess_log(output_data)
except Exception as save_error:
    write_message_log(
        save_error,
        "Unexpected error while trying to save the data:"
    )
