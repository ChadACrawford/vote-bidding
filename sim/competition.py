import simulator
from matplotlib import pyplot


def _calc_utilities_single(candidates, results):
    n = len(results)
    u = dict(map(lambda x: (x, 0), candidates))
    for r in results:
        u[r.candidate] += 1.
    for c in candidates:
        u[c] /= n
    return u


class Competition:
    def __init__(self, candidates, voters, preference_profile, time):
        self._candidates = candidates
        self._voters = voters
        self._preference_profile = preference_profile
        self._time = time
        self._results_t = None

    def run_simulation(self):
        sim = simulator.Simulator(self._candidates, self._voters, self._preference_profile)
        results_t = []
        for _ in range(self._time):
            results_t.append(sim._run_round())
        self._results_t = results_t

    def display_results(self):
        raise NotImplementedError


class MultiAgent(Competition):
    def __init__(self, candidates, competitors, utilities, pref_profile, time=2):
        voters = []
        for voter in competitors:
            for utility_fn in utilities:
                voters.append(voter(candidates, utility_fn, pref_profile))
        Competition.__init__(self, candidates, voters, pref_profile, time)

    def display_results(self):
        us = [_calc_utilities_single(self._candidates, rs) for rs in self._results_t]
        f = dict([(c, map(lambda x: x[c], us)) for c in self._candidates])
        for c in self._candidates:
            # print c,f[c]
            pyplot.plot(f[c], label=c)

        pyplot.legend()
        pyplot.show()
