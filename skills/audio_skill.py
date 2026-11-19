import os
import pygame

class AudioPlayerSkill:
    """Skill encargada exclusivamente de gestionar la reproducción de muestras MP3."""
    
    def __init__(self):
        pygame.mixer.init()

    def play_sample(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"Archivo no encontrado: {file_path}"}
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        return {"status": "playing", "track": file_path}

    def stop_sample(self) -> None:
        pygame.mixer.music.stop()

    def shutdown(self) -> None:
        pygame.mixer.quit()