# Unit Database
# Base Dimensions: M=Mass, L=Length, T=Time, A=Angle, I=Current, Θ=Temperature

UNIT_DB = {
    # Mass (Base: kg)
    "kg":   {"scale": 1.0,          "dims": {"M": 1}},
    "g":    {"scale": 1e-3,         "dims": {"M": 1}},
    "mg":   {"scale": 1e-6,         "dims": {"M": 1}},
    "ug":   {"scale": 1e-9,         "dims": {"M": 1}},  # microgram
    "ng":   {"scale": 1e-12,        "dims": {"M": 1}},  # nanogram
    "t":    {"scale": 1e3,          "dims": {"M": 1}},
    # Imperial Mass
    "lb":   {"scale": 0.453592,     "dims": {"M": 1}},  # pound
    "oz":   {"scale": 0.0283495,    "dims": {"M": 1}},  # ounce
    "gr":   {"scale": 6.479891e-5,  "dims": {"M": 1}},  # grain
    "st":   {"scale": 6.35029,      "dims": {"M": 1}},  # stone
    "slug": {"scale": 14.5939,      "dims": {"M": 1}},  # slug
    "tn":   {"scale": 907.185,      "dims": {"M": 1}},  # US ton (short ton)
    "LT":   {"scale": 1016.05,      "dims": {"M": 1}},  # UK ton (long ton)
    
    # Length (Base: m)
    "m":   {"scale": 1.0,            "dims": {"L": 1}},
    "mm":  {"scale": 1e-3,           "dims": {"L": 1}},
    "cm":  {"scale": 1e-2,           "dims": {"L": 1}},
    "km":  {"scale": 1e3,            "dims": {"L": 1}},
    "um":  {"scale": 1e-6,           "dims": {"L": 1}},  # micrometer
    "nm":  {"scale": 1e-9,           "dims": {"L": 1}},  # nanometer
    "pm":  {"scale": 1e-12,          "dims": {"L": 1}},  # picometer
    # Imperial Length
    "in":  {"scale": 0.0254,         "dims": {"L": 1}},  # inch
    "ft":  {"scale": 0.3048,         "dims": {"L": 1}},  # foot
    "yd":  {"scale": 0.9144,         "dims": {"L": 1}},  # yard
    "mi":  {"scale": 1609.34,        "dims": {"L": 1}},  # mile
    "nmi": {"scale": 1852.0,         "dims": {"L": 1}},  # nautical mile
    "au":  {"scale": 1.495978707e11, "dims": {"L": 1}},  # astronomical unit
    
    # Time (Base: s)
    "s":   {"scale": 1.0,           "dims": {"T": 1}},
    "ms":  {"scale": 1e-3,          "dims": {"T": 1}},  # millisecond
    "us":  {"scale": 1e-6,          "dims": {"T": 1}},  # microsecond
    "ns":  {"scale": 1e-9,          "dims": {"T": 1}},  # nanosecond
    "ps":  {"scale": 1e-12,         "dims": {"T": 1}},  # picosecond
    "min": {"scale": 60.0,          "dims": {"T": 1}},
    "h":   {"scale": 3600.0,        "dims": {"T": 1}},
    "d":   {"scale": 86400.0,       "dims": {"T": 1}},
    "y":   {"scale": 31536000.0,    "dims": {"T": 1}},

    # Angle (Base: rad)
    "rad": {"scale": 1.0,                  "dims": {"A": 1}},
    "deg": {"scale": 0.017453292519943295, "dims": {"A": 1}}, # pi / 180
    "rev": {"scale": 6.283185307179586,    "dims": {"A": 1}}, # 2 * pi

    # Angular Velocity
    "rpm": {"scale": 0.104719755, "dims": {"A": 1, "T": -1}}, # rev/min

    # Frequency (Base: Hz)
    "Hz": {"scale": 1.0, "dims": {"T": -1}},
    "kHz": {"scale": 1e3, "dims": {"T": -1}},
    "MHz": {"scale": 1e6, "dims": {"T": -1}},
    "GHz": {"scale": 1e9, "dims": {"T": -1}},
    "THz": {"scale": 1e12, "dims": {"T": -1}},
    "PHz": {"scale": 1e15, "dims": {"T": -1}},
    "EHz": {"scale": 1e18, "dims": {"T": -1}},
    "ZHz": {"scale": 1e21, "dims": {"T": -1}},
    # Derived / Compound definitions
    # Force: N = kg * m / s^2
    "N":   {"scale": 1.0,    "dims": {"M": 1, "L": 1, "T": -2}},
    "kN":  {"scale": 1e3,    "dims": {"M": 1, "L": 1, "T": -2}},
    "lbf": {"scale": 4.44822, "dims": {"M": 1, "L": 1, "T": -2}},  # pound-force
    "kip": {"scale": 4448.22, "dims": {"M": 1, "L": 1, "T": -2}},  # kip (1000 lbf)
    
    # Pressure: Pa = N / m^2 = kg / (m * s^2)
    "Pa":   {"scale": 1.0,        "dims": {"M": 1, "L": -1, "T": -2}},
    "kPa":  {"scale": 1e3,        "dims": {"M": 1, "L": -1, "T": -2}},
    "MPa":  {"scale": 1e6,        "dims": {"M": 1, "L": -1, "T": -2}},
    "GPa":  {"scale": 1e9,        "dims": {"M": 1, "L": -1, "T": -2}},
    "bar":  {"scale": 1e5,        "dims": {"M": 1, "L": -1, "T": -2}},
    "mbar": {"scale": 1e2,        "dims": {"M": 1, "L": -1, "T": -2}},
    "atm":  {"scale": 101325.0,   "dims": {"M": 1, "L": -1, "T": -2}},
    "torr": {"scale": 133.322,    "dims": {"M": 1, "L": -1, "T": -2}},
    "psi":  {"scale": 6894.76,    "dims": {"M": 1, "L": -1, "T": -2}},  # pounds per square inch
    "ksi":  {"scale": 6894760.0,  "dims": {"M": 1, "L": -1, "T": -2}},  # kips per square inch
    
    # Volume (named units only)
    "L":   {"scale": 1e-3,   "dims": {"L": 3}},  # liter
    "mL":  {"scale": 1e-6,   "dims": {"L": 3}},  # milliliter
    "gal": {"scale": 0.00378541, "dims": {"L": 3}},  # US gallon

    
    # Acceleration (named units only)
    "gn":   {"scale": 9.80665, "dims": {"L": 1, "T": -2}},  # standard gravity
    
    # Energy/Work: M * L^2 / T^2
    "J":    {"scale": 1.0,              "dims": {"M": 1, "L": 2, "T": -2}},  # joule
    "mJ":   {"scale": 1e-3,             "dims": {"M": 1, "L": 2, "T": -2}},
    "kJ":   {"scale": 1e3,              "dims": {"M": 1, "L": 2, "T": -2}},
    "MJ":   {"scale": 1e6,              "dims": {"M": 1, "L": 2, "T": -2}},
    "GJ":   {"scale": 1e9,              "dims": {"M": 1, "L": 2, "T": -2}},
    "Wh":   {"scale": 3600.0,           "dims": {"M": 1, "L": 2, "T": -2}},  # watt-hour
    "kWh":  {"scale": 3.6e6,            "dims": {"M": 1, "L": 2, "T": -2}},
    "MWh":  {"scale": 3.6e9,            "dims": {"M": 1, "L": 2, "T": -2}},
    "eV":   {"scale": 1.602176634e-19,  "dims": {"M": 1, "L": 2, "T": -2}},  # electron-volt
    "keV":  {"scale": 1.602176634e-16,  "dims": {"M": 1, "L": 2, "T": -2}},
    "MeV":  {"scale": 1.602176634e-13,  "dims": {"M": 1, "L": 2, "T": -2}},
    "GeV":  {"scale": 1.602176634e-10,  "dims": {"M": 1, "L": 2, "T": -2}},
    "cal":  {"scale": 4.184,            "dims": {"M": 1, "L": 2, "T": -2}},  # thermochemical calorie
    "kcal": {"scale": 4184.0,           "dims": {"M": 1, "L": 2, "T": -2}},
    "ft_lbf": {"scale": 1.35582,        "dims": {"M": 1, "L": 2, "T": -2}},  # foot-pound (NOTE: underscore breaks parser — use "lbf ft" with a space)
    "Btu":  {"scale": 1055.06,          "dims": {"M": 1, "L": 2, "T": -2}},  # British thermal unit
    
    # Power: M * L^2 / T^3
    "W":   {"scale": 1.0,    "dims": {"M": 1, "L": 2, "T": -3}},  # watt
    "mW":  {"scale": 1e-3,   "dims": {"M": 1, "L": 2, "T": -3}},
    "kW":  {"scale": 1e3,    "dims": {"M": 1, "L": 2, "T": -3}},
    "MW":  {"scale": 1e6,    "dims": {"M": 1, "L": 2, "T": -3}},
    "GW":  {"scale": 1e9,    "dims": {"M": 1, "L": 2, "T": -3}},
    "TW":  {"scale": 1e12,   "dims": {"M": 1, "L": 2, "T": -3}},
    "hp":  {"scale": 745.7,  "dims": {"M": 1, "L": 2, "T": -3}},  # horsepower

    # Volume (named units only)
    "uL":  {"scale": 1e-9,      "dims": {"L": 3}},  # microlitre
    "pt":  {"scale": 4.73176e-4, "dims": {"L": 3}},  # US pint
    "qt":  {"scale": 9.46353e-4, "dims": {"L": 3}},  # US quart
    "bbl": {"scale": 0.158987,   "dims": {"L": 3}},  # oil barrel

    # Temperature (Base: K — offset units °C/°F not supported)
    "K":   {"scale": 1.0,    "dims": {"Theta": 1}},  # kelvin
    "mK":  {"scale": 1e-3,   "dims": {"Theta": 1}},  # millikelvin

    # Electric Current (Base: A)
    "A":    {"scale": 1.0,   "dims": {"I": 1}},  # ampere
    "mA":   {"scale": 1e-3,  "dims": {"I": 1}},
    "uA":   {"scale": 1e-6,  "dims": {"I": 1}},
    "kA":   {"scale": 1e3,   "dims": {"I": 1}},

    # Voltage: M * L^2 * T^-3 * I^-1
    "V":    {"scale": 1.0,   "dims": {"M": 1, "L": 2, "T": -3, "I": -1}},  # volt
    "mV":   {"scale": 1e-3,  "dims": {"M": 1, "L": 2, "T": -3, "I": -1}},
    "kV":   {"scale": 1e3,   "dims": {"M": 1, "L": 2, "T": -3, "I": -1}},
    "MV":   {"scale": 1e6,   "dims": {"M": 1, "L": 2, "T": -3, "I": -1}},

    # Resistance: M * L^2 * T^-3 * I^-2
    "ohm":  {"scale": 1.0,   "dims": {"M": 1, "L": 2, "T": -3, "I": -2}},  # ohm (Ω)
    "kohm": {"scale": 1e3,   "dims": {"M": 1, "L": 2, "T": -3, "I": -2}},
    "Mohm": {"scale": 1e6,   "dims": {"M": 1, "L": 2, "T": -3, "I": -2}},

    # Capacitance: M^-1 * L^-2 * T^4 * I^2
    "F":    {"scale": 1.0,   "dims": {"M": -1, "L": -2, "T": 4, "I": 2}},  # farad
    "mF":   {"scale": 1e-3,  "dims": {"M": -1, "L": -2, "T": 4, "I": 2}},
    "uF":   {"scale": 1e-6,  "dims": {"M": -1, "L": -2, "T": 4, "I": 2}},
    "nF":   {"scale": 1e-9,  "dims": {"M": -1, "L": -2, "T": 4, "I": 2}},
    "pF":   {"scale": 1e-12, "dims": {"M": -1, "L": -2, "T": 4, "I": 2}},

    # Inductance: M * L^2 * T^-2 * I^-2
    "H":    {"scale": 1.0,   "dims": {"M": 1, "L": 2, "T": -2, "I": -2}},  # henry
    "mH":   {"scale": 1e-3,  "dims": {"M": 1, "L": 2, "T": -2, "I": -2}},
    "uH":   {"scale": 1e-6,  "dims": {"M": 1, "L": 2, "T": -2, "I": -2}},
    "nH":   {"scale": 1e-9,  "dims": {"M": 1, "L": 2, "T": -2, "I": -2}},

    # Charge: T * I
    "C":    {"scale": 1.0,   "dims": {"T": 1, "I": 1}},  # coulomb
    "mC":   {"scale": 1e-3,  "dims": {"T": 1, "I": 1}},
    "uC":   {"scale": 1e-6,  "dims": {"T": 1, "I": 1}},
    "nC":   {"scale": 1e-9,  "dims": {"T": 1, "I": 1}},
}

