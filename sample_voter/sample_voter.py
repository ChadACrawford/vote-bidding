"""
sample_voter

The sample voter implementation.
"""
from sim import preference_profile, voter


class SampleVoter(voter.Voter):
    def __init__(self, *args, **kwargs):
        """
        Initializes the sample voter. This code is borrowed from the Dummy Voter
        :param args:
        :param kwargs:
        :return: New SampleVoter object
        """
        # Need to call this to initialize some values
        voter.Voter.__init__(self, *args, **kwargs)
        # This will only run for problems using the "single" preference profile, which means the agent
        # specifies a single agent to choose.
        if not self.preference == preference_profile.Single:
            raise Exception("Invalid preference profile. DummyVoter only accepts single preferences.")
        # The best candidate is initially the greedy one
        self.__best_candidate = max(self.candidate_pool, key=self.utility)

    def get_results(self, results):
        """
        This method returns the preferences that each of the voters reported in the bidding game.
        :param results: An array of preference profiles
        """
        score = dict(map(lambda x: (x, 0.), self.candidate_pool))
        n = 1.*len(results)
        for r in results:
            score[r.candidate] += 1
        u = dict()
        for c in score.iterkeys():
            u[c] = self.utility(c) * score[c] / n
        self.__best_candidate = max(u, key=lambda x: u[x])

    def vote(self):
        """
        This is used to calculate which candidate the agent will vote for during this round.
        :return: A preference profile corresponding to the candidate that this agent selects
        """
        return self.preference(self.__best_candidate)