import json

# JSON 파일을 열어 데이터를 불러옵니다.
with open('example.json', 'r', encoding='utf-8') as f:
    input_data = json.load(f)

def load_and_process_data(json_file_path, output_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            processed_data = []

            for movie_data in data['data']:
                processed_movie = {
                    'model': 'movie.Movie',
                    'fields': {
                        'movie_id': movie_data['movie-id'],
                        'title': movie_data['title'],
                        'release_date': movie_data['released_date'],
                        'popularity': movie_data['popularity'],
                        'vote_avg': movie_data['vote_avg'],
                        'overview': movie_data['overview'],
                        'poster_path': movie_data['poster_path'],
                        'genres': movie_data['genres'],
                        'likes': 0,
                        'directors': [],
                        'actors': []
                    }
                }

                for director in movie_data['directors']:
                    translated_director = {
                        'name_en': director,
                        'name_kr': '김씨'
                    }
                    processed_movie['fields']['directors'].append(translated_director)
                    
                for actor in movie_data['actors']:
                    translated_actor = {
                        'name_en': actor['name'],
                        'name_kr': '김씨'
                    }
                    processed_movie['fields']['actors'].append(translated_actor)

                processed_data.append(processed_movie)

            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                json.dump(processed_data, outfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    input_json_file_path = 'example.json'
    output_json_file_path = 'converted_data.json'
    load_and_process_data(input_json_file_path, output_json_file_path)