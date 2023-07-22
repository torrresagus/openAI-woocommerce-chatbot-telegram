import tensorflow as tf
import numpy as np
import json
from open_ai.embedding_utils import get_embedding
from . import mysql_connection

def parse_embedding(embedding_text):
    # Convert the text embedding into a numeric vector
    embedding_array = json.loads(embedding_text)
    embedding_vector = np.array(embedding_array, dtype=np.float32)
    return embedding_vector

def cosine_similarity(a, b):
    # Calculate the cosine similarity between two vectors
    a = tf.reshape(a, (1, -1))  # Reshape to ensure both vectors have the same shape
    b = tf.reshape(b, (1, -1))
    a = tf.linalg.l2_normalize(a, axis=-1)
    b = tf.linalg.l2_normalize(b, axis=-1)
    cos_sim = tf.reduce_sum(tf.multiply(a, b), axis=-1)
    return cos_sim

def search_reviews(cursor, query, n=3):
    # Get the embeddings, id, and product_id from the table
    cursor.execute("SELECT id, product_id, embedding FROM embeddings LIMIT 50")
    rows = cursor.fetchall()

    query_embedding = get_embedding(query)  # Get the embedding of the query
    query_embedding = query_embedding['data'][0]['embedding']
    
    results = []

    for row in rows:
        id_, product_id, embedding_text = row
        embedding = parse_embedding(embedding_text)
        similarity = cosine_similarity(embedding, query_embedding).numpy()[0]
        if similarity >= 0.75:
           results.append((similarity, embedding, id_, product_id))

    # Sort the results by similarity in descending order
    results.sort(reverse=True, key=lambda x: x[0])

    # Return the top n results
    top_results = results[:n]

    return top_results

def products(query):
    connection = mysql_connection.create_connection()
    if connection is None:
        print("Error connecting to the database.")

    # Create a cursor
    cursor = connection.cursor()

    results = search_reviews(cursor, query, n=3)

    # Print the results
    for similarity, embedding, id_, product_id in results:
        print(f'ID: {id_}, Product ID: {product_id}, Similarity: {similarity}, Embedding: {embedding}')
        
    # Get the Product IDs from the results
    product_ids = [product_id for _, _, _, product_id in results]

    # Create the SQL query to fetch the products
    sql_query = f"SELECT * FROM products WHERE ID IN ({','.join(map(str, product_ids))})"

    # Execute the SQL query
    cursor.execute(sql_query)

    # Get the results of the query
    product_results = cursor.fetchall()

    return product_results