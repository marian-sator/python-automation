# API Monitor - monitors URL availability and response times
# Author: Marian Sator

import requests 
import time 

urls = [
    "https://google.com",
    "https://github.com",
    "https://thisisnotavalidurl123.com",
]

while True:
    
    for url in urls:
        
        start = time.time()
        
        try:
            res = requests.get(url, timeout = 5)
        
            if res.status_code != 200:
                print(f"{url} - FAILED. Status: {res.status_code}")
                continue 
                
            duration = (time.time() - start) * 1000 
            
            print(f"{url} - OK - {duration}ms")

        except requests.exceptions.Timeout:
            print(f"{url} - FAILED - Timeout")
            
        except requests.exceptions.ConnectionError:
            print(f"{url} - FAILED - Connection Error")
            
        except Exception as e:
            print(f"{url} - FAILED - {e}")
   
    time.sleep(5)
