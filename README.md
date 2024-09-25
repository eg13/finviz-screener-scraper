# Finviz Screener Scraper

## Overview
**FinvizScreenerScraper** is a Python class designed to scrape and download result tables from the Finviz website. This tool allows users to automate the extraction of financial data, making it easier to analyze and utilize for various financial and investment purposes.

## Features
- **Automated Data Extraction**: Scrape result tables from Finviz with ease.
- **Customizable Filters**: Apply various filters to tailor the data to your needs.
- **Export to Excel**: Export the scraped data to Excel .xlsx format for further analysis.
- **Export to SQLite**: Export the scraped data to SQLite DB for further analysis.

## Installation
To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

&nbsp;

## Usage

### Using Finviz Screener
Go to Finviz website's screener [https://finviz.com/screener.ashx](https://finviz.com/screener.ashx)

Change the filters and settings and the URL will automatically adjust. 

![Finviz](https://github.com/eg13/finviz-screener-scraper/blob/main/assets/images/Finviz.JPG))



### Using the **FinvizScreenerScraper** class
When you are setisfied with the results copy the **url address** and paste it as the url patameter.

url = 'https://finviz.com/screener.ashx?v=152&f=ipodate_more1,sh_avgvol_o1000,sh_curvol_o20000,sh_price_o5&c=0,1,2,3,4,5,6,7,48,49,52,53,54,59,68,61,63,67,69,65,66'


Here's a basic example of how to use the **FinvizScreenerScraper** class:
```python

from finviz_screener_scraper import FinvizScreenerScraper

# Initialize the scraper
scraper = FinvizScreenerScraper()

# copy the Finviz website url
url = 'https://finviz.com/screener.ashx?v=152&f=ipodate_more1,sh_avgvol_o1000,sh_curvol_o20000,sh_price_o5&c=0,1,2,3,4,5,6,7,48,49,52,53,54,59,68,61,63,67,69,65,66'

# load the screener results into scraper.screener_results DataFrame
scraper.load_screener(base_url=url)
print(scraper.screener_results)

# return a list of all the Tickers in screener results
watchlist = scraper.export_to_watchlist()

# Export results to Excel
excel_path = 'finviz_results.xlsx' # r'd:\finviz_results.xlsx'
scraper.export_to_excel(file_path=excel_path)

# Export results to SQLite
sqlite_path = 'finviz.sqlite3' # r'd:\finviz.sqlite3'
scraper.export_to_sqlite(file_path=sqlite_path)
```

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.




