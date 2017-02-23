import os


class Video(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.endpoints = []
        self.caches = set()
        self.caches_to_latency = {}

    def __repr__(self):
        s = '\tvideo {0} size {1}\n'.format(self.id, self.size)
        s += '\tendpoints:\n'
        for i, e in enumerate(self.endpoints):
            s += '\t\tendpoint {0}:\n'.format(i)
            s += '\t\t' + '\n\t\t'.join(repr(e).splitlines()) + '\n'
        s += '\tcaches:\n'
        s += '\t' + '\n\t\t'.join([repr(r) for r in self.caches])
        s += '\n\tcaches to latency:\n'
        s += '\t\t' + '\n\t\t'.join(
            ['{0} latency to cache server {1}'.format(l, i) for i, l in self.caches_to_latency.iteritems()])
        return s


class Request(object):
    def __init__(self, video_id, endpoint_id, num_requests):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.num_requests = num_requests

    def __repr__(self):
        return '{0} requests of video {1} to endpoint {2}'.format(self.num_requests, self.video_id, self.endpoint_id)


class Endpoint(object):
    def __init__(self, latency_to_data_center, caches):
        self.latency_to_data_center = latency_to_data_center
        self.caches = caches
        self.requests = []

    def __repr__(self):
        s = '\tlatency to data center: ' + str(self.latency_to_data_center) + '\n'
        s += '\tcaches: \n'
        s += '\t\t' + '\n\t\t'.join(
            ['{0} latency to cache server {1}'.format(l, i) for i, l in self.caches.iteritems()])
        s += '\n\trequests: \n'
        s += '\t\t' + '\n\t\t'.join([repr(r) for r in self.requests])
        return s


class Data(object):
    def __init__(self, name):
        with open(os.path.join('a', name + '.in'), 'rb') as f:
            data = f.readlines()
        self.num_videos, self.num_endpoints, self.num_request_descriptions, self.num_cache_servers, \
        self.max_cache_capacity = map(int, data[0].split())
        self.videos = [Video(id, size) for id, size in enumerate(data[1].split())]
        self.endpoints = []
        self.requests = []
        i = 2
        while len(self.endpoints) != self.num_endpoints:
            latency_to_data_center, num_caches = map(int, data[i].split())
            i += 1
            caches = {}
            for j in xrange(i, i + num_caches):
                cache_id, latency_to_enpoint = map(int, data[j].split())
                caches[cache_id] = latency_to_enpoint
            self.endpoints.append(Endpoint(latency_to_data_center, caches))
            i += num_caches
        for i in xrange(i, i + self.num_request_descriptions):
            req = Request(*map(int, data[i].split()))
            self.requests.append(req)
            endpoint_requested_this = self.endpoints[req.endpoint_id]
            endpoint_requested_this.requests.append(req)
            self.videos[req.video_id].endpoints.append(endpoint_requested_this)

        for v in self.videos:
            for e in v.endpoints:
                for cache_id, latency in e.caches.iteritems():
                    if cache_id not in v.caches:
                        v.caches.add(cache_id)
                        v.caches_to_latency[cache_id] = latency

    def run(self):
        pass

    def __repr__(self):
        s = 'num videos: ' + str(self.num_videos) + '\n'
        s += 'num cache servers: ' + str(self.num_cache_servers) + '\n'
        s += 'max cache server capacity: ' + str(self.max_cache_capacity) + '\n'
        for i, e in enumerate(self.endpoints):
            s += 'endpoint {0}:\n'.format(i)
            s += repr(e) + '\n'
        s += 'requests:\n'
        s += '\n'.join(['\t' + repr(e) for e in self.requests])
        s += '\nvideos:\n'
        s += '\n'.join([repr(v) for v in self.videos])
        return s


def main():
    data = Data('example')
    print data


if __name__ == '__main__':
    main()
