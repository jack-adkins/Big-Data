#!/usr/bin/env python3

import importlib
import os
import sys
import time
import random
from click_gen import *

# Initial settings
max_evs = 10000           # Total number of events to generate. Adjust for testing.
n_senders = 5000            # Starting number of senders; this can be increased incrementally.
n_queries = 60           # Number of different queries each sender can send.
delay_mu = 0.01           # Mean delay between queries in seconds.
delay_sigma = 0.001      # Standard deviation of delay (adds variability to simulate human behavior).

# Initialize dispatcher and senders
dispatcher = Dispatcher()
sender_names = shuffle(['sndr%04d' % i for i in range(n_senders)])
senders = [dispatcher.add_sender(Sender(sender_name, n_queries, 0.2, 0.05)) for sender_name in sender_names]


# Generate events
for ev in dispatcher.launch():
    print(ev, flush=True)
    
    # Simulate delay with a Gaussian distribution (delay can go negative, so set a minimum value)
    delay = max(0.05, random.gauss(delay_mu, delay_sigma))  # Minimum delay is set to 0.05 seconds
    time.sleep(delay)
    
    # Decrement max events and check termination condition
    max_evs -= 1
    if max_evs == 0:
        break

    # Optionally increase load dynamically (e.g., by adding senders or reducing delay)
    # For example, add a sender every 1000 events
    if max_evs % 1000 == 0:
        n_senders += 1
        new_sender_name = f'sndr{n_senders:04d}'
        dispatcher.add_sender(Sender(new_sender_name, n_queries, n_senders * 1.0, n_senders * 1.0))
        print(f"Added new sender: {new_sender_name}")

    # Optional: reduce delay incrementally to increase load
    if delay_mu > 0.1:
        delay_mu *= 0.95  # Reduces delay_mu by 5% each time, increasing frequency of events
