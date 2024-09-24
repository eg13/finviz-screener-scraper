from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3

VERSION_TYPES = {
    "110": "Overview",
    "120": "Valuation",
    "130": "Ownership",
    "140": "Performance",
    "150": "Custom",
    "160": "Financial",
    "170": "Technical",
}

class FinvizScreenerScraper:

	def __init__(self):
		print("FinvizScreenerScraper initiating...")

		self.base_url = ""  # original url
		self.screen = ""  # page content
		self.pages = ""
		self.cur_page = 0
		self.total_pages = 0
		self.total_rows = 0
		self.screener_results = pd.DataFrame()
		self.watchlist = []

		# url params
		self.version_original = '150'
		self.version_fixed = '150'
		self.row_original = '1'
		self.row = '1'
		self.tickers = ''
		self.filters = ''
		self.custom = ''
		self.order = ''
		self.signal = ''

	def get_page(self, page_url=''):
		""" Gets page content from URL. """

		# self.screen = ""
		if page_url != '':
			headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

			self.screen = requests.get(str(page_url), headers=headers).text
			self.get_navigation_status()

	def get_table(self, page_url=''):
		"""extract table data from current page"""

		self.get_page(page_url=page_url)

		tables = pd.read_html(StringIO(self.screen))
		# get the table with our data
		cur_table = tables[-2]

		return cur_table

	def get_navigation_status(self):
		"""
        Gets the total number of pages in the results
             the total number current page
             the total number of rows(results).
        """

		# find how many pages and whats the next page
		# the paging has an option tag showing 'Page 1 / 22'
		# in each page there are 20 rows
		# to move to the next page we have to pass
		# parameter 'r=21' with the number of first row of the page
		bs = BeautifulSoup(self.screen, "html.parser")
		self.pages = bs.find_all('option', attrs={'value': '1'})[0].text  # 'Page 1 / 22'
		pages = str(self.pages)
		pages = str(pages).replace('Page', '').split('/')

		self.cur_page = int(pages[0])
		self.total_pages = int(pages[1])
		self.total_rows = self.total_pages * 20

	def parse_url(self, url):
		"""Parse URL and save each parameter and it's value in df"""

		split_query = url.replace("https://finviz.com/screener.ashx?", "")
		split_query = split_query.split("&")

		url_param_df = pd.DataFrame()
		for p in split_query:
			url_param = p.split("=")
			# url_param_df.loc[1,url_param[0]] = url_param[1] # save as one row do not split ","
			url_param_values = url_param[1].split(",")

			for i, v in enumerate(url_param_values):
				# print(i,v)
				url_param_df.loc[i, url_param[0]] = v
		try:
			self.version_original = str(url_param_df["v"][url_param_df["v"].notnull()][0])
			self.version_fixed = str(url_param_df["v"][url_param_df["v"].notnull()][0])
		except Exception as e:
			self.version_original = '0'
			self.version_fixed = '0'

		try:
			self.row_original = url_param_df["r"][url_param_df["r"].notnull()][0]
			self.row = url_param_df["r"][url_param_df["r"].notnull()][0]
		except Exception as e:
			self.row_original = 1
			self.row = 1

		try:
			self.tickers = url_param_df["t"][url_param_df["t"].notnull()]
			self.filters = url_param_df["f"][url_param_df["f"].notnull()]
			self.custom = url_param_df["c"][url_param_df["c"].notnull()]
			self.order = url_param_df["o"][url_param_df["o"].notnull()]
			self.signal = url_param_df["s"][url_param_df["s"].notnull()]
		except Exception as e:
			pass

	def fix_base_url(self, base_url):
		""" Change version and row number for base url """

		fixed_url = ""

		# change version to hide filter option view (0 as last digit)
		# (from 112 to 110, from 151 to 150, ... )
		v = int(self.version_original)
		version_original_str = f"v={str(v)}"  # v=151
		self.version_fixed = str(v - (v % 10))  # 150
		version_fixed_str = f"v={self.version_fixed}"  # v=150
		fixed_url = base_url.replace(version_original_str, version_fixed_str)

		r = int(self.row_original)
		base_row_str = f"&r={str(r)}"
		fixed_row_str = ""
		fixed_url = fixed_url.replace(base_row_str, fixed_row_str)

		return fixed_url

	def check_is_valid_version(self, ver):
		is_valid = False

		try:
			table_header = VERSION_TYPES[ver]
			print(f"{table_header} screener page.\n")
			is_valid = True
		except Exception as e:
			print("Not a valid screener page with Tables")
			is_valid = False

		return is_valid

	def load_screener(self, base_url=''):
		"""
            this function calls 'get_finviz_screener()' to get results from finviz screener page
            it moves from page to page and extracts the result table
            returns the results as a dataframe
        """

		# parse all parameters from url
		self.parse_url(base_url)

		# change version and row number for base url
		fixed_url = self.fix_base_url(base_url)

		# check if the version is supported
		if self.check_is_valid_version(self.version_fixed):

			counter = 0
			while True:
				counter += 1

				# first page add '&r=1'
				if counter == 1:
					cur_page_first_row = '1'
				else:
					cur_page_first_row = str(int(counter * 20) + 1)  # '&r=21' ...

				# add &r=21 parameter to url
				cur_url = fixed_url + f"&r={cur_page_first_row}"

				# get current table from current page and add it to df
				cur_table = self.get_table(page_url=cur_url)
				self.screener_results = pd.concat([self.screener_results, cur_table[:]], ignore_index=True)
				print("Page:", counter, " rows: " + str(cur_page_first_row) + ' - ' + str(int(cur_page_first_row) + 19))

				# we have reached the last page
				if counter == self.total_pages:
					print('\nWe have reached the last page \n')
					break

	def export_to_watchlist(self):
		"""
		Extract Tickers to a list
		"""
		self.watchlist = list(self.screener_results['Ticker'])

		return self.watchlist

	def export_to_excel(self, file_path='finviz_results.xlsx'):
		"""
		Export results to Excel
		"""
		print("Export to Excel: ", file_path)
		self.screener_results.to_excel(file_path, index=False)

	def export_to_sqlite(self, file_path='finviz.sqlite3'):
		"""
		Export and Replace a SQLite database
		"""
		conn = sqlite3.connect(file_path)
		table_name = 'screener'
		self.screener_results.to_sql(table_name, conn, if_exists='replace')
		print("Export to SQLite3: ", file_path)


if __name__ == '__main__':
	
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
	print("         scraper.watchlist             ")
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
	print("          export_to_sqlite              ")
	print("---------------------------------------")
	sqlite_path = 'finviz.sqlite3' # r'd:\finviz.sqlite3'
	scraper.export_to_sqlite(file_path=sqlite_path)
	print("\n\n")