#!/usr/bin/env python3
"""
OSINT Missing Person Finder
A simple and basic script to search for missing persons using Google dorks.
- gl0bal01
"""

import requests
import webbrowser
import time
import os
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import urllib.parse
import argparse
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

class OSINTFinder:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.results = []
        self.search_engines = {
            'Google': 'https://www.google.com/search?q=',
            'Bing': 'https://www.bing.com/search?q=',
            'DuckDuckGo': 'https://duckduckgo.com/?q=',
            'Yandex': 'https://yandex.com/search/?text='
        }

    def generate_dorks(self, firstname, lastname, advanced=False):
        """Generate various Google dorks for finding a person.
        
        Args:
            firstname: First name of the person
            lastname: Last name of the person
            advanced: If True, include more specialized and invasive dorks
        """
        dorks = []
        
        # Basic name searches
        dorks.append(f'"{firstname} {lastname}"')
        dorks.append(f'"{lastname}, {firstname}"')
        dorks.append(f'"{firstname} * {lastname}"')
      
        # Social media
        dorks.append(f'"{firstname} {lastname}" site:facebook.com OR site:linkedin.com OR site:instagram.com OR site:twitter.com')
        dorks.append(f'"{firstname} {lastname}" inurl:profile OR inurl:about OR inurl:bio')
        
        # Contact information
        dorks.append(f'"{firstname} {lastname}" intext:address OR intext:phone OR intext:email OR intext:contact')
        
        # Location information
        dorks.append(f'"{firstname} {lastname}" intext:city OR intext:state OR intext:country OR intext:moved')
        
        # Public records
        dorks.append(f'"{firstname} {lastname}" intext:court OR intext:property OR intext:marriage OR filetype:pdf')
        
        # Digital footprint
        dorks.append(f'"{firstname} {lastname}" site:github.com OR site:medium.com OR site:wordpress.com OR inurl:author')
        
        # Advanced dorks (only included if advanced=True)
        if advanced:
            # Phone and Contact Information Dorks
            dorks.append(f'"{firstname} {lastname}" intext:phone filetype:xlsx OR filetype:csv')
            dorks.append(f'"{firstname} {lastname}" intext:"contact information" OR intext:"emergency contact"')
            dorks.append(f'"{firstname} {lastname}" intext:resume phone')
            dorks.append(f'site:truecaller.com OR site:whitepages.com OR site:spokeo.com "{firstname} {lastname}"')
            
            # Medical and Welfare Dorks
            dorks.append(f'"{firstname} {lastname}" intext:patient OR intext:medical OR intext:hospital -doctor')
            dorks.append(f'"{firstname} {lastname}" intext:insurance OR intext:policy')
            dorks.append(f'"{firstname} {lastname}" intext:welfare OR intext:benefits OR intext:assistance')
            
            # Financial Trace Dorks
            dorks.append(f'"{firstname} {lastname}" intext:bank OR intext:account OR intext:transaction')
            dorks.append(f'"{firstname} {lastname}" intext:paypal OR intext:venmo OR intext:cashapp')
            dorks.append(f'"{firstname} {lastname}" intext:loan OR intext:mortgage OR intext:credit')
            
            # Prison, Legal and Police Dorks
            dorks.append(f'"{firstname} {lastname}" site:vinelink.com')
            dorks.append(f'"{firstname} {lastname}" intext:inmate OR intext:prisoner OR intext:corrections')
            dorks.append(f'"{firstname} {lastname}" site:mugshots.com OR site:arrests.org')
            
            # Education and Employment Dorks
            dorks.append(f'"{firstname} {lastname}" site:.edu intext:student OR intext:alumni')
            dorks.append(f'"{firstname} {lastname}" filetype:pdf intext:transcript OR intext:diploma')
            dorks.append(f'"{firstname} {lastname}" site:linkedin.com AND (inurl:in/ OR inurl:pub/)')
            
            # Historical and Archive Dorks
            dorks.append(f'"{firstname} {lastname}" site:archive.org')
            dorks.append(f'"{firstname} {lastname}" site:newspapers.com OR site:legacy.com')
            dorks.append(f'"{firstname} {lastname}" filetype:pdf intext:yearbook')
            
            # Online Forums and Communities
            dorks.append(f'"{firstname} {lastname}" site:reddit.com OR site:quora.com')
            dorks.append(f'"{firstname} {lastname}" intext:username OR intext:profile site:forum.*')
            
            # Travel and Location Dorks
            dorks.append(f'"{firstname} {lastname}" intext:flight OR intext:booking OR intext:reservation')
            dorks.append(f'"{firstname} {lastname}" intext:passport OR intext:visa OR intext:travel')
            
            # Less Common But Effective Dorks
            dorks.append(f'"{firstname} {lastname}" ext:vcf OR ext:vcard')
            dorks.append(f'"{firstname} {lastname}" intext:"IP address" OR intext:WHOIS')
            dorks.append(f'"{firstname} {lastname}" site:findagrave.com OR site:cemetery')
        
        return dorks

    def search_dork(self, search_engine, dork, firstname, lastname):
        """Search a specific dork using the selected search engine."""
        query = urllib.parse.quote(dork)
        url = f"{self.search_engines[search_engine]}{query}"
        
        print(f"{Fore.BLUE}[*] Searching {search_engine}: {Fore.YELLOW}{dork}{Style.RESET_ALL}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                self.results.append({
                    'engine': search_engine,
                    'dork': dork,
                    'url': url
                })
                return True
            else:
                print(f"{Fore.RED}[!] Error: Status code {response.status_code} for {url}{Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"{Fore.RED}[!] Error searching {search_engine} with dork '{dork}': {str(e)}{Style.RESET_ALL}")
            return False

    def search_people_databases(self, firstname, lastname):
        """Search popular people search databases."""
        people_dbs = [
            {'name': 'Spokeo', 'url': f'https://www.spokeo.com/{firstname}-{lastname}'},
            {'name': 'Whitepages', 'url': f'https://www.whitepages.com/name/{firstname}-{lastname}'},
            {'name': 'TruePeopleSearch', 'url': f'https://www.truepeoplesearch.com/results?name={firstname}%20{lastname}'},
            {'name': 'FastPeopleSearch', 'url': f'https://www.fastpeoplesearch.com/name/{firstname}-{lastname}'},
            {'name': 'BeenVerified', 'url': f'https://www.beenverified.com/people/{firstname}-{lastname}/'}
        ]
        
        print(f"\n{Fore.GREEN}[+] Searching people databases...{Style.RESET_ALL}")
        for db in people_dbs:
            try:
                print(f"{Fore.BLUE}[*] Checking {db['name']}: {db['url']}{Style.RESET_ALL}")
                self.results.append({
                    'engine': 'PeopleDB',
                    'dork': db['name'],
                    'url': db['url']
                })
                # Don't actually request these to avoid rate limiting
            except Exception as e:
                print(f"{Fore.RED}[!] Error with {db['name']}: {str(e)}{Style.RESET_ALL}")

    def run_search(self, firstname, lastname, search_engine='Google', advanced=False):
        """Run the complete search process."""
        if not firstname or not lastname:
            print(f"{Fore.RED}[!] Both firstname and lastname are required{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}[+] Starting OSINT search for {firstname} {lastname}{Style.RESET_ALL}")
        if advanced:
            print(f"{Fore.YELLOW}[!] Advanced mode enabled - using specialized dorks{Style.RESET_ALL}")
        
        # Generate dorks
        dorks = self.generate_dorks(firstname, lastname, advanced)
        
        # Search each dork
        print(f"{Fore.BLUE}[*] Generated {len(dorks)} search queries{Style.RESET_ALL}")
        with ThreadPoolExecutor(max_workers=5) as executor:
            for dork in dorks:
                executor.submit(self.search_dork, search_engine, dork, firstname, lastname)
                time.sleep(2)  # Delay to avoid being blocked
        
        # Search people databases
        self.search_people_databases(firstname, lastname)
        
        # Display results
        self.display_results()

    def display_results(self):
        """Display all search results."""
        if not self.results:
            print(f"\n{Fore.RED}[!] No results found{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}[+] Search Results ({len(self.results)} sources found):{Style.RESET_ALL}")
        
        current_category = ""
        for i, result in enumerate(self.results, 1):
            if result['engine'] != current_category:
                current_category = result['engine']
                print(f"\n{Fore.CYAN}== {current_category} =={Style.RESET_ALL}")
            
            print(f"{Fore.WHITE}{i}. {Fore.YELLOW}[{result['dork']}] {Fore.BLUE}{result['url']}{Style.RESET_ALL}")
    
    def open_results(self):
        """Open search results in browser if requested."""
        if not self.results:
            return
        
        choice = input(f"\n{Fore.GREEN}[?] Open results in browser? (y/n, or number to open specific result): {Style.RESET_ALL}")
        
        if choice.lower() == 'y':
            print(f"{Fore.YELLOW}[*] Opening all results in browser...{Style.RESET_ALL}")
            for result in self.results:
                webbrowser.open(result['url'])
                time.sleep(1)
        elif choice.isdigit() and 1 <= int(choice) <= len(self.results):
            idx = int(choice) - 1
            print(f"{Fore.YELLOW}[*] Opening result {choice} in browser...{Style.RESET_ALL}")
            webbrowser.open(self.results[idx]['url'])


def main():
    parser = argparse.ArgumentParser(description='OSINT Missing Person Finder')
    parser.add_argument('-f', '--firstname', required=True, help='First name of the person')
    parser.add_argument('-l', '--lastname', required=True, help='Last name of the person')
    parser.add_argument('-e', '--engine', default='Google', choices=['Google', 'Bing', 'DuckDuckGo', 'Yandex'], 
                        help='Search engine to use (default: Google)')
    parser.add_argument('-a', '--advanced', action='store_true', 
                        help='Use advanced dorks for more comprehensive but slower search')
    
    args = parser.parse_args()
    
    finder = OSINTFinder()
    finder.run_search(args.firstname, args.lastname, args.engine, args.advanced)
    finder.open_results()

if __name__ == "__main__":
    # Print banner
    print(f"""
{Fore.CYAN}=============================================
        OSINT MISSING PERSON FINDER
=============================================
{Fore.YELLOW}   A tool for finding missing persons
   through open-source intelligence (OSINT)
{Fore.CYAN}=============================================
{Style.RESET_ALL}""")
    
    main()
