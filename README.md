#Setup

The program needs info about the email credentials. They are stored in the file data/email_data.json. the data should be in the format:
>{"smtp_server": "smtp.emailserver.com", "smtp_port": "465", "from_address": "email@sender.com", "pass": "Password123"}

Furthermore, the program need a central database with the webpage data, stored in data/webpages_to_check.json in the format:
>{"Banana Webpage": {"webAddress": "https://www.banana.com", "contactEmail": "server.admin@banana.com", "contactNumber": "031310333"}}

But the program wont start withough those files, so after starting the program once, it will create empty ones, that you can populate.

