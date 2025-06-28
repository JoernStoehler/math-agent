# Selbstkorrektur

## Fehler und Korrekturen während der Lösungserstellung

### 1. Anfänglicher Ansatz
Zunächst hatte ich überlegt, die Identitäten mit vollständiger Induktion zu beweisen (wie in meiner Todo-Liste vermerkt). Dies wäre zwar möglich gewesen, aber deutlich umständlicher als der gewählte Ansatz über De Moivre's Theorem.

### 2. Indexgrenzen bei der sin(nx)-Formel
Bei der Herleitung der sin(nx)-Formel musste ich sorgfältig über die obere Summationsgrenze nachdenken. Die Summe läuft über ungerade Indizes $2k+1$, und ich musste klären, dass:
- Für gerades $n$: Die obere Grenze ist $\lfloor (n-1)/2 \rfloor = n/2 - 1$
- Für ungerades $n$: Die obere Grenze ist $\lfloor (n-1)/2 \rfloor = (n-1)/2$

Ich habe dann erkannt, dass man trotzdem $\lfloor n/2 \rfloor$ als obere Grenze schreiben kann, da für gerades $n$ und $k = n/2$ der Binomialkoeffizient $\binom{n}{n+1} = 0$ ist.

### 3. Notation und Klarheit
In der finalen Lösung habe ich darauf geachtet, alle Schritte klar zu erklären, insbesondere:
- Die Werte von $i^k$ für verschiedene $k$
- Die Trennung in Real- und Imaginärteil
- Die Begründung, warum beide Formeln die gleiche obere Summationsgrenze haben können

### 4. Keine weiteren Rechenfehler
Die Rechnung selbst verlief ohne Fehler, da der Ansatz über De Moivre's Theorem sehr direkt ist und keine komplexen Umformungen erfordert.

## Verbesserungsmöglichkeiten
- Man könnte zusätzlich noch ein oder zwei konkrete Beispiele (z.B. für $n=2$ oder $n=3$) durchrechnen, um die Formeln zu verifizieren.
- Eine alternative Herleitung über die Euler-Formel $e^{ix} = \cos x + i\sin x$ wäre ebenfalls möglich gewesen.