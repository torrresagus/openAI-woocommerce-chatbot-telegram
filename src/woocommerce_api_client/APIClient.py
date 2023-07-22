from woocommerce import API
class APIClient:
    def __init__(self, url, consumer_key, consumer_secret, wp_api=True, version="wc/v3"):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.wp_api = wp_api
        self.version = version
        self.wcapi = API(url=self.url, consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, wp_api=self.wp_api, version=self.version)

    def get_products(self):
    #   List to store all products
        all_products = []

    #   Pagination parameters
        page = 1
        per_page = 100  # Number of products per page

    #   Make requests until all products are obtained
        while True:
            response = self.wcapi.get("products", params={"page": page, "per_page": per_page})
            products = response.json()

        #   Exit the loop if there are no more products on the current page
            if len(products) == 0:
                break

        #   Add products from the current page to the list
            all_products.extend(products)

        #   Increase the page number for the next request
            page += 1

        return all_products
        
    def get_categories(self):
    #   Get all categories
        response = self.wcapi.get("products/categories", params={"per_page": 100})
        categories = response.json()

    #   Create a list to store the data of each category
        new_json = []

    #   Loop through the list of categories and extract the desired fields
        for category in categories:
            category_data = {
                "id": category['id'],
                "name": category['name'],
                "slug": category['slug']
            }
            new_json.append(category_data)
        return new_json
      
    def get_payment_gateways(self):
        payment_gateways = self.wcapi.get("payment_gateways").json()
        return payment_gateways

    def get_shipping_zones(self):
        shipping_zones = self.wcapi.get("shipping/zones").json()
        return shipping_zones
    
    def get_shipping_methods_from_shipping_zone(self, id):
        method_shipping = self.wcapi.get(f"shipping/zones/{id}/methods").json()
        return method_shipping