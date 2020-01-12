import urllib.request as wb
from modules import pylavor
import logging
import datetime

logging.basicConfig(level=logging.DEBUG) #filename='upTimer.log',level=logging.DEBUG, filemode='w')

class WebPage():
    def __init__(self, webpageName, single_page_data):
        self.name = webpageName
        self.webAddress = single_page_data["webAddress"]
        self.contactEmail = single_page_data["contactEmail"]
        self.contactNumber = single_page_data["contactNumber"]
    
    def __str__(self):
        print(f"Website {self.name}, address: {self.webAddress}, started monitoring: {self.startMonitoringDate}")

    def check_if_online(self):
        if wb.urlopen(self.webAddress).getcode() == 200:

            logging.info(f"{self.name} - Online")
            return True

        else:
            logging.info(f"{page} - Offine")
            return False

    def previous_insertion(self):
        logging.debug("Getting data from the database to check the previous insertion.")
        all_insertions = pylavor.json_read(f"data/databases", f"{pylavor.get_valid_filename(self.name)}.json")
        logging.debug(list(all_insertions.keys()))

        return all_insertions[list(all_insertions.keys())[-1]]["status"]

    def add_insertion(self):
        logging.info("Logging the event in to the webpage database.")

        filename = f"{pylavor.get_valid_filename(self.name)}.json"
        location = f"data/databases"
    
        all_insertions = pylavor.json_read(location, filename)
        
        now = datetime.datetime.now()
        
        new_insertion = {}

        if all_insertions[list(all_insertions.keys())[-1]]["status"] == True:
            new_insertion["status"] = False
            new_insertion["date"] = now.__str__()
            

        else:
            new_insertion["status"] = True
            new_insertion["date"] = now.__str__()
        
        all_insertions[len(all_insertions)] = new_insertion
        pylavor.json_write(location, filename, all_insertions)

        logging.info("Event inserted correctly.")

def newWebpage(webpageName, webAddress, contactEmail, contactNumber):
    logging.info("Adding a new webpage to the program.")
    webPages = get_webpage_database()

    webPage = {webpageName: {
        "webAddress": webAddress,
        "contactEmail": contactEmail,
        "contactNumber": contactNumber
            }
        }

    now = datetime.datetime.now()
    new_insertion = {}
    new_insertion["status"] = True
    new_insertion["date"] = now.__str__()
        
    all_insertions = {0: new_insertion}
    
    location = f"data/databases"
    filename = f"{pylavor.get_valid_filename(webpageName)}.json"
    
    pylavor.json_write(location, filename, all_insertions)
    logging.debug("First event inserted correctly.")


    webPages.update(webPage)
    save_webpage_database(webPages)

    logging.debug(f"Successfully added the webpage: {webpageName}")

class WebDictionary():
    def __init__(self):
        self.webPages = []

    def __str__(self):
        print(f"This WebDictionary holds {len(self.webPages)} webpages.")

    def addWebpage(self, webpage: WebPage):
        logging.debug("Adding the webpage to the WebDictionary.")
        self.webPages.append(webpage)


def powerUp():
    logging.info("Starting Up")
    webpages_to_check = get_webpage_database()

    online_to_send = WebDictionary()
    offline_to_send = WebDictionary()

    for page in webpages_to_check:
        webPage = WebPage(page, webpages_to_check[page])
        logging.info(f"Working on {webPage.name}")

        if webPage.check_if_online() == True:
            logging.info(f"The webpage {webPage.name} is online.")

            if webPage.previous_insertion():
                logging.debug("The webpage was also previously online.")

            else:
                logging.debug("The webpage was previously OFFLINE.")
                logging.debug("Creating new insertion, that the webpage went back online.")
                webPage.add_insertion()
                logging.debug("Adding the webpage to the list to send an warning.")
                online_to_send.addWebpage(webPage)

        else:
            logging.info("The webpage is OFFLINE.")
            
            if webPage.previous_insertion():
                logging.debug("The webpage was also previously online.")
                webPage.add_insertion()
                logging.debug("Adding the webpage to the list to send an warning.")
                offline_to_send.addWebpage(webPage)

            else:
                logging.debug("The webpage was previously OFFLINE.")


def get_webpage_database():
    webpages_to_check = pylavor.json_read("data", "webpages_to_check.json")
    logging.debug("Webpages loaded from json correctly.")
    return webpages_to_check

def save_webpage_database(webpages_to_save):
    pylavor.json_write("data", "webpages_to_check.json", webpages_to_save)
    logging.debug("Webpages saved to json correctly.")

if __name__ == "__main__":
    powerUp()
    #newWebpage("Motion Olmo", "https://motion.razor.si", "andrej.zubin@razor.si", "031310333")
