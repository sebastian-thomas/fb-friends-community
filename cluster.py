from random import randint
import math

def kmeans(mat, no_clusters):
	temp_mat = mat
	temp_clust = []
	inital_centroids = []
	i = no_clusters
	while i > 0:
		t = randint(1,len(temp_mat)) -1
		if t not in inital_centroids:
			inital_centroids.append(t)
			temp_clust.append([])
			temp_clust[no_clusters-i].append(t)
			i = i - 1

	for i in range(len(temp_mat)):
		if i not in inital_centroids:
			dist = find_dist(mat[inital_centroids[0]], mat[i] )
			cent_clust = 0
			j = -1
			for centroid in inital_centroids:
				j = j + 1
				distew = find_dist(mat[centroid], mat[i])
				#print dist, distew
				if distew < dist:
					cent_clust = j
			temp_clust[cent_clust].append(i)

	#lets take cluster avg to make more accurate
	clust_avg = find_clust_avg(mat,temp_clust)
	temp_clust2 = [] 
	for x in range(no_clusters):
		temp_clust2.append([])

	for i in range(len(temp_mat)):
		dist = find_dist(clust_avg[0], mat[i] )
		cent_clust = 0
		for centroid in range(len(clust_avg)):
			distew = find_dist(mat[i], clust_avg[centroid])
			#print dist, distew
			if distew < dist:
				cent_clust = centroid
		temp_clust2[cent_clust].append(i)
		

	return temp_clust2


def find_clust_avg(mat,temp_clust):
	new_clust_avg = []
	for clust in temp_clust:
		num_elems = len(clust)
		tvect = [0.0 for x in range(len(mat[0]))]
		if num_elems == 0 :
			new_clust_avg.append(tvect)
			continue
		for elem in clust:
			for i in range(len(mat[elem])):
				tvect[i] = tvect[i] + mat[elem][i]

		for i in range(len(tvect)):
			tvect[i] = tvect[i] / num_elems
		new_clust_avg.append(tvect)
	return new_clust_avg



def find_dist(p,q):
	dist = 0
	for i in range(len(p)):
		dist = dist + (p[i] - q[i])* (p[i] - q[i])
	return dist

def find_similarity(p,q):
	pq = 0.0
	modp = 0.0
	modq = 0.0
	for col in p:
		pq = pq + p[col]*q[col]

	for col in p:
		modp = modp + p[col] * p[col]
	modp = math.sqrt(modp)
	#print modp,p

	for col in q:
		modq = modq + q[col] * q[col]
	modq = math.sqrt(modq)
	#print modq,q
	if modp == 0:
		return 0
	elif modq ==0:
		return 0
	else:
		return pq /(modp * modq)