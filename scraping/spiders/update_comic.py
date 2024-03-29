
import requests
import json

from scraping.spiders.env import  envServer


def update_comic(item):

    variables = item

    variables = json.dumps(variables)

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'http://localhost:4000',
    }

    data = '{"query":"mutation UpdateComic($data: ComicUpdateInput!, $where: ComicWhereUniqueInput!) {\\n  updateComic(data: $data, where: $where) {\\n    title\\n  }\\n}\\n","variables":' + variables + '}'

    response = requests.post(envServer,
                             headers=headers, data=data)

    return response
