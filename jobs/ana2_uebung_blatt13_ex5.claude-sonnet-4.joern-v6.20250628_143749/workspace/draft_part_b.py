# Analyse für Teilaufgabe (b) - Isoperimetrisches Problem

import numpy as np
import matplotlib.pyplot as plt

def isoperimetric_analysis():
    print("Teilaufgabe (b): Isoperimetrisches Problem")
    print("Gesucht: Kurve mit gegebener Länge ℓ die die Fläche maximiert")
    print()
    
    print("Gegeben:")
    print("- z: [0,ℓ] → ℂ mit |ż(t)| = 1 (Parametrisierung nach Bogenlänge)")
    print("- Länge der Kurve ist ℓ")
    print("- Zu maximieren: A(z) = ∫_z v mit v(z) = iz/2")
    print()
    
    print("Mit Green'schem Theorem:")
    print("A(z) = ∫∫_G 1 dA = ∫_∂G (-y/2)dx + (x/2)dy")
    print()
    
    print("Für z(t) = x(t) + iy(t) mit |ż(t)| = 1:")
    print("A(z) = ∫₀^ℓ (-y(t)/2)ẋ(t) + (x(t)/2)ẏ(t) dt")
    print("     = (1/2) ∫₀^ℓ (x(t)ẏ(t) - y(t)ẋ(t)) dt")
    print()
    
    print("Nebenbedingungen:")
    print("1. ẋ(t)² + ẏ(t)² = 1  (Parametrisierung nach Bogenlänge)")
    print("2. x(0) = x(ℓ), y(0) = y(ℓ)  (geschlossene Kurve)")
    print()
    
    print("Lagrange-Ansatz:")
    print("L = (1/2) ∫₀^ℓ (xẏ - yẋ) dt - ∫₀^ℓ λ(t)(ẋ² + ẏ² - 1) dt")
    print()
    
    print("Euler-Lagrange-Gleichungen:")
    print("∂L/∂x - d/dt(∂L/∂ẋ) = 0")
    print("∂L/∂y - d/dt(∂L/∂ẏ) = 0")
    print()
    
    print("∂L/∂x = 0, ∂L/∂ẋ = -ẏ/2 - 2λẋ")
    print("∂L/∂y = 0, ∂L/∂ẏ = x/2 - 2λẏ")
    print()
    
    print("Euler-Lagrange:")
    print("ÿ/2 + 2λ̇ẋ + 2λẍ = 0")
    print("ẍ/2 - 2λ̇ẏ - 2λÿ = 0")
    print()
    
    print("Für konstantes λ (was sich als richtig erweist):")
    print("ÿ + 4λẍ = 0")
    print("ẍ - 4λÿ = 0")
    print()
    
    print("Substitution der zweiten in die erste:")
    print("ÿ + 4λ(4λÿ) = 0")
    print("ÿ(1 + 16λ²) = 0")
    print()
    
    print("Für λ ≠ ±i/4: ÿ = 0, also ẍ = 0")
    print("⟹ x(t) = at + b, y(t) = ct + d")
    print("Aber ẋ² + ẏ² = a² + c² = 1 und geschlossen ⟹ a = c = 0")
    print("⟹ Punkt, nicht Kurve. Widerspruch!")
    print()
    
    print("Also λ = ±i/4. Wähle λ = i/4:")
    print("ÿ - iẍ = 0")
    print("ẍ + iÿ = 0")
    print()
    
    print("Charakteristische Gleichung: r² + i = 0")
    print("r = ±√(-i) = ±e^(-iπ/4) = ±(1-i)/√2")
    print()
    
    print("Allgemeine Lösung:")
    print("z(t) = x(t) + iy(t) = Ae^(rt) + Be^(-rt)")
    print("mit r = (1-i)/√2")
    print()
    
    print("Mit Randbedingungen |ż| = 1 und z(0) = z(ℓ):")
    print("⟹ z(t) = R·e^(it/R) für geeignetes R")
    print("⟹ Kreis mit Radius R")
    print()
    
    print("Aus Längenbedingung ℓ = 2πR folgt R = ℓ/(2π)")

if __name__ == "__main__":
    isoperimetric_analysis()