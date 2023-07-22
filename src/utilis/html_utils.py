from bs4 import BeautifulSoup

def remove_html_tags(html):
#   Create a BeautifulSoup object from the HTML string
    soup = BeautifulSoup(html, 'html.parser')

#   Get the text without HTML tags and remove additional white spaces
    clean_text = soup.get_text().strip().replace('\n', ' ').replace('\r', '').replace('\t', '')

    return clean_text
