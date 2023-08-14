import mysql.connector
import database.mysql_connection as mysql_connection
import open_ai.embedding_utils as eu
import json

from utilis.html_utils import remove_html_tags

# Function to check if a table exists in the database.
def check_table_exists(table_name):
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        table_exists = cursor.fetchone() is not None
        cursor.close()
        return table_exists

    except mysql.connector.Error as error:
        print(f"Error while verifying the existence of the table {table_name}: {error}")

    finally:
        connection.close()

#   Function to create or update the 'payment_gateways' table with the provided data.
def create_or_update_payment_gateways(data):
#   Get the connection to the database
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")
        return

    try:
        # Create cursor
        cursor = connection.cursor()

        #Create the 'payment_gateways' table if it does not exist
        if not check_table_exists('payment_gateways'):
            cursor.execute("""
                CREATE TABLE payment_gateways (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                description TEXT,
                enabled BOOLEAN
                )
            """)

            print("Tabla 'payment_gateways' creada.")

    #   Insert or update data in the table 'payment_gateways'
        for gateway in data:
            cursor.execute("""
                INSERT INTO payment_gateways (title, description, enabled)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                description = VALUES(description),
                enabled = VALUES(enabled)
            """, (
                gateway['title'],
                gateway['description'],
                gateway['enabled']
            ))


        connection.commit()
        print("Payment gateways data inserted or updated successfully.")

    except mysql.connector.Error as error:
        print("Error inserting or updating payment gateways data: ", error)

    finally:
    #   Close cursor and connection
        cursor.close()
        connection.close()

def save_chat_messages(chat_id, messages):
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")
        return

    cursor = connection.cursor()

    try:
        # Crear la 'chat_messages' table si no existe.
        if not check_table_exists('chat_messages'):
            cursor.execute("""
                CREATE TABLE chat_messages (
                chat_id INT PRIMARY KEY,
                messages JSON
                )   
            """)
            print("Tabla 'chat_messages' creada.")
    except mysql.connector.Error as err:
        print("Error creating table:", err)

    try:
        cursor.execute("""
            INSERT INTO chat_messages (chat_id, messages)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE messages = %s
        """, (chat_id, json.dumps(messages), json.dumps(messages)))

        connection.commit()
    except mysql.connector.Error as err:
        print("Error executing query:", err)
        connection.rollback()

    cursor.close()
    connection.close()


# Function to create or update the 'products' and 'categories' tables with the provided data.
def create_or_update_tables_products(data):
#   Get the connection to the database
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")
        return

    try:
        # Create cursor
        cursor = connection.cursor()

    #   Create the 'products' table if it does not exist
        if not check_table_exists('products'):
            cursor.execute("""
                CREATE TABLE products (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    slug VARCHAR(255),
                    permalink VARCHAR(255),
                    date_created_gmt DATETIME,
                    type VARCHAR(255),
                    status VARCHAR(255),
                    featured BOOLEAN,
                    catalog_visibility VARCHAR(255),
                    description TEXT,
                    short_description TEXT,
                    price DECIMAL(10, 2),
                    regular_price DECIMAL(10, 2),
                    on_sale BOOLEAN,
                    purchasable BOOLEAN,
                    tax_status VARCHAR(255),
                    manage_stock BOOLEAN,
                    stock_quantity INT,
                    stock_status VARCHAR(255),
                    weight VARCHAR(255),
                    shipping_required BOOLEAN,
                    shipping_taxable BOOLEAN,
                    menu_order INT,
                    parent_id INT
                )
            """)
            print("Table 'products' created.")

    #   Create the 'categories' table if it does not exist
        if not check_table_exists('categories'):
            cursor.execute("""
                CREATE TABLE categories (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    slug VARCHAR(255)
                )
            """)
            print("Table 'categories' created.")

    #   Insert or update data in the table 'products'
        for product in data:
        #   Check if 'regular_price' is an empty string and assign a default value if it is.
            regular_price = product['regular_price']
            if regular_price == '':
                regular_price = 0.0
                
            newDesc = remove_html_tags(product['description'])

            cursor.execute("""
                INSERT INTO products
                (id, name, slug, permalink, date_created_gmt, type, status, featured, catalog_visibility, description,
                short_description, price, regular_price, on_sale, purchasable, tax_status, manage_stock,
                stock_quantity, stock_status, weight, shipping_required, shipping_taxable, menu_order, parent_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                slug = VALUES(slug),
                permalink = VALUES(permalink),
                date_created_gmt = VALUES(date_created_gmt),
                type = VALUES(type),
                status = VALUES(status),
                featured = VALUES(featured),
                catalog_visibility = VALUES(catalog_visibility),
                description = VALUES(description),
                short_description = VALUES(short_description),
                price = VALUES(price),
                regular_price = VALUES(regular_price),
                on_sale = VALUES(on_sale),
                purchasable = VALUES(purchasable),
                tax_status = VALUES(tax_status),
                manage_stock = VALUES(manage_stock),
                stock_quantity = VALUES(stock_quantity),
                stock_status = VALUES(stock_status),
                weight = VALUES(weight),
                shipping_required = VALUES(shipping_required),
                shipping_taxable = VALUES(shipping_taxable),
                menu_order = VALUES(menu_order),
                parent_id = VALUES(parent_id)
            """, (
                product['id'],
                product['name'],
                product['slug'],
                product['permalink'],
                product['date_created_gmt'],
                product['type'],
                product['status'],
                product['featured'],
                product['catalog_visibility'],
                newDesc,
                product['short_description'],
                product['price'],
                regular_price, # Use the verified value of 'regular_price'    
                product['on_sale'],
                product['purchasable'],
                product['tax_status'],
                product['manage_stock'],
                product['stock_quantity'],
                product['stock_status'],
                product['weight'],
                product['shipping_required'],
                product['shipping_taxable'],
                product['menu_order'],
                product['parent_id']
            ))


        connection.commit()
        print("Product data inserted or updated successfully.")

    except mysql.connector.Error as error:
        print("Error inserting or updating product data: ", error)

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        print("Database connection closed, calling embeddings.")
        create_or_update_embeddings_table()

# Function to create or update the 'shipping_zones' table with the provided data.
def create_or_update_shipping_zones(data):
#   Get the connection to the database
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")
        return

    try:
    #   Create cursor
        cursor = connection.cursor()

    #   Create the 'shipping_zones' table if it does not exist
        if not check_table_exists('shipping_zones'):
            cursor.execute("""
                CREATE TABLE shipping_zones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                `order` INT,
                href VARCHAR(255)
                )
            """)

            print("Table'shipping_zones' created.")

    #   Insert or update data in the table 'shipping_zones'
        for zone in data:
            cursor.execute("""
                INSERT INTO shipping_zones (id, name, `order`, href)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                `order` = VALUES(`order`),
                href = VALUES(href)
            """, (
                zone['id'],
                zone['name'],
                zone['order'],
                zone['_links']['self'][0]['href']
            ))

        connection.commit()
        print("Shipping zones data inserted or updated successfully.")

    except mysql.connector.Error as error:
        print("Error inserting or updating shipping zones data: ", error)

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()

# Function to create or update the 'embeddings' table with product embeddings.
def create_or_update_embeddings_table():
#   Get the connection to the database
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")
        return

    try:
        print("Embedding is runnig")
    #   Enable transactions
        connection.autocommit = False

    #   Create cursor
        cursor = connection.cursor()
    #   Check if the 'embeddings' table exists.
        if not check_table_exists('embeddings'):
            print("Create the 'embeddings' table.")
            cursor.execute("""
                CREATE TABLE embeddings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT,
                    embedding JSON,
                    model VARCHAR(255),
                    object VARCHAR(255),
                    embedding_index INT,
                    prompt_tokens INT,
                    total_tokens INT,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)
            print("Table 'embeddings' created.")

    #   Get records from the 'products' table.  
        cursor.execute("SELECT id, name, description FROM products")
        products = cursor.fetchall()

        # Iniciar transacción
        cursor.execute("START TRANSACTION")

        for product in products:
            product_id = product[0]
            name = product[1]
            description = product[2]

        #   Check if the combined embedding already exists in the 'embeddings' table.
            cursor.execute("SELECT embedding FROM embeddings WHERE product_id = %s AND object = 'combined'", (product_id,))
            existing_embedding = cursor.fetchone()

            if existing_embedding is not None:
            #   The combined embedding already exists in the table, no need to recalculate it
                print("The combined embedding already exists for the product", product_id)
                continue

        #   Combine the name and description into a single string
            combined_text = name + " " + description

        #   Perform the combined embedding.
            print("Attempting combined embedding")
            embedding_combined = eu.get_embedding(combined_text)
            embedding_combined_str = json.dumps(embedding_combined['data'][0]['embedding'])  # Convert the list of embeddings to a JSON string
            print(embedding_combined_str)

        #   Insert or update the combined embedding in the database
            cursor.execute("""
                INSERT INTO embeddings (product_id, embedding, model, object, embedding_index, prompt_tokens, total_tokens)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                embedding = VALUES(embedding),
                model = VALUES(model),
                object = VALUES(object),
                embedding_index = VALUES(embedding_index),
                prompt_tokens = VALUES(prompt_tokens),
                total_tokens = VALUES(total_tokens)
            """, (
                product_id,
                embedding_combined_str,  # Use the JSON string instead of the list of embeddings
                embedding_combined['model'],
                'combined',
                embedding_combined['data'][0]['index'],
                embedding_combined['usage']['prompt_tokens'],
                embedding_combined['usage']['total_tokens'],
            ))

    #   Commit transaction
        cursor.execute("COMMIT")
        print("Embeddings data inserted or updated successfully.")

    except mysql.connector.Error as error:
        print("Error inserting or updating embeddings data: ", error)
    #   Rollback transaction in case of an error
        cursor.execute("ROLLBACK")

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        print("Database connection closed.")

def get_all_messages(chat_id):
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")
        return []

    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT messages FROM chat_messages WHERE chat_id=%s", (chat_id,))
        results = cursor.fetchone()
        
        if results:
            messages = json.loads(results[0])
        else:
            messages = []
    except mysql.connector.Error as err:
        print("Error executing query:", err)
        messages = []

    cursor.close()
    connection.close()

    return messages
