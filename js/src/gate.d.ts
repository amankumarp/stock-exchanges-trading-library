import { Exchange } from './base/Exchange.js';
export default class gate extends Exchange {
    describe(): any;
    setSandboxMode(enable: any): void;
    fetchMarkets(params?: {}): Promise<any>;
    fetchSpotMarkets(params?: {}): Promise<any[]>;
    fetchContractMarkets(params?: {}): Promise<any[]>;
    parseContractMarket(market: any, settleId: any): {
        id: string;
        symbol: string;
        base: any;
        quote: any;
        settle: any;
        baseId: string;
        quoteId: string;
        settleId: any;
        type: string;
        spot: boolean;
        margin: boolean;
        swap: boolean;
        future: boolean;
        option: boolean;
        active: boolean;
        contract: boolean;
        linear: boolean;
        inverse: boolean;
        taker: number;
        maker: number;
        contractSize: number;
        expiry: number;
        expiryDatetime: string;
        strike: any;
        optionType: any;
        precision: {
            amount: number;
            price: number;
        };
        limits: {
            leverage: {
                min: number;
                max: number;
            };
            amount: {
                min: number;
                max: number;
            };
            price: {
                min: number;
                max: number;
            };
            cost: {
                min: any;
                max: any;
            };
        };
        info: any;
    };
    fetchOptionMarkets(params?: {}): Promise<any[]>;
    fetchOptionUnderlyings(): Promise<any[]>;
    prepareRequest(market?: any, type?: any, params?: {}): {}[];
    spotOrderPrepareRequest(market?: any, stop?: boolean, params?: {}): any[];
    multiOrderSpotPrepareRequest(market?: any, stop?: boolean, params?: {}): any[];
    getMarginMode(stop: any, params: any): any[];
    getSettlementCurrencies(type: any, method: any): any;
    fetchCurrencies(params?: {}): Promise<{}>;
    fetchFundingRate(symbol: any, params?: {}): Promise<{
        info: any;
        symbol: any;
        markPrice: number;
        indexPrice: number;
        interestRate: number;
        estimatedSettlePrice: any;
        timestamp: any;
        datetime: any;
        fundingRate: number;
        fundingTimestamp: number;
        fundingDatetime: string;
        nextFundingRate: number;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    }>;
    fetchFundingRates(symbols?: any, params?: {}): Promise<any>;
    parseFundingRate(contract: any, market?: any): {
        info: any;
        symbol: any;
        markPrice: number;
        indexPrice: number;
        interestRate: number;
        estimatedSettlePrice: any;
        timestamp: any;
        datetime: any;
        fundingRate: number;
        fundingTimestamp: number;
        fundingDatetime: string;
        nextFundingRate: number;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    };
    fetchNetworkDepositAddress(code: any, params?: {}): Promise<{}>;
    createDepositAddress(code: any, params?: {}): Promise<{
        info: any;
        code: any;
        currency: any;
        address: any;
        tag: any;
        network: any;
    }>;
    fetchDepositAddress(code: any, params?: {}): Promise<{
        info: any;
        code: any;
        currency: any;
        address: any;
        tag: any;
        network: any;
    }>;
    fetchTradingFee(symbol: any, params?: {}): Promise<{
        info: any;
        symbol: string;
        maker: number;
        taker: number;
    }>;
    fetchTradingFees(params?: {}): Promise<{}>;
    parseTradingFees(response: any): {};
    parseTradingFee(info: any, market?: any): {
        info: any;
        symbol: string;
        maker: number;
        taker: number;
    };
    fetchTransactionFees(codes?: any, params?: {}): Promise<{}>;
    fetchDepositWithdrawFees(codes?: any, params?: {}): Promise<{}>;
    parseDepositWithdrawFee(fee: any, currency?: any): {
        info: any;
        withdraw: {
            fee: number;
            percentage: boolean;
        };
        deposit: {
            fee: number;
            percentage: boolean;
        };
        networks: {};
    };
    fetchFundingHistory(symbol?: any, since?: any, limit?: any, params?: {}): Promise<object[]>;
    parseFundingHistories(response: any, symbol: any, since: any, limit: any): object[];
    parseFundingHistory(info: any, market?: any): {
        info: any;
        symbol: string;
        code: string;
        timestamp: number;
        datetime: string;
        id: any;
        amount: number;
    };
    fetchOrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/ws/OrderBook.js").OrderBook>;
    fetchTicker(symbol: any, params?: {}): Promise<import("./base/types.js").Ticker>;
    parseTicker(ticker: any, market?: any): import("./base/types.js").Ticker;
    fetchTickers(symbols?: any, params?: {}): Promise<any>;
    parseBalanceHelper(entry: any): {
        free: any;
        used: any;
        total: any;
    };
    fetchBalance(params?: {}): Promise<object>;
    fetchOHLCV(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").OHLCV[]>;
    fetchFundingRateHistory(symbol?: any, since?: any, limit?: any, params?: {}): Promise<object[]>;
    parseOHLCV(ohlcv: any, market?: any): number[];
    fetchTrades(symbol: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchOrderTrades(id: any, symbol?: any, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchMyTrades(symbol?: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    parseTrade(trade: any, market?: any): import("./base/types.js").Trade;
    fetchDeposits(code?: any, since?: any, limit?: any, params?: {}): Promise<object[]>;
    fetchWithdrawals(code?: any, since?: any, limit?: any, params?: {}): Promise<object[]>;
    withdraw(code: any, amount: any, address: any, tag?: any, params?: {}): Promise<{
        info: any;
        id: string;
        txid: string;
        currency: any;
        amount: number;
        network: any;
        address: string;
        addressTo: any;
        addressFrom: any;
        tag: string;
        tagTo: any;
        tagFrom: any;
        status: string;
        type: any;
        timestamp: number;
        datetime: string;
        updated: any;
        fee: {
            currency: any;
            cost: number;
        };
    }>;
    parseTransactionStatus(status: any): string;
    parseTransactionType(type: any): string;
    parseTransaction(transaction: any, currency?: any): {
        info: any;
        id: string;
        txid: string;
        currency: any;
        amount: number;
        network: any;
        address: string;
        addressTo: any;
        addressFrom: any;
        tag: string;
        tagTo: any;
        tagFrom: any;
        status: string;
        type: any;
        timestamp: number;
        datetime: string;
        updated: any;
        fee: {
            currency: any;
            cost: number;
        };
    };
    createOrder(symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    editOrder(id: any, symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    parseOrderStatus(status: any): string;
    parseOrder(order: any, market?: any): any;
    fetchOrder(id: any, symbol?: any, params?: {}): Promise<any>;
    fetchOpenOrders(symbol?: any, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchClosedOrders(symbol?: any, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchOrdersByStatus(status: any, symbol?: any, since?: any, limit?: any, params?: {}): Promise<object[]>;
    cancelOrder(id: any, symbol?: any, params?: {}): Promise<any>;
    cancelAllOrders(symbol?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    transfer(code: any, amount: any, fromAccount: any, toAccount: any, params?: {}): Promise<{
        id: any;
        timestamp: number;
        datetime: string;
        currency: any;
        amount: any;
        fromAccount: any;
        toAccount: any;
        status: any;
        info: any;
    }>;
    parseTransfer(transfer: any, currency?: any): {
        id: any;
        timestamp: number;
        datetime: string;
        currency: any;
        amount: any;
        fromAccount: any;
        toAccount: any;
        status: any;
        info: any;
    };
    setLeverage(leverage: any, symbol?: any, params?: {}): Promise<any>;
    parsePosition(position: any, market?: any): {
        info: any;
        id: any;
        symbol: string;
        timestamp: any;
        datetime: any;
        initialMargin: number;
        initialMarginPercentage: number;
        maintenanceMargin: number;
        maintenanceMarginPercentage: number;
        entryPrice: number;
        notional: number;
        leverage: number;
        unrealizedPnl: number;
        contracts: number;
        contractSize: any;
        marginRatio: any;
        liquidationPrice: number;
        markPrice: number;
        collateral: number;
        marginMode: any;
        side: any;
        percentage: number;
    };
    fetchPositions(symbols?: any, params?: {}): Promise<any>;
    fetchLeverageTiers(symbols?: any, params?: {}): Promise<{}>;
    parseMarketLeverageTiers(info: any, market?: any): any[];
    repayMargin(code: any, amount: any, symbol?: any, params?: {}): Promise<{
        id: number;
        currency: any;
        amount: number;
        symbol: any;
        timestamp: number;
        datetime: string;
        info: any;
    }>;
    borrowMargin(code: any, amount: any, symbol?: any, params?: {}): Promise<{
        id: number;
        currency: any;
        amount: number;
        symbol: any;
        timestamp: number;
        datetime: string;
        info: any;
    }>;
    parseMarginLoan(info: any, currency?: any): {
        id: number;
        currency: any;
        amount: number;
        symbol: any;
        timestamp: number;
        datetime: string;
        info: any;
    };
    sign(path: any, api?: any[], method?: string, params?: {}, headers?: any, body?: any): {
        url: any;
        method: string;
        body: any;
        headers: any;
    };
    modifyMarginHelper(symbol: any, amount: any, params?: {}): Promise<{
        info: any;
        amount: any;
        code: any;
        symbol: any;
        total: number;
        status: string;
    }>;
    parseMarginModification(data: any, market?: any): {
        info: any;
        amount: any;
        code: any;
        symbol: any;
        total: number;
        status: string;
    };
    reduceMargin(symbol: any, amount: any, params?: {}): Promise<{
        info: any;
        amount: any;
        code: any;
        symbol: any;
        total: number;
        status: string;
    }>;
    addMargin(symbol: any, amount: any, params?: {}): Promise<{
        info: any;
        amount: any;
        code: any;
        symbol: any;
        total: number;
        status: string;
    }>;
    fetchOpenInterestHistory(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<object[]>;
    parseOpenInterest(interest: any, market?: any): {
        symbol: string;
        openInterestAmount: number;
        openInterestValue: number;
        timestamp: number;
        datetime: string;
        info: any;
    };
    handleErrors(code: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): void;
}
