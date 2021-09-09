# stockXscraper_Updated

This is a failed attempt to scrape StockX. You can use it as a reference for your own bot but it won't get you very far on scraping the website.

Method used:
1. BeautifulSoup -> Doesn't work with sales history data, which requires toggling the button
2. Selenium -> Able to mimic toggling; The scraper works for HTML pages. However, for each request, StockX only returns first 1000 data points and buries the rest. Selenium cannot scrape all data
3. Directly make requests to database -> Theratically you would be able to scrape all data. However, you will have to keep changing headers & ip address to aviod security, which could involve legal issues



