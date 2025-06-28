# Selbstkorrektur

## Fehler und Korrekturen während der Bearbeitung

### 1. Verwechslung von Fibonacci-Identitäten
**Fehler:** Ich habe zunächst versucht, verschiedene bekannte Fibonacci-Identitäten anzuwenden, wie z.B. $f_{2n} = f_n \cdot L_n$ (mit Lucas-Zahlen) oder $f_{2n} = f_n \cdot (f_{n+1} + f_{n-1})$.

**Problem:** Diese Identitäten gelten für die Standard-Fibonacci-Folge mit $F_0 = 0, F_1 = 1$, nicht für die gegebene Folge mit $f_0 = f_1 = 1$.

**Korrektur:** Ich musste erkennen, dass die gegebene Folge um einen Index verschoben ist: $f_n = F_{n+1}$ (wobei $F_n$ die Standard-Fibonacci-Zahlen sind).

### 2. Falsche Annahme bei Teil (b)
**Fehler:** Ich habe anfangs versucht, die Aussage "$f_{2n}$ ist teilbar durch $f_n$" zu beweisen, ohne sie zunächst zu überprüfen.

**Problem:** Die Aussage ist tatsächlich falsch für die gegebene Fibonacci-Folge (außer für $n=1$).

**Korrektur:** Nach ausführlicher numerischer Überprüfung habe ich festgestellt, dass die Aussage falsch ist und ein Gegenbeispiel angegeben. Die korrekte Eigenschaft wäre: $f_n | f_{kn}$ für alle $k \in \mathbb{N}$.

### 3. Fehlerhafte Implementierung der Fibonacci-Identität
**Fehler:** Bei der Überprüfung der Identität $f_{m+n} = f_{m-1} \cdot f_n + f_m \cdot f_{n+1}$ erhielt ich durchweg falsche Ergebnisse.

**Problem:** Die Identität war korrekt, aber ich hatte Indexierungsfehler in meinem Python-Code.

**Korrektur:** Anstatt die komplexen Identitäten zu debuggen, bin ich zu den grundlegenden Eigenschaften zurückgekehrt und habe direkte Beweise verwendet.

### 4. Unklarheit über die Definition von "relativ prim"
**Fehler:** Ich war zunächst unsicher, ob "relativ prim" bedeutet, dass der ggT gleich 1 ist oder ob es reicht, dass kein $a > 1$ beide Zahlen teilt.

**Problem:** Die Formulierung in der Aufgabe war etwas ungewöhnlich.

**Korrektur:** Beide Definitionen sind äquivalent. Ich habe den Beweis über den ggT geführt, was der Standardansatz ist.

### 5. Zu komplizierte Beweisansätze
**Fehler:** Ich habe versucht, komplexe Fibonacci-Identitäten und Formeln zu verwenden, anstatt die einfachen rekursiven Eigenschaften zu nutzen.

**Problem:** Dies machte die Beweise unnötig kompliziert und fehleranfällig.

**Korrektur:** Die finalen Beweise nutzen nur die Rekursionsformel $f_{n+1} = f_n + f_{n-1}$ und grundlegende Eigenschaften der Teilbarkeit.

### 6. Fehlende Überprüfung der Aufgabenstellung
**Fehler:** Ich habe Teil (b) nicht sofort als problematisch erkannt.

**Problem:** Eine einfache numerische Überprüfung hätte sofort gezeigt, dass die Aussage falsch ist.

**Korrektur:** In der finalen Lösung habe ich klar angegeben, dass die Aussage falsch ist, und ein Gegenbeispiel sowie die korrekte Eigenschaft der Fibonacci-Zahlen angegeben.

## Lessons Learned

1. **Immer zuerst verifizieren:** Bei mathematischen Aussagen sollte man zunächst einige Beispiele berechnen, bevor man einen Beweis versucht.

2. **Einfachheit bevorzugen:** Die einfachsten Beweisansätze sind oft die besten. Komplexe Identitäten sind nur nötig, wenn einfache Methoden nicht funktionieren.

3. **Vorsicht bei Indexverschiebungen:** Die Fibonacci-Folge mit $f_0 = f_1 = 1$ unterscheidet sich von der Standardfolge, was bei der Anwendung bekannter Identitäten beachtet werden muss.

4. **Kritisches Hinterfragen:** Wenn eine zu beweisende Aussage nach mehreren Versuchen nicht beweisbar scheint, sollte man ihre Richtigkeit in Frage stellen.