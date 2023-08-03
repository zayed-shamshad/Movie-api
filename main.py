from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import requests
import os
import logging
from flask_restful import Resource, Api
from load_data import Movie_Recommender
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Movie_Recommender
Recommender = Movie_Recommender()
Recommender.clean()
Recommender.prepare()

app = Flask(__name__)
api = Api(app)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variable
API_KEY = os.environ.get("TMDB_API_KEY")
if not API_KEY:
    logger.error("TMDB_API_KEY environment variable not set")
    exit(1)

class Movie(Resource):
    def get(self):
        try:
            info = []  # Initialize as a list
            query_param = request.args.get("s")
            if not query_param:
                return {'message': 'Missing "s" query parameter'}, 400
            result_list = Recommender.recommend(query_param)
            for movie_name in result_list:
                url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                }

                r = requests.get(url, headers=headers)
                logger.info(f"API call for '{movie_name}' - Status code: {r.status_code}")

                if r.status_code == 200:
                    data = r.json()
                    if data['results']:
                        # Extract necessary information from the API response
                        movie_info = {
                            'id': data['results'][0]['id'],  # Use this ID to get more information about the movie
                            'title': data['results'][0]['title'],
                            'poster_path': f"http://image.tmdb.org/t/p/w500/{data['results'][0]['poster_path']}",
                            'overview': data['results'][0]['overview']
                        }
                        info.append(movie_info)
                    else:
                        logger.warning(f"No results found for movie: {movie_name}")
                else:
                    logger.error(f"Error occurred for movie: {movie_name}")

            return make_response(jsonify(info), 200)

        except Exception as e:
            logger.exception(f"An error occurred while processing the request: {e}")
            return {'message': 'An error occurred during processing the request'}, 500

class Status(Resource):
    def get(self):
        return {'data': 'API is Running'
                
                }
class Movie_Trending(Resource):
    def get(self):
        url = f"https://api.themoviedb.org/3/trending/movie/day"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        r = requests.get(url, headers=headers)
        logger.info(f"API call for Trending' - Status code: {r.status_code}")

        if r.status_code == 200:
            return make_response(jsonify(r.json()), 200)
        else:
            logger.error(f"Error occurred for Trending")
            return {'message': 'An error occurred during processing the request'}, 500
class Movie_Upcoming(Resource):
    def get(self):
        url = f"https://api.themoviedb.org/3/movie/upcoming"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        r = requests.get(url, headers=headers)
        logger.info(f"API call for Trending' - Status code: {r.status_code}")

        if r.status_code == 200:
            return make_response(jsonify(r.json()), 200)
        else:
            logger.error(f"Error occurred for Trending")
            return {'message': 'An error occurred during processing the request'}, 500

class Movie_Nowplaying(Resource):
    def get(self):
        url = f"https://api.themoviedb.org/3/movie/now_playing"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        r = requests.get(url, headers=headers)
        logger.info(f"API call for Trending' - Status code: {r.status_code}")

        if r.status_code == 200:
            return make_response(jsonify(r.json()), 200)
        else:
            logger.error(f"Error occurred for Trending")
            return {'message': 'An error occurred during processing the request'}, 500
class Movie_Toprated(Resource):
    def get(self):
        url = f"https://api.themoviedb.org/3/movie/top_rated"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        r = requests.get(url, headers=headers)
        logger.info(f"API call for Trending' - Status code: {r.status_code}")

        if r.status_code == 200:
            return make_response(jsonify(r.json()), 200)
        else:
            logger.error(f"Error occurred for Trending")
            return {'message': 'An error occurred during processing the request'}, 500
class Movie_trailer(Resource):
    def get(self):
        id=request.args.get("id")
        url = f"https://api.themoviedb.org/3/movie/{id}+/videos"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        r = requests.get(url, headers=headers)
        logger.info(f"API call for Trending' - Status code: {r.status_code}")

        if r.status_code == 200:
            return make_response(jsonify(r.json()), 200)
        else:
            logger.error(f"Error occurred for Trending")
            return {'message': 'An error occurred during processing the request'}, 500
class Movie_data(Resource):
    def get(self):
        movie_id=request.args.get("movie_id")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        r = requests.get(url, headers=headers)
        logger.info(f"API call for Trending' - Status code: {r.status_code}")

        if r.status_code == 200:
            return make_response(jsonify(r.json()), 200)
        else:
            logger.error(f"Error occurred for Trending")
            return {'message': 'An error occurred during processing the request'}, 500
        

api.add_resource(Movie, '/movie')
api.add_resource(Status, '/')
api.add_resource(Movie_Trending,'/trending')
api.add_resource(Movie_Upcoming,'/upcoming')
api.add_resource(Movie_Nowplaying,'/nowplaying')
api.add_resource(Movie_Toprated,'/toprated')
api.add_resource(Movie_trailer,'/trailer')
api.add_resource(Movie_data,'/movie_data')


if __name__ == "__main__":
    # Start the Flask app
    app.run()
