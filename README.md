# DORK OSINT Missing Person Finder

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)

A DORK OSINT (Open Source Intelligence) tool designed to search for missing persons using Google dorks and various search techniques. This tool automates the search process across multiple engines and databases to help locate individuals based on their name.

## Features

- **Multiple Search Engines**: Google, Bing, DuckDuckGo, and Yandex
- **Google Dork Generation**: Creates effective search queries based on the person's name
- **People Database Search**: Checks popular people-search websites
- **Advanced Mode**: More specialized dorks for deeper searches
- **Interactive Results**: Browse and open search results directly from the tool
- **Concurrent Searches**: Uses threading for faster results
- **Color-Coded Output**: Easy-to-read terminal output

## Installation

Clone the repository:
```bash
git clone https://github.com/gl0bal01/osint-missing-person-finder.git
cd osint-missing-person-finder
```

Install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Basic search:
```bash
python osint_finder.py -f John -l Doe
```

Advanced search with more specialized dorks:
```bash
python osint_finder.py -f John -l Doe -a
```

Using a different search engine:
```bash
python osint_finder.py -f John -l Doe -e Bing
```

Full options:
```bash
python osint_finder.py -h

usage: osint_finder.py [-h] -f FIRSTNAME -l LASTNAME [-e {Google,Bing,DuckDuckGo,Yandex}] [-a]

OSINT Missing Person Finder

optional arguments:
  -h, --help            show this help message and exit
  -f FIRSTNAME, --firstname FIRSTNAME
                        First name of the person
  -l LASTNAME, --lastname LASTNAME
                        Last name of the person
  -e {Google,Bing,DuckDuckGo,Yandex}, --engine {Google,Bing,DuckDuckGo,Yandex}
                        Search engine to use (default: Google)
  -a, --advanced        Use advanced dorks for more comprehensive but slower search
```

## Types of Dorks Used

### Basic Dorks
- Name searches
- Social media profiles
- Contact information
- Location information
- Public records
- Digital footprint

### Advanced Dorks
- Phone and contact information in spreadsheets
- Medical and welfare records
- Financial traces
- Prison and legal records
- Education and employment history
- Historical and archive searches
- Online forums and community profiles
- Travel and location data
- Specialized format searches (contact cards, IP addresses, etc.)

## Legal Disclaimer

This tool is meant for legitimate purposes such as finding missing persons, conducting background checks with consent, or researching your own digital footprint. The author is not responsible for any misuse of this tool. Always respect privacy laws and terms of service for all websites and services.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
