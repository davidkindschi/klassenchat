# Klassenchat

Einfacher webbasierter Klassenchat als TRL4-Prototyp, entwickelt mit Specification-Driven Development (SDD).

---

## Architektur

```
Browser UI  ──►  Flask App (app.py)  ──►  In-Memory Message Store
                      │
                 Gunicorn (WSGI)
                      │
                 Render.com (Cloud)
```

**Komponenten**

| Komponente | Technologie |
|------------|-------------|
| Web-Framework | Flask 3.1 |
| WSGI-Server | Gunicorn 23 |
| Template-Engine | Jinja2 |
| Session-Speicher | Flask Session (Cookie) |
| Nachrichten-Speicher | In-Memory (Python-Liste) |
| Deployment | Render.com Web Service |

**Endpoint**

| Methode | Pfad | Aktion |
|---------|------|--------|
| GET | `/` | Seite anzeigen |
| POST | `/` | Nachricht senden / Username setzen / Nachricht löschen |

---

## Anforderungen

### Funktionale Anforderungen

**F1 – Nachricht senden**
- FR1.1: Eingabefeld mit max. 500 Zeichen (client- und serverseitig validiert)
- FR1.2: Senden-Button
- FR1.3: Eingabefeld wird nach dem Senden geleert
- FR1.4: Nachrichten aus reinem Whitespace werden nicht gesendet (`.strip()`)
- FR1.5: Nachricht enthält automatisch Absender und Zeitstempel (UTC)
- FR1.6: Bei Validierungsfehler: Fehlermeldung anzeigen, Eingabefeld-Inhalt behalten

**F2 – Nachrichten anzeigen**
- FR2.1: Nachrichten chronologisch, älteste zuerst
- FR2.2: Jede Nachricht zeigt Absender, Zeitstempel, Inhalt
- FR2.3: Liste aktualisiert sich nach jedem Senden
- FR2.4: Zeitstempel im Format `HH:MM:SS` (UTC)
- FR2.5: Leerer Chat zeigt: *"Noch keine Nachrichten — schreib die erste!"*

**F3 – Benutzername festlegen**
- FR3.1: Eingabefeld für Benutzernamen im Header
- FR3.2: Username in Flask Session (Cookie) gespeichert
- FR3.3: Username gilt für alle nachfolgenden Nachrichten
- FR3.5: Fallback auf `Anonym`; bereits gesendete Anonym-Nachrichten bleiben unverändert
- FR3.6: Anonym-Nachrichten können von niemandem gelöscht werden

**F5 – Nachricht löschen** *(Nice-to-have)*
- FR5.1: Löschen-Link nur bei eigenen Nachrichten sichtbar (nicht für Anonym)
- FR5.2: Direktes Löschen via POST, kein Bestätigungsdialog
- FR5.3: Nachricht verschwindet sofort für alle Nutzer

### Nicht-funktionale Anforderungen

| ID | Anforderung |
|----|-------------|
| NFR1 | Nachrichten sind **flüchtig** — bei Server-Neustart oder Redeploy gelöscht |
| NFR2 | Keine Authentifizierung — Benutzernamen sind selbst gewählt und nicht verifiziert |
| NFR3 | Kein Echtzeit-Update — Seite aktualisiert sich nur beim Senden oder manuellen Reload |

---

## Dateistruktur

```
klassenchat/
├── app.py                  # Flask-Applikation
├── templates/
│   └── index.html          # Jinja2-Template
├── static/
│   └── style.css           # Stylesheet
├── prototype.html          # Standalone UI-Prototyp (Schritt 5, kein Server nötig)
├── requirements.txt        # Python-Abhängigkeiten
├── render.yaml             # Render.com Deployment-Konfiguration
└── .gitignore
```

---

## Lokale Entwicklung

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten
python app.py
```

Dann im Browser: `http://localhost:5000`

---

## Deployment auf Render.com

1. Repository auf GitHub pushen
2. [render.com](https://render.com) → **New → Web Service**
3. GitHub-Repository `klassenchat` verbinden
4. Render erkennt `render.yaml` automatisch
5. **Create Web Service** klicken → Build ~1 Minute

**Build-Befehl:** `pip install -r requirements.txt`  
**Start-Befehl:** `gunicorn app:app`

> **Hinweis:** Bei jedem Redeploy werden alle Nachrichten gelöscht (NFR1).

---

## Methodologie

Entwickelt im Rahmen des Moduls *Specification-Driven Development (SDD)* an der FHNW.  
Vorgehen: Anforderungsdefinition → Quality Check → UI-Prototyp → Code-Generierung → Deployment.
