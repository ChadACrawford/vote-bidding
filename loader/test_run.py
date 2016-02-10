import generators.load
import sim.competition, sim.voter, sim.preference_profile


def main():
    print "Loading data file"
    candidates, utilities = generators.load.read_file("datasets/clustered_8.json")
    competition = sim.competition.Grouped(candidates,
                                          (sim.voter.DummyVoter, sim.voter.GreedyVoter),
                                          utilities,
                                          sim.preference_profile.Single,
                                          10)
    print "Running simulation"
    competition.run_simulation()
    print "Printing results"
    competition.display_results()


if __name__ == '__main__':
    main()