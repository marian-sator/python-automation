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
from webdriver_manager.chrome import ChromeDriverManager

# Discord webhook URL - replace with your own
DISCORD_WEBHOOK = ""

# How often to check in seconds (default: 5 minutes)
PARSE_FREQUENCY = 60 * 5

cache = {
    "supplier": {}
}

def init_cache(name):
    cache["supplier"].setdefault(name, {"status": {"prev": 0}, "price": None})

def parse_bauhaus(name, content):

    soup = BeautifulSoup(content, "html.parser")

    scripts = soup.find_all("script") 

    for script in scripts:
        if script.string and "dataLayer" in str(script.string):
            match = re.search(r"var dataLayer=(\{.*?\});", script.string, re.DOTALL)
            if match:
            
                data = json.loads(match.group(1))
                
                item = data["product"]["item"][0]
                price = item["priceWithTax"]
                deliverable = item["deliverable"]

                if deliverable == "1":
                    cache["supplier"][name]["status"]["new"] = 1
                else:
                    cache["supplier"][name]["status"]["new"] = 0

                cache["supplier"][name]["price"] = price
                return 
            
    cache["supplier"][name]["status"]["new"] = 0

def parse_media_markt(name, content):

    soup = BeautifulSoup(content, "html.parser")

    scripts = soup.find_all("script")

    for script in scripts:
        if script.string and "__staticRouterHydrationData" in str(script.string):
            match = re.search(r'window\.__staticRouterHydrationData = JSON\.parse\("(.+?)"\);', script.string, re.DOTALL)
            if match:

                json_string = match.group(1).encode().decode('unicode_escape')
                data = json.loads(json_string)

                price = data["loaderData"]["0-33"]["data"]["cofrProductAggregate"]["cofrPriceFeature"]["price"]["amount"]
            
                online_status = data["loaderData"]["0-33"]["data"]["cofrProductAggregate"]["cofrOnlineStatusFeature"]

                can_purchase = online_status['isAvailableAndBuyable']
                can_pickup = online_status['isAvailableForPickup']
                can_deliver = online_status['isAvailableForDelivery']

                if can_purchase or can_pickup or can_deliver:
                    cache["supplier"][name]["status"]["new"] = 1
                else:
                    cache["supplier"][name]["status"]["new"] = 0

                cache["supplier"][name]["price"] = price
                return 
            
    cache["supplier"][name]["status"]["new"] = 0

def parse_obi(name, content):

    soup = BeautifulSoup(content, "html.parser")

    scripts = soup.find_all("script", {"type": "application/ld+json"})

    card = soup.find("div", {"data-testid": "pdp-buybox-hd-card"})

    found = False

    if card:
        status_div = card.find("div", class_="tw-mt-1")
        if status_div and "Derzeit nicht möglich" not in status_div.text:
            for script in scripts:
                if script.string:
                    data = json.loads(script.string)
                    if "offers" in data:
                        price = data["offers"][0]["price"]
                        cache["supplier"][name]["price"] = price
                        found = True
                        break
                    elif "hasVariant" in data:
                        for variant in data["hasVariant"]:
                            if "offers" in variant:
                                price = variant["offers"][0]["price"]
                                cache["supplier"][name]["price"] = price
                                found = True
                                break
                        if found:
                            break 

    cache["supplier"][name]["status"]["new"] = 1 if found else 0

suppliers = [
    {
        "name": "BAUHAUS",
        "url": "https://www.bauhaus.at/klimaanlagen/midea-klimasplitgeraet-portasplit-12000-btu/p/31934233",
        "handler": parse_bauhaus
    },
    {
        "name": "MediaMarkt",
        "url": "https://www.mediamarkt.at/de/product/_midea-portasplit-mobile-klimaanlage-max-raumgrosse-42-m-eek-a-12000-btuh-weiss-2075674.html",
        "handler": parse_media_markt
    },
    {
        "name": "OBI",
        "url": "https://www.obi.at/p/3586245/midea-mobile-split-klimaanlage-portasplit",
        "handler": parse_obi
    }
]

def status_has_changed(name):
    status = cache["supplier"][name]["status"]
    
    if "prev" not in status or "new" not in status:
        return False
    
    if not cache.get("init", False):
        return True

    return status["prev"] != status["new"]

def update_status():

    if cache.get("message_id", False):
        requests.delete(f"{DISCORD_WEBHOOK}/messages/{cache['message_id']}")
        cache["message_id"] = None

    status = "```Midea PortaSplit Tracker```\n"

    for supplier in suppliers:
        v = cache["supplier"][supplier["name"]]

        status_emoji = ":green_circle:" if v["status"]["new"] == 1 else ":red_circle:"
        price_line = f"\nPrice: {v['price']}€" if v["status"]["new"] == 1 else ""

        status += f"Supplier: {supplier['name']}{price_line}\nUrl: <{supplier['url']}>\nStatus: {status_emoji}\n\n"

    res = requests.post(f"{DISCORD_WEBHOOK}?wait=true", json={
        "content": status
    })

    if res.status_code == 200:
        message_data = res.json()
        cache["message_id"] = message_data["id"]
        cache["init"] = True
        
        for supplier in suppliers:
            cache["supplier"][supplier["name"]]["status"]["prev"] = cache["supplier"][supplier["name"]]["status"]["new"]
            cache["supplier"][supplier["name"]]["status"]["new"] = None


def parse_websites():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        has_changes = False
        
        for supplier in suppliers:

            driver.get(supplier["url"])

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            init_cache(supplier["name"])

            supplier["handler"](supplier["name"], driver.page_source)

            if not has_changes and status_has_changed(supplier["name"]):
                has_changes = True

        if has_changes:
            update_status()
    
    finally:
        driver.quit()


while True:
    print(f"Checking... {time.strftime('%H:%M:%S')}")
    try:
        parse_websites()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(PARSE_FREQUENCY)
