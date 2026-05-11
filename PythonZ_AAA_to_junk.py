import pandas as pd




dane_spolki = []
#odczt pliku z danymi spolek
try:
    dane_spolki = pd.read_csv(r"companies_metrics")
except:
    pass
#dodanie testowego aktywa 
dane_spolki.append({
    "name": "Intel",
    "ticker": "INTC",
    "sector": "Technology",
    "Net Debt": None,  # brak danych
    "EBITDA": 9500000000,
    "FFO": None,
    "Debt (total)": 45031000000,
    "CFO": 9700000000,
    "Interest Expense": 282000000,
    "FCF": -4900000000,
    "Cash & Equivalents": 17247000000,
    "Undrawn Credit Lines": 3000000000,
    "Short-Term Debt": 2499000000,
    "EBITDA Margin": 0.1796,
    "Revenue": 52900000000,
    "Equity": 126360000000,
    "Assets": 211429000000,
    "Working Capital": 32110000000,
  })

print(f"Intel powinien byc warty {dane_spolki[0]["EBITDA"]/(10**9)*7}bn")
