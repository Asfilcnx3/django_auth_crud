from huggingface_hub import hf_hub_download
import numpy as np
import pickle
import faiss
from datasets import load_dataset

# Load dataset and data
# Download embeddings from Hugging Face
file_path = hf_hub_download(
    repo_id="asfilcnx3/embeddings_created",
    filename="embeddings.npy",
    repo_type='dataset'
)
embeddings = np.load(file_path)

with open("tasks/recommender_engine/titles.pkl", "rb") as f:
    titles_list = pickle.load(f)

# FAISS setup
dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embeddings)

def get_index_from_title(title_query, titles_list):
    try:
        return titles_list.index(title_query)
    except ValueError:
        return None

def recommend_by_title(title_query):
    title_query = title_query.lower().strip()
    idx = get_index_from_title(title_query, titles_list)
    if idx is None:
        return ["Movie not found. Please check the title and try again."]

    _, indices = faiss_index.search(embeddings[idx:idx+1], 6)
    similar_titles = [titles_list[i] for i in indices[0] if i != idx]
    return similar_titles[:5]