# OpenAI + WooCommerce API

## Overview

This repository contains a project that combines the power of OpenAI's language model and the WooCommerce API to create an intelligent customer service assistant for an online store. The assistant is designed to interact with customers, provide product information, and offer personalized responses, enhancing the overall shopping experience.

## Workflow

The workflow of the project can be summarized as follows:

1. **Customer Query**: The customer sends a query or message to the customer service assistant via a chat interface.

2. **Input Moderation**: The customer query is first checked using the OpenAI Moderation API to ensure it meets the required standards. If the input is flagged, the assistant responds with an appropriate message, and the conversation ends.

3. **Product Search**: The assistant processes the user query to extract relevant keywords and context. It then performs a similarity search using cosine similarity to find the most relevant products from the WooCommerce API.

4. **Response Generation**: The assistant generates a friendly and informative response to the customer's query. The response includes information about the products that match the customer's needs.

5. **Output Moderation**: The generated response is checked again using the OpenAI Moderation API to ensure it complies with content guidelines. If the response is flagged, the assistant provides a polite message indicating that it cannot provide certain information.

6. **User Feedback**: The assistant asks the user if the response sufficiently answers their question. If the user approves the response, it is provided as the final answer. If not, the assistant offers to connect the user to a human agent for further assistance.

## Product Search with Embeddings

The project leverages word embeddings to convert textual input, such as customer queries, into numerical representations. These embeddings capture the semantic meaning and context of the words, enabling the assistant to find relevant products based on the customer's query.

### Parsing Embeddings

The code in `embedding_utils.py` includes functions for parsing text embeddings into numeric vectors. The `parse_embedding` function takes a text-based embedding representation, converts it into a numeric vector, and returns the resulting embedding vector.

### Cosine Similarity

To measure the similarity between two embedding vectors, the `cosine_similarity` function is used. This function calculates the cosine similarity between two vectors, which indicates how similar the vectors are in direction and magnitude.

### Search Reviews and Product Selection

The main functionality for product search is implemented in `search_reviews` from `mysql_connection.py`. Given a customer query, this function performs the following steps:

1. Retrieve the embeddings and corresponding product information from the database.
2. Calculate the cosine similarity between the query embedding and the embeddings of all products in the database.
3. Select the top N products with the highest similarity scores, where N is a specified number (in this case, N=3).

The results are sorted in descending order based on similarity scores to prioritize the most relevant products.

### Fetching Product Information

After identifying the top N products based on similarity, the code fetches additional information about these products from the database using the Product IDs obtained from the search results.

## OpenAI API and Cost Considerations

The project utilizes OpenAI's powerful language model, specifically the GPT-3.5 architecture, to generate contextually-aware responses. Please note that the use of the OpenAI API is not free and has associated costs. The cost varies depending on the number of queries, the length of text, and the complexity of the tasks performed. As the number of product descriptions to be embedded and the number of customer queries increase, the overall cost of using the API may also increase.

It is essential to monitor and manage API usage to optimize costs and ensure cost-effectiveness while providing excellent customer service.

## Implementation Options

There are two ways to implement the Telegram bot:

### Option 1: Webhooks

To use Webhooks, you need to set up a server that can receive incoming updates from Telegram and process them accordingly. In this project, we utilize Flask to create a simple server, and Ngrok is used to expose the local server to the internet. Webhooks are generally more efficient and recommended for production use.

To run the bot with Webhooks, follow these steps:

1. Set up a public URL using Ngrok and update the bot's webhook with that URL.
2. Run the Flask app on your server to handle incoming updates.

### Option 2: Polling

Polling is a simpler method to implement the bot. The bot continuously checks Telegram's server for new updates by sending requests at regular intervals. While this method is easier to set up, it may not be as efficient as Webhooks, especially for high-traffic bots.

To run the bot with Polling, follow these steps:

1. Run the Flask app on your server to handle incoming updates.
2. Use the Telegram bot library to continuously poll for new updates.

Choose the implementation method that best suits your needs and requirements.

## Contributing

Contributions to the project are welcome! If you have ideas, bug reports, or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
