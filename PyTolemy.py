# 9/1 Created class Sexigesimal, __init__, __repr__, print_60, print_10. Created convert_to_sexigesimal.
# Want to put in the degree symbol, interface, work on arc/chord stuff later.
# 9/2 Created interface. Intro, dec-sex and sex-dec conversion functions. Created chord function,
# solved issue where IT WAS IN RADIANS THE WHOLE TIME. Added graphix. Added non-prompt versions of all functions.
# Added a prompt for sexigesimal chord, but it does not output to sexigesimal.
# 9/4 Changed chord table sexigesimal output to be sexigesimal.
# Do I want this to be a standalone program or a library? Addition/subtraction/more tools might be easier in a library...

# Still want to add: Conversion between sun's days and motion around the circle (365/360), easy addition/subtraction of the results, reverse chords.
# I might want to clean up: The Sexigesimal class, so that all the conversions could be accomplished within the class.
# I might consider: Writing a TI-84 BASIC program for these conversions, for portability.

# -*- coding: utf-8 -*-

from math import sin, radians

class Sexigesimal:
    """Represents a sexigesimal number.
    Attributes: degrees, minutes, seconds.
    Can instantiate with DMS or a decimal."""
    def __init__(self, degrees, minutes=0, seconds=0):
        if degrees % 1 == 0:
            self.degrees = degrees
            self.minutes = minutes
            self.seconds = seconds
        else:
            self.degrees = degrees // 1
            self.minutes = ((degrees - self.degrees) * 60.00) // 1
            self.seconds = ((((degrees - self.degrees) * 60.00) - self.minutes) * 60.00) // 1

    def __repr__(self):
        return "%d * %d ' %d \"" % (self.degrees, self.minutes, self.seconds)

    def convert_to_10(self):
        decimal = 0.000000
        decimal += self.degrees // 1
        decimal += (self.minutes / 60.00)
        decimal += (self.seconds / 60.00**2)
        return decimal


def convert_10to60(n):		
	degrees = n // 1
	minutes = ((n - degrees) * 60.00) // 1
	seconds = ((((n - degrees) * 60.00) - minutes) * 60.00) // 1
	return Sexigesimal(degrees, minutes, seconds)
	
def prompt_10to60():
	print "Enter your decimal value."
	while True:
		n = raw_input("> ")
		if 'q' in n:
			intro()
		else:
			n = float(n)
		degrees = n // 1
		minutes = ((n - degrees) * 60.00) // 1
		seconds = ((((n - degrees) * 60.00) - minutes) * 60.00) // 1
		print "\t", Sexigesimal(degrees, minutes, seconds)
		print "Enter another decimal value or (q) to quit."

def convert_60to10(n): 
	decimal = 0.000000
	decimal += n.degrees // 1
	decimal += (n.minutes / 60.00)
	decimal += (n.seconds / 60.00**2)
	return decimal


def prompt_60to10():
    print "Enter your sexigesimal value in degrees, minutes, and seconds."
    while True:
        degrees = raw_input("degrees = ")
        if 'q' in degrees:
            intro()
        else:
            degrees = int(degrees)
        minutes = int(raw_input("minutes = "))
        seconds = int(raw_input("seconds = "))
        output = Sexigesimal(degrees, minutes, seconds)
        print output.convert_to_10()
        print "Enter another degree-value or (q) to quit."


def convert_chord(arc):
    return sin(radians(arc / 2)) * 120


def prompt_chord_decimal():
    print "Enter the decimal value of your arc to find the chord."
    while True:
        arc = raw_input("arc = ")
        if 'q' in arc:
            intro()
		else:
			arc = float(arc)
		chord = sin(radians(arc / 2)) * 120
		print "\t", chord
		print "Enter another arc or (q) to quit."
		
		"""The chord is equal to half the sine of twice the arc.
		"""
def prompt_chord_sexigesimal():
	print "Enter the sexigesimal value of your arc to find the chord."
	while True:
		degrees = raw_input("degrees = ")
		if 'q' in degrees:
			intro()
		else:
			degrees = int(degrees)
		minutes = int(raw_input("minutes = "))
		seconds = int(raw_input("seconds = "))
		output = Sexigesimal(degrees, minutes, seconds)
		arc = output.convert_to_10()
        chord = sin(radians(arc / 2)) * 120
        print "\t", convert_10to60(chord)
        print "Enter another arc or (q) to quit."
        """The chord is equal to half the sine of twice the arc."""

def intro():
	print """
  ___     _____ ___  _    ___ __  ____   __\t
 | _ \_  |_   _/ _ \| |  | __|  \/  \ \ / /\t
 |  _/ || || || (_) | |__| _|| |\/| |\ V / \t
 |_|  \_, ||_| \___/|____|___|_|  |_| |_|  \t
      |__/                                 \t"""
	print "Max Silbiger made this. ver 9/5"
	print "\ta) Sexigecimal to Decimal"
	print "\tb) Decimal to Sexigecimal"
	print "\tc) Arc to Chord (Decimal)"
	print "\td) Arc to Chord (Sexigesimal)"
	conversion_mode = raw_input("> ")
	if "a" in conversion_mode.lower():
		prompt_60to10()
	elif "b" in conversion_mode.lower():
		prompt_10to60()
	elif "c" in conversion_mode.lower():
		prompt_chord_decimal()
	elif "d" in conversion_mode.lower():
		prompt_chord_sexigesimal()
	else:
		pass

if __name__ == '__main__':
    intro()
