"""Kolorowy kalkulator z rozwijanym panelem funkcji naukowych (Tkinter)."""

import math
import tkinter as tk
from decimal import Decimal


class SilnikKalkulatora:
    """Obliczenia oddzielone od okna graficznego."""

    def __init__(self):
        self.wyczysc()

    def wyczysc(self):
        self.ekran = "0"
        self.pierwsza = None
        self.operator = None
        self.nowy_wpis = True

    def pokaz_liczbe(self, liczba):
        # Decimal usuwa typowy problem np. 0.1 + 0.2.
        tekst = format(liczba.normalize(), "f")
        if "." in tekst:
            tekst = tekst.rstrip("0").rstrip(".")
        self.ekran = tekst if tekst != "-0" else "0"

    def wykonaj_dzialanie(self, a, b, znak):
        if znak == "+":
            return a + b
        if znak == "−":
            return a - b
        if znak == "×":
            return a * b
        if znak == "÷":
            return a / b
        raise ValueError("Nieznany operator")

    def funkcja_naukowa(self, znak):
        x = Decimal(self.ekran)
        if znak == "√x":
            return x.sqrt()
        if znak == "x²":
            return x ** 2
        if znak == "x³":
            return x ** 3
        if znak == "1/x":
            return Decimal(1) / x
        if znak in ("sin", "cos", "tan"):
            # Funkcje trygonometryczne liczymy w stopniach.
            kat = math.radians(float(x))
            if znak == "tan" and abs(math.cos(kat)) < 1e-12:
                raise ValueError("Tangens nie istnieje dla tego kąta")
            funkcje = {"sin": math.sin, "cos": math.cos, "tan": math.tan}
            wynik = funkcje[znak](kat)
            return Decimal(str(round(wynik, 10)))
        raise ValueError("Nieznana funkcja")

    def nacisnij(self, znak):
        if znak == "C":
            self.wyczysc()
            return self.ekran

        if self.ekran == "Błąd":
            self.wyczysc()
            if znak not in "0123456789.":
                return self.ekran

        try:
            if znak in "0123456789" and len(znak) == 1:
                if self.nowy_wpis or self.ekran == "0":
                    self.ekran = znak
                elif len(self.ekran) < 20:
                    self.ekran += znak
                self.nowy_wpis = False

            elif znak == ".":
                if self.nowy_wpis:
                    self.ekran = "0."
                elif "." not in self.ekran:
                    self.ekran += "."
                self.nowy_wpis = False

            elif znak == "⌫":
                if not self.nowy_wpis:
                    self.ekran = self.ekran[:-1]
                    if self.ekran in ("", "-"):
                        self.ekran = "0"

            elif znak == "±":
                if self.ekran != "0":
                    self.ekran = (
                        self.ekran[1:]
                        if self.ekran.startswith("-")
                        else "-" + self.ekran
                    )
                self.nowy_wpis = False

            elif znak == "%":
                self.pokaz_liczbe(Decimal(self.ekran) / 100)
                self.nowy_wpis = False

            elif znak == "π":
                self.ekran = str(round(math.pi, 11))
                self.nowy_wpis = False

            elif znak in ("√x", "x²", "x³", "1/x", "sin", "cos", "tan"):
                self.pokaz_liczbe(self.funkcja_naukowa(znak))
                self.nowy_wpis = False

            elif znak in ("+", "−", "×", "÷"):
                if self.operator is not None and not self.nowy_wpis:
                    wynik = self.wykonaj_dzialanie(
                        self.pierwsza, Decimal(self.ekran), self.operator
                    )
                    self.pokaz_liczbe(wynik)
                self.pierwsza = Decimal(self.ekran)
                self.operator = znak
                self.nowy_wpis = True

            elif znak == "=":
                if self.operator is not None and not self.nowy_wpis:
                    wynik = self.wykonaj_dzialanie(
                        self.pierwsza, Decimal(self.ekran), self.operator
                    )
                    self.pokaz_liczbe(wynik)
                    self.pierwsza = None
                    self.operator = None
                    self.nowy_wpis = True

        except (ArithmeticError, ValueError, OverflowError):
            self.wyczysc()
            self.ekran = "Błąd"

        return self.ekran


# Inny kolor dla każdej cyfry.
KOLORY_CYFR = {
    "0": "#0E7490",  # turkusowy
    "1": "#BE123C",  # czerwony
    "2": "#BE185D",  # różowy
    "3": "#7C3AED",  # fioletowy
    "4": "#0F766E",  # morski
    "5": "#15803D",  # zielony
    "6": "#C2410C",  # pomarańczowy
    "7": "#4338CA",  # indygo
    "8": "#1D4ED8",  # niebieski
    "9": "#0369A1",  # błękitny
}


def uruchom_okno():
    silnik = SilnikKalkulatora()
    okno = tk.Tk()
    okno.title("Kolorowy kalkulator Python")
    okno.geometry("390x600")
    okno.resizable(False, False)
    okno.configure(bg="#111827")

    tk.Label(
        okno, text="KALKULATOR", bg="#111827", fg="#93C5FD",
        font=("Segoe UI", 13, "bold"),
    ).pack(pady=(20, 8))

    wyswietlacz = tk.StringVar(value="0")
    tk.Label(
        okno, textvariable=wyswietlacz,
        bg="#1F2937", fg="white", anchor="e",
        font=("Segoe UI", 32, "bold"), padx=15,
    ).pack(fill="x", padx=14, pady=(0, 12), ipady=12)

    def klik(znak):
        wyswietlacz.set(silnik.nacisnij(znak))

    def przycisk(rodzic, znak, wiersz, kolumna, kolor):
        tk.Button(
            rodzic, text=znak, command=lambda: klik(znak),
            bg=kolor, fg="white", activebackground="#64748B",
            activeforeground="white", font=("Segoe UI", 17, "bold"),
            relief="flat", bd=0, cursor="hand2",
        ).grid(row=wiersz, column=kolumna, sticky="nsew", padx=4, pady=4)

    panel_dodatkowy = tk.Frame(okno, bg="#111827")
    dodatkowe_funkcje = [
        ["√x", "x²", "x³", "1/x"],
        ["sin", "cos", "tan", "π"],
    ]
    for r, wiersz in enumerate(dodatkowe_funkcje):
        panel_dodatkowy.grid_rowconfigure(r, weight=1)
        for c, znak in enumerate(wiersz):
            panel_dodatkowy.grid_columnconfigure(c, weight=1)
            przycisk(panel_dodatkowy, znak, r, c, "#6D28D9")

    panel_glowny = tk.Frame(okno, bg="#111827")

    def pokaz_dodatkowe():
        if panel_dodatkowy.winfo_manager():
            panel_dodatkowy.pack_forget()
            przycisk_funkcji.config(text="Dodatkowe funkcje ▼")
            okno.geometry("390x600")
        else:
            panel_dodatkowy.pack(before=panel_glowny, fill="x", padx=14, pady=(0, 8), ipady=4)
            przycisk_funkcji.config(text="Ukryj dodatkowe funkcje ▲")
            okno.geometry("390x760")

    przycisk_funkcji = tk.Button(
        okno, text="Dodatkowe funkcje ▼", command=pokaz_dodatkowe,
        bg="#334155", fg="white", activebackground="#475569",
        activeforeground="white", font=("Segoe UI", 12, "bold"),
        relief="flat", bd=0, cursor="hand2",
    )
    przycisk_funkcji.pack(fill="x", padx=14, pady=(0, 10), ipady=9)

    panel_glowny.pack(fill="both", expand=True, padx=14, pady=(0, 12))
    uklad = [
        ["C", "⌫", "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "−"],
        ["1", "2", "3", "+"],
        ["±", "0", ".", "="],
    ]
    for r, wiersz in enumerate(uklad):
        panel_glowny.grid_rowconfigure(r, weight=1)
        for c, znak in enumerate(wiersz):
            panel_glowny.grid_columnconfigure(c, weight=1)
            kolor = KOLORY_CYFR.get(znak, "#374151")
            if znak in ("+", "−", "×", "÷"):
                kolor = "#2563EB"
            elif znak == "=":
                kolor = "#059669"
            elif znak == "C":
                kolor = "#DC2626"
            przycisk(panel_glowny, znak, r, c, kolor)

    def obsluga_klawiatury(event):
        if event.keysym in ("Return", "KP_Enter"):
            klik("=")
        elif event.keysym == "BackSpace":
            klik("⌫")
        elif event.keysym == "Escape":
            klik("C")
        elif event.char in "0123456789":
            klik(event.char)
        elif event.char in ("+", "-", "*", "/"):
            klik({"+": "+", "-": "−", "*": "×", "/": "÷"}[event.char])
        elif event.char in (".", ","):
            klik(".")
        elif event.char == "%":
            klik("%")

    okno.bind("<Key>", obsluga_klawiatury)
    okno.mainloop()


if __name__ == "__main__":
    uruchom_okno()