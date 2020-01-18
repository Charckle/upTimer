import urllib.request as wb
from modules import pylavor
from modules import email_sender
import logging
import datetime

logging.basicConfig(level=logging.INFO) #filename='upTimer.log',level=logging.DEBUG, filemode='w')

class WebPage():
    def __init__(self, webpageName, single_page_data):
        self.name = webpageName
        self.webAddress = single_page_data["webAddress"]
        self.contactEmail = single_page_data["contactEmail"]
        self.contactNumber = single_page_data["contactNumber"]
        self.last_contact_time = ""
    
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
        self.last_contact_time = now.__str__()

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

    def send_alert_email(self, status, timedate):

        logging.info(f"Starting the process of sending an email alert for {self.name}.")

        if status == True:
            status = "ONLINE"
        else:
            status = "OFFLINE"
        
        location = "data"
        filename = "email_data.json"

        logging.info("Loading email credentials.")
        try:
            email_credentials = pylavor.json_read(location, filename)

        except:
            logging.debug("Could not locate the .json file with the email credentials, creating one.")
            email_credentials = {"smtp_server": "smtp.emailserver.com", "smtp_port": "465", "from_address": "email@sender.com", "pass": "Password123"}
            pylavor.json_write(location, filename, email_credentials)
            
        
        email_data = {"smtp_server": email_credentials["smtp_server"], "smtp_port": email_credentials["smtp_port"], "from_address": email_credentials["from_address"], "pass": email_credentials["pass"], "to_address": self.contactEmail, "subject": f"Webpage {self.name} is {status}", "body": f"The webpage {self.name}, on the URL {self.webAddress}, went {status} at {timedate}."}
        
        logging.info("Sending alert email.")
        email_sender.sendEmail(email_data)


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
    def __init__(self, status):
        self.webPages = []
        self.status = status

    def __str__(self):
        print(f"This WebDictionary holds {len(self.webPages)} webpages.")

    def addWebpage(self, webpage: WebPage):
        logging.debug("Adding the webpage to the WebDictionary.")
        self.webPages.append(webpage)

    def send_emails(self):
        #check if emails were already sent today
        location = "data"
        if self.status == True:
            filename = "sent_email_online.json"
        else:
            filename = "offline_email_online.json"

        logging.debug("Loading the .json of sent emails.")
        list_of_sent_email = pylavor.json_read(location, filename)
        
        nth_day_year = datetime.now().timetuple().tm_yday

        if list_of_sent_email["day"] == nth_day_year:
            for page in self.webPages:
                if page.name not in list_of_sent_email["pages_sent"].values():
                    page.send_alert_email(self.status, page.last_contact_time)
                    list_of_sent_email["pages_sent"][len(list_of_sent_email["pages_sent"])] = page.name

def powerUp():
    logging.info("Starting Up")
    webpages_to_check = get_webpage_database()

    online_to_send = WebDictionary(True)
    offline_to_send = WebDictionary(False)

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
    
    logging.info("Starting to send emails of ONLINE pages.")
    online_to_send.send_emails()
    logging.info("Starting to send emails of OFFLINE pages.")
    offline_to_send.send_emails()
    

def get_webpage_database():
    try:
        webpages_to_check = pylavor.json_read("data", "webpages_to_check.json")
        logging.debug("Webpages loaded from json correctly.")

    except:
       webpages_to_check = pylavor.json_read("data", "webpages_to_check.json")
       logging.debug("Webpages loaded from json correctly.")

    return webpages_to_check

def save_webpage_database(webpages_to_save):
    pylavor.json_write("data", "webpages_to_check.json", webpages_to_save)
    logging.debug("Webpages saved to json correctly.")

if __name__ == "__main__":
    if not pylavor.check_file_exists("data/webpages_to_check.json") or pylavor.check_file_exists("data/email_data.json"):
        logging.debug("All needed files were found to exists, the program can run as expected.")
        powerUp()
        #newWebpage("Motion Olmo", "https://motion.razor.si", "andrej.zubin@razor.si", "031310333")
    else:
        logging.info("The main webpages db or the db with the email credentials were not found. Will go trough and create the ones that are not found.")
        if  not pylavor.check_file_exists("data/webpages_to_check.json"):
            logging.info("The webpages DB file was not found. Creating one.")
            
            newWebpage("Internet Holidays", "http://ih.razor.si", "info@ksok.si", "031301330")
            
        if not pylavor.check_file_exists("data/email_data.json"):
            logging.info("The email credentials file was not found. Creating one.")
            email_credentials = "smtp_server": "smtp.emailserver.com", "smtp_port": "465", "from_address": "email@sender.com", "pass": "Password123"}
            pylavor.json_write("data", "email_data.json", email_credentials)

