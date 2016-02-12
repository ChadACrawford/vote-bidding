
candidate_names = []

with open("generators/candidate_names.txt") as f:
    candidate_names = map(lambda s: s.strip(), f.read().split('\n'))

with open("generators/issue_names.txt") as f:
    issue_names = map(lambda s: s.strip(), f.read().split('\n'))
