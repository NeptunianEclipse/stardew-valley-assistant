import requests
import bs4
import json
import urllib.parse

def save_all_villager_data(filename):
    data = get_all_villager_data('https://stardewvalleywiki.com/Villagers')
    with open(filename, 'w') as file:
        string = 'let villager_data = ' + json.dumps(data, indent=4)
        file.write(string)


def get_all_villager_data(villagers_url):
    response = requests.get(villagers_url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    parsed_url = urllib.parse.urlparse(villagers_url)
    base_url = parsed_url.scheme + '://' + parsed_url.netloc

    data = []

    lists = soup.find('span', {'id': 'Marriage_Candidates'}).find_all_next('ul', {'class': 'villagergallery'}, limit=5)
    for list in lists:

        elements = list.find_all('li')
        for element in elements:
            anchor = element.find('div', {'class': 'gallerytext'}).find('a')
            image = element.find('div', {'class': 'thumb'}).find('img')

            print('Parsing data for {}'.format(anchor.text))

            url = urllib.parse.urljoin(base_url, anchor['href'])
            image_url = urllib.parse.urljoin(base_url, image['src'])
            data.append({
                'name': anchor.text,
                'image': image_url,
                'url': url,
                'gifts': get_villager_data(url, base_url)
            })

    return { 'villagers': data }


def get_villager_data(url, base_url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    data = {}

    data['love'] = extract_table_data(soup, base_url, 'Love')
    data['like'] = extract_table_data(soup, base_url, 'Like')
    data['neutral'] = extract_table_data(soup, base_url, 'Neutral')
    data['dislike'] = extract_table_data(soup, base_url, 'Dislike')
    data['hate'] = extract_table_data(soup, base_url, 'Hate')

    return data


def extract_table_data(soup, base_url, table_span_id):
    broad_gifts = []
    specific_gifts = []

    span = soup.find('span', {'id': table_span_id})
    if span is None:
        span = soup.find('span', {'id': table_span_id + 's'})

    rows = span.parent.find_next('table', {'class': 'wikitable'}).find_all('tr')

    category_items = rows[1].find('ul').find_all('li', recursive=False)
    for item in category_items:
        anchors = item.find_all('a')
        for anchor in anchors:
            if anchor['href'][0] == '/':
                anchor['href'] = urllib.parse.urljoin(base_url, anchor['href'])
            
            img_url = get_item_img_url(base_url, anchor['href'])
            if img_url is not None:
                a_tag = soup.new_tag('a', title=anchor.text, href=anchor['href'])
                a_tag['class'] = 'gift-img fancy-tooltip'
                a_tag.insert(0, soup.new_tag('img', src=img_url))

                anchor.insert_after(a_tag)
                anchor.extract()

        broad_gifts.append(item.decode_contents(formatter="html"))

    for row in rows[2:]:
        cells = row.find_all('td')

        image_url = urllib.parse.urljoin(base_url, cells[0].find('img')['src'])
        name = cells[1].find('a').text
        item_url = urllib.parse.urljoin(base_url, cells[1].find('a')['href'])

        specific_gifts.append({'image': image_url, 'name': name, 'url': item_url})

    return { 'broad': broad_gifts, 'specific': specific_gifts }


def get_item_img_url(base_url, item_url):
    response = requests.get(item_url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    
    info_box = soup.find('table', {'id': 'infoboxtable'})
    if info_box is not None:
        url = info_box.find('img')['src']

        if url[0] == '/':
            url = urllib.parse.urljoin(base_url, url)

        return url
    
    return None


save_all_villager_data('js/villager_data.js')
