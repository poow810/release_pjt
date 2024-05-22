import json
import os
import django
import openai
from django.conf import settings
from openai import OpenAI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
client = OpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_API_KEY,
)
django.setup()

from movie.models import Genre, Movie, Person

def translate_to_korean(text):
    try:
        request_message = f"Translate the following text to Korean, providing only the Korean pronunciation if the text is an English name. If text is already Korean, please return Korean text: '{text}'"
        chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": request_message
            }
        ],
        model="gpt-3.5-turbo",
        )
        print(chat_completion)
        # 수정된 부분: 응답 구조에 맞게 접근
        translated_text = chat_completion.choices[0].message.content.strip()
        
        if translated_text:
            return translated_text
        else:
            return text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text


def load_and_process_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        for movie_data in data['data']:
            movie, created = Movie.objects.get_or_create(
                movie_id=movie_data["movie-id"], # 수정된 필드 이름
                defaults={
                    'title': movie_data['title'],
                    'release_date': movie_data['released_date'],
                    'popularity': movie_data['popularity'],
                    'vote_avg': movie_data['vote_avg'],
                    'overview': movie_data['overview'],
                    'poster_path': movie_data['poster_path'],
                }
            )

            genre_instances = []
            for genre_id in movie_data['genres']:
                genre, _ = Genre.objects.get_or_create(id=genre_id)
                genre_instances.append(genre)

                # Movie 인스턴스와 Genre 인스턴스 연결
                # 만약 영화가 새로 생성된 경우 또는 장르를 업데이트하고 싶은 경우
                movie.genres.set(genre_instances)
            
            for director in movie_data['directors']:
                Person.objects.create(
                    movie=movie,
                    type='director',
                    name_en=director,
                    name_kr=translate_to_korean(director)  
                )
                
            for actor in movie_data['actors']:
                Person.objects.create(
                    movie=movie,
                    type='actor',
                    name_en=actor['name'],
                    name_kr=translate_to_korean(actor['name'])
                )

if __name__ == "__main__":
    json_file_path = 'example.json'
    load_and_process_data(json_file_path)


# import json
# import os
# import django
# import openai
# from django.conf import settings
# from openai import OpenAI



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# client = OpenAI(
#     api_key=settings.OPENAI_API_KEY,
# )
# django.setup()

# def translate_to_korean(text):
#     try:
#         request_message = f"Translate the following text to Korean, providing only the Korean pronunciation if the text is an English name. If text is already Korean, please return Korean text: '{text}'"
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": request_message
#                 }
#             ],
#             model="gpt-3.5-turbo",
#         )
#         translated_text = chat_completion.choices[0].message.content.strip()
#         print(translated_text)
#         if translated_text:
#             return translated_text
#         else:
#             return text
#     except Exception as e:
#         print(f"Translation failed: {e}")
#         return text


# def load_and_process_data(json_file_path, output_file_path):
#     try:
#         with open(json_file_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)
#             processed_data = []

#             for movie_data in data['data']:
#                 processed_movie = {
#                     'movie_id': movie_data["movie-id"], 
#                     'title': movie_data['title'],
#                     'release_date': movie_data['released_date'],
#                     'popularity': movie_data['popularity'],
#                     'vote_avg': movie_data['vote_avg'],
#                     'overview': movie_data['overview'],
#                     'poster_path': movie_data['poster_path'],
#                     'genres': movie_data['genres'],
#                     'directors': [],
#                     'actors': []
#                 }

#                 for director in movie_data['directors']:
#                     translated_director = {
#                         'name_en': director,
#                         'name_kr': translate_to_korean(director)
#                     }
#                     processed_movie['directors'].append(translated_director)
                    
#                 for actor in movie_data['actors']:
#                     translated_actor = {
#                         'name_en': actor['name'],
#                         'name_kr': translate_to_korean(actor['name'])
#                     }
#                     processed_movie['actors'].append(translated_actor)

#                 processed_data.append(processed_movie)
            
#             with open(output_file_path, 'w', encoding='utf-8') as outfile:
#                 json.dump({'data': processed_data}, outfile, ensure_ascii=False, indent=4)
#     except Exception as e:
#         print('error')

# if __name__ == "__main__":
#     input_json_file_path = 'example.json'
#     output_json_file_path = 'movie_processing.json'
#     load_and_process_data(input_json_file_path, output_json_file_path)
