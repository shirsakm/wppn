# WPPN Scraper

A Python module to scrape Washington Post Public Notices, built on Selenium. The module aims to headlessly scrape the notices, and store them in a `.csv` file for further usage.
It can be extended to improve end-user functionality, either as a TUI application or integration with backend services like Flask or Django.

## Usage

### Environment setup

#### Windows

Create and activate a virtual environment in Python.
```
python -m venv .venv
.\.venv\bin\activate
```

Install the required modules using `pip`.
```
pip install -r requirements.txt
```

Create a `data` directory.
```
mkdir .\data
```

Run `app.py` after making modifications, if required.
```
python .\app.py
```

#### Linux
```bash
python -m venv .venv
source ./.venv/bin/activate
```

Install the required modules using `pip`.
```bash
pip install -r requirements.txt
```

Create a `data` directory.
```bash
mkdir ./data
```

Run `app.py` after making modifications, if required.
```bash
python ./app.py
```
