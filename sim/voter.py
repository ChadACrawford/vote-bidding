# Voter.py
# Specifies the base voter class
import random
import preference_profile


class Voter:
    __voter_id_tracker = 1

    def __init__(self, candidates, utility_fn, pref_profile):
        self.__id = Voter.__voter_id_tracker
        Voter.__voter_id_tracker += 1
        self.__preference_profile = pref_profile
        self.__candidates = candidates
        self.__utility_fn = utility_fn

    @property
    def voter_id(self):
        return self.__id

    @property
    def candidate_pool(self):
        return self.__candidates

    @property
    def preference(self):
        return self.__preference_profile

    def utility(self, candidate):
        return self.__utility_fn[candidate]

    def get_results(self, results):
        raise NotImplementedError

    def vote(self):
        raise NotImplementedError


class RandomVoter(Voter):
    def get_results(self, results):
        pass

    def vote(self):
        return random.choice(self.candidate_pool)


class GreedyVoter(Voter):
    def __init__(self, *args, **kwargs):
        Voter.__init__(self, *args, **kwargs)
        self.__best_candidate = max(self.candidate_pool, key=self.utility)

    def get_results(self, results):
        pass

    def vote(self):
        return self.preference(self.__best_candidate)


class DummyVoter(Voter):
    def __init__(self, *args, **kwargs):
        Voter.__init__(self, *args, **kwargs)
        # print type(self.preference)
        if not self.preference == preference_profile.Single:
            raise Exception("Invalid preference profile. DummyVoter only accepts single preferences.")
        self.__best_candidate = max(self.candidate_pool, key=self.utility)

    def get_results(self, results):
        score = dict(map(lambda x: (x, 0.), self.candidate_pool))
        n = 1.*len(results)
        for r in results:
            score[r.candidate] += 1
        u = dict()
        for c in score.iterkeys():
            u[c] = self.utility(c) * score[c] / n
        self.__best_candidate = max(u, key=lambda x: u[x])

    def vote(self):
        return self.preference(self.__best_candidate)
