
import requests
import json


def save_comic(item):

    variables = {
        "data": item
    }

    variables = json.dumps(variables)

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'http://localhost:4466',
    }

    data = '{"query":"mutation addComic($data: ComicCreateInput!) {\\n  createComic(data: $data) {\\n    id\\n  }\\n}\\n","variables":' + variables + '}'

    response = requests.post('http://localhost:4466/',
                             headers=headers, data=data)

    return response
