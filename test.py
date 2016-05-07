from turing_machine import TuringMachine, EmptyChar as e

transition = {
	(1, 0):   (2, e, "R"),
	(1, "x"): (7, "x", "R"),
	(1, e):   (7, e, "R"),
	(2, 0):   (3, "x", "R"),
	(2, "x"): (2, "x", "R"),
	(2, e):   (6, e, "R"),
	(3, 0):   (4, 0, "R"),
	(3, "x"): (3, "x", "R"),
	(3, e):   (5, e, "L"),
	(4, 0):   (3, "x", "R"),
	(4, "x"): (4, "x", "R"),
	(4, e):   (7, e, "R"),
	(5, 0):   (5, 0, "L"),
	(5, "x"): (5, "x", "L"),
	(5, e):   (2, e, "R"),
}

t = TuringMachine(range(1, 7), [0], [0, "x", e], transition, 1, 6, 7)
print(t.to_dot())
