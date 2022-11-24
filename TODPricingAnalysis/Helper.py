import requests
from bs4 import BeautifulSoup
import re
def WriteToFile():
    url = 'https://web.archive.org/web/20221030064624/https://www.skysports.com/world-cup-fixtures'
    page = requests.get(url).text
    file1 = open('WebPage1.txt', 'w')
    file1.writelines(page)
    return ''

WriteToFile()