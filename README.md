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

### Editing `app.py`

While you can use the module in any way required, app.py is the entrypoint when you open the project.

First, we must initialize a `Scraper` object, as follows.
```py
from wppn import Scraper
scraper = Scraper('https://publicnotices.washingtonpost.com/')
```

The object provides two key public functions, `search(...)` and `save_all_notices(...)`; while the rest are intended for internal usage.

`search(...)` takes all the search arguments that can be given in the Washington Post Public Notices form.


| Args | Note |
| :----- | :------: |
| search_phrase | The text to be entered in the free text search bar |
| start_date | A Python `datetime` object |
| end_date | A Python `datetime` object |
| states | A list of states to be selected (e.g. `['DC', 'Maryland']`) |
| counties | A list of counties to be selected (e.g. `['District of Columbia']`) |
| notice_types | A list of the notice types to be selected (e.g. `['Legal Notices']`) |

`save_all_notices(...)` accpets one argument, where `path` gives the relative path and name of the `.csv` file where the notices will be stored (e.g. `./data/notices`). 
