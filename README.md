# Web Scrapper Pipeline

This is a demo project to compare two web scrapping frameworks, Playwright and Selenium and using the new Pipelining tool Dagster


## Getting Started

### Install Dependencies

To install dependencies simply run:

`pip install -r requirements.txt`

Alternatively, to use virtual environments easily you can run:

`pip install pipenv`

And then:

`pipenv install`

### Individual modes

To run with a particular configuration simply run `python -m app {mode}`

Available modes are:

- playwright
- selenium
- selenium_multi
- selenium_dagster
- playwright_dagster

### Benchmark

To run the benchmark:

1. Update your Neptune.AI key in the `.env` file
1. Run `python -m app.run_benchmark`
