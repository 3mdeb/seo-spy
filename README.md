# SEO Spy

SEO Spy is a Python-based web scraping tool that functions as an SEO error
checking tool, leveraging the capabilities of the renowned web scraper
[Scrapy](https://scrapy.org/).

## Installation

Create new python virtual environment.

``` bash
$ virtualenv venv
```

Activate virtual environment.

```bash
$ source venv/bin/activate
```

Install requirements.

```bash
pip install -r requirements.txt
```

## Usage

```bash
usage: main.py [-h] -d DOMAIN -o

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        URL of the tested domain. Examples:
                        http://127.0.0.1:8000 https://docs.dasharo.com
  -o, --orphan          Run orphan pages check
```

## Current features

### Orphaned Pages

Orphan pages are web pages within a website that lack incoming internal links
from other pages, rendering them isolated and not accessible through navigation
or internal linking structures. Due to the absence of internal links,
search engines may struggle to discover and index these pages, leading
to reduced visibility in search results.

SEO Spy identifies sites that are in the site map, but have no internal links
leading to them.

#### Example output

```bash
2023-07-25 23:56:57 [orphan_pages_spider] ERROR: Orphan pages found:
2023-07-25 23:56:57 [orphan_pages_spider] ERROR: http://127.0.0.1:8000/variants/protectli_ptx01/hardware-matrix/
2023-07-25 23:56:57 [orphan_pages_spider] ERROR: http://127.0.0.1:8000/variants/protectli_ptx01/test-matrix/
2023-07-25 23:56:57 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'custom/orphan_pages': ['http://127.0.0.1:8000/variants/protectli_ptx01/hardware-matrix/',
                         'http://127.0.0.1:8000/variants/protectli_ptx01/test-matrix/'],
...
2023-07-25 23:56:57 [scrapy.core.engine] INFO: Spider closed (finished)
================================================
Orphan pages found:
================================================
http://127.0.0.1:8000/variants/protectli_ptx01/hardware-matrix/
http://127.0.0.1:8000/variants/protectli_ptx01/test-matrix/
```

