import codecs
import math
from functools import reduce
from numpy import *
import matplotlib.pyplot as plt

class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.cd = None
        self.rd = None
        self.processed = False

    def distance(self, point):
        p1_lat, p1_lon, p2_lat, p2_lon = [math.radians(c) for c in
                                          (self.latitude, self.longitude, point.latitude, point.longitude)]

        numerator = math.sqrt(
            math.pow(math.cos(p2_lat) * math.sin(p2_lon - p1_lon), 2) +
            math.pow(
                math.cos(p1_lat) * math.sin(p2_lat) -
                math.sin(p1_lat) * math.cos(p2_lat) *
                math.cos(p2_lon - p1_lon), 2))

        denominator = (
            math.sin(p1_lat) * math.sin(p2_lat) +
            math.cos(p1_lat) * math.cos(p2_lat) *
            math.cos(p2_lon - p1_lon))

        return math.atan2(numerator, denominator) * 6372800

    def to_geo_json_dict(self, properties=None):
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    self.longitude,
                    self.latitude,
                ]
            },
            'properties': properties,
        }

    def __repr__(self):
        return '(%f, %f)' % (self.latitude, self.longitude)


class Cluster:
    def __init__(self, points):
        self.points = points

    def centroid(self):
        return Point(sum([p.latitude for p in self.points]) / len(self.points),
                     sum([p.longitude for p in self.points]) / len(self.points))

    def region(self):
        centroid = self.centroid()
        radius = reduce(lambda r, p: max(r, p.distance(centroid)), self.points)
        return centroid, radius

    def to_geo_json_dict(self, user_properties=None):
        center, radius = self.region()
        properties = {'radius': radius}
        if user_properties: properties.update(user_properties)

        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    center.longitude,
                    center.latitude,
                ]
            },
            'properties': properties,
        }


class Optics:
    def __init__(self, points, max_radius, min_cluster_size):
        self.points = points
        self.max_radius = max_radius
        self.min_cluster_size = min_cluster_size


    def _setup(self):
        for p in self.points:
            p.rd = None
            p.processed = False
        self.unprocessed = [p for p in self.points]
        self.ordered = []

    def _core_distance(self, point, neighbors):
        if point.cd is not None: return point.cd
        if len(neighbors) >= self.min_cluster_size - 1:
            sorted_neighbors = sorted([n.distance(point) for n in neighbors])
            point.cd = sorted_neighbors[self.min_cluster_size - 2]
            return point.cd

    def _neighbors(self, point):
        return [p for p in self.points if p is not point and
                p.distance(point) <= self.max_radius]


    def _processed(self, point):
        point.processed = True
        self.unprocessed.remove(point)
        self.ordered.append(point)

    def _update(self, neighbors, point, seeds):
        for n in [n for n in neighbors if not n.processed]:
            new_rd = max(point.cd, point.distance(n))
            if n.rd is None:
                n.rd = new_rd
                seeds.append(n)
            elif new_rd < n.rd:
                n.rd = new_rd


    def run(self):
        self._setup()
        while self.unprocessed:
            point = self.unprocessed[0]
            self._processed(point)
            point_neighbors = self._neighbors(point)
            if self._core_distance(point, point_neighbors) is not None:
                seeds = []
                self._update(point_neighbors, point, seeds)
                while (seeds):
                    seeds.sort(key=lambda n: n.rd)
                    n = seeds.pop(0)
                    self._processed(n)
                    n_neighbors = self._neighbors(n)
                    if self._core_distance(n, n_neighbors) is not None:
                        self._update(n_neighbors, n, seeds)
        return self.ordered

    def cluster(self, cluster_threshold):
        clusters = []
        separators = []
        for i in range(len(self.ordered)):
            this_i = i
            next_i = i + 1
            this_p = self.ordered[i]
            this_rd = this_p.rd if this_p.rd else float('infinity')
            if this_rd > cluster_threshold:
                separators.append(this_i)
        separators.append(len(self.ordered))
        for i in range(len(separators) - 1):
            start = separators[i]
            end = separators[i + 1]
            if end - start >= self.min_cluster_size:
                clusters.append(Cluster(self.ordered[start:end]))
        return clusters


def load_data(path):
    data_set = list()
    with codecs.open(path) as f:
        for line in f.readlines():
            data = line.strip().split("\t")
            flt_data = list(map(float, data))
            data_set.append(flt_data)
    return data_set


def plot_cluster(data_mat, clusters):
#    plt.figure(figsize=(6, 6), dpi=80)
    k = shape(clusters)[0]
    print(k)

    plt.figure(figsize=(15, 6), dpi=80)

    plt.subplot(121)
    plt.plot(data_mat[:, 0], data_mat[:, 1], 'o', markersize=5)
    plt.title("source data", fontsize=15)

    plt.subplot(122)

    colors = [plt.cm.get_cmap("Spectral")(each) for each in linspace(0, 1, k)]
    for i, col in zip(range(k), colors):
        points = clusters[i].points
        x = []
        y = []
        for p in points:
            x.append(p.latitude)
            y.append(p.longitude)
        plt.plot(x, y, 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=5)
    plt.title("K-Means Cluster", fontsize=15)
    plt.show()


if __name__ == "__main__":
    data_mat = mat(load_data("../dataset/user2.txt"))
    m = shape(data_mat)[0]
    points = []
    for i in range(m):
        points.append(Point(data_mat[i,0], data_mat[i,1]))

    optics = Optics(points, 100000, 100)
    optics.run()
    clusters = optics.cluster(50000)

#    for cluster in clusters:
#        print(cluster.points)

    plot_cluster(data_mat, clusters)