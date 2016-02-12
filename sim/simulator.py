# Simulator.py
# The voting negotiation simulator
import preference_profile


class Simulator:
    def __init__(self, issues, voters, preference_profile, total_time=2):
        self._voters = voters
        self._issues = issues
        self._total_time = total_time
        self._preference_profile = preference_profile

    def _run_round(self):
        results = dict((i, []) for i in self._issues)
        for v in self._voters:
            for issue in self._issues:
                results[issue].append(v.vote(issue))

        for v in self._voters:
            for issue in self._issues:
                v.get_results(issue, results[issue])

        return results

    def _run_sim(self):
        results = None
        for _ in range(self._total_time):
            results = self.__run_round()

        return results

    def _collect_results(self, results):
        return self._preference_profile.summarize(results)

    def run(self):
        results = self._run_sim()
        summary = self._collect_results(results)
        return summary
