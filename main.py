import os


class Request(object):
    def __init__(self, video_id, endpoint_id, num_requests):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.num_requests = num_requests


class Endpoint(object):
    def __init__(self, latency_to_data_center, caches):
        self.latency_to_data_center = latency_to_data_center
        self.caches = caches

    def __repr__(self):
        s = 'latency to data center: ' + self.latency_to_data_center + '\n'
        s += 'caches: ' + self.latency_to_data_center + '\n'


class Data(object):
    def __init__(self, name):
        with open(os.path.join('a', name + '.in'), 'rb') as f:
            data = f.readlines()
        self.num_videos, self.num_endpoints, self.num_request_descriptions, self.num_cache_servers, \
        self.max_cache_capacity = map(int, data[0].split())
        self.video_sizes = map(int, data[1].split())
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
        for i in xrange(i, i+self.num_request_descriptions):
            self.requests.append(Request(*map(int, data[i].split())))

    def __repr__(self):
        s = 'num videos: ' + str(self.num_videos) + '\n'
        s += 'num cache servers: ' + str(self.num_cache_servers) + '\n'
        s += 'max cache server capacity: ' + str(self.max_cache_capacity) + '\n'
        s += 'video sizes: ' + ', '.join(map(str, self.video_sizes)) + '\n'
        s += 'enpoints:\n'
        s += '\n'.join([repr(e) for e in self.endpoints])
        s += 'requests:\n'
        s += '\n'.join([repr(e) for e in self.requests])



def main():
    data = Data('example')

if __name__ == '__main__':
    main()