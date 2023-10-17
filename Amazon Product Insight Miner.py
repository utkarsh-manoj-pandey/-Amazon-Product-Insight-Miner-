import requests
from bs4 import BeautifulSoup
import csv
from prettytable import PrettyTable
import time

# Function to scrape product information with a delay
def scrape_amazon_products_to_pretty_table(url, num_pages=20, delay=2):
    product_data = []

    for page in range(1, num_pages + 1):
        page_url = f"{url}&page={page}"
        try:
            response = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()  # Raise an exception for non-200 status codes

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', {'data-component-type': 's-search-result'})

            for product in products:
                product_url = f"https://www.amazon.in{product.find('a', {'class': 'a-link-normal'})['href']}"
                product_name = product.find('span', {'class': 'a-text-normal'}).get_text()
                product_price = product.find('span', {'class': 'a-offscreen'}).get_text()
                rating = product.find('span', {'class': 'a-icon-alt'})
                num_reviews = product.find('span', {'class': 'a-size-base', 'aria-label': ' customer reviews'})

                if rating:
                    rating = rating.get_text().split(' ')[0]
                else:
                    rating = 'N/A'

                if num_reviews:
                    num_reviews = num_reviews.get_text().split(' ')[0]
                else:
                    num_reviews = 'N/A'

                product_data.append([product_url, product_name, product_price, rating, num_reviews])

            # Introduce a delay to avoid overloading the server
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"Scrapped your data for page {page}")
            continue

    # Create a PrettyTable and add data
    table = PrettyTable()
    table.field_names = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']

    for product in product_data:
        table.add_row(product)

    return table.get_string()  # Return the table as plain text

amazon_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
product_table = scrape_amazon_products_to_pretty_table(amazon_url, num_pages=20, delay=2)
print(product_table)


# Function to scrape product details from a product URL
def scrape_product_details(product_url):
    try:
        response = requests.get(product_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize the details to None
        description = None
        asin = None
        product_description = None
        manufacturer = None

        # Check if the elements exist before accessing their content
        description_meta = soup.find('meta', {'name': 'description'})
        if description_meta:
            description = description_meta['content']

        asin_th = soup.find('th', text='ASIN')
        if asin_th:
            asin_td = asin_th.find_next('td')
            if asin_td:
                asin = asin_td.get_text()

        product_description_th = soup.find('th', text='Product Description')
        if product_description_th:
            product_description_td = product_description_th.find_next('td')
            if product_description_td:
                product_description = product_description_td.get_text()

        manufacturer_th = soup.find('th', text='Manufacturer')
        if manufacturer_th:
            manufacturer_td = manufacturer_th.find_next('td')
            if manufacturer_td:
                manufacturer = manufacturer_td.get_text()

        return {
            'Description': description,
            'ASIN': asin,
            'Product Description': product_description,
            'Manufacturer': manufacturer
        }
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve details for {product_url}. Error: {e}")
        return None

# List of product URLs (200+ URL's)
product_urls = [
    "https://www.amazon.in/gp/bestsellers/hpc/11364892031/ref=sr_bs_0_11364892031_1",
    "https://www.amazon.in/Killer-Backpack-Compartments-Polyester-Waterproof/dp/B07C9XHZT1/ref=sr_1_146?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-146",
    "https://www.amazon.in/Shalimar-Premium-Garbage-Large-Rolls/dp/B07KT98RKS/ref=sr_1_147?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-147",
    "https://www.amazon.in/G-1-Medium-Disposable-Garbage-Dustbin/dp/B077RJ1YMW/ref=sr_1_148?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-148",
    "https://www.amazon.in/GOCART-LOGO-Backpack-Briefcase-Convertible/dp/B0822H451W/ref=sr_1_149?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-149",
    "https://www.amazon.in/Half-Moon-Resistant-Backpack-Compartment/dp/B0BYW5SH4L/ref=sr_1_150?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-150",
    "https://www.amazon.in/Tabelito%C2%AE-Basic-Laptop-Sleeve-Surfacepro/dp/B09NDTW8SP/ref=sr_1_151?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-151",
    "https://www.amazon.in/SFANE-Polyester-Shoulder-Separate-Compartment/dp/B08KG7J7L5/ref=sr_1_152?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-152",
    "https://www.amazon.in/Half-Moon-Rucksack-Bags-Compartment/dp/B09S14TTG6/ref=sr_1_153?crid=2M096C61O4MLT&keywords=bags&qid=1697466517&sprefix=ba%2Caps%2C283&sr=8-153",
    "https://www.amazon.in/UPPERCASE-Professional-Backpack-resistant-sustainable/dp/B0BXFDK5J2/ref=sr_1_1_sspa?crid=2M096C61O4MLT&keywords=bags&qid=1697477215&sprefix=ba%2Caps%2C283&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
    "https://www.amazon.in/Lavie-Sport-Duffle-Luggage-Trolley/dp/B097RJ22Q3/ref=sr_1_233?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-233",
    "https://www.amazon.in/Heart-Home-Garbage-Dustbin-HS41HEARTHH24001/dp/B09DSKVLBG/ref=sr_1_234?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-234",
    "https://www.amazon.in/Murano-Casual-daybackpack-Office-College/dp/B0BX9GLFD6/ref=sr_1_235?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-235",
    "https://www.amazon.in/DZert-Polyester-Black-White-Backpack/dp/B07GXX2BP3/ref=sr_1_236?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-236",
    "https://www.amazon.in/Lavie-Malgana-Womens-Tote-Bag/dp/B07PJBJPV9/ref=sr_1_237?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-237",
    "https://www.amazon.in/DAHSHA-Sling-Messenger-Bag-Grey/dp/B09CGDFNBV/ref=sr_1_238?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-238",
    "https://www.amazon.in/House-Quirk-Maternity-Backpack-Elephant/dp/B07QV7SH4S/ref=sr_1_239?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-239",
    "https://www.amazon.in/Lavie-Spring-Summer-Womens-Tote/dp/B081KGGL8V/ref=sr_1_240?crid=2M096C61O4MLT&keywords=bags&qid=1697469926&sprefix=ba%2Caps%2C283&sr=8-240"
    "https://www.amazon.in/ROZEN-Fabric-Travel-Luggage-Duffle/dp/B085QMBX8H/ref=sr_1_81?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-81",
    "https://www.amazon.in/Newtone-Premium-OXO-Biodegradable-Garbage/dp/B08M5S2NQM/ref=sr_1_82?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-82",
    "https://www.amazon.in/Bennett-Polyester-Drax-Ultrabook-Surfacepro/dp/B091NZ9MYB/ref=sr_1_83?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-83",
    "https://www.amazon.in/Killer-Backpack-Compartments-Polyester-Waterproof/dp/B07CDD6YS2/ref=sr_1_84?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-84",
    "https://www.amazon.in/NORTH-ZONE-Lightweight-Backpacks-Stylish/dp/B0BL3S5NC1/ref=sr_1_85?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-85",
    "https://www.amazon.in/Wildcraft-ltrs-Cms-backpack-204493566_black/dp/B07GNGG435/ref=sr_1_86?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-86",
    "https://www.amazon.in/ADISA-BP005-Weight-Casual-Backpack/dp/B07F3X45WZ/ref=sr_1_87?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-87",
    "https://www.amazon.in/Safari-Spartan-Water-Resistant-Backpack/dp/B09B277CR5/ref=sr_1_88?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-88",
    "https://www.amazon.in/FATMUG-Foldable-Luggage-Packing-Storage/dp/B07YFNXC3H/ref=sr_1_89?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-89",
    "https://www.amazon.in/Step-Backpack-Small-Water-Repellant/dp/B088X9M73T/ref=sr_1_90?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-90",
    "https://www.amazon.in/Puma-Carry-Unisex-Duffel-Bag/dp/B089T8PKSQ/ref=sr_1_91?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-91",
    "https://www.amazon.in/gp/bestsellers/luggage/2917440031/ref=sr_bs_11_2917440031_1",
    "https://www.amazon.in/Motherly-Diaper-Bags-Travel-Basic/dp/B07PKQ3WJZ/ref=sr_1_93?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-93",
    "https://www.amazon.in/HAMMONDS-FLYCATCHER-Laptop-Bag-Men/dp/B083M1QK32/ref=sr_1_94?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-94",
    "https://www.amazon.in/AUXTER-BLACKY-Duffel-Emboss-Black/dp/B07F2H25NP/ref=sr_1_95?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-95",
    "https://www.amazon.in/Shalimar-Reusable-Vegetable-Multi-Purpose-Storage/dp/B096P271BL/ref=sr_1_96?crid=2M096C61O4MLT&keywords=bags&qid=1697527305&sprefix=ba%2Caps%2C283&sr=8-96",
    "https://www.amazon.in/Half-Moon-Hercules-Travelling-Compartment/dp/B0CJ3FDW3K/ref=sr_1_209?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-209",
    "https://www.amazon.in/Lavie-MARMA-Womens-Sling-Bag/dp/B07KMBNKXZ/ref=sr_1_210?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-210",
    "https://www.amazon.in/Lavie-Womens-Closure-Satchel-Handbag_Chocolate/dp/B07DJ9Q1NY/ref=sr_1_211?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-211",
    "https://www.amazon.in/Frantic-Cartoon-Velvet-Preschool-Nursery/dp/B09KY5541N/ref=sr_1_212?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-212",
    "https://www.amazon.in/Genie-Moonlight-compartments-Lightweight-Travelling/dp/B097PGGTNJ/ref=sr_1_213?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-213",
    "https://www.amazon.in/Tabelito-NEO-Backpack-Business-Compartment/dp/B0C2D2GPWJ/ref=sr_1_214?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-214",
    "https://www.amazon.in/Ezee-Garbage-Bags-48x54-Medium/dp/B074CW3JV4/ref=sr_1_215?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-215",
    "https://www.amazon.in/Foldable-Laundry-Capacity-Quality-Combination/dp/B0BRFRVQMX/ref=sr_1_216?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-216",
    "https://www.amazon.in/Gear-DOUBLE-Resistant-Backpack-Navy-Tan/dp/B0BTJ2T26W/ref=sr_1_217?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-217",
    "https://www.amazon.in/LOOKMUSTER-Waterproof-Backpack-College-Business/dp/B0BS6YGKMC/ref=sr_1_218?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-218",
    "https://www.amazon.in/DZert-Hello-School-Backpacks-Cartoon/dp/B08M6FS6W8/ref=sr_1_219?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-219",
    "https://www.amazon.in/Safari-Formal-Backpack-Anti-Theft-VAULT19CBBLK/dp/B07XSTR69N/ref=sr_1_220?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-220",
    "https://www.amazon.in/TRAWOC-Travel-Backpack-Compartment-Women-Olivegreen/dp/B0CFFLCBKZ/ref=sr_1_221?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-221",
    "https://www.amazon.in/DZert-School-Backpacks-Cartoon-Marshall/dp/B07WKM1YZC/ref=sr_1_222?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-222",
    "https://www.amazon.in/Aristocrat-Zeal-Unisex-Grey-Laptop/dp/B0B5YHC1W5/ref=sr_1_223?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-223",
    "https://www.amazon.in/Martucci-Casual-Travelling-Laptop-Backpack/dp/B088B4P6ZW/ref=sr_1_224?crid=2M096C61O4MLT&keywords=bags&qid=1697527311&sprefix=ba%2Caps%2C283&sr=8-224",
    "https://www.amazon.in/Amazon-Basics-Laptop-College-Backpack/dp/B0C8NSJ4RD/ref=sr_1_273?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-273",
    "https://www.amazon.in/AirCase-C25-Messenger-Shoulder-Compartments/dp/B07X6DV3VM/ref=sr_1_274?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-274",
    "https://www.amazon.in/Puma-Unisex-Adult-Backpack-Fizzy-9018304/dp/B0BWF6RYVS/ref=sr_1_275?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-275",
    "https://www.amazon.in/Dell-Pro-Slim-Backpack-15/dp/B07PMQTB6T/ref=sr_1_276?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-276",
    "https://www.amazon.in/Eco-Right-Handbags-College-Shopping/dp/B06XRQRDCY/ref=sr_1_277?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-277",
    "https://www.amazon.in/Hammonds-Flycatcher-Leather-Messenger-LB106BU/dp/B0851H1WS5/ref=sr_1_278?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-278",
    "https://www.amazon.in/Travalate-Waterproof-Polyester-Duffle-Travel/dp/B07S3FW7Z5/ref=sr_1_279?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-279",
    "https://www.amazon.in/Lifelong-LLGB02-Adjustable-Shoulder-Accessories/dp/B0BW3QZBQH/ref=sr_1_280?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-280",
    "https://www.amazon.in/Adjustable-Compartment-Lightweight-Water-Resistant-Travel-Friendly/dp/B0C3R7SN3Q/ref=sr_1_281?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-281",
    "https://www.amazon.in/Wildcraft-Nylon-Travel-Duffle-11550/dp/B075T81DVW/ref=sr_1_282?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-282",
    "https://www.amazon.in/Gear-Executive-Anti-Theft-Backpack-BKPPKREXE0101/dp/B097KCMQKG/ref=sr_1_283?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-283",
    "https://www.amazon.in/Kuber-Industries-Biodegradable-Warehouse-Washroom/dp/B0C3QR3YJV/ref=sr_1_284?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-284",
    "https://www.amazon.in/Storite-Sling-Bag-Shoulder-25-5cmx7cmx20cm/dp/B09P3RQPCG/ref=sr_1_285?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-285",
    "https://www.amazon.in/Bennett-15-6-inch-College-Repellent-Backpack/dp/B09WZHX3B1/ref=sr_1_286?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-286",
    "https://www.amazon.in/Shalimar-Premium-OXO-Biodegradable-Garbage/dp/B08DHV38W8/ref=sr_1_287?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-287",
    "https://www.amazon.in/Purple-Tree-Canvas-Tote-Women/dp/B07PDYTXD7/ref=sr_1_288?crid=2M096C61O4MLT&keywords=bags&qid=1697527316&sprefix=ba%2Caps%2C283&sr=8-288",
    "https://www.amazon.in/Gear-Statement-Duffel-cum-Backpack-Black-Yellow-DUFSTMTMAXS01/dp/B08D1SVKPN/ref=sr_1_289?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-289",
    "https://www.amazon.in/Amazon-Brand-Reusable-Eco-Friendly-Multi-Purpose/dp/B08TTMMGYT/ref=sr_1_290?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-290",
    "https://www.amazon.in/Delrin-Backpack-Motorcycle-Waterproof-Programmable/dp/B0CBSGG3LX/ref=sr_1_291?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-291",
    "https://www.amazon.in/ADISA-Women-Girls-Floral-SL5072-CRE_Cream/dp/B09B56BCXR/ref=sr_1_292?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-292",
    "https://www.amazon.in/Amazon-Basics-Laptop-College-Backpack/dp/B0C8NSJ4RD/ref=sr_1_293?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-293",
    "https://www.amazon.in/CRALOFT-Premium-Water-resistant-Compact-S5/dp/B0BRV3HVZ4/ref=sr_1_294?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-294",
    "https://www.amazon.in/Half-Moon-Messenger-Multi-Pocket-Adjustable/dp/B0C5CFCLLJ/ref=sr_1_295?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-295",
    "https://www.amazon.in/F-Gear-Milestone-Casual-Laptop-Backpack/dp/B08FX1R6WY/ref=sr_1_296?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-296",
    "https://www.amazon.in/DZert-Polyester-Black-White-Backpack/dp/B07GXX2BP3/ref=sr_1_297?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-297",
    "https://www.amazon.in/Martucci-Waterproof-Backpack-College-Business/dp/B0BRJRVH6D/ref=sr_1_298?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-298",
    "https://www.amazon.in/Safari-Overnighter-Resistant-Travelling-All-Purpose/dp/B097JMR4M6/ref=sr_1_299?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-299",
    "https://www.amazon.in/Kuber-Industries-Embroidered-Women-CTKTC8803/dp/B07SWD51BV/ref=sr_1_300?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-300",
    "https://www.amazon.in/Black-Orange-Casual-Backpack-BKPCARYON0106/dp/B019HA8AQO/ref=sr_1_301?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-301",
    "https://www.amazon.in/AirCase-C24-Messenger-Shoulder-Compartments/dp/B07Y3DB5YZ/ref=sr_1_302?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-302",
    "https://www.amazon.in/Safari-Polycarbonate-Midnight-Hardsided-RAY534WMBL/dp/B07WHLHXB9/ref=sr_1_303?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-303",
    "https://www.amazon.in/LuvLap-Travel-Multifunctional-Waterproof-Bag-Backpack/dp/B07W6Z8XKB/ref=sr_1_304?crid=2M096C61O4MLT&keywords=bags&qid=1697527319&sprefix=ba%2Caps%2C283&sr=8-304",
    "https://www.amazon.in/Wesley-Milestone-Waterproof-Backpack-Business/dp/B084JGJ8PF/ref=ice_ac_b_dpb?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-1",
    "https://www.amazon.in/gp/bestsellers/luggage/2917444031/ref=sr_bs_1_2917444031_1",
    "https://www.amazon.in/FUR-JADEN-Leatherette-Polypropylene-DUFF05/dp/B07M9BRCQ5/ref=sr_1_3?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-3",
    "https://www.amazon.in/Safari-Laptop-Backpack-Raincover-college/dp/B097JH4V5G/ref=sr_1_4?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-4",
    "https://www.amazon.in/Lenovo-15-6-Inches-Everyday-Backpack/dp/B08R7RPVJF/ref=sr_1_5?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-5",
    "https://www.amazon.in/Half-Moon-Backpack-Luggage-Compartment/dp/B09VCLZ3K4/ref=sr_1_6?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-6",
    "https://www.amazon.in/Wesley-Spartan-Hiking-Raincover-Organiser/dp/B098QFF5TJ/ref=sr_1_7?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-7",
    "https://www.amazon.in/American-Tourister-AMT-SCH-BAG02/dp/B07CGLDV2C/ref=sr_1_8?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-8",
    "https://www.amazon.in/Impulse-Belux-Backpack-Resistant-Black/dp/B0CJHL12N9/ref=sr_1_9?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-9",
    "https://www.amazon.in/Backpack-Small-Black-Water-Repellant/dp/B088XB5XY8/ref=sr_1_10?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-10",
    "https://www.amazon.in/ADISA-BP010-Weight-Casual-Backpack/dp/B07MXL986B/ref=sr_1_11?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-11",
    "https://www.amazon.in/Number-Backpack-Compartment-Charging-Organizer/dp/B09VTDMRY7/ref=sr_1_12?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-12",
    "https://www.amazon.in/Half-Moon-Resistant-Backpack-Compartment/dp/B0BJ32LQ6X/ref=sr_1_13?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-13",
    "https://www.amazon.in/ADISA-BP004-Weight-Casual-Backpack/dp/B07G3CG9FC/ref=sr_1_14?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-14",
    "https://www.amazon.in/Half-Moon-Waterproof-Backpack-Students/dp/B085MHDJ93/ref=sr_1_15?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-15",
    "https://www.amazon.in/Safari-45L-21-OB-BLK/dp/B07BZ5VC4H/ref=sr_1_16?crid=2M096C61O4MLT&keywords=bags&qid=1697532297&sprefix=ba%2Caps%2C283&sr=8-16",
    "https://www.amazon.in/Killer-Backpack-Compartments-Polyester-Waterproof/dp/B07C9XHZT1/ref=sr_1_97?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-97",
    "https://www.amazon.in/Murano-Casual-daybackpack-Office-College/dp/B0BX9GLFD6/ref=sr_1_98?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-98",
    "https://www.amazon.in/Nivia-5227-Junior-Others-Orange/dp/B08D7QKCX5/ref=sr_1_99?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-99",
    "https://www.amazon.in/Killer-Backpack-Compartments-Polyester-Waterproof/dp/B07CDD6YS2/ref=sr_1_100?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-100",
    "https://www.amazon.in/Corduroy-Reusable-Shopping-Washable-Shoulder/dp/B0BNX437F8/ref=sr_1_101?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-101",
    "https://www.amazon.in/Amazon-Brand-Presto-Oxo-Biodegradable-Garbage/dp/B08TDH2LCP/ref=sr_1_102?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-102",
    "https://www.amazon.in/Dell-Essential-Backpack-15-ES1520P/dp/B07TTCXHRH/ref=sr_1_103?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-103",
    "https://www.amazon.in/Safari-Polycarbonate-Hardside-Trolley-Suitcase/dp/B097JKR13B/ref=sr_1_104?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-104",
    "https://www.amazon.in/ZOUK-Printed-Handmade-Leather-handles/dp/B07NHYLTY7/ref=sr_1_105?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-105",
    "https://www.amazon.in/American-Tourister-Liftoff-Polypropylene-Suitcase/dp/B0C4PSWHRY/ref=sr_1_106?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-106",
    "https://www.amazon.in/Storite-Travel-Bag-Lightweight-GreenPink/dp/B0B3JBYZ8C/ref=sr_1_107?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-107",
    "https://www.amazon.in/ASUS-Backpack-Cross-Dyed-Material-Suitable/dp/B09Q68446F/ref=sr_1_108?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-108",
    "https://www.amazon.in/Sfane-Women-Trendy-Black-Duffel/dp/B07GCR84D9/ref=sr_1_109?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-109",
    "https://www.amazon.in/Amazon-Brand-Presto-Oxo-Biodegradable-Garbage/dp/B08TDGVLVM/ref=sr_1_110?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-110",
    "https://www.amazon.in/ADISA-Womens-Girls-Party-Crossbody/dp/B0B2WBJ2H8/ref=sr_1_111?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-111",
    "https://www.amazon.in/Amazon-Basics-Casual-Backpack-15-6-inch/dp/B09W4WJ1CB/ref=sr_1_112?crid=2M096C61O4MLT&keywords=bags&qid=1697532302&sprefix=ba%2Caps%2C283&sr=8-112",
    "https://www.amazon.in/Swiss-Military-Backpack-Pockets-LTB5A/dp/B0BHJ9WMZK/ref=sr_1_273?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-273",
    "https://www.amazon.in/Corduroy-Capacity-HandBags-Shoulder-Shopping/dp/B0BZYXT8Q7/ref=sr_1_274?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-274",
    "https://www.amazon.in/Dell-Pro-Slim-Backpack-15/dp/B07PMQTB6T/ref=sr_1_275?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-275",
    "https://www.amazon.in/Genie-compartments-Resistant-Lightweight-Travelling/dp/B097JJ64SH/ref=sr_1_276?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-276",
    "https://www.amazon.in/Adjustable-Compartment-Lightweight-Water-Resistant-Travel-Friendly/dp/B0C3R7SN3Q/ref=sr_1_277?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-277",
    "https://www.amazon.in/Wooum-Resistant-Material-Messenger-Compartment/dp/B09KV7Y3KL/ref=sr_1_278?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-278",
    "https://www.amazon.in/HP-15-6-inch-Backpack-Pass-Through-793A7AA/dp/B0BYDWD4VL/ref=sr_1_279?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-279",
    "https://www.amazon.in/Gear-Executive-Anti-Theft-Backpack-BKPPKREXE0101/dp/B097KCMQKG/ref=sr_1_280?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-280",
    "https://www.amazon.in/EUME-Kolkata-Drawstring-Backpack-Compartment/dp/B0BX9P4MJ7/ref=sr_1_281?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-281",
    "https://www.amazon.in/OMRON-BAGS-Compartment-Black-Blue/dp/B0BN34FSF4/ref=sr_1_282?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-282",
    "https://www.amazon.in/Wolpin-Foldable-Shopping-Bag-Grocery/dp/B0B21SYHMB/ref=sr_1_283?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-283",
    "https://www.amazon.in/Mi-Business-Casual-Resistant-Backpack/dp/B07YY6PTMN/ref=sr_1_284?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-284",
    "https://www.amazon.in/Kuber-Industries-Biodegradable-Warehouse-Washroom/dp/B0C3QR3YJV/ref=sr_1_285?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-285",
    "https://www.amazon.in/Shalimar-Premium-OXO-Biodegradable-Garbage/dp/B08DHV38W8/ref=sr_1_286?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-286",
    "https://www.amazon.in/Street27%C2%AE-Canvas-Corduroy-Tote-Multi-Purpose/dp/B0BQCBHJLP/ref=sr_1_287?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-287",
    "https://www.amazon.in/Stylbase-Spider-man-Polyester-Character-Embossed/dp/B0BNL2MJQQ/ref=sr_1_288?crid=2M096C61O4MLT&keywords=bags&qid=1697532308&sprefix=ba%2Caps%2C283&sr=8-288",
    "https://www.amazon.in/Genie-Ltrs-School-Backpack-CAMELLIA17SBPIN/dp/B07QHMKHWH/ref=sr_1_33?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-33",
    "https://www.amazon.in/TRUE-Emperor-Anti-Theft-backpack-charging/dp/B0BYB631NR/ref=sr_1_34?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-34",
    "https://www.amazon.in/Half-Moon-College-Spacious-Multiple/dp/B0C23Z9W18/ref=sr_1_35?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-35",
    "https://www.amazon.in/Safari-Hexa-Water-Resistant-Backpack/dp/B09B263JKS/ref=sr_1_36?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-36",
    "https://www.amazon.in/Step-Backpack-Small-Water-Repellant/dp/B088XG77KN/ref=sr_1_37?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-37",
    "https://www.amazon.in/Arctic-Fox-Backpack-Charging-Laptop/dp/B089QBD333/ref=sr_1_38?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-38",
    "https://www.amazon.in/POLE-STAR-Polyester-Backpack-Compartment/dp/B07D6NXR2Q/ref=sr_1_39?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-39",
    "https://www.amazon.in/Gear-Classic-Leather-Backpack-LBPCLSLTH0519/dp/B07G4JQX2F/ref=sr_1_40?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-40",
    "https://www.amazon.in/Impulse-Diggy-Backpack-Resistant-Green/dp/B0CJHVCZZV/ref=sr_1_41?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-41",
    "https://www.amazon.in/Impulse-Diggy-Backpack-Business-Resistant/dp/B0CJHV6RTS/ref=sr_1_42?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-42",
    "https://www.amazon.in/Half-Moon-Resistant-Backpack-Compartment/dp/B09T2TCSW7/ref=sr_1_43?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-43",
    "https://www.amazon.in/Wesley-Milestone-Waterproof-Backpack-Business/dp/B07K8KLB3P/ref=sr_1_44?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-44",
    "https://www.amazon.in/Zipline-Nexa-Resistant-Bagpack-Backpack/dp/B08WQ668WJ/ref=sr_1_45?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-45",
    "https://www.amazon.in/GOCART-LOGO-Backpack-Briefcase-Convertible/dp/B0822H451W/ref=sr_1_46?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-46",
    "https://www.amazon.in/Shalimar-Capacity-Travel-Storage-Duffel/dp/B09TPHFMX7/ref=sr_1_47?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-47",
    "https://www.amazon.in/AirCase-C34-Laptop-Backpack-Women/dp/B07QN4KXWG/ref=sr_1_48?crid=2M096C61O4MLT&keywords=bags&qid=1697537511&sprefix=ba%2Caps%2C283&sr=8-48",
    "https://www.amazon.in/Impulse-Diggy-Backpack-Resistant-Green/dp/B0CJHVCZZV/ref=sr_1_65?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-65",
    "https://www.amazon.in/Ezee-Garbage-Bag-inches-Pieces/dp/B06VX8YR6Q/ref=sr_1_66?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-66",
    "https://www.amazon.in/Lunars-Comet-Resistant-Casual-Backpack/dp/B07WN833M7/ref=sr_1_67?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-67",
    "https://www.amazon.in/Lavie-Womens-Closure-Satchel-Handbag_Chocolate/dp/B07DJ9Q1NY/ref=sr_1_68?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-68",
    "https://www.amazon.in/Shalimar-Premium-Garbage-Medium-Black/dp/B016DCB9OO/ref=sr_1_69?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-69",
    "https://www.amazon.in/Safari-Spartan-Water-Resistant-Backpack/dp/B09B26MB5M/ref=sr_1_70?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-70",
    "https://www.amazon.in/Amazon-Basics-Casual-Backpack-15-6-inch/dp/B09W4WJ1CB/ref=sr_1_71?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-71",
    "https://www.amazon.in/Half-Moon-Resistant-Backpack-Compartment/dp/B0BHX7GY16/ref=sr_1_72?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-72",
    "https://www.amazon.in/Safari-Sheild-Resistant-Casual-Backpack/dp/B09B26T7KQ/ref=sr_1_73?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-73",
    "https://www.amazon.in/Skybags-Unisex-Polyester-Pattern-Hustle/dp/B07F342RQD/ref=sr_1_74?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-74",
    "https://www.amazon.in/NORTH-ZONE-Lightweight-Backpacks-Stylish/dp/B0BL3SPN16/ref=sr_1_75?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-75",
    "https://www.amazon.in/Handcuffs-Multifunctional-Maternity-Backpack-Nursing/dp/B09413KB4K/ref=sr_1_76?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-76",
    "https://www.amazon.in/AmazonBasics-Vacuum-Compression-Storage-Bags/dp/B07RSCPH4N/ref=sr_1_77?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-77",
    "https://www.amazon.in/Puma-Carry-Unisex-Duffel-Bag/dp/B089T8PKSQ/ref=sr_1_78?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-78",
    "https://www.amazon.in/gp/bestsellers/kitchen/8464314031/ref=sr_bs_14_8464314031_1",
    "https://www.amazon.in/Half-Moon-College-Spacious-Multiple/dp/B0C23Z9W18/ref=sr_1_80?crid=2M096C61O4MLT&keywords=bags&qid=1697537515&sprefix=ba%2Caps%2C283&sr=8-80",
    "https://www.amazon.in/AmazonBasics-Vacuum-Compression-Storage-Bags/dp/B07RP7WHHY/ref=sr_1_113?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-113",
    "https://www.amazon.in/gp/bestsellers/luggage/2917442031/ref=sr_bs_1_2917442031_1",
    "https://www.amazon.in/Nivia-5227-Junior-Others-Orange/dp/B08D7QKCX5/ref=sr_1_115?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-115",
    "https://www.amazon.in/TRUE-HUMAN-Anti-Theft-charging-combination/dp/B09H7PK5ML/ref=sr_1_116?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-116",
    "https://www.amazon.in/Killer-Backpack-Compartments-Polyester-Waterproof/dp/B07CDD6YS2/ref=sr_1_117?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-117",
    "https://www.amazon.in/Ezee-Garbage-Bag-Pieces-Medium/dp/B06VX7PDXC/ref=sr_1_118?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-118",
    "https://www.amazon.in/Half-Moon-Hercules-Travelling-Compartment/dp/B0CJ3FDW3K/ref=sr_1_119?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-119",
    "https://www.amazon.in/American-Tourister-Liftoff-Polypropylene-Suitcase/dp/B0C4PSWHRY/ref=sr_1_120?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-120",
    "https://www.amazon.in/Kleeno-Cello-Clean-Garbage-Medium/dp/B09C284CTH/ref=sr_1_121?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-121",
    "https://www.amazon.in/ADISA-BP005-Weight-Casual-Backpack/dp/B07F3X45WZ/ref=sr_1_122?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-122",
    "https://www.amazon.in/HAMMONDS-FLYCATCHER-Genuine-Shoulder-Messenger/dp/B07P2TQH78/ref=sr_1_123?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-123",
    "https://www.amazon.in/Kuber-Industries-Polyester-Embroidered-CTKTC04387/dp/B07NJ8J98M/ref=sr_1_124?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-124",
    "https://www.amazon.in/Storite-Travel-Bag-Lightweight-GreenPink/dp/B0B3JBYZ8C/ref=sr_1_125?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-125",
    "https://www.amazon.in/Lenovo-Carrying-15-6-Inch-Toploader-GX40Q17229/dp/B075Y6Y9H5/ref=sr_1_126?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-126",
    "https://www.amazon.in/SFANE-Polyester-Shoulder-Separate-Compartment/dp/B08KG7J7L5/ref=sr_1_127?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-127",
    "https://www.amazon.in/Safari-Polyester-Travel-Duffle-PEP55RLBLK/dp/B07DD79VDG/ref=sr_1_128?crid=2M096C61O4MLT&keywords=bags&qid=1697537520&sprefix=ba%2Caps%2C283&sr=8-128",
    "https://www.amazon.in/Ezee-Garbage-Bags-48x54-Medium/dp/B074CW3JV4/ref=sr_1_177?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-177",
    "https://www.amazon.in/ZaySoo-Stylish-Backpack-College-Business/dp/B0BVZL49N8/ref=sr_1_178?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-178",
    "https://www.amazon.in/AirCase-Premium-Waterproof-Neoprene-Warranty/dp/B07JBBKD5S/ref=sr_1_179?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-179",
    "https://www.amazon.in/Lunars-Travel-Laptop-Bag-compartments/dp/B08NHKF2G7/ref=sr_1_180?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-180",
    "https://www.amazon.in/Street27%C2%AE-Canvas-Corduroy-Tote-Multi-Purpose/dp/B0BQCBHJLP/ref=sr_1_181?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-181",
    "https://www.amazon.in/AirCase-C24-Messenger-Shoulder-Compartments/dp/B07Y3DB5YZ/ref=sr_1_182?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-182",
    "https://www.amazon.in/Gear-DOUBLE-DECKER-Resistant-Backpack/dp/B0BTJ3WTMV/ref=sr_1_183?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-183",
    "https://www.amazon.in/DZert-Panda-School-Backpacks-Cartoon/dp/B07Y2BFJ1B/ref=sr_1_184?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-184",
    "https://www.amazon.in/Tabelito-NEXA-Backpack-Business-Compartment/dp/B0C2D3YR7T/ref=sr_1_185?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-185",
    "https://www.amazon.in/ADISA-Laptop-Backpack-Office-College/dp/B09TPVD964/ref=sr_1_186?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-186",
    "https://www.amazon.in/Corduroy-Reusable-Shopping-Washable-Shoulder/dp/B0BNX437F8/ref=sr_1_187?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-187",
    "https://www.amazon.in/Professional-Photographers-Waterproof-Lightweight-Accessories/dp/B0C58VVFQT/ref=sr_1_188?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-188",
    "https://www.amazon.in/Zureni-OXO-Biodegradable-Drawstring-Anti-drip-Warehouse/dp/B0BTHC4F2T/ref=sr_1_189?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-189",
    "https://www.amazon.in/Lino-Perros-women-shoulder-OFFWHITE/dp/B09P69ZNBP/ref=sr_1_190?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-190",
    "https://www.amazon.in/Arctic-Fox-Anti-Theft-Backpack-Charging/dp/B089Q9TM16/ref=sr_1_191?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-191",
    "https://www.amazon.in/Artistix-Unisex-Travel-Backpack-Repellent/dp/B09B5DMGM1/ref=sr_1_192?crid=2M096C61O4MLT&keywords=bags&qid=1697537525&sprefix=ba%2Caps%2C283&sr=8-192",
    "https://www.amazon.in/Corduroy-Capacity-HandBags-Shoulder-Shopping/dp/B0BZYXT8Q7/ref=sr_1_209?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-209",
    "https://www.amazon.in/F-Gear-Milestone-Casual-Laptop-Backpack/dp/B08FX1R6WY/ref=sr_1_210?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-210",
    "https://www.amazon.in/HYDER-Gamepad-Waterproof-Backpack-Everyday/dp/B0BR3KK8TR/ref=sr_1_211?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-211",
    "https://www.amazon.in/Amazon-Brand-Solimo-Underbed-Storage/dp/B084MS8LTW/ref=sr_1_212?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-212",
    "https://www.amazon.in/Travalate-Waterproof-Polyester-Duffle-Travel/dp/B07S3FW7Z5/ref=sr_1_213?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-213",
    "https://www.amazon.in/Red-Lemon-Unisex-adult-Waterproof-Charging/dp/B09VGNTDRZ/ref=sr_1_214?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-214",
    "https://www.amazon.in/Corduroy-Reusable-Shopping-Washable-Shoulder/dp/B0BNX437F8/ref=sr_1_215?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-215",
    "https://www.amazon.in/Gear-LOGI-Q-Resistant-Backpack-Black-White/dp/B0BTJ2VV17/ref=sr_1_216?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-216",
    "https://www.amazon.in/ADISA-laptop-backpack-office-college/dp/B0BXQD8DZX/ref=sr_1_217?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-217",
    "https://www.amazon.in/HARISSONS-Backpack-Black-Grey-Repellent-Organizer/dp/B08LBLKYRY/ref=sr_1_218?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-218",
    "https://www.amazon.in/American-Tourister-Backpack-Organizer-Compatible/dp/B0C86394QQ/ref=sr_1_219?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-219",
    "https://www.amazon.in/Red-Lemon-Capacity-Backpack-Multifunctional/dp/B09RK4BRPM/ref=sr_1_220?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-220",
    "https://www.amazon.in/HAMMONDS-FLYCATCHER-Genuine-Shoulder-Messenger/dp/B07P2TQH78/ref=sr_1_221?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-221",
    "https://www.amazon.in/Kuber-Industries-Embroidered-Women-CTKTC8803/dp/B07SWD51BV/ref=sr_1_222?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-222",
    "https://www.amazon.in/Safari-Polycarbonate-Hardside-Trolley-Suitcase/dp/B097JKR13B/ref=sr_1_223?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-223",
    "https://www.amazon.in/Tabelito%C2%AE-Delta-Waterproof-Backpack-Compatible/dp/B0BLK1Z7DQ/ref=sr_1_224?crid=2M096C61O4MLT&keywords=bags&qid=1697537530&sprefix=ba%2Caps%2C283&sr=8-224"
]

# Create a CSV file to store the data
csv_filename = 'amazon_product_details.csv'
with open('amazon_product_details.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for product_url in product_urls:
        product_details = scrape_product_details(product_url)
        if product_details:
            product_details['Product URL'] = product_url
            writer.writerow(product_details)
            

# Define the CSV file name
csv_filename = 'amazon_product_details.csv'

# Read and print the CSV file
with open(csv_filename, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print("Product URL: ", row['Product URL'])
        if row['Description']:
            print("Description: ", row['Description'])
        if row['ASIN']:
            print("ASIN: ", row['ASIN'])
        if row['Product Description']:
            print("Product Description: ", row['Product Description'])
        if row['Manufacturer']:
            print("Manufacturer: ", row['Manufacturer'])
        print()