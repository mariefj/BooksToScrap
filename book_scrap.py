import requests
from bs4 import BeautifulSoup
import csv


def extract_nb_str(str):
	num = ""

	for char in str:
		if char.isdigit():
			num += char

	return num



def extract_product_data(url, soup):
	product_page_url = url
	universal_product_code = soup.find("th", text="UPC").next_sibling.string
	title = soup.find("div", class_="product_main").h1.string
	price_including_tax = soup.find("th", text="Price (incl. tax)").next_sibling.string
	price_excluding_tax = soup.find("th", text="Price (excl. tax)").next_sibling.string
	number_available = extract_nb_str(soup.find("th", text="Availability").find_next("td").string)
	product_description = soup.find(id="product_description").find_next("p").string
	category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
	review_rating = soup.find("p", class_="star-rating")['class'][1]
	image_url = soup.find("img", alt=title)["src"]

	return [
		product_page_url,
		universal_product_code,
		title,
		price_including_tax,
		price_excluding_tax,
		number_available,
		product_description,
		category,
		review_rating,
		image_url
	]


def load_data(file_name, header, data):
	with open(file_name, 'w') as file_csv:
		writer = csv.writer(file_csv, delimiter=',')
		writer.writerow(header)
		writer.writerow(data)


def get_soup(url):
	reponse = requests.get(url)
	page = reponse.content

	return BeautifulSoup(page, "html.parser")


def etl():
	url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
	soup = get_soup(url)

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
	data = extract_product_data(url, soup)
	load_data("csv/csv_book_scrap/book_scrap.csv", header, data)

# etl()
