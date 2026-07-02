import re 
import json
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager import chrome
from webdriver_manager.chrome import ChromeDriverManager

# Discord webhook URL - replace with your own
DISCORD_WEBHOOK = ""

# How often to check in seconds (default: 5 minutes)
CHECK_INTERVAL = 5 * 60

def notify(supplier, price):
    """Send a Discord notification when the product becomes available."""
    requests.post(DISCORD_WEBHOOK, json={
        "content": f"```Midea PortaSplit is now available at {supplier} for {price}€```"
    })

def parse_websites():
    """Check all supported retailers for Midea PortaSplit availability."""

    # Launch headless Chrome to bypass bot protection
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # --- BAUHAUS ---
    # Price and availability are stored in a dataLayer JS variable
    driver.get("https://www.bauhaus.at/klimaanlagen/midea-klimasplitgeraet-portasplit-12000-btu/p/31934233")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for script in soup.find_all("script"):
        if script.string and "dataLayer" in str(script.string):
            match = re.search(r"var dataLayer=(\{.*?\});", script.string, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                item = data["product"]["item"][0]
                price = item["priceWithTax"]
                # deliverable == "1" means the product can be ordered
                if item["deliverable"] == "1":
                    notify("BAUHAUS", price)

    # --- MEDIA MARKT ---
    # Price and availability are stored in a hydration JSON string embedded in a script tag
    driver.get("https://www.mediamarkt.at/de/product/_midea-portasplit-mobile-klimaanlage-max-raumgrosse-42-m-eek-a-12000-btuh-weiss-2075674.html")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for script in soup.find_all("script"):
        if script.string and "__staticRouterHydrationData" in str(script.string):
            match = re.search(r'window\.__staticRouterHydrationData = JSON\.parse\("(.+?)"\);', script.string, re.DOTALL)
            if match:
                # The JSON is unicode-escaped, so we need to decode it first
                data = json.loads(match.group(1).encode().decode('unicode_escape'))
                product = data["loaderData"]["0-33"]["data"]["cofrProductAggregate"]
                price = product["cofrPriceFeature"]["price"]["amount"]
                status = product["cofrOnlineStatusFeature"]
                # Notify if the product can be purchased, picked up, or delivered
                if status['isAvailableAndBuyable'] or status['isAvailableForPickup'] or status['isAvailableForDelivery']:
                    notify("MediaMarkt", price)

    # --- OBI ---
    # Delivery status is shown in the buybox card, price is in a ld+json script tag
    driver.get("https://www.obi.at/p/3586245/midea-mobile-split-klimaanlage-portasplit")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scripts = soup.find_all("script", {"type": "application/ld+json"})

    # Check if "Derzeit nicht möglich" (currently not possible) is absent from the delivery card
    card = soup.find("div", {"data-testid": "pdp-buybox-hd-card"})
    if card:
        status_div = card.find("div", class_="tw-mt-1")
        if status_div and "Derzeit nicht möglich" not in status_div.text:
            for script in scripts:
                data = json.loads(script.string)
                # Price is either directly in "offers" or nested inside "hasVariant"
                if "offers" in data:
                    notify("OBI", data["offers"][0]["price"])
                    break
                elif "hasVariant" in data:
                    for variant in data["hasVariant"]:
                        if "offers" in variant:
                            notify("OBI", variant["offers"][0]["price"])
                            break

    driver.quit()


while True:
    print(f"Checking... {time.strftime('%H:%M:%S')}")
    try:
        parse_websites()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(CHECK_INTERVAL)
