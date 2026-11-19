import os
import json
import random

# Si instalas google-genai (`pip install google-genai`), el agente usará IA real;
# si no hay API key configurada, usa el fallback local automáticamente.
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class MusicTriviaSkill:
    """Skill impulsada por LLM para generar pistas dinámicas y opciones del mismo artista."""

    def __init__(self, tracks_db: list):
        self.tracks_db = tracks_db
        self.client = genai.Client() if (HAS_GENAI and os.getenv("GEMINI_API_KEY")) else None

    def get_round_options(self, track_data: dict) -> list:
        options = [track_data["titulo"]] + track_data["opciones_falsas"]
        random.shuffle(options)
        return options

    def generate_smart_hint(self, track_data: dict, agent_tone: str) -> str:
        """Usa el LLM para redactar una pista personalizada según el tono del agente."""
        if self.client:
            prompt = (
                f"Actúa con este tono: {agent_tone}. "
                f"Da una pista corta (máximo 15 palabras) sobre la canción '{track_data['titulo']}' "
                f"de {track_data['artista']} ({track_data['año']}, {track_data['genero']}). "
                f"REGLA ESTRICTA: NO menciones el título de la canción."
            )
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                return response.text.strip()
            except Exception:
                pass
        
        # Fallback determinista si no hay API Key activa
        return f"Lanzada en {track_data['año']} • Estilo {track_data['genero']}."