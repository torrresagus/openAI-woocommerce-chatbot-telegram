import os
from database.product_search_cosine_similarity import products
import database.database_operations as db
import openai
from . import user_to_embeding

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


openai.api_key  = os.environ['OPENAI_API_KEY']

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]

def process_user_message(user_input, all_messages, debug=True):
    delimiter = "```"
    
#   Step 1: Check input to see if it flags the Moderation API or is a prompt injection
    response = openai.Moderation.create(input=user_input)
    moderation_output = response["results"][0]

    if moderation_output["flagged"]:
        print("Step 1: Input flagged by Moderation API.")
        return "Sorry, we cannot process this request. Flagged by Moderation API."

    if debug: print("Step 1: Input passed moderation check.")
    
#   Step 2: Extract the list of products
    lista = user_to_embeding.getList(user_input)
    resultados_totales = []  # List to store results from all iterations
    for product in lista:
        product_list = products(product)
        resultados_totales.extend(product_list)  # Add the results of each iteration to the main list
        
    if debug: print("Step 2: Extracted list of products.")
    if debug: print("Step 3: Looked up product information.")

#   Step 4: Answer the user question
    system_message = """
    You are a customer service assistant in an online store. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask relevant follow-up questions to the user. \
    Given the information you have about the products, choose the most relevant one according to the query. \
    If the query has nothing to do with products, politely decline and state that you are an assistant for the store.
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{resultados_totales}"}
    ]

    final_response = get_completion_from_messages(all_messages + messages)
    if debug:print("Step 4: Generated response to user question.")
    all_messages = all_messages + messages[1:]

#   Step 5: Put the answer through the Moderation API
    response = openai.Moderation.create(input=final_response)
    moderation_output = response["results"][0]

    if moderation_output["flagged"]:
        if debug: print("Step 5: Response flagged by Moderation API.")
        return "Sorry, we cannot provide this information."

    if debug: print("Step 5: Response passed moderation check.")

#   Step 6: Ask the model if the response answers the initial user query well
    user_message = f"""
    Customer message: {delimiter}{user_input}{delimiter}
    Agent response: {delimiter}{final_response}{delimiter}

    Does the response sufficiently answer the question?
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    evaluation_response = get_completion_from_messages(messages)
    if debug: print("Step 6: Model evaluated the response.")

#   Step 7: If yes, use this answer; if not, say that you will connect the user to a human
    if "Y" in evaluation_response:  # Using "in" instead of "==" to be safer for model output variation (e.g., "Y." or "Yes")
        if debug: print("Step 7: Model approved the response.")
        return final_response, all_messages
    else:
        if debug: print("Step 7: Model disapproved the response.")
        neg_str = "I'm unable to provide the information you're looking for. Ask me again."
        return neg_str, all_messages

def chat_with_bot(user_input, chat_id):
    previous_messages = db.get_all_messages(chat_id)
    response, all_messages = process_user_message(user_input, previous_messages)
    
    # Guardar los mensajes actualizados en la base de datos
    db.save_chat_messages(chat_id, all_messages)  # Guarda el mensaje del usuario

    print("Chat ID:", chat_id)
    print("User input:", user_input)
    print("Bot response:", response)
    print("All messages:", all_messages)

    return response
