# This library is designed to aid in recreating Ptolemy's astronomical calculations in the Almagest,
# which are done exclusively in sexigesimal numbers for his angles and lengths. His lengths, too, are
# derived from "chords", which are in modern terms the sine of half the angle, and are related to a
# unit circle with length 120.

# The conversions generally happen in the various methods of the Sexigesimal class, but there is also
# a primitive interface which can perform these calculations.

# -*- coding: utf-8 -*-

from math import sin, radians, asin

SOLAR_DAYS_PER_DEGREE = (365.25/360.00)
DIAMETER_OF_CIRCLE = 120                            # Circle diameter is divided into 120 "parts" by Ptolemy.
zodiac = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
          "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

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

    def chord(self):
        return sin(radians(Sexigesimal.decimal(self) / 2)) * DIAMETER_OF_CIRCLE

    def days(self):
        return Sexigesimal.decimal(self) * SOLAR_DAYS_PER_DEGREE

    def zodiac(self):                            # Attribute of the object? No. only generated on demand.
        sign = zodiac[self.degrees / 30]         # Each zodiac sign represents 30 degrees of the circle.
        degrees_into_sign = self.degrees / 30    # (Both kinds of division do the same thing to an int.)
        return "%s %d * %d ' %d \"" % (sign, degrees_into_sign, self.minutes, self.seconds)

    def __add__(self, x):
        if x.degrees:              # If x is a Sexigesimal, it has this attribute.
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
        else:                      # If x is a decimal, make it into a Sexigesimal.
            self + Sexigesimal(x)


    def __sub__(self, x):
        if x.degrees:
            carry_sec = 0
            carry_min = 0
            sec = self.seconds - x.seconds
            while sec <= 0:                       # Do I need to check for the >60 case here?
                sec += 60
                carry_sec -= 1
            min = self.minutes - x.minutes + carry_sec
            while min <= 0:
                min += 60
                carry_min -= 1
            deg = (self.degrees - x.degrees + carry_min) // 360
            if deg < 0:
                return Sexigesimal(360) - self    # Needs testing.
            else:
                return Sexigesimal(deg, min, sec)
        else:
            self - Sexigesimal(x)


    def __mul__(self, x):  # Supports x as a decimal number. Not sure if multiplying Sexigesimals is useful.
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
        print "\t", Sexigesimal(n)
        print "Enter another decimal value or (q) to quit."


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


def convert_arc(chord):
    return Sexigesimal(asin(radians(chord / DIAMETER_OF_CIRCLE)) * 2)

def prompt_chord_decimal():
    print "Enter the decimal value of your arc to find the chord."
    while True:
        arc = raw_input("arc = ")
        if 'q' in arc:
            interface()
        else:
            arc = Sexigesimal(arc)
        chord = arc.chord()
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
        arc = Sexigesimal(degrees, minutes, seconds)
        chord = arc.chord()
        print "\t", Sexigesimal(chord)
        print "Enter another arc or (q) to quit."
        """The chord is equal to half the sine of twice the arc."""

def prompt_angle_zodiac():
    print "Enter the degree value of the arc to find its position in the zodiac, starting at 0 Aries."
    while True:
        degrees = raw_input("degrees = ")
        if 'q' in degrees:
            interface()
        degrees_value = float(degrees)
        print Sexigesimal(degrees_value).zodiac()
        print "Enter another value or (q) to quit."


def prompt_angle_days():
    print "Enter the degree value of the arc to find the number of solar days traversed within it."
    while True:
        degrees = raw_input("degrees = ")
        if 'q' in degrees:
            interface()
        degrees = float(degrees)
        minutes = int(raw_input("minutes = "))
        seconds = int(raw_input("seconds = "))
        print Sexigesimal(degrees, minutes, seconds).days()


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
    print "\te) Angle to Zodiac"
    print "\tf) Angle to Solar Days"
    conversion_mode = raw_input("> ")
    if "a" in conversion_mode.lower():
        prompt_60to10()
    elif "b" in conversion_mode.lower():
        prompt_10to60()
    elif "c" in conversion_mode.lower():
        prompt_chord_decimal()
    elif "d" in conversion_mode.lower():
        prompt_chord_sexigesimal()
    elif "e" in conversion_mode.lower():
        prompt_angle_zodiac()
    elif "f" in conversion_mode.lower():
        prompt_angle_days()
    else:
        pass

if __name__ == '__main__':     # Helps separate interface/implementation.
    interface()