import json
from sim.issue import Issue

def read_file(filename):
    with open(filename, 'r') as f:
        data = json.loads(f.read())
        # print data['issues']
        issues_list, utilities_raw = data['issues'], data['utilities']
        # print issues_list
        issues = dict()
        for issue_name, issue_candidates in issues_list:
            issues[issue_name] = Issue(issue_name, issue_candidates)

        utilities = [dict([(issues[issue], u[issue]) for issue in u.iterkeys()])
                     for u in utilities_raw]
        # print list(issues.itervalues())
        return list(issues.itervalues()), utilities
    return None