import json
from skills.audio_skill import AudioPlayerSkill
from skills.scoring_skill import ScoringAndRulesSkill
from skills.trivia_skill import MusicTriviaSkill

class MusicHostAgent:
    """Agente orquestador que combina personalidad, reglas y skills de audio/trivia."""

    def __init__(self, config_path: str, tracks_db: list):
        with open(config_path, "r", encoding="utf-8") as f:
            self.persona = json.load(f)

        self.tracks_db = tracks_db
        self.current_index = 0

        # Composición de Skills
        self.audio_skill = AudioPlayerSkill()
        self.scoring_skill = ScoringAndRulesSkill(self.persona["rules"])
        self.trivia_skill = MusicTriviaSkill(tracks_db)

    @property
    def current_track(self) -> dict:
        return self.tracks_db[self.current_index]

    def has_more_rounds(self) -> bool:
        return self.current_index < len(self.tracks_db)

    def start_round(self) -> dict:
        self.audio_skill.stop_sample()
        if not self.has_more_rounds():
            return {"game_over": True, "summary": self.scoring_skill.check_game_victory(len(self.tracks_db) * 10)}

        self.scoring_skill.reset_round()
        track = self.current_track
        return {
            "game_over": False,
            "round_number": self.current_index + 1,
            "total_rounds": len(self.tracks_db),
            "artist": track["artista"],
            "options": self.trivia_skill.get_round_options(track),
            "attempts_left": self.scoring_skill.attempts_left,
            "score": self.scoring_skill.score
        }

    def request_audio_sample(self) -> dict:
        return self.audio_skill.play_sample(self.current_track["archivo_audio"])

    def request_hint(self) -> dict:
        new_score = self.scoring_skill.apply_hint_penalty()
        hint_text = self.trivia_skill.generate_smart_hint(self.current_track, self.persona["tone"])
        return {"hint": hint_text, "score": new_score}

    def submit_answer(self, selected_title: str) -> dict:
        correct_title = self.current_track["titulo"]
        result = self.scoring_skill.evaluate_guess(selected_title, correct_title)

        if result["is_correct"]:
            self.audio_skill.stop_sample()
            self.current_index += 1
            result["agent_comment"] = f"[{self.persona['agent_name']}]: ¡Oído absoluto! Era '{correct_title}' (+{result['points_earned']} pts)."
        elif result["round_over"]:
            self.audio_skill.stop_sample()
            self.current_index += 1
            result["agent_comment"] = f"[{self.persona['agent_name']}]: Se acabaron los intentos. Sonaba '{correct_title}'."
        else:
            result["agent_comment"] = f"[{self.persona['agent_name']}]: Casi, pero no es esa. Te queda {result['attempts_left']} intento."

        return result

    def close(self):
        self.audio_skill.shutdown()