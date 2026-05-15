# import pandas as pd
# import matplotlib.pyplot as plt
import time as t
import json

#uzycie zmiennej ilosci argumentów
def inital_assessment(stock, *stocks):
    #funkcje przetwarzających łańcuch znaków
    #funkcja f string
    stock = stock[0]
    ticker = ".".join([stock["Ticker"],"US"])
    zysk_2025 = stock["Zysk_strata_netto"][0]
    sector_pl = sectors_translated[stock["Sektor"]]
    print("\n")
    print(f"Analiza spółki {stock["Podmiot"]} o tickerze {ticker} z sektora {sector_pl}")
    temp = len(f"Analiza spółki {stock["Podmiot"]} o tickerze {ticker} z sektora {sector_pl}")
    print("Analiza".center(temp, "-"))
    t.sleep(1)
    ros = zysk_2025/stock["Przychody_ogolem"]
    roe = zysk_2025/stock["Kapital_wlasny"]
    roa = zysk_2025/stock["Aktywa_ogolem"]
    o_margin = stock["Wynik_operacyjny"] / stock["Przychody_ogolem"]
    ebitda = stock["Wynik_operacyjny"] + stock["Amortyzacja_deprecjacja"]
    debt_ratio = stock["Dlug_dlugoterminowy"]/stock["Kapital_wlasny"]
    equity_ratio = stock["Kapital_wlasny"] - stock["Aktywa_ogolem"]
    net_debt = stock["Dlug_dlugoterminowy"] - stock["Przychody_ogolem"]
    assets_turnover = stock["Aktywa_ogolem"]/stock["Przychody_ogolem"]
    inventory_level = stock["Zapasy"]/stock["Przychody_ogolem"]
    
    indicators = {
    "ros": ros,
    "roe": roe,
    "roa": roa,
    "o_margin": o_margin,
    "ebitda": ebitda,
    "debt_ratio": debt_ratio,
    "equity_ratio": equity_ratio,
    "net_debt": net_debt,
    "assets_turnover": assets_turnover,
    "inventory_level": inventory_level
}

    #avg profit level
    #stdiv of profits
    print("Rentownosć na sprzedaży {}%".format(round(ros,3)*100))
    print("Rentowność operacyjna {}%".format(round(o_margin,3)*100))
    print("Rentowność na kapitale własnym {}%".format(round(roe,3)*100))
    print("Rentowność na aktywach {}%".format(round(roa,3)*100))

    #ternary
    profitability = True if ros > 0 and o_margin > 0 else False
    #operator is
    if profitability is True:
        print("Działalność spółki jest rentowna")
    else: 
        print("Działalność spółki nie jest rentowna")
    print("\n")

    #...wskaźniki


    #przekazanie wskaźników
    #inital_assessment(stocks[0],stocks[:1])
    return indicators

#typowanie zmiennych
def rating(a: dict, scrutiny = 1): #<-- odebranie wskaźników 
    #match do kapitalizacji + pass dla najmniejszej 
    #match do branży
    match a:
        case 6:
            pass
    #wyswietla kontent i zwraca punkty 
    #range od zera do 100 pkt
    return points

#
def summary(nazwa, ticker):
    pass
    
sector_credit_risk = {
    "Energy": 3,
    "Materials": 3,
    "Industrials": 4,
    "Consumer Discretionary": 3,
    "Consumer Staples": 5,
    "Health Care": 4,
    "Financials": 3,
    "Information Technology": 4,
    "Communication Services": 3,
    "Utilities": 5,
    "Real Estate": 3}
sectors_translated  = {
    "Energy": "Energetyka",
    "Materials": "Materiały",
    "Industrials": "Przemysł",
    "Consumer Discretionary": "Dobra konsumpcyjne cykliczne",
    "Consumer Staples": "Dobra konsumpcyjne podstawowe",
    "Health Care": "Ochrona zdrowia",
    "Financials": "Finanse",
    "Information Technology": "Technologie informacyjne",
    "Communication Services": "Usługi komunikacyjne",
    "Utilities": "Użyteczność publiczna",
    "Real Estate": "Nieruchomości"}


dane_spolki = []
#odczt pliku z danymi spolek
with open (r"C:\Users\hubert.dubiel\Documents\Coding_Files\companies_metrics.json","r") as f:
    dane_spolki_json = json.load(f)
#print(dane_spolki_json[1])

# try:
#     dane_spolki = pd.read_csv(r"C:\Users\hubert.dubiel\Documents\Coding_Files\companies_metrics.json") as f:
# except:
#     pass

#dodanie testowej spolki  
dane_spolki.append(
    {
        "Podmiot": "Intel Corporation",
        "Sektor": "Information Technology",
        "Ticker": "INTC",
        "Najwazniejsze_produkty": "Mikroprocesory (Intel Core, Intel Xeon, Intel Atom, Intel Pentium, Intel Celeron), procesory graficzne (Intel Arc), chipset'y, kontrolery sieciowe, FPGA",
        "Koniec_roku_fiskalnego": "27 grudnia 2025",
        "Przychody_ogolem": 52853,
        "Zysk_strata_netto": [-267, -18756, 1689, 8014, 19868],
        "Aktywa_ogolem": 211429,
        "Zobowiazania_ogolem": 85069,
        "Kapital_wlasny": 114281,
        "Gotowka_i_ekwiwalenty": 14265,
        "Dlug_dlugoterminowy": 44086,
        "Wynik_operacyjny": -2214,
        "Amortyzacja_deprecjacja": 10757,
        "Zapasy": 11618}
)


print(f"{dane_spolki[0]["Podmiot"]} powinien byc warty {dane_spolki[0]["Zysk_strata_netto"][0]/1000*7:.2f}bn")
indicators = inital_assessment(dane_spolki, dane_spolki_json)
print(indicators)
punkty = rating(indicators)
#print(f"Analizowane spolki: {",".join([stock["Podmiot"], stocks["Podmiot"],])}") -> na pozniej 