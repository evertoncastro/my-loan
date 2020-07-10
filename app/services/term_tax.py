
class TermTaxes:

    def __init__(self, _6: float, _9: float, _12: float):
        self._6 = _6
        self._9 = _9
        self._12 = _12
        self._order = [6, 9, 12]

    def get_tax_by_term(self, term: int):
        try:
            return getattr(self, f'_{term}')
        except AttributeError:
            raise Exception('Invalid term')

    def get_next_term(self, term: int):
        return next((t for t in self._order if t > term), None)


class Range:

    def __init__(self, _min: int, _max: int, term_taxes: TermTaxes):
        self._min_score = _min
        self._max_score = _max
        self._term_taxes = term_taxes

    @property
    def min_score(self):
        return self._min_score

    @property
    def max_score(self):
        return self._max_score

    @property
    def term_taxes(self):
        return self._term_taxes

    def __repr__(self):
        return f'{self._min_score, self._max_score, self._term}'


class ScoreTermTaxes:

    __ranges = [
        Range(600, 699, TermTaxes(6.4, 6.6, 6.9)),
        Range(700, 799, TermTaxes(5.5, 5.8, 6.1)),
        Range(800, 899, TermTaxes(4.7, 5.0, 5.3)),
        Range(900, 1000, TermTaxes(3.9, 4.2, 4.5))
    ]

    def get_by_score(self, score: int):
        if score < 600 or score > 1000:
            raise Exception('Invalid score')
        return next(
            (t.term_taxes for t in self.__ranges
                if t.min_score <= score <= t.max_score),
            None
        )
