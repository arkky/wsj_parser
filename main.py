import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
import warnings
  
warnings.filterwarnings('ignore')


def get_pages(url: str, name: str):
    for page in range(1, int(page_data[name])+1):
        time.sleep(2)
        url_page = url + str(page)
        response = requests.get(url_page, headers=headers)
        with open(f"data/{name}/pages/page_{page}.html", "w") as f:
            f.write(response.text)


def get_links(name):
    with open(f"data/{name}/links/all_links.txt", "w") as f:
        pass
    codes = [open(f"data/{name}/pages/page_{x}.html").read() for x in range(1, int(page_data[name])+1)]
    for code in codes[:1]: # delete [:1] from codes[:1]
        soup = bs(code, "html.parser")
        tbody = soup.find("table").find("tbody")
        links_a = tbody.find_all("a")
        with open(f"data/{name}/links/all_links.txt", "a") as f:
            for link in links_a:
                f.write(link["href"] + "\n")


def get_info(name):
    # example url - https://www.wsj.com/market-data/quotes/TGIFF/company-people
    # empty DataFrame for saving rows
    df = pd.DataFrame(columns=["sector", "country", "name", "sales", "email"])

    # read links
    with open(f"data/{name}/links/all_links.txt", "r") as f:
        text = f.read()
    urls = text.split("\n")[:-1]
    urls = [x + "/company-people" for x in urls]
    counter = 1

    # loop urls
    for url in urls:
        try:
            time.sleep(2)
            response = requests.get(url, headers=headers)
            soup = bs(response.text, "html.parser")

            row = {"sector": None, "country": None, "name": None, "sales": None, "email": None}

            # get email
            ul = soup.find("ul", class_="company-web")
            a_email = ul.find_all("a")[0]
            if "mail" in a_email.text.lower() and "null" not in a_email['href']:
                email = a_email["href"].split(":")[-1]
                row['email'] = email
            else:
                print("current link:", counter)
                counter += 1
                continue

            # get Sector and Sales or Revenue
            main_div = soup.find("div", class_="cr_overview_data cr_data")
            divs = main_div.find_all("div")
            sector, sales = None, None
            for div in divs:
                div_span = div.find("span", class_="data_lbl")
                if "Sector" in div_span.text:
                    sector = div.find("span", class_="data_data").text.strip()
                if "Sales or Revenue" in div_span.text:
                    sales = div.find("span", class_="data_data").text.strip()
            row['sector'] = sector
            row['sales'] = sales

            # get company name
            div = soup.find("div", id="cr_info_mod")
            company_name = div.find("h3").span.text
            row['name'] = company_name

            # get country
            country = soup.find("span", class_="country").text
            row['country'] = country

            df = df.append(row, ignore_index=True)
        except Exception as e:
            print(e)
            print(url)
        print(f"current link: {counter}/{len(urls)}")
        print("Total companies include duplicates:", len(df))
        print()
        counter += 1
    df.drop_duplicates(subset=["email"], inplace=True)
    df.to_excel(f"data/{name}/excels/{name}.xlsx", sheet_name="main_info", index=False)


def get_dev(url):
    response = requests.get(url, headers=headers)
    with open(f"trash/company_list.html", "w") as f:
        f.write(response.text)


def get_categories():
    time.sleep(2)
    response = open("trash/company_list.html", "r").read()
    soup = bs(response, "html.parser")
    div = soup.find("div", class_="index-sector border-box")
    urls = div.find_all("a")
    for url in urls:
        category_url = url['href'] + "/"
        category = "-".join("-".join(url.text.lower().replace("&", "").strip().split()).split("/"))
        print(category)
        os.makedirs(f"data/{category}", exist_ok=True)
        os.makedirs(f"data/{category}/excels", exist_ok=True)
        os.makedirs(f"data/{category}/links", exist_ok=True)
        os.makedirs(f"data/{category}/pages", exist_ok=True)
        get_pages(category_url, category)
        get_links(category)
        get_info(category)


if __name__ == "__main__":
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    headers = {"User-Agent": user_agent}
    pages = open("data/category_pages", "r").read()
    page_data = pages.split("\n")
    page_data = [x.split(":") for x in page_data]
    page_data = {x: y for x, y in page_data}
    html_code = open("trash/company_list.html", "r").read()
    soup = bs(html_code, "html.parser")
    div = soup.find("div", class_="index-sector border-box")
    category_tags = div.find_all("a")
    os.makedirs(f"data", exist_ok=True)
    for category_tag in category_tags[1:]:
        category_url = category_tag['href'] + "/"
        category = "-".join("-".join(category_tag.text.lower().replace("&", "").strip().split()).split("/"))
        os.makedirs(f"data/{category}", exist_ok=True)
        os.makedirs(f"data/{category}/excels", exist_ok=True)
        os.makedirs(f"data/{category}/links", exist_ok=True)
        os.makedirs(f"data/{category}/pages", exist_ok=True)
        get_pages(category_url, category) # func 1
        print(f"Func 1 was executed")
        get_links(category) # func 2
        print(f"Func 2 was executed")
        get_info(category) # func 3
        print(f"Func 3 was executed")
