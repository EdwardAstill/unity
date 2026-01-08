from unity import Quantity
import numpy as np

def main() -> None:
    print("=== Angle Support Demo ===\n")

    # 1. Basic Angle Conversions
    theta = Quantity(180, "deg")
    print(f"Angle: {theta}")
    print(f"In radians: {theta.to('rad')}")
    print(f"In revolutions: {theta.to('rev')}")
    print("-" * 30)

    # 2. Angular Velocity
    # 3000 RPM to rad/s
    omega_rpm = Quantity(3000, "rpm")
    omega_rad_s = omega_rpm.to("rad s-1")
    print(f"Angular Velocity: {omega_rpm}")
    print(f"In rad/s: {omega_rad_s.format('.2f')}")
    
    # Calculate linear velocity v = r * omega
    # r = 50 cm
    radius = Quantity(50, "cm")
    
    # We need consistent units. 
    # rad is "dimensionless" in standard physics but here it has dimension 'A'.
    # Standard SI formula v = r * omega implies omega is in 1/s for v to be m/s.
    # However, since we track 'A', v = r * omega will be 'L * A / T'.
    # So the result unit will be 'cm rad s-1'. 
    # To get linear velocity in m/s, we conceptually treat 'rad' as 1 (dimensionless) 
    # or explicitly handle it if we want strict angular tracking.
    
    linear_v_raw = radius * omega_rad_s
    print(f"Tangential Velocity (raw): {linear_v_raw.format('.2f')}")
    
    # Note: 'rad' is a unit here. 
    # 'cm rad s-1' is physically equivalent to speed if we consider rad dimensionless.
    print("-" * 30)

    # 3. Trigonometry (using raw values)
    # The Quantity class doesn't wrap sin/cos yet, so we access .value
    # But we must ensure it's in radians first!
    angle_vals = Quantity([0, 30, 45, 60, 90], "deg")
    
    # Convert to rad before passing to numpy sin
    angle_rads = angle_vals.to("rad")
    sin_vals = np.sin(angle_rads.value)
    
    print("Angles:", angle_vals)
    print("Sines: ", np.round(sin_vals, 3))

if __name__ == "__main__":
    main()

