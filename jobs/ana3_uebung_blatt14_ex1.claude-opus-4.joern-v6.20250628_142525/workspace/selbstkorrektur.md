# Selbstkorrektur

## Fehler und Korrekturen während der Lösungserstellung

### 1. LaTeX-Kompilierungsfehler
- **Fehler**: Versuchte die Pakete `enumitem` und `tikz` einzubinden, die in der Umgebung nicht verfügbar waren.
- **Korrektur**: Entfernte diese unnötigen Pakete aus der Präambel.

### 2. Command-Redefinition-Fehler
- **Fehler**: Definierte `\newcommand{\perp}{\perp}`, was zu einem Fehler führte, da `\perp` bereits in LaTeX definiert ist.
- **Korrektur**: Entfernte diese redundante Definition.

### 3. Dimensionsargument in Teil (a)
- **Verbesserung während des Schreibens**: Beim ersten Durchdenken war mir nicht sofort klar, wie man zeigt, dass die Dimension von $T_a M \cap T_a^{\perp}(\partial M)$ genau 1 ist. 
- **Lösung**: Verwendete die Dimensionsformel für Schnitte von Untervektorräumen und bemerkte, dass man zuerst zeigen muss, dass $T_a M + T_a^{\perp}(\partial M) = \mathbb{R}^n$ gilt.

### 4. Klarheit bei der Konstruktion des Normalenfelds
- **Verbesserung**: Die anfängliche Erklärung, warum der Vektor $D\phi(y)(e_1)$ senkrecht auf $T_x(\partial M)$ steht, war nicht ausreichend klar.
- **Korrektur**: Fügte die Erklärung hinzu, dass $\phi$ den Rand $\partial H^k$ auf $\partial M$ abbildet und daher das Differential den Tangentialraum entsprechend abbildet.

### 5. Fehlende Details bei der Unabhängigkeit von der Kartenwahl
- **Ursprünglicher Ansatz**: Wollte zunächst nur argumentieren, dass die Konstruktion "offensichtlich" unabhängig von der Karte ist.
- **Verbesserung**: Fügte eine detaillierte Erklärung mit dem Kartenwechsel-Diffeomorphismus hinzu und zeigte, warum dieser die Orientierung (nach außen zeigend) erhält.

### 6. Notation
- **Kleine Inkonsistenz**: Verwendete manchmal $\partial$ und manchmal $\del$ für den Rand.
- **Korrektur**: Konsistent `\del` verwendet, wie in der Aufgabenstellung.

## Allgemeine Beobachtungen

Die Hauptschwierigkeit bei dieser Aufgabe lag darin, die abstrakten Konzepte von Tangentialräumen und deren orthogonalen Komplementen klar und präzise zu behandeln. Besonders die Dimensionsargumente erforderten sorgfältiges Nachdenken über die Beziehungen zwischen den verschiedenen Räumen.

Die Konstruktion des Normalenfelds in Teil (b) war konzeptionell anspruchsvoll, da man zeigen muss, dass die lokalen Definitionen zu einer globalen, wohldefinierten und stetigen Abbildung führen.