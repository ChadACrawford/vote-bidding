# Simulator.py
# The voting negotiation simulator
import preference_profile


class Simulator:
    def __init__(self, candidates, voters, preference_profile, total_time=2):
        self._voters = voters
        self._candidates = candidates
        self._total_time = total_time
        self._preference_profile = preference_profile

    def _run_round(self):
        results = []
        for v in self._voters:
            results.append(v.vote())

        for v in self._voters:
            v.get_results(results)

        return results

    def _run_sim(self):
        results = None
        for _ in range(self._total_time):
            results = self.__run_round()

        return results

    def __collect_results(self, results):
        return self._preference_profile.summarize(results)

    def run(self):
        results = self.__run_sim()
        summary = self.__collect_results(results)
        return summary
