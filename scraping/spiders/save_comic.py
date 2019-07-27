
import requests
import json


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

    data = '{"query":"mutation addComic($data: ComicCreateInput!) {\\n  createComic(data: $data) {\\n    id\\n  }\\n}\\n","variables":' + variables + '}'

    response = requests.post('http://localhost:4466/',
                             headers=headers, data=data)

    return response
