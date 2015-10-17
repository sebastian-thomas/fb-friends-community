import facebook
import requests
import json
import settings

users = {}
graph = {}

total_photos_fetched = 0
max_photos = 200


def add_photo_tags_to_graph(fb_photos):
	global total_photos_fetched
	global graph

	for fb_photo in fb_photos['data']:
		#print json.dumps(fb_photo, indent=4, sort_keys=True)
		total_photos_fetched = total_photos_fetched + 1
		tagged_users = []
		for tagged_user in fb_photo['tags']['data']:
			if('id' in tagged_user):
				#print tagged_user['name'] +" "+ tagged_user['id']
				users[tagged_user['id']] = tagged_user['name']
				tagged_users.append(tagged_user['name'])

		for tuser in tagged_users:
			if tuser not in graph:
				graph[tuser] = {}
			for tuser2 in tagged_users:
				if tuser != tuser2:
					if tuser2 in graph[tuser]:
						graph[tuser][tuser2] = graph[tuser][tuser2] + 1
					else:
						graph[tuser][tuser2] = 1 

def print_major_friends(user):
	print 'Major friends'
	for key,val  in graph[user].iteritems():
		if val > 10 :
			print key +" "+ str(val)

def get_major_friends(user):
	major_friends = []
	for key,val in graph[user].iteritems():
		if val > 10 :
			major_friends.append(key)
	return major_friends

def get_major_friends_of_friends(user):
	major_friends_set = {}
	mlist = get_major_friends(user)
	major_friends_set[user] = mlist
	for friend in mlist:
		major_friends_set[friend] = get_major_friends(friend)
	return major_friends_set



def main():
	fb_graph = facebook.GraphAPI(settings.access_token)
	fb_profile = fb_graph.get_object("me")
	#friends = graph.get_connections("me", "friends")
	args = {'fields' : 'id,tags', }
	
	#initialize the graph with only node as you
	graph[fb_profile['name']] = {}

	print '....'
	fb_photos = fb_graph.get_connections("me" , "photos", **args)
	add_photo_tags_to_graph(fb_photos)
	while total_photos_fetched < max_photos :
		if 'paging' in fb_photos:
			if 'next' in fb_photos['paging']:
				print '....'
				fb_photos = requests.get(fb_photos['paging']['next']).json()
				add_photo_tags_to_graph(fb_photos)

	
	major_friends_set = get_major_friends_of_friends(fb_profile['name'])
	#print json.dumps(fb_photos, indent=4, sort_keys=True)

	#print json.dumps(graph, indent=4, sort_keys=True)
	print json.dumps(graph[fb_profile['name']], indent=4, sort_keys=True)
	print "Toatal Photos :" +str(total_photos_fetched)
	print "Total Nodes :" 
	print len(graph.keys())
	#print print_major_friends(fb_profile['name'])
	print json.dumps(major_friends_set, indent=4, sort_keys=True)
	


if __name__ == "__main__":
	main()