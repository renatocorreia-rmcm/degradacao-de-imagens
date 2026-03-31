from __future__ import annotations  # allow to reference type class inside herself

import math
from math import log, floor
from typing import Union

# MACHINE SETTINGS
b = 10
t = 4
k1 = -3
k2 = 3


class Fl:
	"""
    Type class for representable floats inside small machine
    Closed for math operations
    """

	value: float

	# used in representation only

	sinal: int
	m: float
	e: int

	def __init__(self, x):

		if isinstance(x, Fl):  # avoid redundancy in parsing
			self.value = x.value
			self.sinal = x.sinal
			self.m = x.m
			self.e = x.e
			return

		# absolute zero
		if x == 0:
			self.value = 0
			return
		if math.isinf(x):
			self.value = x
			return

		# other cases

		# scientific notation
		self.sinal = -1 if x < 0 else 1
		x = abs(x)
		self.e = int(floor(log(x, b))) + 1
		self.m = x / (b ** self.e)
		self.m = round(self.m, t)  # todo: allow truncation
		if self.m >= 1:
			self.m /= b
			self.e += 1

		# infinite
		if self.e > k2:
			self.value = float('inf')
			return
		# zero
		if self.e < k1:
			self.value = 0
			return

		# ordinary representable
		self.value = self.sinal * self.m * (b ** self.e)
		return

	def __add__(self, other):
		if isinstance(other, Fl):
			return Fl(self.value + other.value)

		return self.__add__(Fl(other))

	def __radd__(self, other):
		return self.__add__(other)

	def __neg__(self):
		return Fl(-self.value)

	def __sub__(self, other):
		return self.__add__(-other)

	def __rsub__(self, other):
		return (-self).__add__(other)

	def __mul__(self, other):
		if isinstance(other, Fl):
			return Fl(self.value.__mul__(other.value))
		return self.__mul__(Fl(other))

	def __rmul__(self, other):
		return self.__mul__(other)

	def __truediv__(self, other):
		if isinstance(other, Fl):
			return Fl(self.value / other.value)
		return self.__truediv__(Fl(other))

	def __rtruediv__(self, other):
		if isinstance(other, Fl):
			return Fl(other.value / self.value)
		return Fl(other).__truediv__(self)

	def __repr__(self):
		if self.value == float('inf') or self.value == 0:
			return str(self.value)
		return f"{'-' if self.sinal == -1 else '+'}{self.m}{(t+2-len(str(self.m)))*'0'}*{b}^{self.e}"  # todo: optimize trailling zeros format

	def __eq__(self, other):
		if isinstance(other, Fl):
			return Fl(other.value == self.value)
		return Fl(other).__eq__(self)

	def __ne__(self, other):
		if isinstance(other, Fl):
			return Fl(other.value != self.value)
		return Fl(other).__ne__(self)

	def __gt__(self, other):
		if isinstance(other, Fl):
			return Fl(other.value > self.value)
		return Fl(other).__gt__(self)

	def __ge__(self, other):
		if isinstance(other, Fl):
			return Fl(other.value >= self.value)
		return Fl(other).__ge__(self)
	
	def __lt__(self, other):
		if isinstance(other, Fl):
			return Fl(other.value < self.value)
		return Fl(other).__lt__(self)

	def __le__(self, other):
		if isinstance(other, Fl):
			return Fl(other.value <= self.value)
		return Fl(other).__le__(self)