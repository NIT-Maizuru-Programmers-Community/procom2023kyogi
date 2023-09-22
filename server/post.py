import requests

headers = {
    'Content-Type': 'application/json',
}

params = {
    'token': '1234',
}

json_data = {
    'turn': 1,
    'actions': [
        {
            'type': 1,
            'dir': 3,
        },
        {
            'type': 2,
            'dir': 1,
        },
    ],
}

response = requests.post('http://localhost:3000/matches/10', params=params, headers=headers, json=json_data)
print(response)