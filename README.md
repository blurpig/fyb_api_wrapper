FYB API Wrapper
===================

Python wrapper for FYB API

ticker
------
ticker(exchange) to initialize.

**exchange**

		1 = SGD exchange (default)
		2 = SEK exchange

ticker.update() to get new ticker values

ticker.update_simpler() to get new ticker values (without last trade or volume)

**members:**

	ticker.ask
	ticker.bid
	ticker.last
	ticker.volume

orderbook
----------
orderbook(exchange) to initialize.

**exchange**

		1 = SGD exchange (default)
		2 = SEK exchange
		
orderbook.update() to get latest orderbook

**members:**

	orderbook.asks[]
		array of ob_entry objects containing asks
	orderbook.bids[]
		array of ob_entry objects containing bids

**ob_entry memebers:**

	ob_entry.price
	ob_entry.units

tradehistory
-------------
tradehistory(exchange) to initialize.

**exchange**

		1 = SGD exchange (default)
		2 = SEK exchange
		
tradehistory.update() to get latest orderbook

If latest_tid is uninitialized a full trade history is downloaded.  

Every call to this function afterwards only downloads tids newer than latest_tid.
	
**members:**

	tradehistory.entries[]
		array of th_entry objects containing trade history items
	tradehistory.latest_tid
		
**th_entry members:**

	th_entry.amount
	th_entry.date
	th_entry.price
	th_entry.tid
