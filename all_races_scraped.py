import requests, os, bs4, re, openpyxl

def get_page_and_soup(url): 
    try:
        print('Downloading page %s...' % url)
        res = requests.get(url)  # downloads it
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="lxml")
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    return soup

def get_p_and_a_elem(soup):
    span = soup.find('span', { 'class': 'cb-itemprop' })
    p_elements = [tag.text for tag in span.find_all('p')]
    p_elements = p_elements[1:] # drop the first one
    a_elements = [tag['href'] for tag in span.select('p a[href]')]
    return p_elements, a_elements

url = 'http://4run.ro/calendar-curse-alergare/'  # starting url
os.chdir('D:/Python_code/Web_Scraping/projects')
os.makedirs('races', exist_ok=True)
os.chdir('D:/Python_code/Web_Scraping/projects/races')

soup = get_page_and_soup(url)
p_elements, a_elements = get_p_and_a_elem(soup)

for i in range(len(p_elements)):
    if len(p_elements[i].split(',')) == 4:
        content = ' -'.join(p_elements[i].split(',')) + ' - ' + a_elements[i]
        content = bytes(content, 'UTF-8')
        content = content.decode("ascii", "ignore")
        print(content)

fname = 'races.txt'
with open(fname, "w", encoding="utf-8") as f:
    for i in range(len(p_elements)):
        if len(p_elements[i].split(',')) == 4:
            f.write(' -'.join(p_elements[i].split(',')) + ' - ' + a_elements[i])
            f.write('\n')
            f.write('\n')

# create the excel
wb = openpyxl.Workbook()
sheet = wb.active
bold = openpyxl.styles.Font(bold=True)
sheet['A1'] = 'Race Name'
sheet['B1'] = 'Day'
sheet['C1'] = 'Month'
sheet['D1'] = 'Location'
sheet['E1'] = 'Race Link'
for col in ['A', 'B', 'C', 'D', 'E']:
    sheet[f'{col}1'].font = bold
    sheet[f'{col}1'].alignment = openpyxl.styles.Alignment(horizontal='center')

for i in range(2, len(p_elements) + 2):
    if len(p_elements[i-2].split(',')) == 4:
        link = a_elements[i-2]
        name, date, location, *junk = p_elements[i-2].split(',')
        if len(date.strip(' ').split(' ')) == 2:
            day, month = date.strip().split(' ')
            if len(day) > 2 or day == '1o': # if day looks like 4-5 or 14-16
                sheet.cell(row = i, column = 2).value = day
            else: # if day looks like 5 or 22
                sheet.cell(row = i, column = 2).value = int(day)
            sheet.cell(row = i, column = 3).value = month.title()
        else:
            sheet.cell(row = i, column = 2).value = date

        sheet.cell(row = i, column = 2).alignment = openpyxl.styles.Alignment(horizontal='center')
        sheet.cell(row = i, column = 3).alignment = openpyxl.styles.Alignment(horizontal='center')
        sheet.cell(row = i, column = 1).value = name
        sheet.cell(row = i, column = 4).value = location
        sheet.cell(row = i, column = 5).value = '=HYPERLINK("{}", "{}")'.format(link, "Link")

sheet.freeze_panes = 'A2' # freezes row 1
sheet.column_dimensions['A'].width = 55
sheet.column_dimensions['D'].width = 25
sheet.column_dimensions['E'].width = 35



wb.save('races.xlsx')
