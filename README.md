# Movie Recommender + Django Auth & CRUD
A full-stack web application built with Django that combines user authentication, full CRUD functionality, and a movie recommendation system powered by embeddings.

# Usefull Links
- [Live Demo](https://django-auth-crud-c60l.onrender.com)
- [Embedded Dataset](https://huggingface.co/datasets/asfilcnx3/embeddings_created)
- [NLP Dataset](https://huggingface.co/datasets/asfilcnx3/clean-embedding-movies)
- [Free Deploy](https://dashboard.render.com/login)

# What does this project do?
>- Allows users to register, log in, and log out
>- Includes full CRUD operations for managing movies
>- Features a movie recommender system based on text embeddings and semantic similarity using FAISS
>- Efficiently loads large files from Hugging Face Datasets (no Git LFS required!)
>- Clean UI with Bootstrap 5

# Tech Stack
>- Django – Web framework (Auth + CRUD)
>- Python – Backend logic + embeddings handling
>- FAISS – Fast Approximate Nearest Neighbor Search
>- Hugging Face Datasets – For loading precomputed embeddings
>- Bootstrap 5 – For frontend styling
>- Render / GitHub Pages – Deployment

# Local Installation (On Windows)
>- git clone https://github.com/Asfilcnx3/django_auth_crud.git
>- cd django_auth_crud
>- py -m venv venv
>- source venv\Scripts\activate
>- pip install -r requirements.txt
>- python manage.py migrate
> python manage.py runserver
(Make sure to configure environment variables if you're using a .env file.)

# 09/06/2025 update
## Adding "Recommendation System with Embeddings"
### How the Recommender Works
- Movie titles are embedded as text vectors using a language model
- These vectors are indexed using FAISS for fast similarity search
- Instead of storing large .npy files in the repo, we host them on Hugging Face and load them at runtime

# Authentication
>> User authentication is handled via Django
>> Only authenticated users can access the movie CRUD and recommender system
