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
├── app.py                # Código fuente principal de la aplicación
├── README.md             # Documentación del proyecto
└── audios/               # Carpeta con los fragmentos de audio en MP3
    ├── aintinla.mp3
    ├── boompala.mp3
    ├── everytime.mp3
    ├── love.mp3
    ├── nda.mp3
    ├── reminder.mp3
    ├── saveyourtears.mp3
    ├── sawadika.mp3
    ├── seoulcity.mp3
    └── whrsmyhsbn.mp3
