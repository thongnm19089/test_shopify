import requests
import json
from tabulate import tabulate
def show_product(products_data):
    headers = ["ID", "Title", "Handle", "Vendor", "Product Type"]
    rows = []
    for product_data in products_data:
        rows.append([
            product_data.get('id', 'N/A'),
            product_data.get('title', 'N/A'),
            product_data.get('handle', 'N/A'),
            product_data.get('vendor', 'N/A'),
            product_data.get('productType', 'N/A')
        ])
    print("\nProduct Information:")
    print(tabulate(rows, headers, tablefmt="grid"))

def graphql_create(shop_url , api_version , headers):  
    #thêm
    add_product_query = """
    mutation {
      productCreate(input: {
        title: "Product create with graphql1",
        bodyHtml: "<strong>Good product!</strong>",
        vendor: "Vendor Name",
        productType: "Hat",
        status: ACTIVE,
        variants: {
          price: "19.99"
        }
      }) {
        product {
          id
          title
        }
      }
    }
    """

    response = requests.post(f"https://{shop_url}/admin/api/{api_version}/graphql.json", headers=headers, data=json.dumps({"query": add_product_query}))
    product_data = response.json()
    if 'errors' in product_data:
        print("Errors:", product_data['errors'])
    else:
        print("tạo mới thành công !!!!")
        show_product([product_data['data']['productCreate']['product']])

def graphql_query(shop_url , api_version , headers):
    # Truy vấn các sản phẩm
    query_products = """
    {
      products(first: 10) {
        edges {
          node {
            id
            title
            handle
            vendor
            productType
            variants(first: 10) {
              edges {
                node {
                  id
                  title
                  price
                }
              }
            }
          }
        }
      }
    }
    """

    response = requests.post(f"https://{shop_url}/admin/api/{api_version}/graphql.json", headers=headers, data=json.dumps({"query": query_products}))
    product_data = response.json()
    if 'errors' in product_data:
        print("Errors:", product_data['errors'])
    else:
        products = [edge['node'] for edge in product_data['data']['products']['edges']]
        show_product(products)

    # Sửa sản phẩm
def graphql_update(shop_url , api_version , headers):   
    update_product_query = """
    mutation {
      productUpdate(input: {
        id: "gid://shopify/Product/7492289757253",
        title: "Updated Product Title",
        bodyHtml: "<strong>a a a!</strong>"
      }) {
        product {
          id
          title
        }
      }
    }
    """

    response = requests.post(f"https://{shop_url}/admin/api/{api_version}/graphql.json", headers=headers, data=json.dumps({"query": update_product_query}))
    print(response.json())

    # Xóa sản phẩm
def graphql_delete(shop_url , api_version , headers):
    delete_product_query = """
    mutation {
      productDelete(input: {
        id: "gid://shopify/Product/PRODUCT_ID"
      }) {
        deletedProductId
      }
    }
    """

    response = requests.post(f"https://{shop_url}/admin/api/{api_version}/graphql.json", headers=headers, data=json.dumps({"query": delete_product_query}))
    print(response.json())


def graphql_query_id (shop_url , api_version , headers ,product_id):
    product_id = product_id  
    query_product = f"""
    {{
      product(id: "{product_id}") {{
        id
        title
        handle
        bodyHtml
        vendor
        productType
        variants(first: 10) {{
          edges {{
            node {{
              id
              title
              price
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(f"https://{shop_url}/admin/api/{api_version}/graphql.json", headers=headers, data=json.dumps({"query": query_product}))
    product_data = response.json()
    if 'errors' in product_data:
        print("Errors:", product_data['errors'])
    else:
        show_product([product_data['data']['product']])
