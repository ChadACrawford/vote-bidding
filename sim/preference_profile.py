

class PreferenceProfile:
    def __init__(self, preferences):
        raise NotImplementedError

    @staticmethod
    def summarize(results, candidates):
        raise NotImplementedError

    def set_preference(self, preferences):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class Single(PreferenceProfile):
    def __init__(self, preference):
        self.__candidate = preference

    def set_preference(self, preference):
        self.__candidate = preference

    @staticmethod
    def summarize(results, candidates):
        n = len(candidates)
        score = dict(map(lambda x: (x, 0), candidates))
        for r in results:
            if not isinstance(r, Single):
                raise TypeError
            score[r.candidate] += 1

    @property
    def candidate(self):
        return self.__candidate

    def __repr__(self):
        return "[%s]" % (self.__candidate,)


class Total(PreferenceProfile):
    def __init__(self, preferences):
        self.__candidates = preferences
        self._index = 1

    def set_preference(self, preferences):
        self.__candidates = preferences

    @staticmethod
    def summarize(results, candidates):
        n = len(candidates)
        score = dict(map(lambda x: (x, 0), candidates))
        for r in results:
            if not isinstance(r, Single):
                raise TypeError
            for b in range(n):
                score[r[-b]] += b
        return sorted(score, key=lambda candidate: score[candidate])

    def __getitem__(self, item):
        return self.__candidates[item-1]

    def __iter__(self):
        return self

    def next(self):
        if self._index > len(self.__candidates):
            raise StopIteration
        else:
            self._index += 1
            return self[self._index - 1]

    def __len__(self):
        return len(self.__candidates)

    def __repr__(self):
        return "[%s]" % (','.join(self.__candidates),)
