# AutoClicker for Blum Drop Mini-Game

Ein Python-basierter AutoClicker für das "Blum Drop"-Minispiel, der automatisch Objekte erkennt und darauf klickt.

## Voraussetzungen

- Python 3.x
- Windows-Betriebssystem (für `win32gui`)
- Bibliotheken aus der `requirements.txt` Datei

## Installation

1. Klone das Repository:

    ```bash
    git clone https://github.com/SoldatenEnte/blum-clicker.git
    cd blum-clicker
    ```

2. Installiere die benötigten Bibliotheken:

    ```bash
    pip install -r requirements.txt
    ```

## Nutzung

1. Starte das Spiel "Blum Drop" und lasse das Fenster im Vordergrund.
2. Führe das Script aus:

    ```bash
    python main.py [anzahl_der_spiele]
    ```

    Ersetze `[anzahl_der_spiele]` durch die gewünschte Anzahl der Spiele.

3. Verwende die folgenden Tastenkombinationen:
    - `K`: Pause des Autoclickers
    - `L`: Fortsetzen des Autoclickers

## Konfiguration

- Die Einstellungen für Farberkennung und Positionstrigger befinden sich in der Datei `constants.py`.
- Um das Skript für verschiedene Bildschirmgrößen anzupassen, ändere die Werte in `DEV_SCREEN_SIZE_CONST`.

## Dateien

- **main.py**: Hauptskript für den AutoClicker.
- **constants.py**: Enthält die Trigger-Konstanten und Einstellungen.
- **prepare_app.py**: Positioniert das Fenster und holt die Fensterkoordinaten.
- **README.md**: Diese Datei.
- **requirements.txt**: Liste der benötigten Python-Bibliotheken.