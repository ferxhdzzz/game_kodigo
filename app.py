import tkinter as tk
from tkinter import messagebox
from agents.music_host_agent import MusicHostAgent

TRACKS_DB = [
    {"titulo": "Ain't In LA", "artista": "Adela", "genero": "Pop / Indie", "año": "2023", "archivo_audio": "audios/aintinla.mp3", "opciones_falsas": ["Homewrecker", "Over & Over", "Ego"]},
    {"titulo": "Boompala", "artista": "LE SSERAFIM", "genero": "K-Pop", "año": "2023", "archivo_audio": "audios/boompala.mp3", "opciones_falsas": ["ANTIFRAGILE", "UNFORGIVEN", "FEARLESS"]},
    {"titulo": "Everytime", "artista": "Ariana Grande", "genero": "Pop / R&B", "año": "2018", "archivo_audio": "audios/everytime.mp3", "opciones_falsas": ["7 rings", "thank u, next", "positions"]},
    {"titulo": "LOVE.", "artista": "Kendrick Lamar", "genero": "Hip-Hop / R&B", "año": "2017", "archivo_audio": "audios/love.mp3", "opciones_falsas": ["HUMBLE.", "DNA.", "Swimming Pools"]},
    {"titulo": "NDA", "artista": "Billie Eilish", "genero": "Alternative Pop", "año": "2021", "archivo_audio": "audios/nda.mp3", "opciones_falsas": ["bad guy", "Happier Than Ever", "ocean eyes"]},
    {"titulo": "Reminder", "artista": "The Weeknd", "genero": "R&B / Pop", "año": "2016", "archivo_audio": "audios/reminder.mp3", "opciones_falsas": ["Blinding Lights", "Starboy", "The Hills"]},
    {"titulo": "Save Your Tears", "artista": "The Weeknd", "genero": "Synthwave / Pop", "año": "2020", "archivo_audio": "audios/saveyourtears.mp3", "opciones_falsas": ["Die For You", "Can't Feel My Face", "Heartless"]},
    {"titulo": "Sawadika", "artista": "LISA", "genero": "K-Pop / Hip-Hop", "año": "2024", "archivo_audio": "audios/sawadika.mp3", "opciones_falsas": ["LALISA", "MONEY", "Rockstar"]},
    {"titulo": "Seoul City", "artista": "JENNIE", "genero": "K-Pop", "año": "2023", "archivo_audio": "audios/seoulcity.mp3", "opciones_falsas": ["SOLO", "You & Me", "Mantra"]},
    {"titulo": "Where Is My Husband", "artista": "RAYE", "genero": "Pop / Jazz", "año": "2023", "archivo_audio": "audios/whrsmyhsbn.mp3", "opciones_falsas": ["Escapism.", "Flip A Switch.", "Prada"]}
]

class GuessTheTrackUI:
    def __init__(self, root: tk.Tk, agent: MusicHostAgent):
        self.root = root
        self.agent = agent
        self.current_options = []

        self.root.title(f"Guess The Track • Host: {self.agent.persona['agent_name']}")
        self.root.geometry("480x590")
        self.root.configure(bg="#F8FAFC")
        self.root.resizable(False, False)

        self._build_ui()
        self._load_next_round()

    def _build_ui(self):
        tk.Label(self.root, text="GUESS THE TRACK", font=("Segoe UI", 16, "bold"), bg="#F8FAFC", fg="#1E293B").pack(pady=(20, 2))

        stats = tk.Frame(self.root, bg="#F8FAFC")
        stats.pack(pady=(0, 10))
        self.lbl_score = tk.Label(stats, text="Puntos: 0", font=("Segoe UI", 10, "bold"), bg="#F8FAFC", fg="#2563EB")
        self.lbl_score.grid(row=0, column=0, padx=15)
        self.lbl_attempts = tk.Label(stats, text="Intentos: ❤️❤️", font=("Segoe UI", 10, "bold"), bg="#F8FAFC", fg="#EF4444")
        self.lbl_attempts.grid(row=0, column=1, padx=15)

        tk.Button(
            self.root, text="▶  Escuchar Muestra", font=("Segoe UI", 11, "bold"),
            bg="#2563EB", fg="white", bd=0, padx=20, pady=8, cursor="hand2",
            command=self._on_play_click
        ).pack(pady=5)

        card = tk.Frame(self.root, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1, padx=20, pady=15)
        card.pack(fill="x", padx=30, pady=15)

        self.lbl_artist = tk.Label(card, text="", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#1E293B", anchor="w")
        self.lbl_artist.pack(fill="x", pady=2)
        self.lbl_hint = tk.Label(card, text="", font=("Segoe UI", 10), bg="#FFFFFF", fg="#64748B", anchor="w", wraplength=380, justify="left")
        self.lbl_hint.pack(fill="x", pady=2)

        self.btn_hint = tk.Button(
            card, text="Pedir Pista al Agente (-2 pts)", font=("Segoe UI", 9),
            bg="#EFF6FF", fg="#2563EB", bd=0, padx=10, pady=4, cursor="hand2",
            command=self._on_hint_click
        )
        self.btn_hint.pack(anchor="e", pady=(8, 0))

        options_frame = tk.Frame(self.root, bg="#F8FAFC")
        options_frame.pack(fill="x", padx=30, pady=10)
        self.option_buttons = []
        for idx in range(4):
            btn = tk.Button(
                options_frame, text="", font=("Segoe UI", 10), bg="#FFFFFF", fg="#1E293B",
                highlightbackground="#E2E8F0", highlightthickness=1, bd=0, pady=9, cursor="hand2",
                command=lambda i=idx: self._on_option_click(i)
            )
            btn.pack(fill="x", pady=4)
            self.option_buttons.append(btn)

    def _load_next_round(self):
        state = self.agent.start_round()
        if state["game_over"]:
            summary = state["summary"]
            if summary["won"]:
                messagebox.showinfo("¡Victoria!", f" Ganaste con {summary['final_score']}/{summary['max_score']} pts (mínimo {summary['threshold']}).")
            else:
                messagebox.showerror("Juego Perdido", f" Obtuviste {summary['final_score']} pts. Necesitabas {summary['threshold']} pts.")
            self.agent.close()
            self.root.quit()
            return

        self.current_options = state["options"]
        self.lbl_score.config(text=f"Puntos: {state['score']}")
        self.lbl_attempts.config(text="Intentos: " + "❤️" * state["attempts_left"])
        self.lbl_artist.config(text=f"👤 Artista: {state['artist']}  ({state['round_number']}/{state['total_rounds']})")
        self.lbl_hint.config(text="💡 Pista: Disponible bajo solicitud")
        self.btn_hint.config(state=tk.NORMAL)

        for i, btn in enumerate(self.option_buttons):
            btn.config(text=self.current_options[i], state=tk.NORMAL, bg="#FFFFFF", fg="#1E293B")

    def _on_play_click(self):
        res = self.agent.request_audio_sample()
        if res["status"] == "error":
            messagebox.showwarning("Audio no encontrado", res["message"])

    def _on_hint_click(self):
        res = self.agent.request_hint()
        self.lbl_hint.config(text=f"💡 {res['hint']}")
        self.lbl_score.config(text=f"Puntos: {res['score']}")
        self.btn_hint.config(state=tk.DISABLED)

    def _on_option_click(self, idx: int):
        res = self.agent.submit_answer(self.current_options[idx])
        self.lbl_score.config(text=f"Puntos: {res['total_score']}")

        if res["is_correct"]:
            messagebox.showinfo("¡Correcto!", res["agent_comment"])
            self._load_next_round()
        else:
            self.option_buttons[idx].config(state=tk.DISABLED, bg="#FEE2E2", fg="#991B1B")
            self.lbl_attempts.config(text="Intentos: " + ("❤️" * res["attempts_left"] if res["attempts_left"] > 0 else "❌"))
            if res["round_over"]:
                messagebox.showerror("Sin Intentos", res["agent_comment"])
                self._load_next_round()
            else:
                messagebox.showwarning("Intenta de nuevo", res["agent_comment"])

if __name__ == "__main__":
    root = tk.Tk()
    host_agent = MusicHostAgent("config/agent_persona.json", TRACKS_DB)
    app = GuessTheTrackUI(root, host_agent)
    root.mainloop()