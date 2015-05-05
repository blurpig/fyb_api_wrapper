FYB API Wrapper
===================

Python wrapper for FYB API

PUBLIC
-------

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
	
PRIVATE
--------

fyb_private
-----------

fyb_private(key, secret, exchange) to initialize

**exchange**

		1 = SGD exchange (default)
		2 = SEK exchange
		
**test()**

    Verifies key/secret with exchange.  The test must pass before any other call will execute.
    This is automatically run during init of an object and when the key is changed so there is 
    little reason to run it manually.  To check whether it has passed check if the member valid
    contains True.  Returns -1 if servers HTTP response is not 200 or 1 if call was processed.
    
**change_key(key, secret)**

    Changes the key/secret of the object and then runs test().  Check the member valid for results
    of test().
    
**get_acc_info()**

    Gets account info associated with the key.  Populates members acc_num, btc_bal, btc_deposit, email
    and sgd_bal.  Returns -1 if member valid is not true, -2 if server's HTTP response is not 200, -3
    if the server reports an error with the call or 1 if everthing processed fine.
    
**get_pending_orders()**

    Gets pending order of account.  Populates member pending with pending_order objects built from 
    data returned by server.  Returns -1 if member valid is not true, -2 if server's HTTP response is not 
    200, -3 if the server reports an error with the call or 1 if everthing processed fine.
    
**get_order_history(limit)**

    Gets limit number of order history items for account.  Populates member history with historical_order 
    objects build from data returned by server.  Returns -1 if member valid is not true, -2 if server's 
    HTTP response is not 200, -3 if the server reports an error with the call or 1 if everthing processed 
    fine.
    
**cancel_pending_order(order)**

    Cancels the pending order number specified by order.  Returns -1 if member valid is not true, -2 if 
    server's HTTP response is not 200, -3 if the server reports an error with the call or True or False
    depending on status of cancel order.
    
**place_order(quantity, price, type)**

    Places an order for a certain quantity of XBT at a certain price.  Type should be 'B' for buy or 'S'
    for sell.  Returns -1 if member valid is not true, -2 if server's HTTP response is not 200, -3
    if the server reports an error with the call or the pending order number if everthing processed fine.

**withdraw(amount, destination, type)**

    Withdraws a certain amount of XBT to a destination bitcoin address.  Type should be 'BTC' or 'XFERS'.
    Returns -1 if member valid is not true, -2 if server's HTTP response is not 200, -3 if the server 
    reports an error with the call or server's response if everthing processed fine.
    
**members**

    fyb_private.pending[]
    fyb_private.historical[]
    fyb_private.valid
    fyb_private.acc_num
    fyb_private.btc_bal
    fyb_private.btc_deposit
    fyb_private.email
    fyb_private.sgd_bal
    
**pending_order members**

    pending_order.date
    pending_order.price
    pending_order.qty
    pending_order.ticket
    pending_order.order_type
    
**historical_order members**

    historical_order.date_created
    historical_order.date_executed
    historical_order.price
    historical_order.qty
    historical_order.ticket
    historical_order.order_type