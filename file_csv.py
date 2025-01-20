import shopify
import csv
import sys

def import_from_file(file):
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        total_products = len(rows)
        for index, row in enumerate(rows):
            product = shopify.Product()
            product.title = row['Title']
            product.body_html = row['Body (HTML)']
            product.vendor = row['Vendor']
            product.product_type = row['Type']
            product.save()

            if product.errors:
                print(f"Error importing product '{row['Title']}': {product.errors.full_messages()}")
            else:
                print(f"Product '{product.title}' imported successfully with ID: {product.id}")

          

    # In ra dòng hoàn thành tổng thể
    print("\nImport hoàn thành tất cả sản phẩm")