from sklearn.cluster import KMeans
import numpy as np

from collections import Counter
from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the CSV data into a DataFrame
df = pd.read_csv('./emails.csv')

# Preprocess the text data
def preprocess_text(text):
    if isinstance(text, str):
        # Remove special characters and numbers
        text = re.sub(r'[^A-Za-z\s]', '', text)
        # Convert to lowercase
        text = text.lower()
    return text

df['Content'] = df['Content'].apply(preprocess_text)

# Load the pre-trained BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Function to convert text to BERT embeddings
def get_bert_embeddings(text):
    # Ensure that text is a string
    if not isinstance(text, str):
        text = str(text)

    # Tokenize the text
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)

    # Get BERT embeddings
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract the embeddings from the BERT model
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    
    return embeddings

# Apply BERT embeddings to the entire dataset
df['BERT_Embeddings'] = df['Content'].apply(get_bert_embeddings)



# Extract BERT embeddings and convert to numpy array
embeddings = np.array(df['BERT_Embeddings'].tolist())

# Determine the optimal number of clusters (you can customize this)
n_clusters = 5  # Adjust as needed

# Perform clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(embeddings)




cluster_word_counts = []

for cluster_id in range(n_clusters):
    cluster_data = df[df['Cluster'] == cluster_id]

    # Filter out rows with NaN values and non-string values
    cluster_data = cluster_data.dropna(subset=['Content'])
    cluster_data = cluster_data[cluster_data['Content'].apply(lambda x: isinstance(x, str))]

    # Join the filtered text
    cluster_text = ' '.join(cluster_data['Content'])
    words = cluster_text.split()
    word_counts = Counter(words)
    cluster_word_counts.append(word_counts)

# Find the most common words in each cluster
for cluster_id, word_counts in enumerate(cluster_word_counts):
    common_words = word_counts.most_common(10)  # Change 10 to the number of top words you want to display
    print(f"Cluster {cluster_id} - Top Words:")
    for word, count in common_words:
        print(f"{word}: {count}")


# Visualize the most common words in each cluster
for cluster_id, word_counts in enumerate(cluster_word_counts):
    common_words = word_counts.most_common(10)  # Change 10 to the number of top words you want to display
    words, counts = zip(*common_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title(f"Cluster {cluster_id} - Top Words")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.show()
