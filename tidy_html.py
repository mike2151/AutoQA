# File used to clean up HTML files. 
# It uses the BeautifulSoup library to prettify the HTML files.
import argparse
import os
import glob
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Tidy up HTML files.')
parser.add_argument('path', help='the path to the folder containing HTML files')
args = parser.parse_args()

for filename in glob.glob(os.path.join(args.path, '**', '*.html'), recursive=True):
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    with open(filename, 'w') as f:
        f.write(soup.prettify())