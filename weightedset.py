'''
Weighted set.

Ron Rothman
'''

__version__ = 1.0

import sys
from os import getpid
from time import time
from random import seed, uniform
from bisect import bisect_left
from operator import attrgetter
from collections import namedtuple
from abc import ABCMeta, abstractmethod


__all__ = ['WeightedSet', 'WeightedRandomSetWithReplacement', 'WeightedRandomSetWithoutReplacement', 'Empty']


_DEBUG = False


def _init():
    seed(time() * getpid())


_Entry = namedtuple('_Entry', ['cumulative_weight', 'weight', 'item'])


class Empty(Exception):
    '''Raised when an attempt is made to draw from an empty WeightedSet.'''
    pass


class _WeightedSetBase(object):
    '''Base class for weight sets with and without replacement.'''

    __metaclass__ = ABCMeta

    def __init__(self):
        self.cumulative_weight = 0.0
        self._members = []
        self._is_sorted = False


    @abstractmethod
    def draw(self):
        raise RuntimeError('abstract method')


    def clone(self):
        twin = type(self)()
        twin.cumulative_weight = self.cumulative_weight
        twin._members = self._members[:] # N.B.: NOT a deep copy
        twin._is_sorted = self._is_sorted
        return twin


    def add(self, item, weight):
        weight = float(weight)

        if weight == 0:
            raise ValueError(weight)

        self.cumulative_weight += weight
        self._members.append(_Entry(self.cumulative_weight, weight, item))

        self._is_sorted = False

        return


    def _draw_random_item(self):
        '''returns index into self._members.'''

        rand_val = uniform(0, self.cumulative_weight)

        return self._draw_item_at(rand_val)


    def _draw_item_at(self, float_idx):
        '''returns index into self._members.'''

        assert float_idx <= self.cumulative_weight

        if not self._is_sorted:
            # sort so that:
            # a) we can use bisect to quickly index into the list, and
            # b) larger items are near the back of the list, where they'll
            # cost us less to remove (see _drawWithoutReplacement).
            self._members.sort(key=attrgetter('cumulative_weight'))
            self._is_sorted = True

        # binary search to select an item
        item = bisect_left(self._members, (float_idx, None, None))
        return item


    def __len__(self):
        return len(self._members)


    def __repr__(self):
        return str(vars(self))


    def _check_sanity(self):
        '''Confirm invariants.'''

        if hasattr(self, '_last_item_drawn_idx'):
            assert self._last_item_drawn_idx <= len(self._members), '{} > {}\n{}'.format(self._last_item_drawn_idx, len(self._members), self)

        if self._members:
            assert self._members[-1].cumulative_weight == self.cumulative_weight, '{} != {}\n{}'.format(self._members[-1].cumulative_weight, self.cumulative_weight, self)

        sum_of_weights = sum([x.weight for x in self._members])
        assert sum_of_weights == self.cumulative_weight, '{} != {}\n{}'.format(sum_of_weights, self.cumulative_weight, self)

        for i in range(len(self._members) - 1):
            cur = self._members[i]
            next = self._members[i + 1]
            assert next.cumulative_weight == cur.cumulative_weight + cur.weight, '{}, {}, {}\n{}'.format(i, cur, next, str(self))


class WeightedSet(_WeightedSetBase):
    def __init__(self):
        _WeightedSetBase.__init__(self)

    def draw(self, idx):
        if not self._members:
            raise Empty()

        if idx > self.cumulative_weight:
            raise IndexError(idx)

        return self._members[self._draw_item_at(idx)].item


class WeightedRandomSetWithReplacement(_WeightedSetBase):
    def __init__(self):
        _WeightedSetBase.__init__(self)

    def draw(self):
        if not self._members:
            raise Empty()

        return self._members[self._draw_random_item()].item


class WeightedRandomSetWithoutReplacement(_WeightedSetBase):
    def __init__(self):
        _WeightedSetBase.__init__(self)
        self._last_item_drawn_idx = None


    def clone(self):
        twin = _WeightedSetBase.clone(self)
        twin._last_item_drawn_idx = self._last_item_drawn_idx
        return twin


    def draw(self):
        if not self._members:
            raise Empty()

        if (len(self._members) == 1) and (self._last_item_drawn_idx is not None):
            raise Empty()

        # remove the previous item drawn (JIT)
        if self._last_item_drawn_idx is not None:
            removed_weight = self._members[self._last_item_drawn_idx].weight
            self.cumulative_weight -= removed_weight
            #FIXME: probably slow!
            self._members.pop(self._last_item_drawn_idx)

            # adjust all "downstream" members
            for i in xrange(self._last_item_drawn_idx, len(self._members)):
                orig_entry = self._members[i]

                # replace with a new (adjusted) tuple
                self._members[i] = _Entry(orig_entry.cumulative_weight - removed_weight, orig_entry.weight, orig_entry.item)

        self._last_item_drawn_idx = self._draw_random_item()

        if _DEBUG:
            self._check_sanity()

        return self._members[self._last_item_drawn_idx].item

    def __len__(self):
        return len(self._members) - (0 if self._last_item_drawn_idx is None else 1)



_init()



if __name__ == '__main__':
    '''Usage: python weightedsed.py <weight1> <weight2> ...'''

    num_iters = 1

    for dummy in range(0, num_iters):
        wrs = WeightedRandomSetWithoutReplacement()
        print('created WRS', wrs)

        [wrs.add('<{}>'.format(x), float(x)) for x in sys.argv[1:]]

        for i in range(0, len(wrs)):
            print(' drew', wrs.draw())
