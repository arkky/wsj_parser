# Company email parser from wsj.com

# Features

- This parser receives data about the name of the company, the country of the company, the sales volume of the company and the official email of the company
- All necessary links and html pages are saved in the project

# Usage

1) pip install requests beautifulsoup4 pandas openpyxl
2) python3 main.py
3) Get your emails for each company on wsj

## P.S.

At the moment, requests are synchronous and the process of parsing all mails can take several days. In the future, maybe I will write asynchronous logic