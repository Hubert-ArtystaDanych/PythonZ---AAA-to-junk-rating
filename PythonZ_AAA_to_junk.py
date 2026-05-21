import pandas as pd
# import matplotlib.pyplot as plt
import time as t
import json
import random as r
from typing import Generator

#uzycie zmiennej ilosci argumentów
def inital_assessment(stock, *stocks):
    #funkcje przetwarzających łańcuch znaków
    #funkcja f string
    #stock = stock[0] -> odkomentowac pozniej 
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
    equity_ratio = stock["Kapital_wlasny"] / stock["Aktywa_ogolem"]
    net_debt = stock["Dlug_dlugoterminowy"] - stock["Przychody_ogolem"]
    assets_turnover = stock["Aktywa_ogolem"]/stock["Przychody_ogolem"]
    inventory_level = stock["Zapasy"]/stock["Przychody_ogolem"]
    
    indicators = {
    "sektor": stock["Sektor"],
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
    print("\n")
        
    #ternary
    profitability = True if ros > 0 and o_margin > 0 else False
    #operator is
    if profitability is True:
        print("Działalność spółki jest rentowna")
    else: 
        print("Działalność spółki nie jest rentowna")
    print("\n")

    #uzycie iteratora
    zysk_iter = iter(stock["Zysk_strata_netto"])
    print("Zyski firmy na przestrzeni lat: ")
    rok = 2025
    for it in range(5):
        print(rok, " - ", next(zysk_iter), end="; ")
    print("\n")
    
    return indicators

#typowanie zmiennych
#argumenty domyslne
def rating(a: dict, scrutiny:int = 0):
    if a["sektor"] not in prefered_sectors:
        scrutiny += 1
        if scrutiny > 9:
            scrutiny = 9
    # print("Wskazniki spolki: ")
    # for wskaznik in a:
    #     print(wskaznik, " -> ", a[wskaznik])
    points = 25

        #uzycie nested functions

    def no_more_than_ten(pts: float):
        if pts>10:
            return 10
        else:
            return pts
    def pokaz_punkty(wskaznik: str, pts: float):
        pts = int(round(pts,0))
        print(f"Wskaznik {wskaznik} dodal {pts} do oceny")
        return None

    #uzycie lambda
    simple_as = lambda indic: no_more_than_ten(indic * 90)/3
    enterprise_size_bonus = lambda ebitda: (
        100 if ebitda > 10000 else
        50 if ebitda > 1000 else
        25 if ebitda > 500 else
        10 if ebitda > 100 else
        5 if ebitda > 25 else
        0
    )
    
    points +=simple_as(a["ros"])
    pokaz_punkty("ros",simple_as(a["ros"]))
    points +=simple_as(a["roe"]) * 3
    pokaz_punkty("roe",simple_as(a["roe"]))
    points +=simple_as(a["o_margin"])
    pokaz_punkty("o_margin",simple_as(a["o_margin"]))
    points +=simple_as(a["roa"]) * 2
    pokaz_punkty("roa",simple_as(a["roa"]))
    points +=enterprise_size_bonus(a["ebitda"])
    pokaz_punkty("ebitda",enterprise_size_bonus(a["ebitda"]))
    points +=enterprise_size_bonus(a["net_debt"]+7*a["ebitda"])/1.8
    pokaz_punkty("net debt -3 x ebitda",enterprise_size_bonus(a["net_debt"]+3*a["ebitda"])/1.8)
    points = points - simple_as(a["debt_ratio"])*6
    pokaz_punkty("debt_ratio",simple_as(a["debt_ratio"])*6)
    points = points + simple_as(a["equity_ratio"]) * 2 #equity ratio
    pokaz_punkty("equity_ratio",simple_as(a["equity_ratio"]))
    #uzycie walrus := 
    if(inventory_usage:= simple_as(a["inventory_level"])) == 10:
        points = points - inventory_usage /2
    else:
        points = points - inventory_usage/4
    pokaz_punkty("inventory_level", simple_as(a["inventory_level"]))
    #uzycie match, uzycie pass
    match a["sektor"]:
        case "Information Technology":
            points = points + 10
        case "Energy":
            points = points + 10
        case "Financials":
            points = points - 10
        case "Consumer Staples":
            pass
        case _:
            point = points + sector_credit_risk[a["sektor"]]
    pokaz_punkty("sektor", 10)


    return (points * ((10-scrutiny)/10) if points > 0 else 0)


def summary(Punkty, Stock):
    nazwa = Stock["Podmiot"]
    result = (
        'AAA' if Punkty > 100 else
        'AA' if Punkty > 90 else
        'A' if Punkty > 80 else
        'BBB' if Punkty > 70 else
        'BB' if Punkty > 50 else
        'B' if Punkty > 25 else
        'CCC' if Punkty > 10 else
        'Junk'
    )
    return result
    
#deklaracja generatora 
def est_debt_cost(Stock: dict, wibor_3m = 0.05) -> Generator[float, None, None]:
    """"Cost of debt based on risk deducted from financial indicators"""
    for klucz in Stock:
      Punkty = Stock[klucz]
      margin = ( 
      0.005 if Punkty > 100 else
      0.01 - (Punkty/10000)if Punkty > 90 else
      0.02 - (Punkty/10000)if Punkty > 75 else
      0.04 - (Punkty/10000)if Punkty > 25 else
      0.19
      )
      cost_of_debt = wibor_3m + margin
      yield  (f"Spółka {klucz} powinna miec koszt dlugu {round(cost_of_debt,2)*100}%") if cost_of_debt < 0.20 else f"Spółka {klucz} jest nieinwestowalna"


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
prefered_sectors = ("Energy","Information Technology","Consumer Staples")
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
#uzycie with
with open (r"C:\Users\hubert.dubiel\Documents\Coding_Files\companies_metrics.json","r") as f:
    dane_spolki_json = json.load(f)

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
indicators = inital_assessment(dane_spolki[0])
#print(indicators)
punkty = rating(indicators)
#print(f"Analizowane spolki: {",".join([stock["Podmiot"], stocks["Podmiot"],])}") -> na pozniej 
print(f"Ilosc punktow za ocene kredytowa: {punkty:.0f}pkt")

all_stocks = {}
for sto in dane_spolki_json:
    #liczenie wskaznikow
    indicators = inital_assessment(sto)
    # losowanie czy firma bedzie ostrozniej oceniana
    if r.randint(0,10) < 5:
        scr = 2
    else:
        scr = 0
    #przyznawanie punktow
    punkty = rating(indicators,scrutiny=scr)
    print(f"Ilosc punktow {sto["Podmiot"]}za ocene kredytowa: {punkty:.0f}pkt")
    all_stocks[sto["Podmiot"]] = punkty

print("\n")
#uzycie generatora
gen = est_debt_cost(all_stocks)

for ita in dane_spolki_json:
    al = ita["Podmiot"]
    print(f"Spolka {al} otrzymala: {all_stocks[al]:.0f}pkt rating: {summary(all_stocks[al],ita)}")
    print(next(gen))
    print("\n")