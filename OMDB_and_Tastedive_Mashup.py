import requests
import requests_with_caching
import json

def get_movies_from_tastedive(name):
    baseurl = "https://tastedive.com/api/similar"
    parameters = {'q':name,'type':'movies','limit':'5'}
    resp = requests_with_caching.get(baseurl, params = parameters)
    return (resp.json())

def extract_movie_titles(resultsdic):
    return([i['Name'] for i in resultsdic['Similar']['Results']])
    
def get_related_titles(movie_list):
    new_list1=[]
    new_list2=[]
    for movie_title in movie_list:
        new_list1 = (extract_movie_titles(get_movies_from_tastedive(movie_title)))
        for title in new_list1:
            if title not in new_list2:
                new_list2.append(title)
    return(new_list2)

def get_movie_data(name):
    baseurl = 'http://www.omdbapi.com/'
    parameters = {'t':name, 'r':'json'}
    resp = requests_with_caching.get(baseurl, params=parameters)
    return (resp.json())

def get_movie_rating(movie_data):
    rating=""
    for typelist in movie_data['Ratings']:
        if typelist['Source']== "Rotten Tomatoes":
            rating = typelist["Value"]
    if rating != "":
        rating = int(rating[:2])
    else: rating = 0
    return rating

def get_sorted_recommendations(movie_list):
    movie_list = get_related_titles(movie_list)
    movie_list = sorted(movie_list, key = lambda name: (get_movie_rating(get_movie_data(name)), name), reverse = True)
    return movie_list
