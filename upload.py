import argparse
import requests
import logging
import os
import sys

token = None
password = None

def account_id():
    """
    Return your account ID that is necessary to all others steps when using
    the Livestream API

    You must to set the variables token and password correctly to work correctly

    To get the API token just access https://livestream.com/developers/api
    """
    url = "https://livestreamapis.com/v3/accounts"
    response = requests.get(url, auth=(token, password))
    if response.status_code != 200:
        sys.exit(logging.error("Error to access {} using {}:{} credentials".format(url, token, password)))
    return response.json()[0]["id"]

def events():
    """
    List all availables events on your account.

    This information is needed to upload a video.
    """
    url = "https://livestreamapis.com/v3/accounts/{}/upcoming_events".format(account_id())
    response = requests.get(url, auth=(token, password))
    return [event["id"] for event in response.json()["data"]]

def upload(filename, caption, event_id):
    """
    Livestreaming API has 3 steps to send a video according to its documentation
    https://livestream.com/developers/docs/api/#video-object

    1. You need to get server URL
    2. You need to send the video file as a binary
    3. You need to post the claimId get in the last step to the video previously sended

    All steps are implemented below and commented to show de process
    """
    # 1st step: You need to get server URL
    url = "https://livestreamapis.com/v3/accounts/{}/events/{}/videos/upload_metadata".format(account_id(), event_id)
    response = requests.get(url, auth=(token, password))
    upload_url = response.json()["server"]

    # 2nd step: You need to send the video file as a binary
    data = open(filename, "rb").read()
    headers = { "Content-Type": "application/octet-stream" }
    response = requests.post(upload_url, auth=(token, password), data=data, headers=headers)

    # 3rd step: You need to to post claimId to the video previously sended
    claim_id = response.json()["data"]["id"]
    url = "https://livestreamapis.com/v3/accounts/{}/events/{}/videos".format(account_id(), event_id)
    data = {
        "caption": caption,
        "claimId": claim_id,
    }
    response = requests.post(url, auth=(token, password), data=data)
    return response.json()

def main():
    if not token or not password:
        sys.exit(logging.error("You must to set your token and password!"))

    parser = argparse.ArgumentParser()
    parser.add_argument("--event_id", type=int, choices=events(), required=True)
    parser.add_argument("--video", required=True)
    parser.add_argument("--caption")

    filename = str(parser.parse_args().video)
    if not os.path.exists(filename):
        sys.exit(logging.error("{} not found".format(filename)))

    caption = str(parser.parse_args().caption)
    event_id = str(parser.parse_args().event_id)

    return upload(filename, caption, event_id)

if __name__ == "__main__":
    print(main())
