from PyTolemy import *

simple_value = Sexigesimal(50, 40, 30)
integer_value = Sexigesimal(20, 0, 0)


print "Testing Sexigesimal object initialization with degrees/minutes/seconds."
print (simple_value.degrees, simple_value.minutes, simple_value.seconds) == (50, 40, 30)

print "Testing initialization with decimal numbers."
test_b = Sexigesimal(14.5)
print (test_b.degrees, test_b.minutes, test_b.seconds) == (14, 30, 0)

test_c = Sexigesimal(14.50833333333)
print (test_c.degrees, test_c.minutes, test_c.seconds) == (14, 30, 30)

test_d = Sexigesimal(14)
print (test_d.degrees), test_d.minutes, test_d.seconds) == (14, 0, 0)

print "Testing retrieving the decimal representation of a Sexigesimal."
print test_b.decimal() == 14.5
print test_c.decimal() == 14.5083333333 # Careful with this one.
print test_d_decimal() ==