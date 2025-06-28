# Selbstkorrektur

## Fehler und Korrekturen während der Lösungsfindung

### 1. Anfängliche Fehler bei der Ableitung
- **Fehler**: In der ersten Python-Analyse hatte ich die vereinfachte Form der Ableitung falsch berechnet. Die Ausgabe zeigte `y'(t) = -6*sin(t)**3 + 4*sin(t)`, was nicht korrekt war.
- **Korrektur**: Ich habe die Ableitungen nochmals von Hand mit der Produktregel berechnet und die korrekten Formen erhalten:
  - $x'(t) = 2\cos(2t)\cos t - \sin(2t)\sin t = \cos t + \cos(3t)$
  - $y'(t) = 2\cos(2t)\sin t + \sin(2t)\cos t = \sin t + \sin(3t)$

### 2. Unvollständige Analyse der singulären Punkte
- **Fehler**: Zunächst hatte ich nur nach Punkten gesucht, wo beide Ableitungen null sind, ohne zu beachten, dass diese Punkte auch auf der Kurve liegen müssen.
- **Korrektur**: Ich habe erkannt, dass die singulären Punkte bei $t = \pi/2$ und $t = 3\pi/2$ beide am Ursprung liegen, wo die Kurve sich selbst schneidet.

### 3. Verwirrung bei der Charakterisierung der Doppelpunkte
- **Fehler**: Anfangs war nicht klar, ob der Ursprung als ein Doppelpunkt oder als mehrfacher Punkt zu zählen ist.
- **Korrektur**: Ich habe klargestellt, dass der Ursprung ein vierfacher Punkt ist, da die Kurve dort viermal durchläuft (bei $t = 0, \pi/2, \pi, 3\pi/2$).

### 4. Technisches Problem mit TikZ
- **Fehler**: Ich habe TikZ für die Zeichnung verwendet, aber das Paket war nicht installiert.
- **Korrektur**: Ich habe die TikZ-Zeichnung durch eine verbale Beschreibung der Kurve ersetzt.

### 5. Kleinere Formatierungsfehler
- **Fehler**: Die ursprüngliche LaTeX-Datei hatte kleinere Formatierungsprobleme.
- **Korrektur**: Diese wurden beim zweiten Kompilierungsversuch behoben.

## Positive Aspekte der Lösung

1. Die Verwendung der Polardarstellung $f(t) = \sin(2t) \cdot (\cos t, \sin t)$ hat die Struktur der Kurve sehr klar gemacht.

2. Die Berechnung der Kurvenlänge mittels der Identität $|f'(t)|^2 = 4\cos^2 t$ war elegant und führte zu einem sauberen Ergebnis.

3. Die systematische Analyse aller Durchgänge durch den Ursprung half bei der vollständigen Charakterisierung der Kurve.

## Lessons Learned

1. Bei parametrischen Kurven ist es wichtig, sowohl die geometrische Intuition (Polardarstellung) als auch die analytischen Berechnungen (Ableitungen) zu nutzen.

2. Bei der Suche nach singulären Punkten muss man beachten, dass diese auf der Kurve liegen müssen - es reicht nicht, nur $f'(t) = 0$ zu lösen.

3. Die Visualisierung der Kurve am Anfang war sehr hilfreich für das Verständnis der Struktur.