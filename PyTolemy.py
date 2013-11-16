# This library is designed to aid in recreating Ptolemy's astronomical calculations in the Almagest,
# which are done exclusively in sexigesimal numbers for his angles and lengths. His lengths, too, are
# derived from "chords", which are in modern terms the sine of half the angle, and are related to a
# unit circle with length 120.

# The conversions generally happen in the various methods of the Sexigesimal class, but there is also
# a primitive interface which can perform these calculations.

# Still want to add: reverse chords, zodiac.

# -*- coding: utf-8 -*-

from math import sin, radians

SOLAR_DAYS_PER_DEGREE = (365.25/360.00)
DIAMETER_OF_CIRCLE = 120                            # Circle diameter is divided into 120 "parts" by Ptolemy.

class Sexigesimal:
    """Represents a sexigesimal number.
    Attributes: degrees, minutes, seconds.
    Can instantiate with DMS or a decimal."""
    def __init__(self, degrees, minutes=0, seconds=0):
        if degrees % 1 == 0:        # Accepting DMS values.
            self.degrees = degrees
            self.minutes = minutes % 60                   # Too-large values handled differently than in __add__,
            self.seconds = seconds % 60                   # since only user error can create them here.
        else:                       # Accepting decimal values.
            self.degrees = degrees // 1
            self.minutes = ((degrees - self.degrees) * 60.00) // 1
            self.seconds = ((((degrees - self.degrees) * 60.00) - self.minutes) * 60.00) // 1

    def __repr__(self):
        return "%d * %d ' %d \"" % (self.degrees, self.minutes, self.seconds)

    def decimal(self):
        decimal = 0.000000
        decimal += self.degrees // 1
        decimal += (self.minutes / 60.00)
        decimal += (self.seconds / 60.00**2)
        return decimal

    def days(self):
        return decimal(self) * SOLAR_DAYS_PER_DEGREE

    def __add__(self, x):   # Supports x as a Sexigesimal.
        carry_sec = 0
        carry_min = 0
        sec = self.seconds + x.seconds
        while sec >= 60:
            sec -= 60
            carry_sec += 1
        min = self.minutes + x.minutes + carry_sec
        while min >= 60:
            min -= 60
            carry_min += 1
        deg = (self.degrees + x.degrees + carry_min) // 360
        return Sexigesimal(deg, min, sec)

    def __mul__(self, x):  # Supports x as a decimal number. Not sure if multiplying Sexigesimals is useful to support.
        carry_sec = 0
        carry_min = 0
        sec = self.seconds * x
        while sec >= 60:
            sec -= 60
            carry_sec += 1
        min = (self.minutes * x) + carry_sec
        while min >= 60:
            min -= 60
            carry_min += 1
        deg = ((self.degrees * x) + carry_min) // 60
        return Sexigesimal(deg, min, sec)




def prompt_10to60():
    print "Enter your decimal value."
    while True:
        n = raw_input("> ")
        if 'q' in n:
            interface()
        else:
            n = float(n)
        degrees = n // 1
        minutes = ((n - degrees) * 60.00) // 1
        seconds = ((((n - degrees) * 60.00) - minutes) * 60.00) // 1
        print "\t", Sexigesimal(degrees, minutes, seconds)
        print "Enter another decimal value or (q) to quit."

def convert_60to10(n):           # Currently only used in the arc/chord function.
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
            interface()
        else:
            degrees = int(degrees)
        minutes = int(raw_input("minutes = "))
        seconds = int(raw_input("seconds = "))
        output = Sexigesimal(degrees, minutes, seconds)
        print output.decimal()
        print "Enter another degree-value or (q) to quit."


def convert_chord(arc):
    return sin(radians(arc / 2)) * 120


def prompt_chord_decimal():
    print "Enter the decimal value of your arc to find the chord."
    while True:
        arc = raw_input("arc = ")
        if 'q' in arc:
            interface()
        else:
            arc = float(arc)
        chord = sin(radians(arc / 2)) * DIAMETER_OF_CIRCLE
        print "\t", chord
        print "Enter another arc or (q) to quit."


def prompt_chord_sexigesimal():
    print "Enter the sexigesimal value of your arc to find the chord."
    while True:
        degrees = raw_input("degrees = ")
        if 'q' in degrees:
            interface()
        else:
            degrees = int(degrees)
        minutes = int(raw_input("minutes = "))
        seconds = int(raw_input("seconds = "))
        output = Sexigesimal(degrees, minutes, seconds)
        arc = output.decimal()
        chord = sin(radians(arc / 2)) * DIAMETER_OF_CIRCLE
        print "\t", convert_10to60(chord)
        print "Enter another arc or (q) to quit."
        """The chord is equal to half the sine of twice the arc."""


def interface():
    print """
  ___     _____ ___  _    ___ __  ____   __\t
 | _ \_  |_   _/ _ \| |  | __|  \/  \ \ / /\t
 |  _/ || || || (_) | |__| _|| |\/| |\ V / \t
 |_|  \_, ||_| \___/|____|___|_|  |_| |_|  \t
      |__/                                 \t"""
    print "Max Silbiger made this. ver 11/11"
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

if __name__ == '__main__':     # Helps separate interface/implementation.
    interface()
