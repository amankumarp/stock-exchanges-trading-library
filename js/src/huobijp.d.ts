import { Exchange } from './base/Exchange.js';
export default class huobijp extends Exchange {
    describe(): any;
    fetchTime(params?: {}): Promise<number>;
    fetchTradingLimits(symbols?: any, params?: {}): Promise<{}>;
    fetchTradingLimitsById(id: any, params?: {}): Promise<{
        info: any;
        limits: {
            amount: {
                min: number;
                max: number;
            };
        };
    }>;
    parseTradingLimits(limits: any, symbol?: any, params?: {}): {
        info: any;
        limits: {
            amount: {
                min: number;
                max: number;
            };
        };
    };
    costToPrecision(symbol: any, cost: any): any;
    fetchMarkets(params?: {}): Promise<any[]>;
    parseTicker(ticker: any, market?: any): import("./base/types.js").Ticker;
    fetchOrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/ws/OrderBook.js").OrderBook>;
    fetchTicker(symbol: any, params?: {}): Promise<import("./base/types.js").Ticker>;
    fetchTickers(symbols?: any, params?: {}): Promise<any>;
    parseTrade(trade: any, market?: any): {
        id: string;
        info: any;
        order: string;
        timestamp: number;
        datetime: string;
        symbol: any;
        type: string;
        side: string;
        takerOrMaker: string;
        price: number;
        amount: number;
        cost: number;
        fee: any;
    };
    fetchOrderTrades(id: any, symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchMyTrades(symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchTrades(symbol: any, since?: any, limit?: number, params?: {}): Promise<any>;
    parseOHLCV(ohlcv: any, market?: any): number[];
    fetchOHLCV(symbol: any, timeframe?: string, since?: any, limit?: number, params?: {}): Promise<import("./base/types.js").OHLCV[]>;
    fetchAccounts(params?: {}): Promise<any>;
    fetchCurrencies(params?: {}): Promise<{}>;
    parseBalance(response: any): object;
    fetchBalance(params?: {}): Promise<object>;
    fetchOrdersByStates(states: any, symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchOrder(id: any, symbol?: any, params?: {}): Promise<any>;
    fetchOrders(symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchOpenOrders(symbol?: any, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchOpenOrdersV1(symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchClosedOrders(symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchOpenOrdersV2(symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    parseOrderStatus(status: any): string;
    parseOrder(order: any, market?: any): any;
    createOrder(symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<{
        info: any;
        id: string;
        timestamp: number;
        datetime: string;
        lastTradeTimestamp: any;
        status: any;
        symbol: any;
        type: any;
        side: any;
        price: any;
        amount: any;
        filled: any;
        remaining: any;
        cost: any;
        trades: any;
        fee: any;
        clientOrderId: any;
        average: any;
    }>;
    cancelOrder(id: any, symbol?: any, params?: {}): Promise<any>;
    cancelOrders(ids: any, symbol?: any, params?: {}): Promise<any>;
    cancelAllOrders(symbol?: any, params?: {}): Promise<any>;
    currencyToPrecision(code: any, fee: any, networkCode?: any): any;
    safeNetwork(networkId: any): string;
    parseDepositAddress(depositAddress: any, currency?: any): {
        currency: any;
        address: string;
        tag: string;
        network: string;
        info: any;
    };
    fetchDeposits(code?: any, since?: any, limit?: any, params?: {}): Promise<object[]>;
    fetchWithdrawals(code?: any, since?: any, limit?: any, params?: {}): Promise<object[]>;
    parseTransaction(transaction: any, currency?: any): {
        info: any;
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        address: string;
        addressTo: any;
        addressFrom: any;
        tag: string;
        tagTo: any;
        tagFrom: any;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: {
            currency: any;
            cost: number;
            rate: any;
        };
    };
    parseTransactionStatus(status: any): string;
    withdraw(code: any, amount: any, address: any, tag?: any, params?: {}): Promise<{
        info: any;
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        address: string;
        addressTo: any;
        addressFrom: any;
        tag: string;
        tagTo: any;
        tagFrom: any;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: {
            currency: any;
            cost: number;
            rate: any;
        };
    }>;
    sign(path: any, api?: string, method?: string, params?: {}, headers?: any, body?: any): {
        url: string;
        method: string;
        body: any;
        headers: any;
    };
    handleErrors(httpCode: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): void;
}
