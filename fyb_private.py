# Copyright Adam Parker 2015, MIT Liscense

import httplib
import time
import hmac
import hashlib
import urllib
import json

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

    return hsock.getresponse()


class fyb_private:
    
    class pending_order:
        def __init__(self, date, price, qty, ticket, tpe):
            self.date = date
            self.price = price
            self.qty = qty
            self.ticket = ticket
            self.order_type = tpe
    
    class historical_order:
        def __init__(self, date_created, date_executed, price, qty, status, ticket, tpe):
            self.date_created = date_created
            self.date_executed = date_executed
            self.price = price
            self.qty = qty
            self.status = status
            self.ticket = ticket
            self.order_type = tpe
        
    pending = []
    historical = []
    
    def test(self):
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp)
        r = exch_request(self.url, self.exchange, "test", self.key, self.sig, data)
        if(r.status == 200):
            jsond = json.loads(r.read())
            self.valid = jsond['error'] == 0
            return 1
        else:
            return -1
    
    def get_acc_info(self):
        if(self.valid != True):
            return -1
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp)
        r = exch_request(self.url, self.exchange, "getaccinfo", self.key, self.sig, data)
        if(r.status == 200):
            jsond = json.loads(r.read())
            if(jsond['error'] == 0):
                self.acc_num = jsond['accNo']
                self.btc_bal = jsond['btcBal']
                self.btc_deposit = jsond['btcDeposit']
                self.email = jsond['email']
                self.sgd_bal = jsond['sgdBal']
                return 1
            else:
                return -3
        else:
            return -2
    
    def get_pending_orders(self):
        if(self.valid != True):
            return -1
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp)
        r = exch_request(self.url, self.exchange, "getpendingorders", self.key, self.sig, data)
        if(r.status == 200):
            jsond = json.loads(r.read())
            if(jsond['error'] == 0):
                pending = []
                for entry in jsond['orders']:
                    pending.append(self.pending_order(entry['date'], entry['price'], 
                        entry['qty'], entry['ticket'], entry['type']))
                return 1
            else:
                return -3
        else:
            return -2
    
    def get_order_history(self, limit):
        if(self.valid != True):
            return -1
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&limit=" + str(limit)
        r = exch_request(self.url, self.exchange, "getorderhistory", self.key, self.sig, data)
        if(r.status == 200):
            jsond = json.loads(r.read())
            if(jsond['error'] == 0):
                history = []
                for entry in jsond['orders']:
                    history.append(self.historical_order(entry['date_created'], entry['date_executed'], 
                        entry['price'], entry['qty'], entry['status'], entry['ticket'], entry['type']))
                return 1
            else:
                return -3
        else:
            return -2
        
    def cancel_pending_order(self, order):
        if(self.valid != True):
            return -1
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&orderNo=" + str(order)
        r = exch_request(self.url, self.exchange, "cancelpendingorder", self.key, self.sig, data)
        if(r.status == 200):
            jsond = json.loads(r.read())
            return jsond['error'] == 0
        else:
            return -2
        
    def place_order(self, qty, price, tpe):
        if(self.valid != True):
            return -1
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&qty=" + str(qty) + "&price=" + str(price) + "&type=" + tpe
        r = exch_request(self.url, self.exchange, "placeorder", self.key, self.sig, data)
        if(r.status == 200):
            jsond = json.loads(r.read())
            if(jsond['error'] == 0):
                return jsond['pending_oid']
            else:
                return -3
        else:
            return -2
        
    def withdraw(self, amount, destination, tpe):
        if(self.valid != True):
            return -1
        timestamp = int(time.time())
        data = "timestamp=" + str(timestamp) + "&amount=" + str(amount) + "&destination=" + str(destination) + "&type=" + tpe
        r = exch_request(self.url, self.exchange, "withdraw", self.key, self.sig, data)
        if(r.status == 200):
            jsond = json.loads(r.read())
            if(jsond['error'] == 0):
                return jsond['msg']
            else:
                return -3
        else:
            return -2
   
    def change_key(self, ky, sg):
        self.key = ky
        self.sig = sg
        self.test()
    
    def __init__(self, ky, sg, exchange=1):
        self.exchange = exchange
        self.url = exch_url(exchange)
        self.change_key(ky, sg)
