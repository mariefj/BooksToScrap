## Overview

This script is designed to extract pricing information from the Books To Scrap bookstore : http://books.toscrape.com/

The script - website_scrap.py - extracts information from all books of the website, and also download the pictures of the products in empty folders - csv/ and img/ - contained in this repository.

## Installation

First, start by cloning the repository:

```
git clone https://github.com/mariefj/BooksToScrap.git
```

- Access the project folder
```
cd BooksToScrap
```

- Create a virtual environment
```
python -m venv env
```

- Enable the virtual environment
```
source env/bin/activate
```

- Install the python dependencies on the virtual environment
```
pip install -r requirements.txt
```

- Start
```
python website_scrap.py
```
