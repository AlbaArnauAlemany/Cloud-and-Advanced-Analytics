# -*- coding: utf-8 -*-
"""Lab_1_Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OAYfE194p7jXLtYnGX-f8cFwhtxVsVb7

# **Lab 1: APIs, Google Cloud Functions, Docker and cloud Run:**

---

# **Exercise 2: Google Cloud Functions:**

- **0.** Check to see that the API key works correctly
- **1.** Write a function on GCP in Python
- **2.** Call the function from a Notebook (either in Colab or in Jupyter).

## **0. Check to see that the API key works correctly**

**Goal**: The goal of these two functions are to:
- **Function 1:** Fetch a list of movies
- **Function 2:** Fetch the poster of a specific movie ID
"""

api_key = 'YOUR_API_KEY'
r = requests.get('https://api.themoviedb.org/3/movie/464052?api_key=' + api_key)
obj = json.loads(r.text)
movie_name = obj['title']
print(movie_name)

"""## **1. Write two functions on GCP in Python**

### **Function 1:** Fetch a list of movies

**Note:** The same code can be used on Google Cloud, you just need to modify the three following lines:
- Add: import functions_framework
- Add: @functions_framework.http
- Add: request to the function: def get_movie_titles(request):

You should also add in the requirements.txt the two following libraries:
- functions-framework==3.*
- requests==2.31.0
"""

#import functions_framework
import requests
from flask import jsonify

# @functions_framework.http
def get_movie_titles(): # request
    try:
        movie_database_url = 'https://api.themoviedb.org/3/discover/movie'
        api_key = 'YOUR_API_KEY'

        response = requests.get(movie_database_url, params={'api_key': api_key, 'page': 1})

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Check if there are results
        if 'results' in data and data['results']:
            # Filter movies that have a poster path
            movies_with_poster = [movie for movie in data['results'] if 'poster_path' in movie]

            movie_details = [{'title': movie['title'], 'id': movie['id']} for movie in movies_with_poster]

            # Return a JSON response with the list of movie details
            return {'movie_details': movie_details}
        else:
            return {'error': 'No results found.'}, 404
    except requests.RequestException as e:
        # Log the error details
        print(f"Error making API request: {e}")
        return 'Internal Server Error', 500
    except requests.exceptions.HTTPError as e:
        # Log the HTTP error details
        print(f"HTTP Error: {e}")
        return 'Internal Server Error', 500
    except json.JSONDecodeError as e:
        # Log the error details
        print(f"Error decoding JSON response: {e}")
        return 'Internal Server Error', 500

# Call the function and print the result
result = get_movie_titles()
result

"""### **Function 2:** Fetch the poster of a specific Movie

#### **Main.py**
"""

import functions_framework
from flask import jsonify
import requests

api_key = 'YOUR_API_KEY'


@functions_framework.http
def get_movie_details(request):
    try:
        # Extract the movie ID from the request parameters
        movie_id = request.args.get('movie_id')

        # Make the API request using the provided movie ID
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the JSON response
        obj = response.json()

        poster_path_prefix = 'https://image.tmdb.org/t/p/w1280/'
        poster_path = f"{poster_path_prefix}{obj.get('poster_path')}"


        # Return a JSON response with the movie details
        response_data = {'movie_name': obj["title"], 'movie_poster': poster_path}
        return jsonify(response_data)
    except requests.RequestException as e:
        # Log the error details
        print(f"Error making API request: {e}")
        return 'Internal Server Error', 500
    except requests.exceptions.HTTPError as e:
        # Log the HTTP error details
        print(f"HTTP Error: {e}")
        return 'Internal Server Error', 500
    except json.JSONDecodeError as e:
        # Log the error details
        print(f"Error decoding JSON response: {e}")
        return 'Internal Server Error', 500

"""#### Requirements.txt

- functions-framework==3.*
- requests==2.31.0

## **2. Deploy the function on Google Cloud Platform**

## **3. Call the function from a Notebook (either in Colab or in Jupyter)**
"""

# Testing function 1:
r = requests.get('YOUR_URL')
obj = json.loads(r.text)
print(obj)


# Testing function 2:
movie_id = '933131'
r = requests.get(f'YOUR_URL?movie_id={movie_id}')
obj = json.loads(r.text)
print(obj)