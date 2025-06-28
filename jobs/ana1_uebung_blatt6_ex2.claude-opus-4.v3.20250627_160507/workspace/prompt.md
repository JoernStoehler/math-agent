Du bist Teil eines KI-Evaluations projekts.
Du sollst eine Mathe-Übungsaufgabe lesen, lösen und eine Musterlösung schreiben.

Die Aufgabe ist @exercise.tex
Schreibe die finale Lösung nach @solution.tex
WICHTIG: Kopiere die komplette Aufgabe aus @exercise.tex an den Anfang von @solution.tex
Die Lösung soll in gültigem LaTeX geschrieben sein.
Du kannst `pdflatex` verwenden um zu prüfen, ob die Lösung kompiliert.

Eine Musterlösung muss folgende Eigenschaften haben:
- korrekt
- vollständig
- gut lesbar und gut erklärt
- keine Sprünge und Lücken
- keine Fehler
- in LaTeX geschrieben
- keine unnötigen oder gar falschen Bemerkungen
- mathematisch halbwegs schön und einfach

WICHTIG:
- wenn du eine Teilaufgabe löst, schreibe nicht dass sie "analog zu" einer anderen Teilaufgabe gelöst werden kann, sondern präsentiere den adaptierten Lösungsweg vollständig.
  Beispiel:
  Statt zu schreiben:
    "Die Lösung für Teilaufgabe b) ist analog zu a), daher gilt: (Endresultat)"
  Schreibe:
    "Wir lösen die Teilaufgabe b) analog zu a) indem wir $a$ durch $b+a$ ersetzen. Schritt für Schritt ergibt sich dann: (voller Lösungsweg)"    
- beschreibe bei Umformungen was du machst, damit der Korrektur/Student dir einfach folgen kann.
  Beispiel:
  $$
    (1-\frac{1}{n+1})^n = (1-\frac{1}{n+1})^{(n+1) \cdot \frac{n}{n+1}}
    \to (e^{-1})^{n/(n+1)} \to e^{-1} \text{ für } n \to \infty
  $$
  Statt z.B. das vorletzte $=$ zu überspringen.

WICHTIG:
- nachdem du @solution.tex geschrieben hast schreibe ein weiteres deliverable: @selbstkorrektur.md indem du beschreibst welche Fehler du alles gemacht hast auf dem Weg zur finalen Lösung, z.B. Rechenfehler, falsche Beweise, erfundene Sätze die es doch nicht gibt, Lücken die geschlossen werden mussten, unklare Erklärungen, etc. Das hilft dem Benchmark-Team nachzuvollziehen, welche Fehler häufig gemacht werden und in zukünftigen Versionen des Prompts kann dann darauf hingewiesen werden und somit die Qualität der Musterlösungen verbessert werden.

Du darfst beliebige drafts, reviews, python skripte, etc. schreiben um die Aufgabe zu lösen.
Wichtig ist nur dass die finale Lösung in @solution.tex abgelegt wird.