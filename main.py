import shopify
import csv
import requests
import json
from graphql import graphql_create , graphql_update , graphql_delete ,graphql_query  ,graphql_query_id
from import_xml import import_xml
from ssh import download_file_from_server  ,check_ssh_connection
from file_csv import import_from_file 
from gg_sheet import gg_sheet
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv('SHOPIFY_ACCESS_TOKEN')
# Kết nối tới Shopify
# shop_url = "https://mhthcw-0b.myshopify.com/admin"
shop_url = "thommy-bulkflow.myshopify.com"

api_version = "2021-07"
api_key = "d11faa2ec99f9ac5be2cd54da77fdebc"
password = os.getenv('SHOPIFY_ACCESS_TOKEN')  

shopify.ShopifyResource.set_site(f"https://{api_key}:{password}@{shop_url}/admin/api/{api_version}")
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": password
}

try:
    shop = shopify.Shop.current()
    print(f"Connected to shop: {shop.name}")
except Exception as e:
    print(f"Error connecting to Shopify: {e}")

    
# Đọc file CSV và đẩy dữ liệu lên Shopify
file = 'product_template.csv'


def main():
    try:
        while True:
            print("\nMenu:")
            print("1. Import từ file CSV")
            print("2. Import file từ ssh")
            print("3. Import dữ liệu từ Google Sheets")
            print("4. Import dữ liệu từ XML")   
            print("5. Crud dữ liệu với Graphql")
            print("0. Thoát")
            choice = input("\nChọn chức năng: ")
            if choice == '1':
                import_from_file(file)
            elif choice == '2':
                server_ip = input("Nhập địa chỉ ip server( coppy: 36.50.134.109): ")
                username = input("Nhập username server(coppy: thongnm): ")
                ssh_password = input("Nhập mật khẩu SSH(coppy: thongnm): ")
                remote_path = input("Nhập đường dẫn file trên server(coppy: /home/thongnm/uploads/product_template.csv): ")
                local_dir = input("Nhập đường dẫn lưu file trên máy local(coppy: download/): ")   
                local_path = f"{local_dir}/product_template.csv"
                if check_ssh_connection(username, server_ip, ssh_password):
                    print("Kết nối SSH thành công")
                    download_file_from_server(remote_path, local_path, username, server_ip, ssh_password)
                    import_from_file(local_path)
                else:
                    print("Kết nối SSH thất bại. Vui lòng kiểm tra lại thông tin.")
            elif choice == '3':
                link = input("Nhập link gg sheet (link vd: https://docs.google.com/spreadsheets/d/1HMrC3Sds-BsWCQdFFM_kfYjaECzMGnmXMsW2ybp1_JM/edit?gid=1949959635#gid=1949959635) : ")    
                gg_sheet(link)
            elif choice == '4':
                xml_file = 'product_template.xml'
                import_xml(xml_file = xml_file ,shop_url= shop_url, api_version = api_version, headers=headers)
            elif choice == '5':
                while True:
                    print("\nMenu:")
                    print("1. Truy vấn thông tin tất cả các sản phẩm của Shop")
                    print("2. Thêm sản sản phẩm")
                    print("3. Sửa sản phẩm")
                    print("4. Xóa sản phẩm")
                    print("5. Truy vấn một sản phẩm cụ thể")
                    print("0. Thoát")
                    choice = input("\nChọn chức năng: ")
                    if choice == '1':
                        graphql_query(shop_url=shop_url, api_version = api_version, headers=headers)
                    elif choice == '2':
                        graphql_create(shop_url=shop_url, api_version = api_version, headers=headers)
                    elif choice == '3':
                        graphql_update(shop_url=shop_url, api_version = api_version, headers=headers)
                    elif choice == '4':
                        graphql_delete(shop_url=shop_url, api_version = api_version, headers=headers)
                    elif choice == '5':
                        input_id = input("Nhập id sản phẩm cần tìm (fomat :'gid://shopify/Product/9840538779937' ): ")
                        graphql_query_id(shop_url=shop_url, api_version = api_version, headers=headers, product_id = input_id)      
                    elif choice == '0':
                        break 
                    else:
                        print("Lựa chọn không hợp lệ , Vui lòng chọn lại !!!!!")
            elif choice == '0': 
                break
            else:
                print("ádasd")
        
    except KeyboardInterrupt:
        print(f"thoát chương trình")


if __name__ == "__main__":
    main()