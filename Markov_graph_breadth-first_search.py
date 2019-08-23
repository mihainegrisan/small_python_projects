import requests
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host = '127.0.0.1',
                       user = 'root',
                       passwd = 'm1i3h5a7i9MIHAI!',
                       db = 'mysql',
                       charset = 'utf8')
cur = conn.cursor()
cur.execute('USE wikipedia')


class SolutionFound(RuntimeError):
    """write trail message when solution found."""
    def __init__(self, message):
        self.message = message


def get_links(from_page_id):
    cur.execute('SELECT to_page_id FROM links WHERE from_page_id = %s', (from_page_id))
    if cur.rowcount == 0:
        return None
    else:
        return [x[0] for x in cur.fetchall()]

def construct_dict(current_page_id):
    links = get_links(current_page_id)
    if links:
        # convert two lists into a dictionary
        return dict(zip(links, [{}]*len(links)))
    return {}

#The link tree may either be empty or contain multiple links
def search_depth(target_page_id, current_page_id, link_tree, depth):
    if depth == 0:
        #Stop recursing and return, regardless
        return link_tree
    if not link_tree:
        link_tree = construct_dict(current_page_id)
        if not link_tree:
            #No links found. Cannot continue at this node
            return {}
    if target_page_id in link_tree.keys():
        print('TARGET ' + str(target_page_id) + ' FOUND!')
        raise SolutionFound('PAGE: ' + str(current_page_id))

    for branch_key, branch_value in link_tree.items():
        try:
            #Recurse here to continue building the tree
            link_tree[branch_key] = search_depth(target_page_id, branch_key, branch_value, depth - 1)
        except SolutionFound as e:
            print(e.message)
            raise SolutionFound('PAGE: ' + str(current_page_id))
    return link_tree

try:
    search_depth(2551, 1, {}, 4)
    print("No solution found")
except SolutionFound as e:
    print(e.message)
