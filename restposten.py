import requests
from bs4 import BeautifulSoup
import csv
import re
import random

def generate_short_description():
    conditions = ["Neu", "B-Ware", "C-Ware"]
    condition = random.choice(conditions)
    
    min_abnahme = random.randint(100, 500)  # range for "Mindestabnahme"
    verfuegbare_menge = random.randint(500, 20000)  # range for "Verfügbare Menge"
    
    short_description = f"""
    <div style="font-family: 'Maven Pro', sans-serif; margin: 0; padding: 0;">
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
            <h2 style="font-size: 18px; font-weight: 700; margin-bottom: 10px; color: #333;">Produktdetails</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Mindestabnahme:</span> {min_abnahme} Stück</p>
                <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Verfügbare Menge:</span> {verfuegbare_menge} Stück</p>
                <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Zustand:</span> {condition}</p>
                <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Lieferdauer:</span> 3-5 Werktage</p>
            </div>
        </div>
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 8px; margin-bottom: 10px; background-color: #f9f9f9;">
            <h2 style="font-size: 18px; font-weight: 700; margin-bottom: 10px; color: #333;">Kontaktdaten des Verkäufers</h2>
            <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Anbieter:</span> KFZ-Beizel GmbH</p>
            <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Adresse:</span> Lerchenstraße 39, 49152 Bad Essen</p>
            <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Email:</span> beispiel@firma.de</p>
            <p style="font-size: 14px; margin: 4px 0;"><span style="font-weight: 500; color: #555;">Telefon:</span> 01234 / 567890</p>
        </div>
    </div>
    """
    return short_description

def scrape_product_page(link):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(link, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Successfully fetched product page: {link}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product title
        product_title = soup.find("span", class_="breadcrumb-item separators active").text.strip()
        price = soup.find("span", class_="bigPrice").text.strip()
        price = int(re.search(r'\d+', price.replace('.', '').replace(',', '.')).group(0))
        description = soup.find("div", class_="col-md-12 col-lg-10").text.strip()
        image_tags = soup.find_all("li", class_="link-cursor thumbs col-3 hidden-md-down float-left m-0")
        
        image_links = []
        for picture in image_6666tags:
            img_tag = picture.find("img")
            if img_tag and 'src' in img_tag.attrs:
                full_src = img_tag['src']
                # Strip everything after '.jpeg', '.jpg', or '.png'
                cleaned_src = re.sub(r'(\.jpeg|\.jpg|\.png).*', r'\1', full_src)
                image_links.append(cleaned_src)
        
        short_description = generate_short_description()
        
        product_data = {
            "ID": "",
            "Type": "simple",
            "SKU": "",
            "Name": product_title,
            "Published": 1,
            "Is featured?": 0,
            "Visibility in catalog": "visible",
            "Short description": short_description,
            "Description": description,
            "Date sale price starts": "",
            "Date sale price ends": "",
            "Tax status": "taxable",
            "Tax class": "",
            "In stock?": 1,
            "Stock": "",
            "Low stock amount": "",
            "Backorders allowed?": 0,
            "Sold individually?": 0,
            "Weight (kg)": "",
            "Length (cm)": "",
            "Width (cm)": "",
            "Height (cm)": "",
            "Allow customer reviews?": 1,
            "Purchase note": "",
            "Sale price": "",
            "Regular price": price,
            "Categories": "",
            "Tags": "",
            "Shipping class": "",
            "Images": ",".join(image_links),
            "Download limit": "",
            "Download expiry days": "",
            "Parent": "",
            "Grouped products": "",
            "Upsells": "",
            "Cross-sells": "",
            "External URL": "",
            "Button text": "",
            "Position": 0,
            "Meta: _custom_field": "",
        }
        
        return product_data
    
    except Exception as e:
        print(f"Error scraping product page {link}: {e}")
        return None

def save_to_csv(products_data, filename):
    if not products_data:
        print("No data to save.")
        return
    
    fieldnames = list(products_data[0].keys())
    
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product_data in products_data:
                writer.writerow(product_data)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

try:
    for i in range(1, 20):
        url = f"https://www.restposten.de/maincategory.php?cid=20109&page={i}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"Successfully fetched page {i}")
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            product_links = soup.find_all("a", class_="p-0")
            links = [link['href'] for link in product_links if link and 'href' in link.attrs]     
            all_products_data = []  # Initialize a list to collect all product data for the current page
            
            for link in links:
                full_link = f"https://www.restposten.de/{link}"
                product_data = scrape_product_page(full_link)
                if product_data:
                    all_products_data.append(product_data)
            
            # Save all products from the current page to the CSV
            csv_filename = f'turntables{i}.csv'
            save_to_csv(all_products_data, filename=csv_filename)
            
        except Exception as e:
            print(f"Error fetching or processing page {i}: {e}")
except Exception as e:
    print(f"General error: {e}")
