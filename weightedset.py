'''
Weighted set.

Ron Rothman
'''

__version__ = 1.0

import sys
import copy
from os import getpid
from time import time
from random import seed, uniform
from bisect import bisect_left
from operator import attrgetter
from collections import namedtuple
from abc import ABCMeta, abstractmethod
from functools import reduce


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

	def __init__(self, weight_function):
		self.cumulative_weight = 0.0
		self._members = []
		self._is_sorted = False
		self.weight_function = weight_function


	@abstractmethod
	def draw(self):
		raise RuntimeError('abstract method')


	def clone(self):
		twin = type(self)()
		twin.cumulative_weight = self.cumulative_weight
		twin._members = self._members[:] # N.B.: NOT a deep copy
		twin._is_sorted = self._is_sorted
		return twin


	def add(self, item):
		weight = float(self.weight_function(item))

		if weight == 0:
			# raise ValueError(weight)
			return

		self.cumulative_weight += weight
		self._members.append(_Entry(self.cumulative_weight, weight, copy.copy(item)))

		self._is_sorted = False

		return


	def _draw_random_item(self):
		'''returns index into self._members.'''

		self.sort()

		rand_val = uniform(0, self.cumulative_weight)

		return self._draw_item_at(rand_val)


	def _draw_item_at(self, float_idx):

		self.sort()

		'''returns index into self._members.'''

		assert float_idx <= self.cumulative_weight
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

	def __getitem__(self, index):
		self.sort()
		print("__getitem__: returning", self._members[index])
		return self._members[index][2]

	def __contains__(self, element):
		return element in map(lambda member: member[2], self._members)

	def sort(self):
		if not self._is_sorted:

			# print("\nitems before sort:", list(map(lambda m:m[2], self._members)))

			self._members.sort(key=attrgetter("weight"))
			self._members.reverse()
			print(list(map(lambda e: e[1], self._members)))

			self.cumulative_weight = 0
			for key in range(len(self._members)):
				value = self._members[key]
				weight = value.weight
				self.cumulative_weight += weight
				new_value = _Entry(self.cumulative_weight, weight, value.item)
				self._members[key] = new_value

			self._is_sorted = True

			# print("\nitems after sort:", list(map(lambda m:m[2], self._members)))

	def trim(self, amount):
		print("\nactual before trim:", list(map(self.weight_function, list(map(lambda m:m[2], self._members)))))
		self.sort()
		self._members = self._members[:amount]
		self.cumulative_weight = self._members[-1].cumulative_weight
		print("\nactual after trim:", list(map(self.weight_function, list(map(lambda m:m[2], self._members)))), "\n")


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
	def __init__(self, weight_function):
		_WeightedSetBase.__init__(self, weight_function)

	def draw(self):
		if not self._members:
			raise Empty()

		return self._members[self._draw_random_item()].item


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
