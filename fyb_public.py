# Copyright Adam Parker 2015, MIT Liscense

import httplib
import json

def exch_url(exchange):
    url = "www.fyb"
    if(exchange == 1):
        url += "sg.com"
    else:
        url += "se.se"
    return url
    
def exch_request(url, exchange, item):
    if(exchange == 1):
        path = "/api/SGD/" + item
    else:
        path = "/api/SEK/" + item
    
    hsock = httplib.HTTPSConnection(url)
    hsock.request("GET", path)
    
    r = hsock.getresponse()
    
    if(r.status != 200):
        print r.status
        
    return r.read()

class ticker:
    exchange = 0
    url = ""
        
    def set_values(self, ask, bid, lst = "UNK", vol = "UNK"):
        self.ask = ask
        self.bid = bid
        self.last = lst
        self.volume = vol
    
    def decode(tick):
        tickjson = json.loads(self, tick)
        self.set_values(tickjson['ask'], tickjson['bid'])
    
    def decode_detailed(self, tick):
        tickjson = json.loads(tick)
        self.set_values(tickjson['ask'], tickjson['bid'], tickjson['last'], tickjson['vol'])

    def update_simple(self):
        tick = exch_request(self.url, self.exchange, "ticker.json")
        self.decode(tick)
      
    def update(self):
        tick = exch_request(self.url, self.exchange, "tickerdetailed.json")
        self.decode_detailed(tick)

    def __init__(self, exchange = 1):
        self.exchange = exchange
        self.url = exch_url(self.exchange)
        self.update()

class orderbook:
    class ob_entry:
        def __init__(self, prce, unts):
            self.price = prce
            self.units = unts
    
    exchange = 0
    url = ""
    asks = []
    bids = []
    
    def orderbook_decode(self, ob):
        objson = json.loads(ob)
        
        x = 0
        for entry in objson['asks']:
            self.asks.append(self.ob_entry(objson['asks'][x][0], objson['asks'][x][1])) 
            x += 1
            
        x = 0
        for entry in objson['bids']:
            self.bids.append(self.ob_entry(objson['bids'][x][0], objson['bids'][x][1]))
            x += 1
            
    def update(self):
        url = exch_url(self.exchange)
        ob = exch_request(url, self.exchange, "orderbook.json")
        self.orderbook_decode(ob)
    
    def __init__(self, exchange = 1):
        self.exchange = exchange
        self.url = exch_url(self.exchange)
        self.update()
            
class tradehistory:
    class th_entry:
        def __init__(self, amt, dt, prce, td):
            self.amount = amt
            self.date = dt
            self.price = prce
            self.tid = td
    
    exchange = 1
    url = ""
    entries = []
    latest_tid= -1
    
    def __init__(self, th):
        self.tradehistory_decode(th)
        
    def tradehistory_decode(self, th):
        thjson = json.loads(th)
        
        try:
            for entry in thjson:
                self.entries.append(self.th_entry(entry['amount'], entry['date'], entry['price'], entry['tid']))
            
            self.latest_tid = entry['tid']
        except:
            return
    
    def update(self):
        if self.latest_tid != -1:
            item = "trades.json?since=" + str(self.latest_tid)
        else:
            item = "trades.json"

        th = exch_request(self.url, self.exchange, item)
        self.tradehistory_decode(th)
            
    def __init__(self, exchange = 1):
        self.exchange = exchange
        self.url = exch_url(self.exchange)
        self.update()

if __name__ == "__main__":
    print "init"
    thry = tradehistory()
    print "update"
    thry.update()
    
