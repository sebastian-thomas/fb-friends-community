import facebook
import requests
import json
import settings

graph = facebook.GraphAPI(settings.access_token)
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")
print json.dumps(friends,indent=4, sort_keys=True)