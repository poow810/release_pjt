import os
import django
import requests
import json
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
TMDB_API_KEY = settings.TMDB_API_KEY
django.setup()



# url = f"https://api.themoviedb.org/3/movie/3/credits?api_key={TMDB_API_KEY}&language=en-US"

# headers = {
#     "accept": "application/json",
# }

# response = requests.get(url, headers=headers)

def get_movie_detail(movie_id):
    request_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR'
    response = requests.get(request_url)
    if response.status_code == 200:
        credits = response.json()
        
        # 배우 정보 추출 (최대 5명)
        cast = credits.get('cast', [])
        actors = [{'name': actor['name'], 'character': actor['character']} for actor in cast[:5]]
        
        # 감독 정보 추출
        crew = credits.get('crew', [])
        directors = [member['name'] for member in crew if member['job'] == 'Director']
        
        return {
            'actors': actors,
            'directors': directors
        }
    else:
        return {
            'actors': [],
            'directors': []
        }

def get_movie_datas():
    total_data = []
    a = 0
    for i in range(1, 401):
        a += 1
        print(a)
        request_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=ko-KR&sort_by=popularity.desc&include_adult=false&include_video=false&page={i}&with_watch_providers=providers%3A8&with_watch_monetization_types=flatrate'
        movies = requests.get(request_url).json()

        for movie in movies['results']:
            if movie.get('release_date', ''):
                data = {
                    'movie-id': movie['id'],
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_avg': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'genres': movie['genre_ids']
                }
                
                # 영화의 배우 및 감독 정보 추가
                details = get_movie_detail(movie['id'])
                data.update(details)

                total_data.append(data)

    json_data = {
        'name': 'movie data',
        'data': total_data  
    }

    with open("movie_data.json", "w", encoding="utf-8") as w:
        json.dump(json_data, w, indent="\t", ensure_ascii=False) 

def get_movie(request):
    get_movie_datas()


