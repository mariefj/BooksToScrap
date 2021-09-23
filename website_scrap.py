import requests
from bs4 import BeautifulSoup
import csv


def get_soup(url):
	reponse = requests.get(url)
	page = reponse.content

	return BeautifulSoup(page, "html.parser")


def extract_product_data(url, soup):
	universal_product_code = soup.find("th", text="UPC").next_sibling.string
	title = soup.find("div", class_="product_main").h1.string
	price_including_tax = soup.find("th", text="Price (incl. tax)").next_sibling.string
	price_excluding_tax = soup.find("th", text="Price (excl. tax)").next_sibling.string
	number_available = extract_nb_str(soup.find("th", text="Availability").find_next("td").string)
	if soup.find(id="product_description") is None:
		product_description = ""
	else:
		product_description = soup.find(id="product_description").find_next("p").string
	category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
	review_rating = soup.find("p", class_="star-rating")['class'][1]
	image_url = soup.find("img", alt=title)["src"]


	return [
		url,
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


def extract_nb_str(str):
	num = ""

	for char in str:
		if char.isdigit():
			num += char

	return num


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

def get_list_categories(soup, url):
	url_categories = []
	for link in soup.select('a[href^="catalogue/category/books/"]'):
		url_categories.append((url.replace("index.html", link["href"]), link.string.strip()))

	return url_categories


def load_data(file_name, header, data):
	with open("csv/csv_website_scrap/" + file_name + ".csv", 'w') as file_csv:
		writer = csv.writer(file_csv, delimiter=',')
		writer.writerow(header)
		for item in data:
			writer.writerow(item)


def download_img(url, name):
	new_url = url.replace("../..", "http://books.toscrape.com")
	new_name = name.replace("/", " ")
	response = requests.get(new_url)
	img = response.content
	with open("img/" + new_name + ".jpg", "wb") as handler:
		handler.write(img)


def etl_category(url, name):
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
		data_product = extract_product_data(url, soup)
		data.append(data_product)
		download_img(data_product[9], data_product[2])
	load_data(name, header, data)


def etl_website():
	url = "http://books.toscrape.com/index.html"
	soup = get_soup(url)

	list_categories = get_list_categories(soup, url)
	for category in list_categories:
		etl_category(category[0], category[1])


etl_website()
