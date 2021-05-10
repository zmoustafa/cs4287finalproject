#
#
# Author: Aniruddha Gokhale
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 6, 2020
#
# Purpose:
#
#    Demonstrate the use of Kafka Python streaming APIs.
#    In this example, we use the "top" command and use it as producer of events for
#    Kafka. The consumer can be another Python program that reads and dumps the
#    information into a database OR just keeps displaying the incoming events on the
#    command line consumer (or consumers)
#
import json
import os   # need this for popen
import time # for sleep
from kafka import KafkaProducer  # producer of events
from datetime import datetime
import csv 
import sys
import requests

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)


producer = None
while not producer:
    try:
        producer = KafkaProducer (bootstrap_servers="129.114.25.94:30000", acks=1)  # wait for leader to write to log
    except Exception:
        pass
while True:
    #r1 = requests.get('http://192.168.56.104:8080/stats/flow/1')
    r1 = requests.get('http://192.168.56.104:8080/stats/flow/1')
    #r3 = requests.get('http://192.168.56.104:8080/stats/meter/1')
    #r4 = requests.get('http://192.168.56.104:8080/stats/port/1')
    print("r1", json.dumps(r1.json()))
    #print("r2", 2.json())
    #list_data = [json.dumps(r.json()) for r in [r1, r2, r3, r4]]
    #producer.send("utilization1", value=bytes("test_string",'ascii'))
    
    producer.send("utilization1", value=bytes(json.dumps(r1.json()),'ascii'))
    """producer.send("counts_flows", value=bytes(json.dumps(r2.json()),'ascii'))
    producer.send("packet_ins",value=bytes(json.dumps(r3.json()),'ascii'))
    producer.send("tx_rx", value=bytes(json.dumps(r4.json()),'ascii'))
    """
    time.sleep(5)
# Open csv file 
"""
with open('energy_sorted2.csv') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='|')
    cur_batch = []
    for r in read:
        cur_batch.append(",".join(r))
        if (len(cur_batch) == 1000):
            print("\n".join(cur_batch))
            producer.send("utilization2", value=bytes("\n".join(cur_batch), 'ascii'))
            producer.flush()
            cur_batch = []
"""
"""
sys.exit(0)

# say we send the contents 100 times after a sleep of 1 sec in between
for i in range (100):
    
    # get the output of the top command
    process = os.popen ("top -n 1 -b")

    # read the contents that we wish to send as topic content
    contents = process.read ()
    current_datetime = str(datetime.now())
    # send the contents under topic utilizations. Note that it expects
    # the contents in bytes so we convert it to bytes.
    #
    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #

    data = {current_datetime: contents}
    producer.send ("utilization1", value=bytes(contents, 'ascii'))
    producer.flush ()   # try to empty the sending buffer

    # sleep a second
    time.sleep (1)
"""
# we are done
producer.close ()
    






