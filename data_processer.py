# Data Processor - processes large transaction datasets with performance tracking
# Author: Marian Sator

import time 
import random 

def generate_transactions(count):
    customers = ["Marian", "Anna", "Bob", "Clara", "David", "Eva", "Frank", "Grace"]
    types = ["purchase", "refund"]
    
    return [
        {
            "id": i,
            "customer": random.choice(customers),
            "amount": random.randint(10, 500),
            "type": random.choice(types)
        }
        for i in range(count)
    ]
    
def process_transactions(transactions, sort=True):

    # dictionary lookup instead of iteration - O(1) performance
    id_cache = {}
  
    processed = {}
    start = time.time()

    # single pass to avoid O(n²) complexity
    for entry in transactions:   
        # skip duplicates and non-purchases in single pass - avoids multiple iterations
        if not id_cache.get(entry["id"], False) and entry["type"] == "purchase":
            id_cache[entry["id"]] = True 
            processed[entry["customer"]] = processed.get(entry["customer"], 0) + entry["amount"]

    # sort only if needed - avoids unnecessary computation
    processed_sorted = sorted(processed.items(), key = lambda entry: entry[1], reverse=True) if sort else None
    
    processing_time = (time.time() - start) * 1000
    
    return processed, processed_sorted, processing_time
    

transactions = generate_transactions(100000)

processed, processed_sorted, processing_time = process_transactions(transactions)

print(f"Processing transcations took {processing_time}ms.")
