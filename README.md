Basic Twitter OAuth Token Collector
===================================

A web interface for collecting Twitter oauth access tokens from your account or your friends' accounts for prototyping purposes.

Why?
----
The Twitter REST/Streaming API v1.1 requires user authentication on all API calls. To raise your limit above 1 account (you can get your own access token from the built-in OAuth tool), you need to implement the standard OAuth three-party handshake to collect your friends' access tokens. It is not hard (as you can see from the source) but this app will save you that pain and jumpstart your prototype.


Requirements
------------
You need `python`, `twython`, and `flask` to set it up. If you don't already have them installed, You can install them from `pip`.

```bash
$ pip install flask twython
```

Then you need to [create your application on Twitter](https://dev.twitter.com/apps/new) and put your consumer token and secret into `consumer_credentials.py` like the following

```python
consumer_key = 'your application's consumer key'
consumer_secret = 'your application's consumer secret'
```

Start the app

```bash
$ python app.py
```

Author
------
Falcon Dai

License
-------
MIT License