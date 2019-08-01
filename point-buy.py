#!/usr/bin/env python3

"""
D&D 5E Point Buy Calculator

Empirically speaking, the marginal cost for any score increase in the Point Buy
algorithm is `max(1, modifier(score))`, where `modifier` is calculated as
`floor((score - 10) / 2)`.

This tool differs from the RAW implementation of Point Buy because it allows
ability scores to exceed 15. Using the same algorithm described, we can
calculate values for scores between 8-20.
"""

import argparse
import math


MINIMUM_SCORE = 8
MAXIMUM_SCORE = 20


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
    return math.floor((score - 10) / 2)


def score_to_marginal_cost(score):
    return max(1, score_to_modifier(score))


def score_to_cost(score):
    if score <= MINIMUM_SCORE:
        return 0

    cost = 0
    for marginal_score in range(MINIMUM_SCORE, score):
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
