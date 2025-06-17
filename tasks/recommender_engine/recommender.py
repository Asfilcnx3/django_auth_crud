from huggingface_hub import hf_hub_download
import numpy as np
import pickle
import faiss

## Load data only one time
Embeddings = None
Title_List = None
Faiss_Index = None

# Load dataset and data one
def load_model_once():
    global Embeddings, Title_List, Faiss_Index

    if Embeddings is None or Title_List is None or Faiss_Index is None:

    # Download embeddings from Hugging Face
        file_path = hf_hub_download(
            repo_id="asfilcnx3/embeddings_created",
            filename="embeddings.npy",
            repo_type='dataset'
        )

        Embeddings = np.load(file_path)

        # Open the titles.pkl
        with open("tasks/recommender_engine/titles.pkl", "rb") as f:
            Title_List = pickle.load(f)

        # FAISS setup
        dimension = Embeddings.shape[1]
        Faiss_Index = faiss.IndexFlatL2(dimension)
        Faiss_Index.add(Embeddings)

def get_index_from_title(title_query):
    """
    This function return the index of the name of the input title query if exists on the titles.pkl

    input:
        title_query(str): A word or group of words from a movie name
        titles_list(list): List of the titles inside the embeddings
    
    output:
        index(int): The index of the title_query inside the list of titles
    """
    try:
        return Title_List.index(title_query)
    except ValueError:
        return None

def recommend_by_title(title_query):
    """
    This function normalize the title_query with 'lower', then call the function 'get_index_from_title' with the normalized title query as a input, if the another function return a 'None' this function returns a str, if the function return a index, the funcion start to find the embedding index with faiss, then return the first 5 similar movies.

    input:
        title_query(str): The function expect a str as the input that references a movie title

    output:
        similar_titles(list): Return the first 5 titles of movies with similar embedding index.
    """
    load_model_once()

    title_query = title_query.lower().strip()
    idx = get_index_from_title(title_query)
    if idx is None:
        return ["Movie not found. Please check the title and try again."]

    _, idxs = Faiss_Index.search(Embeddings[idx:idx+1], 6)
    similar_titles = [Title_List[i] for i in idxs[0] if i != idx]
    return similar_titles[:5]