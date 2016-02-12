# Voter.py
# Specifies the base voter class
import random
import preference_profile


class Voter:
    __voter_id_tracker = 1

    def __init__(self, issues, utility_fn, pref_profile):
        self.__id = Voter.__voter_id_tracker
        Voter.__voter_id_tracker += 1
        self.__preference_profile = pref_profile
        self._issues = issues
        self._utility_fn = utility_fn

    @property
    def voter_id(self):
        return self.__id

    @property
    def issue_pool(self):
        return self._issues

    @property
    def preference(self):
        return self.__preference_profile

    def utility(self, issue, candidate=None):
        if not candidate:
            return lambda c: self._utility_fn[issue][c]
        else:
            return self._utility_fn[issue][candidate]

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
            self._vote = dict([(issue, max(issue.candidates, key=self.utility(issue))) for issue in self.issue_pool])
        elif self.preference == preference_profile.Total:
            self._vote = dict([(issue, sorted(issue.candidates, key=self.utility(issue), reverse=True))
                               for issue in self.issue_pool])
        else:
            raise Exception("Invalid preference profile. DummyVoter only accepts single preferences.")

    def get_results(self, issue, results):
        if self.preference == preference_profile.Single:
            score = dict(map(lambda x: (x, 0.), issue.candidates))
            n = 1.*len(results)
            for r in results:
                score[r.candidate] += 1
            u = dict()
            for c in score.iterkeys():
                u[c] = self.utility(issue, c) * score[c] / n
            self._vote[issue] = max(u, key=lambda x: u[x])
        else:
            score = dict(map(lambda x: (x, 0), issue.candidates))
            for r in results:
                for i, v in enumerate(reversed(r)):
                    score[v] += i
            u = dict()
            for c in score.iterkeys():
                u[c] = self.utility(issue, c) * score[c]
            self._vote[issue] = sorted(u, key=lambda x: u[x], reverse=True)

    def vote(self, issue):
        return self.preference(self._vote[issue])
