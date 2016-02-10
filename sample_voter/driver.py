"""
driver

This will run the sample voter in the simulation with the given parameters.
"""
import generators.load
import sim.competition, sim.voter, sim.preference_profile
import sample_voter

FILENAME = "datasets/clustered_1.json"
COMPETITORS = (sample_voter.SampleVoter,)
PREF_PROFILE = sim.preference_profile.Single
MAX_TIME = 10

def main(filename, competitors, pref_profile, max_time):
    print "Loading data file"
    candidates, utilities = generators.load.read_file(filename)
    competition = sim.competition.MultiAgent(candidates,
                                             competitors,
                                             utilities,
                                             pref_profile,
                                             max_time)
    print "Running simulation"
    competition.run_simulation()
    print "Printing results"
    competition.display_results()


if __name__ == '__main__':
    main(FILENAME, COMPETITORS, PREF_PROFILE, MAX_TIME)