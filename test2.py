from mutable_hl_tl import MutableHLTM
import number_encoders

mtm1 = MutableHLTM(100, number_encoders.unary, 1)
f = open("graf1.dot", "w")
f.write(mtm1.get_machine().to_dot())

mtm2 = MutableHLTM(100, number_encoders.unary, 1)
f = open("graf2.dot", "w")
f.write(mtm2.get_machine().to_dot())

f = open("graf3.dot", "w")
f.write((mtm1 * mtm2).get_machine().to_dot())
