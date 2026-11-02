# Kolorowy kalkulator Python

Kalkulator w Pythonie z graficznym interfejsem Tkinter.

## Funkcje
- Dodawanie, odejmowanie, mnożenie i dzielenie.
- Kolorowe przyciski cyfr.
- Przycisk **Dodatkowe funkcje ▼**, który otwiera panel naukowy.
- Pierwiastek kwadratowy (√x), kwadrat (x²), sześcian (x³), odwrotność (1/x).
- Sinus, cosinus i tangens **w stopniach**.
- Liczba π, procenty, zmiana znaku i cofanie cyfr.
- Obsługa klawiatury.

## Uruchomienie

1. Zainstaluj Pythona na komputerze.
2. Otwórz cały folder w Visual Studio Code.
3. W terminalu uruchom:

```powershell
python kalkulator.py
```

Na Windows, gdy `python` nie jest rozpoznawane, spróbuj:

```powershell
py kalkulator.py
```

Tkinter jest częścią standardowej instalacji Pythona w Windows.

## Obsługa

Kliknij **Dodatkowe funkcje ▼**, aby pokazać przyciski naukowe. Ponowne kliknięcie ukrywa panel. Sinus, cosinus i tangens używają stopni, np. `30 → sin → 0.5`.

Procenty działają jako podzielenie bieżącej liczby przez 100 (np. `50 → % → 0.5`). Przy dzieleniu przez zero kalkulator wyświetla **Błąd**.

## GitHub

Po utworzeniu pustego repozytorium `Kalkulator-Python`:

```bash
git init
git add .
git commit -m "Dodano kolorowy kalkulator z funkcjami naukowymi"
git branch -M main
git remote add origin https://github.com/TWOJ_LOGIN/Kalkulator-Python.git
git push -u origin main
```

Gdy repozytorium już istnieje i jest połączone z GitHubem, wystarczą:

```bash
git add .
git commit -m "Dodano kolorowe przyciski i panel naukowy"
git push
```
