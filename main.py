class Request(object):
    def __init__(self, video_id, endpoint_id, num_requests):
        self.video_id = video_id
        self.endpoint_id = endpoint_id
        self.num_requests = num_requests


class Endpoint(object):
    def __init__(self, latency_to_data_center, caches):
        self.latency_to_data_center = latency_to_data_center
        self.caches = caches


class Data(object):
    def __init__(self, name):
        with open(name, 'rb') as f:
            data = f.readlines()
        self.num_videos, self.num_endpoints, self.num_request_descriptions, self.num_cache_servers, \
        self.max_cache_capacity = data[0].split()
        self.video_sizes = data[1].split()
        self.endpoints = []
        self.requests = []
        i = 2
        while len(self.endpoints) == self.num_endpoints:
            latency_to_data_center, num_caches = data[i]
            i += 1
            caches = {}
            for j in xrange(i, i + num_caches):
                cache_id, latency_to_enpoint = data[j].split()
                caches[cache_id] = latency_to_enpoint
            self.endpoints.append(Endpoint(latency_to_data_center, caches))
            i += num_caches
        for i in xrange(i, i+self.num_request_descriptions):
            self.requests.append(Request(*data[i].split()))

def main():
    data = Data()

if __name__ == '__main__':
    main()