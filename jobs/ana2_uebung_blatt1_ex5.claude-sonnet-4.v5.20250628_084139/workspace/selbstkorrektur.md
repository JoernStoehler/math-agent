# Selbstkorrektur

## Fehler und Korrekturen während der Lösungserstellung

### 1. Polynomdivision in Teil (a)
- **Fehler**: Keine signifikanten Fehler. Die Polynomdivision wurde korrekt durchgeführt.
- **Korrektur**: Keine erforderlich.

### 2. Faktorisierung in Teil (b)
- **Potentieller Fehler**: Bei der ersten Durchführung war die Faktorisierung nicht sofort offensichtlich.
- **Korrektur**: Verwendete die Methode des Ausklammerns durch Gruppierung:
  - $x^3 + x^2 - x - 1 = x^2(x+1) - 1(x+1) = (x+1)(x^2-1) = (x-1)(x+1)^2$
- **Überprüfung**: Verifizierte durch Ausmultiplizieren, dass $(x-1)(x+1)^2 = x^3 + x^2 - x - 1$

### 3. Partialbruchzerlegung in Teil (b)
- **Fehler**: Keine Rechenfehler. Der Ansatz mit drei Termen $\frac{A}{x-1} + \frac{B}{x+1} + \frac{C}{(x+1)^2}$ war korrekt.
- **Überprüfung**: Verifizierte die Lösung durch Differentiation der Stammfunktion.

### 4. Faktorisierung in Teil (c)
- **Anfängliche Unsicherheit**: Die Faktorisierung von $x^3 - x^2 + x - 1$ war nicht sofort ersichtlich.
- **Korrektur**: Verwendete wieder die Gruppierungsmethode:
  - $x^3 - x^2 + x - 1 = x^2(x-1) + 1(x-1) = (x-1)(x^2+1)$
- **Wichtige Erkenntnis**: $x^2 + 1$ ist über den reellen Zahlen irreduzibel (keine reellen Nullstellen).

### 5. Partialbruchzerlegung in Teil (c)
- **Wichtiger Punkt**: Da $x^2 + 1$ irreduzibel ist, musste der Ansatz $\frac{Ax+B}{x^2+1}$ statt $\frac{A}{x+a} + \frac{B}{x+b}$ verwendet werden.
- **Korrektur**: Der korrekte Ansatz war $\frac{A}{x-1} + \frac{Bx + C}{x^2+1}$.

### 6. Integration in Teil (c)
- **Potentieller Fehler**: Die Integration von $\frac{1-x}{2(x^2+1)}$ erforderte Aufspaltung in zwei Terme.
- **Korrektur**: 
  - $\int \frac{1}{x^2+1} dx = \arctan(x)$
  - $\int \frac{x}{x^2+1} dx = \frac{1}{2}\ln(x^2+1)$ (durch Substitution $u = x^2+1$)

### 7. Formatierung und Vollständigkeit
- **Verbesserung**: Stellte sicher, dass alle Schritte ausführlich erklärt wurden, insbesondere:
  - Die Polynomdivision in Teil (a) wurde Schritt für Schritt nachgerechnet
  - Alle Koeffizientenvergleiche wurden explizit durchgeführt
  - Alle Integrationen wurden vollständig ausgeführt

### 8. Überprüfung
- **Methode**: Für alle Teile wurde die Lösung durch Ableitung der Stammfunktion verifiziert.
- **Ergebnis**: Alle Lösungen wurden als korrekt bestätigt.

## Zusammenfassung
Die Hauptherausforderungen lagen in der korrekten Faktorisierung der Nennerpolynome und der Wahl des richtigen Ansatzes für die Partialbruchzerlegung, insbesondere bei irreduziblen quadratischen Faktoren. Die systematische Überprüfung durch Differentiation half, die Korrektheit der Lösungen sicherzustellen.