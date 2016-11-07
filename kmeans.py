#!/usr/bin/env python
#This module includes functionality for k-means clustering

import numpy as np
from math import log, erfc
import scipy.cluster.vq as vq
from sklearn.decomposition import PCA
from math import erf

def kmeans(points, k, max_iter = 10000):
    whitened = vq.whiten(points)
    centroids = vq.kmeans(whitened, k)[0]
    
    print "centroids shape: %s"%centroids.shape.__str__()
    
    #Deciding point-to-cluster correspondence (assignment)
    assignment = dict((clusterID,[]) for clusterID in xrange(k))
    for i in xrange(dims(points)[0]):
        assignment[assign(whitened[i], centroids)].append(i)
    
    #Making non-whitened centroids given assignment
    for clusterID in xrange(dims(centroids)[0]):
        clusterPoints = points[assignment[clusterID]]
        centroids[clusterID] = np.mean(clusterPoints, 0)
    
    return clusterGroup(points, np.array(centroids), assignment)

def dims(array):
    '''Returns the dimensions of a numpy array, 'caus f*ck numpy.shape'''
    shape = array.shape
    if len(shape) == 1:
        return (1,shape[0])
    else:
        return shape

def assign(point, centroids):
    return np.argmin(distances(point, centroids))

def distance(v1, v2):
    return np.linalg.norm(v1 - v2)

def distances(point, otherPoints):
    return sq_distances(point, otherPoints)**0.5

def sq_distances(point, otherPoints):
    comparison = np.array([point]*dims(otherPoints)[0])
    differences = comparison - otherPoints
    return np.sum(differences**2, 1)

def average_sq_distance(point, otherPoints):
    #Returns the average square distance from point to otherPoints
    return np.mean(sq_distances(point, otherPoints))

class clusterGroup():

    def __init__(self, points, centroids, assignment):
        self.points = points
        self.centroids = centroids
        self.k = dims(centroids)[0]
        self.assignment = assignment

    def deviations(self):
        deviations = []
        for clusterID in self.assignment:
            pointIDs = self.assignment[clusterID]
            mean_sq_err = average_sq_distance(self.centroids[clusterID], self.points[pointIDs])
            deviations.append(mean_sq_err**0.5)
        return deviations

    def points_of_cluster(self, cluster):
        return self.points[self.assignment[cluster]]

    def cluster_of_point(self, point_index):
        for cluster in self.assignment:
            if point_index in self.assignment[cluster]:
                return cluster

    def getSilhouettes(self):
        s = []
        for clusterID in xrange(self.k):
            a = []
            b = []
            sForCluster = []
            clusterPoints = self.points[self.assignment[clusterID]]
            for point in clusterPoints:
                num_points_in_cluster = dims(clusterPoints)[0]
                bi = None
                for otherID in xrange(self.k):
                    otherPoints = self.points[self.assignment[otherID]]
                    dissimilarity = np.mean(distances(point, otherPoints))
                    print "dissim: %.3f"%dissimilarity
                    if otherID == clusterID:
                        a.append(dissimilarity)
                    else:
                        if bi == None or dissimilarity <= bi:
                            bi = dissimilarity
                b.append(bi)
            for i in xrange(len(a)):
                sForCluster.append((b[i]-a[i])/max(a[i],b[i]))
            sForCluster.sort()
            s += sForCluster
        return s

    def getAverageSilhouette(self):
        return np.mean(self.getSilhouettes())

    def get_assignment_vector(self):
        return [self.cluster_of_point(i) for i in xrange(len(self.points))]

    def getPC(self, N):
        assigned_pc = np.zeros((len(self.points),N+1))
        assigned_pc[:,0] = self.get_assignment_vector()
        pca = PCA(n_components=N)
        assigned_pc[:,range(1,N+1)] = pca.fit_transform(self.points)
        return assigned_pc

    def score_new_point(self, newPoint):
        closest_cluster = np.argmin(sq_distances(newPoint, self.centroids))
        closest_centroid = self.centroids[closest_cluster]
        new_distance = distance(newPoint, closest_centroid)
        
        num_cluster_points = len(self.assignment[closest_cluster])
        if num_cluster_points > 2:
            cluster_points = self.points[closest_cluster]
            rmsd = np.sqrt(np.mean(sq_distances(closest_centroid, cluster_points)))
        else:
            #Agerage within-cluster deviation from centroid for all clusters with more than 2 members
            all_sq_dists = np.array([])
            for i in xrange(len(self.centroids)):
                all_sq_dists = np.append(all_sq_dists, sq_distances(self.centroids[i], self.points_of_cluster(i)))
            rmsd = np.sqrt(np.mean(all_sq_dists))
            
        return log(erfc(new_distance/(np.sqrt(2)*rmsd)))
