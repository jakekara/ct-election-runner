import requests


def get_url(url):
    resp = requests.get(url, headers={"user-agent": "election-runner"})

    if resp.status_code != 200:
        raise Exception(f"Error fetching '{url}': {resp.status_code}")

    return resp


def get_json(url):
    resp = get_url(url)

    try:
        return resp.json()
    except Exception as e:
        raise Exception(f"Error fetching JSON from '{url}")
