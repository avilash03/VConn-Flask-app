import torch
from transformers import AutoTokenizer, AutoModel
import mysql.connector
import numpy as np
from dotenv import load_dotenv
import os
# Load environment variables from .env
load_dotenv()
# Replace with your model and database information
model_name = "bert-base-uncased"
embeddings_db_host =os.environ.get("embeddings_db_host")
embeddings_db_user = os.environ.get("embeddings_db_user")
embeddings_db_password = os.environ.get("embeddings_db_password")
embeddings_db_database = os.environ.get("embeddings_db_database")

# Load the Hugging Face model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Establish a connection to the database
conn = mysql.connector.connect(
    host=embeddings_db_host,
    user=embeddings_db_user,
    password=embeddings_db_password,
    database=embeddings_db_database
)
cursor = conn.cursor()

def text_to_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # Assuming mean pooling
    return embeddings[0].tolist()

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity

def vector_search(input_text, threshold=0.7, top_n=10):
    input_embedding = text_to_embedding(input_text)

    query = """
    SELECT content, embedding
    FROM hostel_embeddings
    """

    cursor.execute(query)
    results = cursor.fetchall()

    matching_results = []

    while threshold >= 0.1:
        for result in results:
            content, embedding_blob = result
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            similarity = cosine_similarity(input_embedding, embedding)

            if similarity > threshold:
                matching_results.append((content, similarity))

        if len(matching_results) > 0:
            break

        threshold -= 0.1

    # Sort the results by similarity in descending order and take the top 'n' results
    matching_results.sort(key=lambda x: x[1], reverse=True)
    matching_results = matching_results[:top_n]

    return matching_results


if __name__ == "__main__":
    input_text = "3 BCE before 11pm"
    threshold = 0.9

    results = vector_search(input_text, threshold)

    for content, similarity in results:
        print(f"Content: {content}")

    cursor.close()
    conn.close()