import sys
import os

# Add the src directory to the python path so we can import the unity module
# This allows running the example without installing the package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unity.main import Quantity, conv, valid

def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def basic_conversions():
    print_header("1. Basic Unit Conversions")
    
    # Simple Length
    val = 1000
    res = conv(val, "m", "km")
    print(f"{val} m = {res} km")

    # Mass
    val = 1
    res = conv(val, "kg", "lb")
    print(f"{val} kg = {res:.4f} lb")
    
    # Temperature / Pressure (Derived)
    val = 101325
    res = conv(val, "Pa", "psi")
    print(f"{val} Pa = {res:.2f} psi")

def quantity_basics():
    print_header("2. Quantity Objects")
    
    q1 = Quantity(5, "km")
    print(f"Created Quantity: {q1}")
    
    q2 = q1.to("m")
    print(f"Converted to meters: {q2}")
    
    q3 = Quantity(100, "psi")
    print(f"Pressure: {q3}")
    print(f"Pressure in kPa: {q3.to('kPa')}")

def quantity_arithmetic():
    print_header("3. Quantity Arithmetic")
    
    # Addition
    d1 = Quantity(10, "m")
    d2 = Quantity(50, "cm")
    d3 = d1 + d2
    print(f"Addition: {d1} + {d2} = {d3}")
    
    # Subtraction
    t1 = Quantity(1, "h")
    t2 = Quantity(30, "min")
    t3 = t1 - t2
    print(f"Subtraction: {t1} - {t2} = {t3}")
    
    # Multiplication
    f = Quantity(10, "N")
    d = Quantity(5, "m")
    w = f * d
    print(f"Multiplication (Work): {f} * {d} = {w}")
    # We can try to convert the result (N m) to Joules (J) if we implement that logic or just check validity
    # Currently conv() handles units, let's see if we can convert 'N m' to 'J'
    try:
        w_joules = w.to("J")
        print(f"  -> In Joules: {w_joules}")
    except Exception as e:
        print(f"  -> Could not convert to J: {e}")

    # Division
    dist = Quantity(100, "m")
    time = Quantity(9.58, "s")
    speed = dist / time
    print(f"Division (Speed): {dist} / {time} = {speed}")

def error_handling():
    print_header("4. Error Handling")
    
    print("Attempting to add incompatible units (m + kg)...")
    try:
        q1 = Quantity(1, "m")
        q2 = Quantity(1, "kg")
        q3 = q1 + q2
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("\nChecking validity directly:")
    print(f"Is 'm' compatible with 's'? {valid('m', 's')}")
    print(f"Is 'N' compatible with 'kg m s-2'? {valid('N', 'kg m s-2')}")

if __name__ == "__main__":
    basic_conversions()
    quantity_basics()
    quantity_arithmetic()
    error_handling()

