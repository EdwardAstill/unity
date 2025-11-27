# Unit Database
# Base Dimensions: M=Mass, L=Length, T=Time

UNIT_DB = {
    # Mass (Base: kg)
    "kg": {"scale": 1.0,    "dims": {"M": 1}},
    "g":  {"scale": 1e-3,   "dims": {"M": 1}},
    "mg": {"scale": 1e-6,   "dims": {"M": 1}},
    "t":  {"scale": 1e3,    "dims": {"M": 1}},
    # Imperial Mass
    "lb": {"scale": 0.453592, "dims": {"M": 1}},  # pound
    "oz": {"scale": 0.0283495, "dims": {"M": 1}},  # ounce
    "tn": {"scale": 907.185, "dims": {"M": 1}},  # US ton (short ton)
    "LT": {"scale": 1016.05, "dims": {"M": 1}},  # UK ton (long ton)
    
    # Length (Base: m)
    "m":  {"scale": 1.0,    "dims": {"L": 1}},
    "mm": {"scale": 1e-3,   "dims": {"L": 1}},
    "cm": {"scale": 1e-2,   "dims": {"L": 1}},
    "km": {"scale": 1e3,    "dims": {"L": 1}},
    # Imperial Length
    "in": {"scale": 0.0254, "dims": {"L": 1}},  # inch
    "ft": {"scale": 0.3048, "dims": {"L": 1}},  # foot
    "yd": {"scale": 0.9144, "dims": {"L": 1}},  # yard
    "mi": {"scale": 1609.34, "dims": {"L": 1}},  # mile
    
    # Time (Base: s)
    "s":  {"scale": 1.0,    "dims": {"T": 1}},
    "min":{"scale": 60.0,   "dims": {"T": 1}},
    "h":  {"scale": 3600.0, "dims": {"T": 1}},
    "d":  {"scale": 86400.0, "dims": {"T": 1}},
    "y":  {"scale": 31536000.0, "dims": {"T": 1}},

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
    
    # Pressure: Pa = N / m^2 = kg / (m * s^2)
    "Pa":  {"scale": 1.0,    "dims": {"M": 1, "L": -1, "T": -2}},
    "kPa": {"scale": 1e3,    "dims": {"M": 1, "L": -1, "T": -2}},
    "psi": {"scale": 6894.76, "dims": {"M": 1, "L": -1, "T": -2}},  # pounds per square inch
    
    # Volume (named units only)
    "L":   {"scale": 1e-3,   "dims": {"L": 3}},  # liter
    "mL":  {"scale": 1e-6,   "dims": {"L": 3}},  # milliliter
    "gal": {"scale": 0.00378541, "dims": {"L": 3}},  # US gallon

    
    # Acceleration (named units only)
    "g":   {"scale": 9.80665, "dims": {"L": 1, "T": -2}},  # standard gravity
    
    # Energy/Work: M * L^2 / T^2
    "J":   {"scale": 1.0,    "dims": {"M": 1, "L": 2, "T": -2}},  # joule
    "kJ":  {"scale": 1e3,    "dims": {"M": 1, "L": 2, "T": -2}},
    "MJ":  {"scale": 1e6,    "dims": {"M": 1, "L": 2, "T": -2}},
    "ft_lbf": {"scale": 1.35582, "dims": {"M": 1, "L": 2, "T": -2}},  # foot-pound
    "Btu": {"scale": 1055.06, "dims": {"M": 1, "L": 2, "T": -2}},  # British thermal unit
    
    # Power: M * L^2 / T^3
    "W":   {"scale": 1.0,    "dims": {"M": 1, "L": 2, "T": -3}},  # watt
    "kW":  {"scale": 1e3,    "dims": {"M": 1, "L": 2, "T": -3}},
    "MW":  {"scale": 1e6,    "dims": {"M": 1, "L": 2, "T": -3}},
    "hp":  {"scale": 745.7,  "dims": {"M": 1, "L": 2, "T": -3}},  # horsepower
}

