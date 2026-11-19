# Guess the song

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/Tkinter-GUI-informational?style=for-the-badge)
![Audio Library](https://img.shields.io/badge/Pygame-Mixer-green?style=for-the-badge&logo=pygame)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**Guess the song** es una aplicación interactiva de escritorio desarrollada en Python utilizando técnicas de *vibecoding* y *prompt engineering*. 
El juego desafía a los usuarios a adivinar canciones populares
a partir de muestras de audio y pistas, utilizando un sistema de opciones 
múltiples con distractores reales del mismo artista.

---

## Características Principales

* **Interfaz Minimalista Clara:** Diseñada con una paleta de colores limpia en tonos *slate* y azul profesional mediante `Tkinter`.
* **Audio a Demanda:** Control total sobre la reproducción de muestras MP3 usando `pygame.mixer` (sin reproducción automática molesta).
* **Opciones por Mismo Artista:** Algoritmo dinámico que presenta 4 opciones de canciones pertenecientes a la discografía real de cada artista.
* **Sistema de Intentos:** 2 vidas por ronda con retroalimentación visual inmediata (deshabilitación y cambio de color en opciones incorrectas).
* **Sistema de Pistas:** Opción de revelar información clave (Año / Género) penalizando únicamente -2 puntos.
* **Condición de Victoria Exigente:** Requiere un puntaje mínimo de **60 / 100 puntos** al finalizar las 10 rondas para ganar la partida.

---

##  Estructura del Repositorio

```text
GuessTheTrack/
├── config/
│   └── agent_persona.json      # Configuración declarativa: personalidad, tono y reglas de puntuación del agente
├── skills/
│   ├── __init__.py             # Inicializador del paquete de skills
│   ├── audio_skill.py          # Skill 1: Control encapsulado de reproducción MP3 (Pygame Mixer)
│   ├── scoring_skill.py        # Skill 2: Motor de reglas, vidas/intentos, puntajes y umbral de victoria
│   └── trivia_skill.py         # Skill 3: Generación de opciones del mismo artista y pistas con LLM (Gemini)
├── agents/
│   ├── __init__.py             # Inicializador del paquete de agentes
│   └── music_host_agent.py     # Agente orquestador ("DJ Nova") que integra las skills y la persona
├── audios/                     # Carpeta de recursos multimedia (fragmentos .mp3)
│   ├── aintinla.mp3
│   ├── boompala.mp3
│   ├── everytime.mp3
│   ├── love.mp3
│   ├── nda.mp3
│   ├── reminder.mp3
│   ├── saveyourtears.mp3
│   ├── sawadika.mp3
│   ├── seoulcity.mp3
│   └── whrsmyhsbn.mp3
├── main.py                     # Capa de presentación (UI en Tkinter) desacoplada de la lógica
├── requirements.txt            # Dependencias del proyecto (pygame, google-genai)
└── README.md                   # Documentación técnica y guía de ejecución

##  Ficha Técnica de la actualizacion

| Atributo | Detalle |
| :--- | :--- |
| **Nombre del Proyecto** | Guess The Track — Agentic Edition |
| **Versión** | 2.0.0 (Refactorización Modular basada en Agentes y Skills) |
| **Tipo de Aplicación** | Juego interactivo de trivia musical de escritorio con asistente IA |
| **Patrón Arquitectónico** | Arquitectura Desacoplada por Capas (Configuración → Skills → Agente → UI) |
| **Lenguaje Principal** | Python 3.10+ (probado en Python 3.13) |
| **Interfaz Gráfica (UI)** | `Tkinter` (Light Mode minimalista desacoplado de la lógica de negocio) |
| **Motor Multimedia** | `Pygame Mixer` (encapsulado en `AudioPlayerSkill`, reproducción bajo demanda) |
| **Integración LLM / IA** | SDK `google-genai` (`gemini-2.5-flash`) con respaldo determinista local (*fallback*) |
| **Agente Implementado** | `MusicHostAgent` ("DJ Nova"), configurable vía `config/agent_persona.json` |
| **Skills Encapsuladas** | `AudioPlayerSkill`, `ScoringAndRulesSkill`, `MusicTriviaSkill` |
| **Reglas de Negocio** | 10 rondas • 4 opciones del mismo artista • 2 intentos/ronda • Umbral de victoria: ≥ 60/100 pts |
| **Formatos Soportados** | Audio `.mp3` / `.wav` (entrada) • Configuración `.json` |
| **Dependencias Externas** | `pygame`, `google-genai` (opcional para pistas generativas) |
