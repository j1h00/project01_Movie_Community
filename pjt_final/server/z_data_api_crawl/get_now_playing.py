import requests
from pprint import pprint
import json

def get_movie_detail():
    API_KEY = 'a6ab9d9bd8cd66cb4f2a13186cf46926'
    API_URL = 'https://api.themoviedb.org/3/'

    result = []
    movie_for_recommendation = []
    
    crews_info = []
    keywords_info = []
    now_playing = []
    for page in range(1, 6):
        MOVIE_URL = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=ko-KR&page={page}"
        now_playing_res = requests.get(MOVIE_URL).json()
        
        for movie_results in now_playing_res['results']:
            now_playing.append(movie_results['id'])
    
    for movie_id in now_playing:

        MOVIE_URL = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=ko-KR"
        movie = requests.get(MOVIE_URL).json()

        if 'status_code' in movie.keys():
            pass
        
        crews_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=ko-KR'
        crew = requests.get(crews_url).json()

        trailer_url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=ko-KR'
        trailer = requests.get(trailer_url).json()
        trailer_key = ''

        if trailer['results']:
            trailer_key = trailer['results'][-1]['key']

        crews = []
        for i in crew['cast']:
            if i['known_for_department'] == 'Acting':
                crews_info.append({'model' : 'movies.crew', 'pk' : i['id'], 'fields' : {'name' : i['name'], 'role' : i['known_for_department'], 'profile_path' : i['profile_path']}})
                crews.append(i['id'])
        for i in crew['crew']:
            if i['job'] == 'Director':
                crews_info.append({'model' : 'movies.crew', 'pk' : i['id'], 'fields' : {'name' : i['name'], 'role' : i['job'], 'profile_path' : i['profile_path']}})
                crews.append(i['id'])

        KEYWORD_URL = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={API_KEY}&language=ko-KR"
        keywords_json = requests.get(KEYWORD_URL).json()

        keywords = []
        keywords_r = []
        if 'keywords' in keywords_json.keys():
            for keyword in keywords_json['keywords']:
                keywords.append(keyword['id'])
                keywords_info.append({
                    'model' : 'movies.keyword',
                    'pk': keyword['id'],
                    'fields': {
                        'name': keyword['name']
                    }
                })
                keywords_r.append(keyword['name'])
        
        genres = []
        genres_r = []
        if 'genres' in movie.keys():
            for genre in movie['genres']:
                genres.append(genre['id'])
                genres_r.append(genre['name'])
        
        result.append({
            "model": "movies.movie",
            "pk": movie['id'],
            "fields": {
                "title": movie['title'],
                "original_title": movie['original_title'],
                "backdrop_path": movie['backdrop_path'],
                "poster_path": movie['poster_path'],
                "overview": movie['overview'],
                "release_date": movie['release_date'],
                "adult": movie['adult'],
                "runtime": movie['runtime'],
                "production_countries": movie['production_countries'][0]['name'],
                "trailer_path": trailer_key,
                "genres": genres,
                "crews" : crews,
                "keywords": keywords,
            }
        })

    
        movie_for_recommendation.append({
            "id": movie['id'],
            "title": movie['title'],
            "original_title": movie['original_title'],
            "genres": genres,
            "keywords": keywords,
        })

    return result, crews_info, keywords_info, movie_for_recommendation


def main():
    now_playing_movies, crews_info, keywords_info, movie_for_recommendation = get_movie_detail()
    now_playing_movies.sort(key=lambda x: x['fields']['release_date'], reverse=True)
    
    with open('crews.json', 'w', encoding='UTF-8') as outfile:
        json.dump(crews_info, outfile, indent=4, ensure_ascii = False)

    with open('keywords.json', 'w', encoding='UTF-8') as outfile:
        json.dump(keywords_info, outfile, indent=4, ensure_ascii = False)
        
    with open('movies.json', 'w', encoding='UTF-8') as outfile:
        json.dump(now_playing_movies, outfile, indent=4, ensure_ascii = False)

    with open('movie_rec.json', 'w', encoding='UTF-8') as outfile:
        json.dump(movie_for_recommendation, outfile, indent=4, ensure_ascii = False)
main()
