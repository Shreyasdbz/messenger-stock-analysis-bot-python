import yfinance as yf
from yahoo_fin import stock_info as si
import csv
# import emoji


# 
# Entry point when a StockBot message is received
def processStockbotMsg(text):
    if("$" in text):
        mainText = text.split("$")[1]
        textSplit = mainText.split(" ")
        # CASE 1 -- Just the stock ticker --- Give back price and short Info
        if(len(textSplit) == 1):
            symbol = textSplit[0]
            ticker = yf.Ticker(symbol)
            tickerInfo = ticker.info
            name = tickerInfo['shortName']
            stockPrice = round(si.get_live_price(symbol), 2)
            openPrice = round(tickerInfo['regularMarketOpen'],2)
            closePrice = round(tickerInfo['previousClose'],2)

            rtnMsg = "`{}` is currently trading at ${}.\n".format(name, stockPrice)
            rtnMsg += "It opened at ${}. Previous close was ${}".format(openPrice, closePrice)

            return rtnMsg

        # CASE 2 -- Additional Info
        elif(len(textSplit) == 2):
            symbol = textSplit[0]
            ticker = yf.Ticker(symbol)
            tickerInfo = ticker.info
            name = tickerInfo['longName']
            stockPrice = round(si.get_live_price(symbol), 2)
            openPrice = round(tickerInfo['regularMarketOpen'],2)
            closePrice = round(tickerInfo['previousClose'],2)
            fiftyTwoWeekHigh = round(tickerInfo['fiftyTwoWeekHigh'],2)
            fiftyTwoWeekLow = round(tickerInfo['fiftyTwoWeekLow'],2)
            profitMargin = round(tickerInfo['profitMargins'],3)
            companyInfo = tickerInfo['longBusinessSummary']

            rtnMsg = ""

            # CASE 2A -- Full info
            if(textSplit[1].lower() == "info"):
                rtnMsg += "`{}` is currently trading at ${}\n".format(name, stockPrice)
                rtnMsg += "Last open was ${} and last close ${}.\n".format(openPrice, closePrice)
                rtnMsg += "52 Week H: ${} and 52 Week L: ${}\n".format(fiftyTwoWeekHigh, fiftyTwoWeekLow)
                rtnMsg += "Profit Margin: {}\n".format(profitMargin)
                rtnMsg += "Here is a brief description: \n"
                rtnMsg += companyInfo

            elif(textSplit[1].lower() == "history"):
                hist = ticker.history(period="max")
                financials = ticker.financials
                qFinancials = ticker.quarterly_financials
                majorHolders = ticker.major_holders
                institutionalHolders = ticker.institutional_holders
                balanceSheet = ticker.balance_sheet
                qBalanceSheet = ticker.quarterly_balancesheet
                cashflow = ticker.cashflow
                qCashflow = ticker.quarterly_cashflow
                earnings = ticker.earnings
                qEarnings = ticker.quarterly_earnings
                sustainability = ticker.sustainability
                recs = ticker.recommendations
                cal = ticker.calendar
                options = ticker.options
                optionsChain = ticker.option_chain('2020-12-18')
                w = csv.writer(open("history.csv", "w"))
                for key, val in hist.items():
                    w.writerow([key, val])

                w = csv.writer(open("financials.csv", "w"))
                for key, val in financials.items():
                    w.writerow([key, val])

                w = csv.writer(open("quarterly_financials.csv", "w"))
                for key, val in qFinancials.items():
                    w.writerow([key, val])

                w = csv.writer(open("major_shareholders.csv", "w"))
                for key, val in majorHolders.items():
                    w.writerow([key, val])

                w = csv.writer(open("institutional_shareholders.csv", "w"))
                for key, val in institutionalHolders.items():
                    w.writerow([key, val])

                w = csv.writer(open("balanceSheet.csv", "w"))
                for key, val in balanceSheet.items():
                    w.writerow([key, val])

                w = csv.writer(open("quarterly_balanceSheet.csv", "w"))
                for key, val in qBalanceSheet.items():
                    w.writerow([key, val])

                w = csv.writer(open("cashflow.csv", "w"))
                for key, val in cashflow.items():
                    w.writerow([key, val])

                w = csv.writer(open("quarterly_cashflow.csv", "w"))
                for key, val in qCashflow.items():
                    w.writerow([key, val])

                w = csv.writer(open("earnings.csv", "w"))
                for key, val in earnings.items():
                    w.writerow([key, val])

                w = csv.writer(open("quarterly_earnings.csv", "w"))
                for key, val in qEarnings.items():
                    w.writerow([key, val])

                w = csv.writer(open("sustainibility.csv", "w"))
                for key, val in sustainability.items():
                    w.writerow([key, val])

                w = csv.writer(open("recommendations.csv", "w"))
                for key, val in recs.items():
                    w.writerow([key, val])

                w = csv.writer(open("calendar.csv", "w"))
                for key, val in cal.items():
                    w.writerow([key, val])

                # w = csv.writer(open("options.csv", "w"))
                # for key, val in options.items():
                #     w.writerow([key, val])
                print("Options: ", options)

                # w = csv.writer(open("optionsChain_2020-12-18.csv", "w"))
                # for key, val in optionsChain.items():
                #     w.writerow([key, val])
                print("Options Chain: ", optionsChain)

                pass

                rtnMsg += "--"

            return rtnMsg
        else:
            return "Incorrect arguments"
    else:
        return "Incorrect use of bot"





"""
--------DICT MESSAGE FROM YF
{
'zip': '94304', 
'sector': 'Consumer Cyclical', 
'fullTimeEmployees': 48016, 
'longBusinessSummary': 'Tesla, Inc. designs, develops, manufactures, leases, and s
ells electric vehicles, and energy generation and storage systems in the United States, China, Netherlands, Norway, and internationally. The company operates 
in two segments, Automotive; and Energy Generation and Storage. The Automotive segment offers sedans and sport utility vehicles. It also provides electric pow
ertrain components and systems; and services for electric vehicles through its company-owned service locations, and Tesla mobile service technicians, as well 
as sells used vehicles. This segment markets and sells its products through a network of company-owned stores and galleries, as well as through its own Websit
e. The Energy Generation and Storage segment offers energy storage products, such as rechargeable lithium-ion battery systems for use in homes, industrial, co
mmercial facilities, and utility grids; and designs, manufactures, installs, maintains, leases, and sells solar energy generation and energy storage products 
to residential and commercial customers. It also provides vehicle insurance services, as well as renewable energy. The company was formerly known as Tesla Mot
ors, Inc. and changed its name to Tesla, Inc. in February 2017. Tesla, Inc. was founded in 2003 and is headquartered in Palo Alto, California.', 
'city': 'Palo Alto', 
'phone': '650-681-5000', 
'state': 'CA', 
'country': 'United States', 
'companyOfficers': [], 
'website': 'http://www.tesla.com', 
'maxAge': 1, 
'address1': '3500 Deer Creek Road', 
'industry': 'Auto Manufacturers', 
'previousClose': 639.83, 
'regularMarketOpen': 643.28, 
'twoHundredDayAverage': 373.42252, 
'trailingAnnualDividendYield': None, 
'payoutRatio': 0, 
'volume24Hr': None, 
'regularMarketDayHigh': 646.9, 
'navPrice': None, 
'averageDailyVolume10Day': 59555300, 
'totalAssets': None, 
'regularMarketPreviousClose': 639.83, 
'fiftyDayAverage': 499.4603, 
'trailingAnnualDividendRate': None, 
'open': 643.28, 
'toCurrency': None, 
'averageVolume10days': 59555300, 
'expireDate': None, 
'yield': None, 
'algorithm': None, 
'dividendRate': None, 
'exDividendDate': None, 
'beta': 2.151181, 
'circulatingSupply': None, 
'startDate': None, 
'regularMarketDayLow': 623.83, 
'priceHint': 2, 
'currency': 'USD', 
'trailingPE': 1218.7667, 
'regularMarketVolume': 40256330, 
'lastMarket': None, 
'maxSupply': None, 
'openInterest': None, 
'marketCap': 604206268416, 
'volumeAllCurrencies': None, 
'strikePrice': None, 
'averageVolume': 47851864, 
'priceToSalesTrailing12Months': 21.444006, 
'dayLow': 623.83, 
'ask': 637.7, 
'ytdReturn': None, 
'askSize': 2200, 
'volume': 40256330, 
'fiftyTwoWeekHigh': 654.32, 
'forwardPE': 165.13342, 
'fromCurrency': None, 
'fiveYearAvgDividendYield': None, 
'fiftyTwoWeekLow': 70.102, 
'bid': 637.5, 
'tradeable': False, 
'dividendYield': None, 
'bidSize': 1100, 
'dayHigh': 646.9, 
'exchange': 'NMS', 
'shortName': 'Tesla, Inc.', 
'longName': 'Tesla, Inc.', 
'exchangeTimezoneName': 'America/New_York', 
'exchangeTimezoneShortName': 'EST', 
'isEsgPopulated': False, 
'gmtOffSetMilliseconds': '-18000000', 
'quoteType': 'EQUITY', 
'symbol': 'TSLA', 
'messageBoardId': 'finmb_27444752', 
'market': 'us_market', 
'annualHoldingsTurnover': None, 
'enterpriseToRevenue': 21.6, 
'beta3Year': None, 
'profitMargins': 0.01973, 
'enterpriseToEbitda': 151.43, 
'52WeekChange': 7.4412527, 
'morningStarRiskRating': None, 
'forwardEps': 3.86, 
'revenueQuarterlyGrowth': None, 
'sharesOutstanding': 947900992, 
'fundInceptionDate': None, 
'annualReportExpenseRatio': None, 
'bookValue': 16.91, 
'sharesShort': 46499466, 
'sharesPercentSharesOut': 0.049099997, 
'fundFamily': None, 
'lastFiscalYearEnd': 1577750400, 
'heldPercentInstitutions': 0.42407, 
'netIncomeToCommon': 533000000, 
'trailingEps': 0.523, 
'lastDividendValue': None, 
'SandP52WeekChange': 0.14251125, 
'priceToBook': 37.694557, 
'heldPercentInsiders': 0.20021, 
'nextFiscalYearEnd': 1640908800, 
'mostRecentQuarter': 1601424000, 
'shortRatio': 1.18, 
'sharesShortPreviousMonthDate': 1604016000, 
'floatShares': 759514941, 
'enterpriseValue': 608596328448, 
'threeYearAverageReturn': None, 
'lastSplitDate': 1598832000, 
'lastSplitFactor': '5:1', 
'legalType': None, 
'lastDividendDate': None, 
'morningStarOverallRating': None, 
'earningsQuarterlyGrowth': 1.315, 
'dateShortInterest': 1606694400, 
'pegRatio': 0.77, 
'lastCapGain': None, 
'shortPercentOfFloat': 0.0612, 
'sharesShortPriorMonth': 47802859, 
'impliedSharesOutstanding': None, 
'category': None, 
'fiveYearAverageReturn': None, 
'regularMarketPrice': 643.28, 
'logo_url': 'https://logo.clearbit.com/tesla.com'
}
"""