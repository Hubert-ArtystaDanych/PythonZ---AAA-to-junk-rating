# import pandas as pd
# import matplotlib.pyplot as plt

def inital_assessment(stock, *stocks):
    #funkcje przetwarzających łańcuch znaków
    ticker = ".".join([stock["Ticker"],"US"])
    print("\n")
    print(f"Analiza spółki {stock["Podmiot"]} o tickerze  {ticker}")
    print("Rentownosć na sprzedaży {}%".format(round(stock["Zysk_strata_netto"]/stock["Przychody_ogolem"],5)*100))
    return None


# def rating():
#     match
#         case 6:
    
#     pass

def summary(*args):
    pass
    


dane_spolki = []
#odczt pliku z danymi spolek
try:
    dane_spolki = pd.read_csv(r"companies_metrics")
except:
    pass

#dodanie testowej spolki  
dane_spolki.append(
    {
        "Podmiot": "Intel Corporation",
        "Sektor": "Semiconductors",
        "Ticker": "INTC",
        "Najwazniejsze_produkty": "Mikroprocesory (Intel Core, Intel Xeon, Intel Atom, Intel Pentium, Intel Celeron), procesory graficzne (Intel Arc), chipset'y, kontrolery sieciowe, FPGA",
        "Koniec_roku_fiskalnego": "27 grudnia 2025",
        "Przychody_ogolem": 52853,
        "Zysk_strata_netto": -267,
        "Aktywa_ogolem": 211429,
        "Zobowiazania_ogolem": 85069,
        "Kapital_wlasny": 114281,
        "Gotowka_i_ekwiwalenty": 14265,
        "Dlug_dlugoterminowy": 44086,
        "Wynik_operacyjny": -2214,
        "Amortyzacja_deprecjacja": 10757,
        "Zapasy": 11618}
)


print(f"{dane_spolki[0]["Podmiot"]} powinien byc warty {dane_spolki[0]["Zysk_strata_netto"]/1000*7}bn")
inital_assessment(dane_spolki[0], dane_spolki[:1])
#print(f"Analizowane spolki: {",".join([stock["Podmiot"], stocks["Podmiot"],])}") -> na pozniej 