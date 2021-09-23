import requests
from bs4 import BeautifulSoup
import csv

from book_scrap import extract_product_data, get_soup


def extract_nb_str_array(str):
	return [int(i) for i in str.split() if i.isdigit()]


def get_nb_page(soup):
	pager = soup.find(class_="pager")
	if pager:
		return extract_nb_str_array(pager.find(class_="current").string)[1]

	return 1


def get_url_pages(nb_page, url_start):
	url_pages = [url_start]
	for i in range(2, nb_page + 1, 1):
		url_pages.append(url_start.replace("index", "page-" + str(i)))

	return url_pages


def get_url_products(url_pages, url_start):
	url_products = []
	for url in url_pages:
		soup = get_soup(url)
		for link in soup.select("[class=image_container] > a"):
			url_products.append(link["href"].replace("../../..", "http://books.toscrape.com/catalogue"))

	return url_products


def load_data(file_name, header, data):
	with open(file_name, 'w') as file_csv:
		writer = csv.writer(file_csv, delimiter=',')
		writer.writerow(header)
		for item in data:
			writer.writerow(item)


def etl():
	url = "http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
	soup = get_soup(url)

	nb_page = get_nb_page(soup)
	url_pages = get_url_pages(nb_page, url)
	url_products = get_url_products(url_pages, url)

	header = [
		"product_page_url",
		"universal_product_code",
		"title",
		"price_including_tax",
		"price_excluding_tax",
		"number_available",
		"product_description",
		"category",
		"review_rating",
		"image_url"
	]

	data = []
	for url in url_products:
		soup = get_soup(url)
		data.append(extract_product_data(url, soup))
	load_data("csv/csv_category_scrap/category_scrap.csv", header, data)

# etl()