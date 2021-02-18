<!-- ABOUT THE PROJECT -->

# About The Project

![Scraper tag][product-screenshot]

This is a demo project that scrapes book information from [books.toscrape.com](https://books.toscrape.com). This demo uses a lot of features of Scrapy like image pipeline, configuring crawl arguments to get different results, and scrapy with selenium working together.

This scrapy project has three spiders:

- **_books_** : that collects only books from the homepage
- **_books_selenium_** : gets all books in site pagination using selenium
- **_books_only_scrapy_** : gets all books in site pagination using only scrapy

This site doesn't have javascript rendering, so the spider with selenium is just for demonstration purposes. The scrapy only version obviously is much faster than selenium.

## Built With

- [Python](https://www.python.org)
- [Scrapy](https://scrapy.org)
- [Selenium WebDriver](https://www.selenium.dev)

## Prerequisites

This application requires the following software components:

- Python (I recommend install as a virtual environment).

  To install Python follow instructions at https://www.python.org. After Python installation on your system run these commands in the project folder :

  ```sh
  pip install virtualenv
  virtualenv venv
  ./venv/Scripts/activate
  ```

  Install these Python librarys on your system or virtual environment:

- Scrapy

  ```sh
  pip install scrapy
  ```

- Selenium

  ```sh
  pip install selenium
  ```

- Pillow (used for image pipeline)
  ```sh
  pip install pillow
  ```

## Installation

- See the prerequisites above and clone the repo inside a folder.

```sh
git clone https://github.com/vol-automation/webscraping-books_scrapy_scraper.git
```

## Usage

There are three spiders. Bellow the usage of each one:

### 1. Spider **_books_** :

```sh
scrapy crawl books -o homepage.csv
```

where:

- **_-o name_of_file.csv_** exports a CSV file at the root of the project

* this spider also generates an excel file (.xlsx) with the same name as the CSV file

### 2. Spider **_books_selenium_** :

| This features selenium to fetch the pagination pages and scrapy fetching book details pages |
| ------------------------------------------------------------------------------------------- |

```sh
scrapy crawl books_selenium -o books_selenium.csv
```

where:

- **_-o name_of_file.csv_** exports a csv file at the root of project

### 3. Spider **_books_only_scrapy_** :

| This spider has two variations:

1. Get only specific category page:

```sh
scrapy crawl books_only_scrapy -a category="https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html" -o output.csv
```

where:

- **_-a category="category_page_url_**" copy URL of a category page and add to this argument. This way the spider only get data from this category
- **_-o output.csv_** exports a CSV file at the root of the project. The name doesn't matter because this spider renames the artifact to books-_[category_name]_.csv (like books-philosophy.csv)

2. Get all pages:

```sh
scrapy crawl books_only_scrapy -o output.csv
```

| this spider saves all images using scrapy image pipeline. Images are saved at **_[project root path]_**_/downloads/images_ folder |
| --------------------------------------------------------------------------------------------------------------------------------- |

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: images/tag.png
