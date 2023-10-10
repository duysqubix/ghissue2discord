import requests
import json
import time

url = "http://localhost:8000/gopxl/webhook"


def test_open_issue():
    with open("issue_open.json") as f:
        payload = json.load(f)
    r = requests.post(url, json=payload)
    print(r.status_code)


def test_close_issue():
    with open("issue_close.json") as f:
        payload = json.load(f)

    r = requests.post(url, json=payload)
    print(r.status_code)


def main():
    test_open_issue()
    time.sleep(3)
    test_close_issue()


if __name__ == "__main__":
    main()
