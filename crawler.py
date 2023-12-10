from helper import *
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Web Crawler with URL and Domain filtering.')
parser.add_argument('--url', required=True, help='Starting URL for crawling')
parser.add_argument('--domain', required=True, help='Domain to filter crawling')
args = parser.parse_args()

max_depth = 30
data_path = Path(f'{os.getcwd()}\\research\data')
        
crawl_website(args.url, args.domain, data_path, max_depth) 
