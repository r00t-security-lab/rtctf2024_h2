from z3 import *

a,b,c,d,e = Ints('a b c d e')
solver = Solver()
solver.add(a * -32 + b * 90 + c * 98 + d * 23 + e * 55 == 333322)
solver.add(a * -322 + b * 32 + c * 68 + d * 123 + e * 67 == 707724)
solver.add(a * -34 + b * 32 + c * 43 + d * 266 + e * 8 == 1272529)
solver.add(a * -352 + b * 5 + c * 58 + d * 343 + e * 65 == 1672457)
solver.add(a * -321 + b * 970 + c * 938 + d * 231 + e * 555 == 3372367)

solver.check()
print(solver.model())
