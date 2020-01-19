#!/usr/bin/env python3

"""
D&D 5E Experimental Point Buy Calculator
"""

import argparse
import math


MINIMUM_SCORE = 1
MAXIMUM_SCORE = 20
NEUTRAL_SCORE = 10


def ability_score(arg):
    score = int(arg)
    if score < MINIMUM_SCORE or score > MAXIMUM_SCORE:
        raise argparse.ArgumentTypeError(
                "Ability scores must be between {} and {}. {} given.".format(
                    MINIMUM_SCORE,
                    MAXIMUM_SCORE,
                    score,
                    ),
                )
        return score


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("scores", nargs=6, type=ability_score)
    return parser.parse_args()


def score_to_modifier(score):
    return math.floor((score - NEUTRAL_SCORE) / 2)


def score_to_marginal_cost(score):
    return score_to_modifier(score)


def score_to_cost(score):
    cost = 0
    for marginal_score in range(score, NEUTRAL_SCORE, +1):
        cost += score_to_marginal_cost(marginal_score - 1)
    for marginal_score in range(score, NEUTRAL_SCORE, -1):
        cost += score_to_marginal_cost(marginal_score + 1)
    return cost


def main():
    args = parse_args()
    total = 0
    print("Scores:")
    for index, score in enumerate(args.scores):
        cost = score_to_cost(score)
        total += cost
        print("  {}: {:2} -> {:2}".format(index + 1, score, cost))
    print("Total: {}".format(total))


if __name__ == "__main__":
    main()
