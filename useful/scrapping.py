import requests
import json
from bs4 import BeautifulSoup

amazon_url = "https://www.amazon.in/s?k=" + query
amazon_soup = BeautifulSoup(amazon_r.text, "html.parser")
amazon_r = requests.get(amazon_url)

ajio_url = "https://www.ajio.com/search/?text=" + query
ajio_r = requests.get(ajio_url)
ajio_soup = BeautifulSoup(ajio_r.text, "html.parser")

myntra_url = "https://www.myntra.com/" + query
myntra_r = requests.get(myntra_url)
myntra_soup = BeautifulSoup(myntra_r.text, "html.parser")


# Amazon scraping
amazon_box = amazon_soup.find('div', class_='sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16')
if amazon_box:

    for item in amazon_box:
        image = item.find_all('img', class_='s-image')
        print(image)
        name = item.find_all('span', class_='a-size-medium a-color-base a-text-normal')
        # description = item.find_all('span', class_='a-size-medium a-color-base a-text-normal')
        brand = item.find_all('span', class_='a-size-medium a-color-base a-text-normal')
        price = item.find_all('span', class_='a-price-whole')
        if image and name and price and brand:
            product = {
                'image_link': image['src'] if image else '',
                'product_name': name.text if name else '',
                'price': price.text.replace('.00', '') if price else '',
                # 'product_description': description.text if name else '',
                'product_brand': brand.text if name else '',
                'source': 'Amazon'
            }
            print(amazon_r.text)
            results.append(product)

# Myntra scraping
myntra_box = myntra_soup.find("ul", class_="results-base")
if myntra_box:
    myntra_items = myntra_box.find_all("li", class_="product-base")
    for item in myntra_items:
        image = item.find("img", class_="product-sliderContainer")
        name = item.find("div", class_="product-brand")
        description = item.find("div", class_="product-product")
        price = item.find("span", class_="product-discountedPrice")
        if image and name and price:
            product = {
                'image_link': image['src'] if image else '',
                'product_name': name.text.strip() if name else '',
                'price': price.text.strip() if price else '',
                'product_description': description.text() if description else '',
                'product_brand': name.text.strip() if name else '',
                'source': 'Myntra'
            }
            results.append(product)
            
# Ajio scraping
ajio_box = ajio_soup.find("div", class_="row search-base")
if ajio_box:
    ajio_items = ajio_box.find_all("div", class_="contentHolder")
    for item in ajio_items:
        image = item.find("img", class_="lazy")
        
        name = item.find("div", class_="brand")
        price = item.find("span", class_="final-price")
        if image and name and price:
            product = {
                'image_link': image['src'] if image else '',
                'product_name': name.text.strip() if name else '',
                'price': price.text.strip() if price else '',
                # 'product_description': '',  # Add description logic if available
                'product_brand': name.text.strip() if name else '',
                'source': 'Ajio'
            }
            results.append(product)


with open('data.json', 'w') as file:
    json.dump(results, file, indent=4)