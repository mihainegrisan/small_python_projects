from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       passwd='****',
                       db='mysql',
                       charset='utf8')

cur = conn.cursor()
cur.execute("USE wikipedia")

def insert_page_if_not_exists(url):
    """ Insert page into db
        Return id of the url """
    cur.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO pages (url) VALUES (%s)", (url))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]

def insert_link(from_page_id, to_page_id):
    cur.execute("SELECT * FROM links WHERE from_page_id = %s AND to_page_id = %s", (int(from_page_id), int(to_page_id)))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (from_page_id, to_page_id) VALUES (%s, %s)", (int(from_page_id), int(to_page_id)))
        conn.commit()

pages = set()
def get_links(page_url, recursion_level):
    global pages
    if recursion_level > 3:
        return;
    page_id = insert_page_if_not_exists(page_url) # returneaza id-ul link-ului din 'pages' .. link-ul cu care lucram acum
    html = urlopen("http://en.wikipedia.org" + page_url)
    bs_obj = BeautifulSoup(html, 'lxml')
    for link in bs_obj.find_all('a', href = re.compile("^(/wiki/)((?!:).)*$")):
        insert_link(page_id, insert_page_if_not_exists(link.attrs['href']))
        #page_id = from_page_id   has links to   to_page_id ( the new found link)
        if link.attrs['href'] not in pages:
            #Encountered a new page, add it and search it for links
            new_page = link.attrs['href']
            pages.add(new_page)
            get_links(new_page, recursion_level + 1)


get_links("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()
