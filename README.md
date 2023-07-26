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
usage: main.py [-h] -d DOMAIN (-o | -c)

SEO Spy is a Python-based web scraping tool that functions as an SEO error
checking tool, leveraging the capabilities of the renowned web scraper
Scrapy.

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        URL of the tested domain. Examples:
                        http://127.0.0.1:8000 https://docs.dasharo.com
  -o, --orphan          Run orphan pages check
  -c, --canonical       Run canonical links check
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

### Canonical links

Canonical links, also known as canonical tags or rel="canonical" links,
are HTML elements used to address duplicate content issues on the internet.
When multiple versions of the same content exist on different URLs, website
owners and developers can add a canonical link tag to the HTML header of the
duplicate pages. This tag specifies the URL of the preferred version
(the canonical page) that should be considered as the main or authoritative
source. Search engines then understand that the canonical URL is the primary
one to index and display in search results, consolidating the ranking signals
for all duplicate versions onto the preferred URL. By using canonical links,
website owners can improve search engine optimization (SEO) efforts and ensure
that search engines attribute the content's relevance and authority to a single,
preferred page, avoiding dilution of search rankings and confusion
in search results.

SEO Spy identifies sites that have no canonical links.

#### Example output

```bash
2023-07-26 19:13:26 [canonical_link_spider] ERROR: Pages with no canonical link found:
2023-07-26 19:13:26 [canonical_link_spider] ERROR: https://3mdeb.com/tags/
2023-07-26 19:13:26 [canonical_link_spider] ERROR: https://3mdeb.com/categories/
2023-07-26 19:13:26 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'custom/canonical': ['https://3mdeb.com/tags/',
                      'https://3mdeb.com/categories/'],
 'downloader/request_bytes': 7340,
 'downloader/request_count': 28,
...
================================================
Pages with no canonical link found:
================================================
https://3mdeb.com/tags/
https://3mdeb.com/categories/
```
