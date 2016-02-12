import itertools, random
import aux
import numpy.random as npr
import json
import operator


def gen_dataset(name, issues_num_candidates, cluster_size, random_noise=0.2):
    filename = "datasets/%s.json" % (name,)

    num_issues = len(issues_num_candidates)
    issue_names = list(npr.choice(aux.issue_names, len(issues_num_candidates), replace=False))
    issues = []
    for issue, num_candidates in zip(issue_names, issues_num_candidates):
        candidates = list(npr.choice(aux.candidate_names, num_candidates, replace=False))
        issues.append((issue, candidates))

    # us = [dict() for _ in range(3**num_issues)]
    us = []
    for u in itertools.product(*([[0, 0.5, 1]] * reduce(operator.mul, issues_num_candidates))):
        us.append(dict())
        i = 0
        # print u
        for issue, candidates in issues:
            us[-1][issue] = dict()
            for c in candidates:
                us[-1][issue][c] = u[i]
                i += 1

    utilities = []
    for u in us:
        for _ in range(cluster_size):
            v = dict([(issue, dict()) for issue in issue_names])
            for issue, candidates in issues:
                for c in candidates:
                    v[issue][c] = min(1, max(0, npr.normal(u[issue][c], random_noise)))
            utilities.append(v)

    with open(filename, "w") as f:
        data = json.dumps({
            "issues": issues,
            "utilities": utilities
        })
        f.write(data)

    return True


def main():
    for i in range(1, 6):
        gen_dataset("iterated_%d" % (i,), #dataset name
                    [2, 2], #number of candidates per issue
                    5, #cluster size
                    random_noise=0.15) #noise
    pass


if __name__ == "__main__":
    main()
