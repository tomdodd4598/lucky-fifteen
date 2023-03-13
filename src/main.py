import math

from fractions import Fraction
from itertools import chain, combinations


def at_to(prob):
    return prob.denominator - prob.numerator, prob.numerator


class Odds:

    def __init__(self, at, to):
        self.prob = Fraction(to, at + to)
        self.at, self.to = at_to(self.prob)

    def __mul__(self, other):
        return Odds(*at_to(self.prob * other.prob))

    def __str__(self):
        return f'{self.at}:{self.to}'

    def __repr__(self):
        return str(self)


def place_str(place):
    if place == 1:
        return '1st'
    elif place == 2:
        return '2nd'
    elif place == 3:
        return '3rd'
    else:
        return f'{place}th'


class EachWay:

    def __init__(self, odds_div, max_place):
        self.odds_div = odds_div
        self.max_place = max_place

    def modify(self, odds):
        at, to = at_to(odds.prob)
        return Odds(at, to * self.odds_div)

    def __str__(self):
        pl_str = f'1st to {place_str(self.max_place)}'
        return f'{pl_str} at 1/{self.odds_div} odds'

    def __repr__(self):
        return str(self)


class Horse:

    def __init__(self, name, odds, each_way):
        self.name = name
        self.odds = odds
        self.each_way = each_way

    def __str__(self):
        ew_str = f'E/W {self.each_way}' if self.each_way else 'no E/W'
        return f'{self.name} ({self.odds}, {ew_str})'

    def __repr__(self):
        return str(self)


def powerset(iterable, min_len=0):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(min_len, 1 + len(s)))


def potential(results):
    total = Fraction(0)
    if all(x[2] == 1 for x in results):
        total += math.prod(1 / x[0].prob for x in results)
    if all(x[2] <= x[1].max_place for x in results):
        total += math.prod(1 / x[1].modify(x[0]).prob for x in results)
    return total


class Lucky:

    def __init__(self, horses):
        self.horses = horses

    def winnings(self, total_bet, places):
        combos = list(powerset(self.horses, 1))
        total = Fraction(0)
        for combo in combos:
            total += potential([(x.odds, x.each_way, places[x.name]) for x in combo])
        individual_bet = Fraction(total_bet) / (2 * len(combos))
        return individual_bet * total


def pounds(frac):
    fp = float(frac)
    return f'£{fp:.2f}'


def main():
    martin_horses = [
        Horse('Etalon', Odds(10, 1), EachWay(5, 5)),
        Horse('Givega', Odds(7, 1), EachWay(5, 5)),
        Horse('Casa No Mento', Odds(11, 4), EachWay(5, 3)),
        Horse('Easy As That', Odds(5, 4), EachWay(4, 2))
    ]

    mark_horses = [
        Horse('Henri The Second', Odds(13, 2), EachWay(5, 5)),
        Horse('Man O Work', Odds(15, 2), EachWay(5, 6)),
        Horse('Dontyawantme', Odds(5, 1), EachWay(5, 3)),
        Horse('Lac De Constance', Odds(5, 1), EachWay(4, 2))
    ]

    paul_horses = [
        Horse('Churchills Boy', Odds(15, 2), EachWay(5, 6)),
        Horse('Playful Saint', Odds(6, 1), EachWay(5, 6)),
        Horse('Larchmont Lass', Odds(5, 1), EachWay(5, 3)),
        Horse('Lac De Constance', Odds(11, 2), EachWay(4, 2))
    ]

    places = {
        'Etalon': 4,
        'Henri The Second': 9,
        'Churchills Boy': 9,

        'Givega': 9,
        'Man O Work': 9,
        'Playful Saint': 3,

        'Casa No Mento': 2,
        'Dontyawantme': 3,
        'Larchmont Lass': 1,

        'Easy As That': 5,
        'Lac De Constance': 4,
    }

    def print_winnings(player, horses, total_bet):
        print(f'{player}: {pounds(total_bet)} -> {pounds(Lucky(horses).winnings(total_bet, places))}')

    print_winnings('Martin', martin_horses, 15)
    print_winnings('Mark', mark_horses, 30)
    print_winnings('Paul', paul_horses, 30)


if __name__ == '__main__':
    main()
