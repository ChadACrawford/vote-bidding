import simulator, preference_profile
from matplotlib import pyplot
import random


def _calc_utilities_single(issue, results):
    n = len(results[issue])
    u = dict(map(lambda x: (x, 0), issue.candidates))
    for r in results[issue]:
        u[r.candidate] += 1.
    for c in issue.candidates:
        u[c] /= n
    return u


def _calc_utilities_total(candidates, results):
    n = len(results)
    u = dict(map(lambda x: (x, 0), candidates))
    for r in results:
        for i, v in enumerate(reversed(r)):
            u[v] += i
    for c in candidates:
        u[c] /= 1. * n
    return u


class Competition:
    def __init__(self, issues, voters, preference_profile, time):
        self._issues = issues
        self._voters = voters
        self._preference_profile = preference_profile
        self._time = time
        self._results_t = None

    def run_simulation(self):
        sim = simulator.Simulator(self._issues, self._voters, self._preference_profile)
        results_t = []
        for _ in range(self._time):
            results_t.append(sim._run_round())
        self._results_t = results_t

    def display_results(self):
        calc_utilities = _calc_utilities_single if self._preference_profile == preference_profile.Single\
            else _calc_utilities_total
        count = 0
        for issue in self._issues:
            pyplot.subplot(211 + count)
            count += 1
            us = [calc_utilities(issue, rs) for rs in self._results_t]
            f = dict([(c, map(lambda x: x[c], us)) for c in issue.candidates])

            pyplot.title(issue.name)
            for c in issue.candidates:
                pyplot.plot(f[c], label=c)
            pyplot.legend()

        pyplot.show()


class Grouped(Competition):
    def __init__(self, issues, competitors, utilities, pref_profile, time=2):
        voters = []
        for voter in competitors:
            for utility_fn in utilities:
                voters.append(voter(issues, utility_fn, pref_profile))
        Competition.__init__(self, issues, voters, pref_profile, time)


class RandomAssignment(Competition):
    def __init__(self, issues, competitors, utilities, pref_profile, time=2):
        voters = []
        for utility_fn in utilities:
            voter = random.choice(competitors)
            voters.append(voter(issues, utility_fn, pref_profile))
        Competition.__init__(self, issues, voters, pref_profile, time)
