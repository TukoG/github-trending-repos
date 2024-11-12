import requests
from bs4 import BeautifulSoup
import os

url = 'https://github.com/trending'

# Send GET request
response = requests.get(url)

# Create BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all 'h2' tags with class 'h3 lh-condensed'
h2_tags = soup.find_all('h2', class_='h3 lh-condensed')
dir = os.getcwd()

log = os.path.join(dir,'github_trending.txt')
print(f"\nOutput\t: {log}\n")

try:
    with open(log, 'w', encoding='utf-8') as f:
        for i, h2 in enumerate(h2_tags, start=1):
            link = h2.find('a')
            href = 'https://github.com' + link.get('href')
            f.write(f"{i}. {href}\n")
            
            # Send GET request to repository page
            repo_response = requests.get(href)
            repo_soup = BeautifulSoup(repo_response.content, 'html.parser')
            
            # Find the 'About' section
            about = repo_soup.find('div', class_='repository-content').find('p', class_='f4 my-3')
            if about:
                f.write(f"About: {about.text.strip()}\n")
                about_repo = about.text.strip()
            else:
                f.write("No 'About' section found.\n")
                about_repo = "None"
            
            f.write('\n')

            print(f'{href}')
            
            print(f"\tAbout: {about_repo}\n\n")
except KeyboardInterrupt:
    print("\n[+] Bye !")