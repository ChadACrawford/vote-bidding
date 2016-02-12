"""
driver

This will run the sample voter in the simulation with the given parameters.
"""
import generators.load
import sim.competition, sim.voter, sim.preference_profile
import sample_voter

FILENAME = "datasets/iterated_1.json"
COMPETITION_MODULE = sim.competition.RandomAssignment
COMPETITORS = (sim.voter.DummyVoter,)
PREF_PROFILE = sim.preference_profile.Single
MAX_TIME = 20


def main(filename, competition_module, competitors, pref_profile, max_time):
    print "Loading data file"
    issues, utilities = generators.load.read_file(filename)
    competition = competition_module(issues,
                                     competitors,
                                     utilities,
                                     pref_profile,
                                     max_time)
    print "Running simulation"
    competition.run_simulation()
    print "Printing results"
    competition.display_results()


if __name__ == '__main__':
    main(FILENAME, COMPETITION_MODULE, COMPETITORS, PREF_PROFILE, MAX_TIME)