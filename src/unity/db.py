# Unit Database
# Base Dimensions: M=Mass, L=Length, T=Time

UNIT_DB = {
    # Mass (Base: kg)
    "kg": {"scale": 1.0,    "dims": {"M": 1}},
    "g":  {"scale": 1e-3,   "dims": {"M": 1}},
    "mg": {"scale": 1e-6,   "dims": {"M": 1}},
    "t":  {"scale": 1e3,    "dims": {"M": 1}},
    
    # Length (Base: m)
    "m":  {"scale": 1.0,    "dims": {"L": 1}},
    "mm": {"scale": 1e-3,   "dims": {"L": 1}},
    "cm": {"scale": 1e-2,   "dims": {"L": 1}},
    "km": {"scale": 1e3,    "dims": {"L": 1}},
    
    # Time (Base: s)
    "s":  {"scale": 1.0,    "dims": {"T": 1}},
    "min":{"scale": 60.0,   "dims": {"T": 1}},
    "h":  {"scale": 3600.0, "dims": {"T": 1}},
    
    # Derived / Compound definitions
    # N = kg * m / s^2
    "N":   {"scale": 1.0,    "dims": {"M": 1, "L": 1, "T": -2}},
    "kN":  {"scale": 1e3,    "dims": {"M": 1, "L": 1, "T": -2}},
    # Pa = N / m^2 = kg / (m * s^2)
    "Pa":  {"scale": 1.0,    "dims": {"M": 1, "L": -1, "T": -2}},
    "kPa": {"scale": 1e3,    "dims": {"M": 1, "L": -1, "T": -2}},
}

