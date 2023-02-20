# This script checks the biggest retail shop in Cyprus and checks if there is a Playstation 5 available for purchase.
# If there is, it sends an email (using gmail) with the store name and url to buy it.

from bs4 import BeautifulSoup as bs
import re
from urllib.request import Request, urlopen
import smtplib
import ssl
import schedule
import time
import logging

# Email account information
sender_email = "your_email@example.com"
sender_password = "your_password"
receiver_email = "receiver_email@example.com"
# SMTP server information
smtp_server = "smtp.gmail.com"
smtp_port = 587
# Create a secure SSL context
context = ssl.create_default_context()

# Set up logging
logging.basicConfig(filename='ps5.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


# List of dictionaries containing store URLs and search keywords
stores = [
    {"name": "Bionic", "url": "https://bionic.com.cy/products/c/game-consoles?keywords=playstation%205", "keyword": "Digital Edition"},
    {"name": "Stefanis", "url": "https://www.stephanis.com.cy/el/products/gaming/gaming-consoles/all-gaming-consoles", "keyword": "SONY"},
    {"name": "Kotsovolos", "url": "https://www.kotsovolos.cy/gaming-gadgets/playstation-5", "keyword": "Κονσόλες PS5"},
    {"name": "Electroline", "url": "https://electroline.com.cy/product-category/computing/gaming-products/gaming-consoles/?filter100=brand&filter100value1=sony", "keyword": "Digital Edition"}
]

# Function to check a store's URL for a search keyword and send an email if found
def check_store(store):
    url = store["url"]
    keyword = store["keyword"]
    name = store["name"]
    website_soup = bs(urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8'), 'html.parser')
    if re.findall(keyword, str(website_soup)):
        send_email(name, url)
        logging.info(f"Found in {name} Store ! ! ! !")
    else:
        logging.info(f"Not found in {name} Store")    

# Function to send email
def send_email(name, url):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender_email, sender_password)
        message = f"Subject: A PlayStation 5 Digital Edition is found in {name}!\n\nURL: {url}"
        server.sendmail(sender_email, receiver_email, message)
        logging.info(f"Email is send to {receiver_email} Store")

# Make a job to me scheduled and run every day
def scheduled_job():
    for store in stores: check_store(store)

# Schedule the task to run in a specific timeframes.
schedule.every().hour.at(":00").do(scheduled_job)


while True:
    schedule.run_pending()
    time.sleep(1)
