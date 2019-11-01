# Livestream video upload example

This is **not** a Python library, but a simple example how to send a video to Livestream through its [API](https://livestream.com/developers/docs/api/#upload-video).

# Requirements

* Python 3
* Python PIP

### Installing dependencies

```
python3 -m pip install --upgrade requests
```

# Trying out

Fist of all, you must to set your API token and password into **upload.py** file.

```
token = "your token here"
password = "your password here"
```

When it has been set, you can run the code below to send a video to an event of your account.

```
python3 upload.py --event_id "your event_id"  --video sample.mp4 --caption "Title of the video here"
```

### Expected output

```
{'id': 198494830, 'draft': False, 'views': 0, 'likes': {'total': 0}, 'comments': {'total': 0}, 'caption': 'Title of the video here', 'description': None, 'duration': 0, 'eventId': 8433784, 'createdAt': '2019-11-01T10:55:24.044Z', 'publishAt': '2019-11-01T10:55:23.797Z', 'tags': [], 'thumbnailUrl': None, 'thumbnailUrlSmall': None, 'm3u8': None}
```
