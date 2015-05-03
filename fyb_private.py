# Copyright Adam Parker 2015, MIT Liscense

import httplib
import time
import hmac
import hashlib
import urllib

def exch_url(exchange):
    url = "www.fyb"
    if(exchange == 1):
        url += "sg.com"
    else:
        url += "se.se"
    if(exchange == -1):
        url = "private-anon-468445e24-fyb.apiary-mock.com"
    return url
    
def exch_request(url, exchange, item, key, sig, data):
    if(exchange == 1):
        path = "/api/SGD/" + item
    else:
        path = "/api/SEK/" + item
    if(exchange == -1):
        path = "/" + item
    
    hsock = httplib.HTTPSConnection(url)
    signature = hmac.new(sig, data, hashlib.sha1)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "key" : key, "sig": signature.digest().encode('hex')}
    hsock.request("POST", path, body=data, headers=headers)
    
    r = hsock.getresponse()
    
    if(r.status != 200):
        print r.status
        
    print r.read()
    return r.read()


class fyb_private:
    
    def test(self):
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp)
        exch_request(self.url, self.exchange, "test", self.key, self.sig, data)
    
    def get_acc_info(self):
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp)
        exch_request(self.url, self.exchange, "getaccinfo", self.key, self.sig, data)
    
    def get_pending_orders(self):
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp)
        exch_request(self.url, self.exchange, "getpendingorders", self.key, self.sig, data)
    
    def get_order_history(self, limit):
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&limit=" + str(limit)
        exch_request(self.url, self.exchange, "getorderhistory", self.key, self.sig, data)
        
    def cancel_pending_order(self, order):
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&orderNo=" + str(order)
        exch_request(self.url, self.exchange, "cancelpendingorder", self.key, self.sig, data)
        
    def place_order(self, qty, price, tpe)
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&qty=" + str(qty) + "&price=" + str(price) + "&type=" + tpe
        exch_request(self.url, self.exchange, "placeorder", self.key, self.sig, data)
        
    def withdrawl(self, amount, destination, tpe)
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&amount=" + str(amount) + "&destination=" + str(destination) + "&type=" + tpe
        exch_request(self.url, self.exchange, "withdraw", self.key, self.sig, data)
    
    def __init__(self, ky, sg, exchange=1):
        self.key = ky
        self.sig = sg
        self.exchange = exchange
        self.url = exch_url(exchange)
        #self.test() # it is messing with the timestamp generation on the actual call
