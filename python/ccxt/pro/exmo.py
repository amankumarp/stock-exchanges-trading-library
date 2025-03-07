# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById
import hashlib
from ccxt.base.errors import NotSupported


class exmo(ccxt.async_support.exmo):

    def describe(self):
        return self.deep_extend(super(exmo, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': True,
                'watchTicker': True,
                'watchTickers': False,
                'watchTrades': True,
                'watchMyTrades': True,
                'watchOrders': False,  # TODO
                'watchOrderBook': True,
                'watchOHLCV': False,
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://ws-api.exmo.com:443/v1/public',
                        'spot': 'wss://ws-api.exmo.com:443/v1/private',
                        'margin': 'wss://ws-api.exmo.com:443/v1/margin/private',
                    },
                },
            },
            'options': {
            },
            'streaming': {
            },
            'exceptions': {
            },
        })

    def request_id(self):
        requestId = self.sum(self.safe_integer(self.options, 'requestId', 0), 1)
        self.options['requestId'] = requestId
        return requestId

    async def watch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.authenticate(params)
        type, query = self.handle_market_type_and_params('watchBalance', None, params)
        messageHash = 'balance:' + type
        url = self.urls['api']['ws'][type]
        subscribe = {
            'method': 'subscribe',
            'topics': [type + '/wallet'],
            'id': self.request_id(),
        }
        request = self.deep_extend(subscribe, query)
        return await self.watch(url, messageHash, request, messageHash, request)

    def handle_balance(self, client, message):
        #
        #  spot
        #     {
        #         ts: 1654208766007,
        #         event: 'snapshot',
        #         topic: 'spot/wallet',
        #         data: {
        #             balances: {
        #                 ADA: '0',
        #                 ALGO: '0',
        #                 ...
        #             },
        #             reserved: {
        #                 ADA: '0',
        #                 ALGO: '0',
        #                 ...
        #             }
        #         }
        #     }
        #
        #  margin
        #     {
        #         "ts": 1624370076651,
        #         "event": "snapshot",
        #         "topic": "margin/wallets",
        #         "data": {
        #             "RUB": {
        #                 "balance": "1000000",
        #                 "used": "0",
        #                 "free": "1000000"
        #             },
        #             "USD": {
        #                 "balance": "1000000",
        #                 "used": "1831.925",
        #                 "free": "998168.075"
        #             }
        #         }
        #     }
        #     {
        #         "ts": 1624370185720,
        #         "event": "update",
        #         "topic": "margin/wallets",
        #         "data": {
        #             "USD": {
        #                 "balance": "1000123",
        #                 "used": "1831.925",
        #                 "free": "998291.075"
        #             }
        #         }
        #     }
        #
        topic = self.safe_string(message, 'topic')
        parts = topic.split('/')
        type = self.safe_string(parts, 0)
        if type == 'spot':
            self.parse_spot_balance(message)
        elif type == 'margin':
            self.parse_margin_balance(message)
        messageHash = 'balance:' + type
        client.resolve(self.balance, messageHash)

    def parse_spot_balance(self, message):
        #
        #     {
        #         "balances": {
        #             "BTC": "3",
        #             "USD": "1000",
        #             "RUB": "0"
        #         },
        #         "reserved": {
        #             "BTC": "0.5",
        #             "DASH": "0",
        #             "RUB": "0"
        #         }
        #     }
        #
        event = self.safe_string(message, 'event')
        data = self.safe_value(message, 'data')
        self.balance['info'] = data
        if event == 'snapshot':
            balances = self.safe_value(data, 'balances', {})
            reserved = self.safe_value(data, 'reserved', {})
            currencies = list(balances.keys())
            for i in range(0, len(currencies)):
                currencyId = currencies[i]
                code = self.safe_currency_code(currencyId)
                free = balances[currencyId]
                used = reserved[currencyId]
                account = self.account()
                account['free'] = self.parse_number(free)
                account['used'] = self.parse_number(used)
                self.balance[code] = account
        elif event == 'update':
            currencyId = self.safe_string(data, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_number(data, 'balance')
            account['used'] = self.safe_number(data, 'reserved')
            self.balance[code] = account
        self.balance = self.safe_balance(self.balance)

    def parse_margin_balance(self, message):
        #
        #     {
        #         "RUB": {
        #             "balance": "1000000",
        #             "used": "0",
        #             "free": "1000000"
        #         },
        #         "USD": {
        #             "balance": "1000000",
        #             "used": "1831.925",
        #             "free": "998168.075"
        #         }
        #     }
        #
        data = self.safe_value(message, 'data')
        self.balance['info'] = data
        currencies = list(data.keys())
        for i in range(0, len(currencies)):
            currencyId = currencies[i]
            code = self.safe_currency_code(currencyId)
            wallet = self.safe_value(data, currencyId)
            account = self.account()
            account['free'] = self.safe_number(wallet, 'free')
            account['used'] = self.safe_number(wallet, 'used')
            account['total'] = self.safe_number(wallet, 'balance')
            self.balance[code] = account
            self.balance = self.safe_balance(self.balance)

    async def watch_ticker(self, symbol, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws']['public']
        messageHash = 'ticker:' + symbol
        message = {
            'method': 'subscribe',
            'topics': [
                'spot/ticker:' + market['id'],
            ],
            'id': self.request_id(),
        }
        request = self.deep_extend(message, params)
        return await self.watch(url, messageHash, request, messageHash, request)

    def handle_ticker(self, client, message):
        #
        #  spot
        #      {
        #          ts: 1654205085473,
        #          event: 'update',
        #          topic: 'spot/ticker:BTC_USDT',
        #          data: {
        #              buy_price: '30285.84',
        #              sell_price: '30299.97',
        #              last_trade: '30295.01',
        #              high: '30386.7',
        #              low: '29542.76',
        #              avg: '29974.16178449',
        #              vol: '118.79538518',
        #              vol_curr: '3598907.38200826',
        #              updated: 1654205084
        #          }
        #      }
        #
        topic = self.safe_string(message, 'topic')
        topicParts = topic.split(':')
        marketId = self.safe_string(topicParts, 1)
        symbol = self.safe_symbol(marketId)
        ticker = self.safe_value(message, 'data', {})
        market = self.safe_market(marketId)
        parsedTicker = self.parse_ticker(ticker, market)
        messageHash = 'ticker:' + symbol
        self.tickers[symbol] = parsedTicker
        client.resolve(parsedTicker, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws']['public']
        messageHash = 'trades:' + symbol
        message = {
            'method': 'subscribe',
            'topics': [
                'spot/trades:' + market['id'],
            ],
            'id': self.request_id(),
        }
        request = self.deep_extend(message, params)
        trades = await self.watch(url, messageHash, request, messageHash, request)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        #      {
        #          ts: 1654206084001,
        #          event: 'update',
        #          topic: 'spot/trades:BTC_USDT',
        #          data: [{
        #              trade_id: 389704729,
        #              type: 'sell',
        #              price: '30310.95',
        #              quantity: '0.0197',
        #              amount: '597.125715',
        #              date: 1654206083
        #          }]
        #      }
        #
        topic = self.safe_string(message, 'topic')
        parts = topic.split(':')
        marketId = self.safe_string(parts, 1)
        symbol = self.safe_symbol(marketId)
        market = self.safe_market(marketId)
        trades = self.safe_value(message, 'data', [])
        messageHash = 'trades:' + symbol
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        for i in range(0, len(trades)):
            trade = trades[i]
            parsed = self.parse_trade(trade, market)
            stored.append(parsed)
        self.trades[symbol] = stored
        client.resolve(self.trades[symbol], messageHash)

    async def watch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        get the list of trades associated with the user
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        await self.authenticate(params)
        type, query = self.handle_market_type_and_params('watchMyTrades', None, params)
        url = self.urls['api']['ws'][type]
        messageHash = None
        if symbol is None:
            messageHash = 'myTrades:' + type
        else:
            market = self.market(symbol)
            symbol = market['symbol']
            messageHash = 'myTrades:' + market['symbol']
        message = {
            'method': 'subscribe',
            'topics': [
                type + '/user_trades',
            ],
            'id': self.request_id(),
        }
        request = self.deep_extend(message, query)
        trades = await self.watch(url, messageHash, request, messageHash, request)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    def handle_my_trades(self, client, message):
        #
        #  spot
        #     {
        #         ts: 1654210290219,
        #         event: 'update',
        #         topic: 'spot/user_trades',
        #         data: {
        #             trade_id: 389715807,
        #             type: 'buy',
        #             price: '30527.77',
        #             quantity: '0.0001',
        #             amount: '3.052777',
        #             date: 1654210290,
        #             order_id: 27352777112,
        #             client_id: 0,
        #             pair: 'BTC_USDT',
        #             exec_type: 'taker',
        #             commission_amount: '0.0000001',
        #             commission_currency: 'BTC',
        #             commission_percent: '0.1'
        #         }
        #     }
        #
        #  margin
        #     {
        #         "ts":1624369720168,
        #         "event":"snapshot",
        #         "topic":"margin/user_trades",
        #         "data":[
        #            {
        #               "trade_id":"692844278081167054",
        #               "trade_dt":"1624369773990729200",
        #               "type":"buy",
        #               "order_id":"692844278081167033",
        #               "pair":"BTC_USD",
        #               "quantity":"0.1",
        #               "price":"36638.5",
        #               "is_maker":false
        #            }
        #         ]
        #     }
        #     {
        #         "ts":1624370368612,
        #         "event":"update",
        #         "topic":"margin/user_trades",
        #         "data":{
        #            "trade_id":"692844278081167693",
        #            "trade_dt":"1624370368569092500",
        #            "type":"buy",
        #            "order_id":"692844278081167674",
        #            "pair":"BTC_USD",
        #            "quantity":"0.1",
        #            "price":"36638.5",
        #            "is_maker":false
        #         }
        #     }
        #
        topic = self.safe_string(message, 'topic')
        parts = topic.split('/')
        type = self.safe_string(parts, 0)
        messageHash = 'myTrades:' + type
        event = self.safe_string(message, 'event')
        rawTrades = []
        myTrades = None
        if self.myTrades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            myTrades = ArrayCacheBySymbolById(limit)
            self.myTrades = myTrades
        else:
            myTrades = self.myTrades
        if event == 'snapshot':
            rawTrades = self.safe_value(message, 'data', [])
        elif event == 'update':
            rawTrade = self.safe_value(message, 'data', {})
            rawTrades = [rawTrade]
        trades = self.parse_trades(rawTrades)
        symbols = {}
        for j in range(0, len(trades)):
            trade = trades[j]
            myTrades.append(trade)
            symbols[trade['symbol']] = True
        symbolKeys = list(symbols.keys())
        for i in range(0, len(symbolKeys)):
            symbol = symbolKeys[i]
            symbolSpecificMessageHash = 'myTrades:' + symbol
            client.resolve(myTrades, symbolSpecificMessageHash)
        client.resolve(myTrades, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws']['public']
        messageHash = 'orderbook:' + symbol
        params = self.omit(params, 'aggregation')
        subscribe = {
            'method': 'subscribe',
            'id': self.request_id(),
            'topics': [
                'spot/order_book_updates:' + market['id'],
            ],
        }
        request = self.deep_extend(subscribe, params)
        orderbook = await self.watch(url, messageHash, request, messageHash)
        return orderbook.limit()

    def handle_order_book(self, client, message):
        #
        #     {
        #         "ts": 1574427585174,
        #         "event": "snapshot",
        #         "topic": "spot/order_book_updates:BTC_USD",
        #         "data": {
        #             "ask": [
        #                 ["100", "3", "300"],
        #                 ["200", "4", "800"]
        #             ],
        #             "bid": [
        #                 ["99", "2", "198"],
        #                 ["98", "1", "98"]
        #             ]
        #         }
        #     }
        #
        #     {
        #         "ts": 1574427585174,
        #         "event": "update",
        #         "topic": "spot/order_book_updates:BTC_USD",
        #         "data": {
        #             "ask": [
        #                 ["100", "1", "100"],
        #                 ["200", "2", "400"]
        #             ],
        #             "bid": [
        #                 ["99", "1", "99"],
        #                 ["98", "0", "0"]
        #             ]
        #         }
        #     }
        #
        topic = self.safe_string(message, 'topic')
        parts = topic.split(':')
        marketId = self.safe_string(parts, 1)
        symbol = self.safe_symbol(marketId)
        orderBook = self.safe_value(message, 'data', {})
        messageHash = 'orderbook:' + symbol
        timestamp = self.safe_number(message, 'ts')
        storedOrderBook = self.safe_value(self.orderbooks, symbol)
        if storedOrderBook is None:
            storedOrderBook = self.order_book({})
            self.orderbooks[symbol] = storedOrderBook
        event = self.safe_string(message, 'event')
        if event == 'snapshot':
            snapshot = self.parse_order_book(orderBook, symbol, timestamp, 'bid', 'ask')
            storedOrderBook.reset(snapshot)
        else:
            asks = self.safe_value(orderBook, 'ask', [])
            bids = self.safe_value(orderBook, 'bid', [])
            self.handle_deltas(storedOrderBook['asks'], asks)
            self.handle_deltas(storedOrderBook['bids'], bids)
            storedOrderBook['timestamp'] = timestamp
            storedOrderBook['datetime'] = self.iso8601(timestamp)
        client.resolve(storedOrderBook, messageHash)

    def handle_delta(self, bookside, delta):
        bidAsk = self.parse_bid_ask(delta, 0, 1)
        bookside.storeArray(bidAsk)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_message(self, client, message):
        #
        # {
        #     ts: 1654206362552,
        #     event: 'info',
        #     code: 1,
        #     message: 'connection established',
        #     session_id: '7548931b-c2a4-45dd-8d71-877881a7251a'
        # }
        #
        # {
        #     ts: 1654206491399,
        #     event: 'subscribed',
        #     id: 1,
        #     topic: 'spot/ticker:BTC_USDT'
        # }
        event = self.safe_string(message, 'event')
        events = {
            'logged_in': self.handle_authentication_message,
            'info': self.handle_info,
            'subscribed': self.handle_subscribed,
        }
        eventHandler = self.safe_value(events, event)
        if eventHandler is not None:
            return eventHandler(client, message)
        if (event == 'update') or (event == 'snapshot'):
            topic = self.safe_string(message, 'topic')
            if topic is not None:
                parts = topic.split(':')
                channel = self.safe_string(parts, 0)
                handlers = {
                    'spot/ticker': self.handle_ticker,
                    'spot/wallet': self.handle_balance,
                    'margin/wallet': self.handle_balance,
                    'margin/wallets': self.handle_balance,
                    'spot/trades': self.handle_trades,
                    'margin/trades': self.handle_trades,
                    'spot/order_book_updates': self.handle_order_book,
                    # 'spot/orders': self.handleOrders,
                    # 'margin/orders': self.handleOrders,
                    'spot/user_trades': self.handle_my_trades,
                    'margin/user_trades': self.handle_my_trades,
                }
                handler = self.safe_value(handlers, channel)
                if handler is not None:
                    return handler(client, message)
        raise NotSupported(self.id + ' received an unsupported message: ' + self.json(message))

    def handle_subscribed(self, client, message):
        #
        # {
        #     method: 'subscribe',
        #     id: 2,
        #     topics: ['spot/orders']
        # }
        #
        return message

    def handle_info(self, client, message):
        #
        # {
        #     ts: 1654215731659,
        #     event: 'info',
        #     code: 1,
        #     message: 'connection established',
        #     session_id: '4c496262-e259-4c27-b805-f20b46209c17'
        # }
        #
        return message

    def handle_authentication_message(self, client, message):
        #
        #     {
        #         method: 'login',
        #         id: 1,
        #         api_key: 'K-************************',
        #         sign: '******************************************************************',
        #         nonce: 1654215729887
        #     }
        #
        messageHash = 'authenticated'
        client.resolve(message, messageHash)

    def authenticate(self, params={}):
        messageHash = 'authenticated'
        type, query = self.handle_market_type_and_params('authenticate', None, params)
        url = self.urls['api']['ws'][type]
        client = self.client(url)
        future = self.safe_value(client.subscriptions, messageHash)
        if future is None:
            time = self.milliseconds()
            self.check_required_credentials()
            requestId = self.request_id()
            signData = self.apiKey + str(time)
            sign = self.hmac(self.encode(signData), self.encode(self.secret), hashlib.sha512, 'base64')
            request = {
                'method': 'login',
                'id': requestId,
                'api_key': self.apiKey,
                'sign': sign,
                'nonce': time,
            }
            message = self.extend(request, query)
            future = self.watch(url, messageHash, message)
            client.subscriptions[messageHash] = future
        return future
