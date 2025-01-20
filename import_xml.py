import xml.etree.ElementTree as ET
import requests
import json


import xml.etree.ElementTree as ET
import shopify

# def import_xml_to_shopify(xml_file):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     for product in root.findall('product'):
#         title = product.find('title').text
#         body_html = product.find('body_html').text
#         vendor = product.find('vendor').text
#         product_type = product.find('product_type').text
#         price = product.find('price').text

#         product = shopify.Product()
#         product.title = title
#         product.body_html = body_html
#         product.vendor = vendor
#         product.product_type = product_type
#         variant = shopify.Variant()
#         variant.price = price
#         product.variants = [variant]
#         product.save()

def import_xml(xml_file, shop_url, api_version, headers):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for product in root.findall('product'):
            title = product.find('Title').text if product.find('Title') is not None else 'N/A'
            body_html = product.find('Body_HTML').text if product.find('Body_HTML') is not None else 'N/A'
            vendor = product.find('Vendor').text if product.find('Vendor') is not None else 'N/A'
            product_type = product.find('Type').text if product.find('Type') is not None else 'N/A'
            price = product.find('Variant_Price').text if product.find('Variant_Price') is not None else 'N/A'

            product_data = {
                "product": {
                    "title": title,
                    "body_html": body_html,
                    "vendor": vendor,
                    "product_type": product_type,
                    "variants": [
                        {
                            "price": price
                        }
                    ]
                }
            }

            response = requests.post(f"https://{shop_url}/admin/api/{api_version}/products.json", headers=headers, data=json.dumps(product_data))
            response_data = response.json()
            if 'errors' in response_data:
                print("Errors:", response_data['errors'])
            else:
                print("tạo product mới thành công !!!!")
                print(f"Product '{title}' created successfully with ID: {response_data['product']['id']}")
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")