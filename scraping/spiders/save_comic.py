
import requests
import json

from scraping.spiders.env import envLocal, envServer


def save_comic(item):

    genres = list(map(lambda x: x['genre'], item["genres"]["create"]))

    if item.get("genres"):
        del item["genres"]

    variables = {
        "data": item,
        "genres": genres
    }

    variables = json.dumps(variables)

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'http://localhost:4000',
    }

    data = '{"query":"mutation addComic($data: ComicCreateInput!, $genres: [String!]!) {\\n  createComic(data: $data, genres: $genres) {\\n    title\\n  }\\n}\\n","variables":' + variables + '}'

    response = requests.post(envServer,
                             headers=headers, data=data)

    return response
