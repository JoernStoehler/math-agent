# Hilfsskript zur Berechnung der Kurvenintegrale

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Für Kreis: z(t) = R*e^(it) für t von 0 bis 2π
# z'(t) = iR*e^(it)
# v(z) = iz/2 = i*R*e^(it)/2
# ∫v dz = ∫(i*R*e^(it)/2) * (iR*e^(it)) dt = ∫(-R²*e^(2it)/2) dt

def kreis_berechnung():
    R = 1  # Radius
    print(f"Kreis mit Radius R = {R}")
    print(f"Parametrisierung: z(t) = {R}*e^(it), t ∈ [0, 2π]")
    print(f"z'(t) = i*{R}*e^(it)")
    print(f"v(z(t)) = i*z(t)/2 = i*{R}*e^(it)/2")
    print(f"∫v dz = ∫(i*{R}*e^(it)/2) * (i*{R}*e^(it)) dt")
    print(f"      = ∫(-{R}²*e^(2it)/2) dt")
    print(f"      = -{R}²/2 * ∫e^(2it) dt")
    print(f"      = -{R}²/2 * [e^(2it)/(2i)]₀^(2π)")
    print(f"      = -{R}²/2 * (e^(4πi)/(2i) - 1/(2i))")
    print(f"      = -{R}²/2 * (1/(2i) - 1/(2i))")
    print(f"      = -{R}²/2 * 0 = 0")
    print("Das ist falsch! Lass mich nochmal rechnen...")
    
    # Korrekte Berechnung
    print("\nKorrekte Berechnung:")
    print("Für z(t) = R*e^(it) = R(cos(t) + i*sin(t))")
    print("z'(t) = R*i*e^(it) = R*i*(cos(t) + i*sin(t)) = R*(-sin(t) + i*cos(t))")
    print("v(z) = iz/2 = i*R*e^(it)/2 = R*i*(cos(t) + i*sin(t))/2")
    print("     = R*(-sin(t) + i*cos(t))/2")
    
    # Real- und Imaginärteil von v
    print("\nReal(v) = -R*sin(t)/2")
    print("Imag(v) = R*cos(t)/2")
    
    # dz = z'(t)dt
    print("\ndz = z'(t)dt = R*(-sin(t) + i*cos(t))dt")
    print("Real(dz) = -R*sin(t)dt")
    print("Imag(dz) = R*cos(t)dt")
    
    # Kurvenintegral ∫v·dz
    print("\n∫v·dz = ∫[Real(v)*Real(dz) - Imag(v)*Imag(dz)] + i*∫[Real(v)*Imag(dz) + Imag(v)*Real(dz)]")
    print("Real part: ∫(-R*sin(t)/2)*(-R*sin(t)) - (R*cos(t)/2)*(R*cos(t)) dt")
    print("         = ∫(R²*sin²(t)/2 - R²*cos²(t)/2) dt")
    print("         = R²/2 * ∫(sin²(t) - cos²(t)) dt")
    print("         = R²/2 * ∫(-cos(2t)) dt")
    print("         = -R²/2 * [sin(2t)/2]₀^(2π)")
    print("         = -R²/2 * (0 - 0) = 0")
    
    print("\nImag part: ∫(-R*sin(t)/2)*(R*cos(t)) + (R*cos(t)/2)*(-R*sin(t)) dt")
    print("         = ∫(-R²*sin(t)*cos(t)/2 - R²*cos(t)*sin(t)/2) dt")
    print("         = ∫(-R²*sin(t)*cos(t)) dt")
    print("         = -R² * ∫sin(t)*cos(t) dt")
    print("         = -R² * [sin²(t)/2]₀^(2π)")
    print("         = -R² * (0 - 0) = 0")
    
    print("\nDas ergibt wieder 0, was falsch ist...")
    print("Ich muss das Green'sche Theorem verwenden!")

def green_theorem():
    print("\nVerwendung des Green'schen Theorems:")
    print("Für v(x,y) = (P(x,y), Q(x,y)) mit P = -y/2, Q = x/2")
    print("da iz/2 = i(x+iy)/2 = (ix-y)/2 = -y/2 + ix/2")
    print("∂Q/∂x - ∂P/∂y = ∂(x/2)/∂x - ∂(-y/2)/∂y = 1/2 - (-1/2) = 1")
    print("∫∫_G 1 dA = Flächeninhalt von G")
    print("Das stimmt mit der erwarteten Formel überein!")

if __name__ == "__main__":
    kreis_berechnung()
    green_theorem()