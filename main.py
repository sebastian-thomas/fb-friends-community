import facebook
import requests
import json
import settings
from random import randint
import random
from pprint import pprint
import cluster


users = {}
graph = {}

total_photos_fetched = 0
max_photos = 200
num_clust = 2
access_token =''

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

def print_gangs(gangs):
	for gang in gangs:
		print gang

def cluster_friends(major_friends_set):
	mat = []
	user_mat = []
	dims = major_friends_set.keys()
	for key,val in major_friends_set.items():
		user_mat.append(key)
		dim_vector = []
		for d in dims:
			if d in val:
				dim_vector.append(1)
			else:
				dim_vector.append(0)
		mat.append(dim_vector)

	
	temp_clust = cluster.kmeans(mat,num_clust)
	for clust in temp_clust:
		print "Cluster ----"
		for p in clust:
			print user_mat[p]

	return temp_clust



def get_major_friends(user):
	major_friends = []
	for key,val in graph[user].iteritems():
		if val > 10 :
			major_friends.append(key)
	major_friends.sort()
	return major_friends

def get_major_friends_of_friends(user):
	major_friends_set = {}
	mlist = get_major_friends(user)
	#major_friends_set[user] = mlist
	for friend in mlist:
		major_friends_set[friend] = get_major_friends(friend)
	return major_friends_set

def get_a_gang(num_of_players,major_friends_set):
	num_itr = 0
	while True:
		num_itr = num_itr + 1
		mjf_list = []
		gang_list = []
		mjf_list = major_friends_set.keys()
		for x in range(0,num_of_players):
			index = randint(1,len(mjf_list)) - 1
			gang_list.append(mjf_list[index])
			tmp_item = mjf_list[index]
			#print str(num_of_players)+" : "+str(x)+" - "+str(tmp_item)
			mjf_list.remove(tmp_item)
		break_loop = True
		for user1 in gang_list:
			for user2 in gang_list:
				if user1 != user2:
					if user1 not in major_friends_set[user2]:
						break_loop = False
		if break_loop or num_itr > 10:
			break
	print num_itr
	print gang_list

def get_gangs_rand(major_friends_set):
	num_itr = 0
	all_close_friends = major_friends_set.keys()
	gangs = []
	done = False
	while not done:
		num_itr = num_itr + 1
		rand_friend = random.choice(all_close_friends)
		rand_friend_gang = list(set(all_close_friends).intersection(major_friends_set[rand_friend]))
		if len(rand_friend_gang) > 0:
			gangs.append(rand_friend_gang)
			all_close_friends = [x for x in all_close_friends if x not in rand_friend_gang]
		if len(all_close_friends) <= 0 or num_itr > 10 :
			done = True
	return gangs


def main():
	fb_graph = facebook.GraphAPI(access_token)
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
	#get_a_gang(5,major_friends_set)
	#get_a_gang(5,major_friends_set)
	#get_a_gang(5,major_friends_set)

	#print "Major Gangs"
	#print "1"
	#print_gangs(get_gangs_rand(major_friends_set))
	#print "2"
	#print_gangs(get_gangs_rand(major_friends_set))
	#print "3"
	#print_gangs(get_gangs_rand(major_friends_set))
	tc = cluster_friends(major_friends_set)
	return tc

def run_pgm(access_token_t, num_clust_t):
	global access_token
	global num_clust
	num_clust = num_clust_t
	access_token = access_token_t
	main()

if __name__ == "__main__":
	access_token = settings.access_token
	main()