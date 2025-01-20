import gspread
import shopify
import pandas as pd
import sys

from oauth2client.service_account import ServiceAccountCredentials
def gg_sheet(link):
# đọc fille gg sheet
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth_gg.json', scope)
    client = gspread.authorize(creds)


    sheet = 'product_template'
    # sheet_id = '1HMrC3Sds-BsWCQdFFM_kfYjaECzMGnmXMsW2ybp1_JM'

    sheet_id = link.split('/d/')[1].split('/')[0]

    # mowr  gg sheet
    try:
        # Mở Google Sheets
        # sheet = client.open(sheet).sheet1
        sheet = client.open_by_key(sheet_id).sheet1
        print(f"Đã connect tới Google Sheets {sheet}")
    except gspread.SpreadsheetNotFound:
        print(f"Không tìm thấy bảng tính có tên {sheet}")
        exit()
    except PermissionError:
        print("Không có quyền truy cập vào bảng tính. Hãy chắc chắn rằng bạn đã chia sẻ bảng tính với tài khoản dịch vụ.")
        exit()

    #lấy dữ liệu
    records = sheet.get_all_records()

    # đổi dữ liệu thành dataframe
    df = pd.DataFrame(records)

    # đẩy dữ liệu lên shopify
    total_products = len(df)

    for index, row in df.iterrows():
        product = shopify.Product()
        product.title = row['Title']
        product.body_html = row['Body (HTML)']
        product.vendor = row['Vendor']
        product.product_type = row['Type']
        product.save()

        sys.stdout.write(f"\rHoàn thành: {index + 1}/{total_products}")
        sys.stdout.flush()
    
        if product.errors:
            print(f"Error importing product '{row['Title']}': {product.errors.full_messages()}")
        else:
            print(f"Product '{product.title}' imported successfully with ID: {product.id}")
        
        # print(f"Hoàn thành: {index + 1}/{total_products}")
        
    print("\nImport hoàn thành tất cả sản phẩm")

