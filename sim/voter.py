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


class GreedyVoter(Voter):
    def __init__(self, *args, **kwargs):
        Voter.__init__(self, *args, **kwargs)
        if self.preference == preference_profile.Single:
            self.__best_candidate = max(self.candidate_pool, key=self.utility)
        elif self.preference == preference_profile.Total:
            self.__best_candidate = sorted(self.candidate_pool, key=self.utility, reverse=True)
        else:
            raise Exception("Invalid preference profile for GreedyVoter. Accepts Single or Total preference profiles.")

    def get_results(self, results):
        pass

    def vote(self):
        self.preference(self.__best_candidate)


class RandomVoter(Voter):
    def __init__(self, *args, **kwargs):
        Voter.__init__(self, *args, **kwargs)
        if not self.preference == preference_profile.Single or not self.preference == preference_profile.Total:
            raise Exception("Invalid preference profile. RandomVoter only accepts single preferences.")

    def get_results(self, results):
        pass

    def vote(self):
        if self.preference == preference_profile.Single:
            return self.preference(random.choice(self.candidate_pool))
        else:
            return self.preference(random.shuffle(self.candidate_pool))


class DummyVoter(Voter):
    def __init__(self, *args, **kwargs):
        Voter.__init__(self, *args, **kwargs)
        # print type(self.preference)
        if self.preference == preference_profile.Single:
            self.__best_candidate = max(self.candidate_pool, key=self.utility)
        elif self.preference == preference_profile.Total:
            self.__best_candidate = sorted(self.candidate_pool, key=self.utility, reverse=True)
        else:
            raise Exception("Invalid preference profile. DummyVoter only accepts single preferences.")

    def get_results(self, results):
        if self.preference == preference_profile.Single:
            score = dict(map(lambda x: (x, 0.), self.candidate_pool))
            n = 1.*len(results)
            for r in results:
                score[r.candidate] += 1
            u = dict()
            for c in score.iterkeys():
                u[c] = self.utility(c) * score[c] / n
            self.__best_candidate = max(u, key=lambda x: u[x])
        else:
            score = dict(map(lambda x: (x, 0), self.candidate_pool))
            for r in results:
                for i, v in enumerate(reversed(r)):
                    score[v] += i
            u = dict()
            for c in score.iterkeys():
                u[c] = self.utility(c) * score[c]
            self.__best_candidate = sorted(u, key=lambda x: u[x], reverse=True)

    def vote(self):
        return self.preference(self.__best_candidate)
