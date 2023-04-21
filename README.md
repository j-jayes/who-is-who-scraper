# Who-is-Who Scraper

This project is a web scraper designed to extract information about famous Swedes from the website Who-is-Who ([https://www.whoiswho.se/](https://www.whoiswho.se/) ).
## Requirements

To run this scraper, you will need to have the following installed on your machine:
- Python 3
- pip
- Beautiful Soup 4
- Requests
## Installation

To install the necessary dependencies, run the following command in your terminal:

```

pip install beautifulsoup4 requests
```


## Usage

To run the scraper, simply run the following command in your terminal:

```

python scrape.py
```



The scraper will output a CSV file containing the following information for each famous Swede listed on Who-is-Who:
- Name
- Birth year
- Profession
- Link to their Who-is-Who page
## Limitations

Please note that scraping websites without permission may violate their terms of service and/or be illegal. It is your responsibility to ensure that you have the legal right to scrape the website in question before running this scraper.
## License

This project is licensed under the MIT License. See the LICENSE file for more information.
## Acknowledgements

This project was inspired by the Who-is-Who website ([https://www.whoiswho.se/](https://www.whoiswho.se/) ), and uses Beautiful Soup 4 and Requests to scrape data from it.