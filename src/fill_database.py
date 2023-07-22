from woocommerce_api_client import APIClient as api
import database.database_operations as database_operations
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

wc_client = api.APIClient(
    url=os.environ['WC_URL'],
    consumer_key=os.environ['WC_CONSUMER_KEY'],
    consumer_secret=os.environ['WC_CONSUMER_SECRET'],
    wp_api=True,
    version="wc/v3"
)

payment_gateways = (wc_client.get_payment_gateways())

shipping_zones = (wc_client.get_shipping_zones())

products = wc_client.get_products()

database_operations.create_or_update_tables_products(products)
database_operations.create_or_update_payment_gateways(payment_gateways)
database_operations.create_or_update_shipping_zones(shipping_zones)