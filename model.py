from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def remove_stopwords(line):
    words = line.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# Load the data into a DataFrame
file_path = './emails.csv'
df = pd.read_csv(file_path)

# Preprocess the text in the DataFrame
df['Content'] = df['Content'].apply(lambda line: re.sub(r'http\S+', '', line.strip()))
df['Content'] = df['Content'].apply(remove_stopwords)

# Encode the sentences
embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
corpus_embeddings = embedder.encode(df['text'].tolist())

# Perform K-Means clustering
num_clusters = 5
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(corpus_embeddings)
cluster_assignment = clustering_model.labels_
df['cluster'] = cluster_assignment

# Group sentences by cluster
clustered_sentences = df.groupby('cluster')['Content'].apply(list)

# Convert the clustered sentences into separate documents for TF-IDF analysis
clustered_documents = [' '.join(cluster) for cluster in clustered_sentences]

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the clustered documents
tfidf_matrix = tfidf_vectorizer.fit_transform(clustered_documents)

# Get the feature names (words) from the TF-IDF vectorizer
feature_names = tfidf_vectorizer.get_feature_names_out()

# For each cluster, find the top N keywords
num_keywords = 5  # You can adjust this value as needed
cluster_labels = []

for i, cluster_matrix in enumerate(tfidf_matrix):
    feature_index = cluster_matrix.toarray().argsort()[:, -num_keywords][0]
    cluster_keywords = [feature_names[idx] for idx in feature_index]
    cluster_labels.append(cluster_keywords)

# Print the cluster labels
for i, labels in enumerate(cluster_labels):
    print(f"Cluster {i + 1} - Labels: {', '.join(labels)}")
