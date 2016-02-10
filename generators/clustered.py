import aux
import random
import numpy.random as npr
import json


def gen_dataset(name, num_candidates, num_clusters, cluster_size, random_noise=0.2):
    filename = "datasets/%s.json" % (name,)

    candidates = list(npr.choice(aux.candidate_names, num_candidates, replace=False))
    us = [dict() for _ in range(num_clusters)]
    for i in range(num_clusters):
        for c in candidates:
            us[i][c] = random.random()

    utilities = []
    for u in us:
        for _ in range(cluster_size):
            v = dict()
            for c in candidates:
                v[c] = min(1, max(0, npr.normal(u[c], random_noise)))
            utilities.append(v)

    with open(filename, "w") as f:
        data = json.dumps({
            "candidates": candidates,
            "utilities": utilities
        })
        f.write(data)

    return True


def main():
    for i in range(1, 11):
        gen_dataset("clustered_%d" % (i,), 10, 5, 10, random_noise=0.2)
    pass


if __name__ == "__main__":
    main()