
candidate_names = []

with open("generators/candidate_names.txt") as f:
    candidate_names = map(lambda s: s.strip(), f.read().split('\n'))

