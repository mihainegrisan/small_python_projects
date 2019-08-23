#! python3
# downloadXkcd.py - Downloads every single XKCD comic.

import requests, os, bs4

url = 'http://xkcd.com'  # starting url
os.chdir('D:/Python_code/Automate_stuff/Part2')
# the exist_ok=True keyword argument prevents the function from throwing an exception if this folder already exists.
os.makedirs('xkcd', exist_ok=True)   # store comics in ./xkcd

while not url.endswith('#'):
    # Download the page.
    try:
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="lxml")
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    # Find the URL of the comic image.
    # <img> element for the comic image is inside a <div> element with the id attribute set to 'comic', so the selector '#comic img' will get you the correct <img> element from the BeautifulSoup object.
    # <div id='comic'> .. <img> .... </img> .. </div>
    comic_elem = soup.select('#comic img')
    if comic_elem == []:
        print('Could not find comic image.')
    else:
        try:
            comic_url = 'http:' + comic_elem[0].get('src') # the first image
            # Download the image.
            print('Downloading image %s...' % (comic_url))
            res = requests.get(comic_url)
            res.raise_for_status()
        except requests.exceptions.MissingSchema:
            # skip this comic
            prev_link = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prev_link.get('href')
            continue

        # Save the image to ./xkcd.
        with open(os.path.join('xkcd', os.path.basename(comic_url)), 'wb') as image_file:
            for chunk in res.iter_content(100000):
                image_file.write(chunk)

    # Get the Prev button's url.
    prev_link = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prev_link.get('href')

print('Done.')
