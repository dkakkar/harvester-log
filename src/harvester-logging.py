import smtplib
from kafka import SimpleClient
from kafka.protocol.offset import OffsetRequest, OffsetResetStrategy
from kafka.common import OffsetRequestPayload
import time
import os
import logging

client = SimpleClient('kafka-kafka-1:9092, kafka-kafka-2:9092,kafka-kafka-3:9092')

partitions = client.topic_partitions['TweetsRealTime']
lyst_offset =[0,0]
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ["SENDER_EMAIL"], os.environ["SENDER_PASSWORD"])
    msg = "%s\n%s" % ('Hi', 'CGA-Harvester offline, please restart')
    server.sendmail(os.environ["SENDER_EMAIL"], os.environ["RECEIVER_EMAIL"], msg)
    server.quit()

def response():
    offset_requests = [OffsetRequestPayload(os.environ["TWEET_TOPIC"], p, -1, 1) for p in partitions.keys()]
    offsets_responses = client.send_offset_request(offset_requests)
    return offsets_responses    

def main():
     while 1:
        offsets_responses = response()
        for r in offsets_responses:
            #logging.info("partition = %s, offset = %s"%(r.partition, r.offsets[0]))
            #print ("partition = %s, offset = %s"%(r.partition, r.offsets[0]))
            lyst_offset[1] = r.offsets[0]
            diff =lyst_offset[1]-lyst_offset[0]
            if (diff == 0):
                logging.info("Harvester offline, sending email")
                #print("Harvester offline, sending email")
                send_email()
                time.sleep(3600)
            #print(diff,lyst_offset[1], lyst_offset[0])      
        lyst_offset[0]=lyst_offset[1]
        time.sleep(60)
        
if __name__ == "__main__":
    main()        

 

