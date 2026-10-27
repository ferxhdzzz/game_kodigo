import os
import sys
import random
import tkinter as tk
from tkinter import messagebox
import pygame

# Inicializar únicamente el módulo de audio de Pygame
pygame.mixer.init()

# Banco de canciones con discografía extendida y descripciones sintéticas
CANCIONES = [
    {
        "titulo": "Ain't In LA",
        "artista": "Adela",
        "genero": "Pop / Indie",
        "año": "2023",
        "archivo_audio": "audios/aintinla.mp3",
        "opciones_falsas": ["Homewrecker", "Over & Over", "Ego"]
    },
    {
        "titulo": "Boompala",
        "artista": "LE SSERAFIM",
        "genero": "K-Pop",
        "año": "2023",
        "archivo_audio": "audios/boompala.mp3",
        "opciones_falsas": ["ANTIFRAGILE", "UNFORGIVEN", "FEARLESS"]
    },
    {
        "titulo": "Everytime",
        "artista": "Ariana Grande",
        "genero": "Pop / R&B",
        "año": "2018",
        "archivo_audio": "audios/everytime.mp3",
        "opciones_falsas": ["7 rings", "thank u, next", "positions"]
    },
    {
        "titulo": "LOVE.",
        "artista": "Kendrick Lamar",
        "genero": "Hip-Hop / R&B",
        "año": "2017",
        "archivo_audio": "audios/love.mp3",
        "opciones_falsas": ["HUMBLE.", "DNA.", "Swimming Pools"]
    },
    {
        "titulo": "NDA",
        "artista": "Billie Eilish",
        "genero": "Alternative Pop",
        "año": "2021",
        "archivo_audio": "audios/nda.mp3",
        "opciones_falsas": ["bad guy", "Happier Than Ever", "ocean eyes"]
    },
    {
        "titulo": "Reminder",
        "artista": "The Weeknd",
        "genero": "R&B / Pop",
        "año": "2016",
        "archivo_audio": "audios/reminder.mp3",
        "opciones_falsas": ["Blinding Lights", "Starboy", "The Hills"]
    },
    {
        "titulo": "Save Your Tears",
        "artista": "The Weeknd",
        "genero": "Synthwave / Pop",
        "año": "2020",
        "archivo_audio": "audios/saveyourtears.mp3",
        "opciones_falsas": ["Die For You", "Can't Feel My Face", "Heartless"]
    },
    {
        "titulo": "Sawadika",
        "artista": "LISA",
        "genero": "K-Pop / Hip-Hop",
        "año": "2024",
        "archivo_audio": "audios/sawadika.mp3",
        "opciones_falsas": ["LALISA", "MONEY", "Rockstar"]
    },
    {
        "titulo": "Seoul City",
        "artista": "JENNIE",
        "genero": "K-Pop",
        "año": "2023",
        "archivo_audio": "audios/seoulcity.mp3",
        "opciones_falsas": ["SOLO", "You & Me", "Mantra"]
    },
    {
        "titulo": "Where Is My Husband",
        "artista": "RAYE",
        "genero": "Pop / Jazz",
        "año": "2023",
        "archivo_audio": "audios/whrsmyhsbn.mp3",
        "opciones_falsas": ["Escapism.", "Flip A Switch.", "Prada"]
    }
]

class JuegoAdivinaCancionClean:
    def __init__(self, root):
        self.root = root
        self.root.title("guess the songg")
        self.root.geometry("480x580")
        self.root.configure(bg="#F8FAFC")  # Slate muy claro
        self.root.resizable(False, False)

        self.indice_actual = 0
        self.puntaje = 0
        self.intentos_restantes = 2

        # Paleta de Colores
        self.BG_COLOR = "#F8FAFC"
        self.CARD_BG = "#FFFFFF"
        self.TEXT_MAIN = "#1E293B"
        self.TEXT_MUTED = "#64748B"
        self.ACCENT_BLUE = "#2563EB"
        self.ACCENT_HOVER = "#1D4ED8"
        self.LIGHT_BLUE = "#EFF6FF"
        self.BORDER_COLOR = "#E2E8F0"
        self.DANGER_COLOR = "#EF4444"

        self.crear_widgets()
        self.cargar_cancion()

    def crear_widgets(self):
        self.lbl_header = tk.Label(
            self.root, text="Adivina la cancion", font=("Segoe UI", 16, "bold"),
            bg=self.BG_COLOR, fg=self.TEXT_MAIN
        )
        self.lbl_header.pack(pady=(20, 2))

        frame_stats = tk.Frame(self.root, bg=self.BG_COLOR)
        frame_stats.pack(pady=(0, 10))

        self.lbl_puntaje = tk.Label(
            frame_stats, text="Puntos: 0", font=("Segoe UI", 10, "bold"),
            bg=self.BG_COLOR, fg=self.ACCENT_BLUE
        )
        self.lbl_puntaje.grid(row=0, column=0, padx=15)

        self.lbl_intentos = tk.Label(
            frame_stats, text="Intentos: ❤️❤️", font=("Segoe UI", 10, "bold"),
            bg=self.BG_COLOR, fg=self.DANGER_COLOR
        )
        self.lbl_intentos.grid(row=0, column=1, padx=15)

        # Botón de reproducción bajo demanda
        self.btn_play = tk.Button(
            self.root, text="▶  Escuchar pista", font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT_BLUE, fg="white", activebackground=self.ACCENT_HOVER,
            activeforeground="white", bd=0, padx=20, pady=8, cursor="hand2",
            command=self.reproducir_audio
        )
        self.btn_play.pack(pady=5)

        self.card = tk.Frame(self.root, bg=self.CARD_BG, highlightbackground=self.BORDER_COLOR, highlightthickness=1, padx=20, pady=15)
        self.card.pack(fill="x", padx=30, pady=15)

        self.lbl_pista1 = tk.Label(self.card, text="", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.TEXT_MAIN, anchor="w")
        self.lbl_pista1.pack(fill="x", pady=2)

        self.lbl_pista2 = tk.Label(self.card, text="", font=("Segoe UI", 10), bg=self.CARD_BG, fg=self.TEXT_MUTED, anchor="w")
        self.lbl_pista2.pack(fill="x", pady=2)

        self.btn_pista = tk.Button(
            self.card, text="Ver pistas (-2 pts)", font=("Segoe UI", 9),
            bg=self.LIGHT_BLUE, fg=self.ACCENT_BLUE, bd=0, padx=10, pady=4, cursor="hand2",
            command=self.revelar_pista
        )
        self.btn_pista.pack(anchor="e", pady=(8, 0))

        self.frame_opciones = tk.Frame(self.root, bg=self.BG_COLOR)
        self.frame_opciones.pack(fill="x", padx=30, pady=10)

        self.botones_opciones = []
        for i in range(4):
            btn = tk.Button(
                self.frame_opciones, text="", font=("Segoe UI", 10),
                bg=self.CARD_BG, fg=self.TEXT_MAIN, activebackground=self.LIGHT_BLUE,
                activeforeground=self.ACCENT_BLUE, highlightbackground=self.BORDER_COLOR,
                highlightthickness=1, bd=0, pady=9, cursor="hand2",
                command=lambda idx=i: self.verificar_opcion(idx)
            )
            btn.pack(fill="x", pady=4)
            self.botones_opciones.append(btn)

    def reproducir_audio(self):
        audio_path = CANCIONES[self.indice_actual]["archivo_audio"]
        if os.path.exists(audio_path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        else:
            messagebox.showwarning("Audio no encontrado", f"No se encontró el archivo:\n{audio_path}")

    def cargar_cancion(self):
        # Detener cualquier audio previo al pasar de ronda
        pygame.mixer.music.stop()

        if self.indice_actual < len(CANCIONES):
            cancion_actual = CANCIONES[self.indice_actual]
            self.intentos_restantes = 2
            self.pista_revelada = False
            self.actualizar_intentos_ui()

            # Cargar Pistas
            self.lbl_pista1.config(text=f"👤 Artista: {cancion_actual['artista']}")
            self.lbl_pista2.config(text="📅 Año / Género: ¿??? (Solicita pista)")
            self.btn_pista.config(state=tk.NORMAL)

            # Generar Opciones
            opcion_correcta = cancion_actual["titulo"]
            opciones = [opcion_correcta] + cancion_actual["opciones_falsas"]
            random.shuffle(opciones)
            self.opciones_actuales = opciones

            for i, btn in enumerate(self.botones_opciones):
                btn.config(text=self.opciones_actuales[i], state=tk.NORMAL, bg=self.CARD_BG, fg=self.TEXT_MAIN)

            # NOTA: Se eliminó reproducir_audio() de aquí para que NO suene automáticamente
        else:
            # Evaluación final de puntaje (Umbral de 60 puntos)
            if self.puntaje >= 60:
                messagebox.showinfo(
                    "¡Juego Ganado! 🎉",
                    f"¡Felicidades! Lograste {self.puntaje} puntos de 100 posibles.\n¡Demostraste un gran conocimiento musical!"
                )
            else:
                messagebox.showerror(
                    "Juego Perdido ❌",
                    f"Obtuviste {self.puntaje} puntos.\nNecesitabas al menos 60 puntos para ganar. ¡Inténtalo de nuevo!"
                )
            pygame.mixer.quit()
            self.root.quit()

    def revelar_pista(self):
        cancion = CANCIONES[self.indice_actual]
        if not self.pista_revelada:
            self.lbl_pista2.config(text=f"📅 Año / Género: {cancion['año']} • {cancion['genero']}")
            self.puntaje = max(0, self.puntaje - 2)
            self.pista_revelada = True
            self.btn_pista.config(state=tk.DISABLED)
            self.lbl_puntaje.config(text=f"Puntos: {self.puntaje}")

    def actualizar_intentos_ui(self):
        corazones = "❤️" * self.intentos_restantes
        if self.intentos_restantes == 0:
            corazones = "❌"
        self.lbl_intentos.config(text=f"Intentos: {corazones}")

    def verificar_opcion(self, indice_seleccionado):
        respuesta_usuario = self.opciones_actuales[indice_seleccionado]
        respuesta_correcta = CANCIONES[self.indice_actual]["titulo"]

        if respuesta_usuario == respuesta_correcta:
            pygame.mixer.music.stop()
            puntos_ganados = 10 if not self.pista_revelada else 7
            self.puntaje += puntos_ganados
            messagebox.showinfo("¡Correcto!", f"✨ ¡Excelente! Es '{respuesta_correcta}'.\n+{puntos_ganados} puntos.")
            self.indice_actual += 1
            self.lbl_puntaje.config(text=f"Puntos: {self.puntaje}")
            self.cargar_cancion()
        else:
            self.intentos_restantes -= 1
            self.actualizar_intentos_ui()
            
            # Deshabilitar la opción fallida
            self.botones_opciones[indice_seleccionado].config(state=tk.DISABLED, bg="#FEE2E2", fg="#991B1B")

            if self.intentos_restantes > 0:
                messagebox.showwarning("Incorrecto", "❌ Respuesta equivocada. Te queda 1 intento para esta canción.")
            else:
                pygame.mixer.music.stop()
                messagebox.showerror("Sin Intentos", f"💥 Perdiste esta ronda. La canción era '{respuesta_correcta}'.")
                self.indice_actual += 1
                self.cargar_cancion()

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoAdivinaCancionClean(root)
    root.mainloop()