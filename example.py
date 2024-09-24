
from finviz_screener_scraper import FinvizScreenerScraper

scraper = FinvizScreenerScraper()

url = 'https://finviz.com/screener.ashx?v=152&f=ipodate_more1,sh_avgvol_o1000,sh_curvol_o20000,sh_price_o5&c=0,1,2,3,4,5,6,7,48,49,52,53,54,59,68,61,63,67,69,65,66'

scraper.load_screener(base_url=url)
print("---------------------------------------")
print("         screener_results              ")
print("---------------------------------------")
print(scraper.screener_results.head(5))
print("\n\n")

watchlist = scraper.export_to_watchlist()
print("---------------------------------------")
print("         scraper.watchlist          ")
print("---------------------------------------")
print(scraper.watchlist)
print("\n\n")

print("---------------------------------------")
print("            watchlist                  ")
print("---------------------------------------")
print(watchlist)
print("\n\n")


print("---------------------------------------")
print("          export_to_excel              ")
print("---------------------------------------")
excel_path = 'finviz_results.xlsx' # r'd:\finviz_results.xlsx'
scraper.export_to_excel(file_path=excel_path)
print("\n\n")


print("---------------------------------------")
print("          export_to_sqlite             ")
print("---------------------------------------")
sqlite_path = 'finviz.sqlite3' # r'd:\finviz.sqlite3'
scraper.export_to_sqlite(file_path=sqlite_path)
print("\n\n")