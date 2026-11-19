class ScoringAndRulesSkill:
    """Skill que gestiona vidas, puntajes, penalizaciones y condición de victoria."""

    def __init__(self, rules_config: dict):
        self.rules = rules_config
        self.score = 0
        self.attempts_left = self.rules["max_attempts_per_track"]
        self.hint_used = False

    def reset_round(self):
        self.attempts_left = self.rules["max_attempts_per_track"]
        self.hint_used = False

    def apply_hint_penalty(self) -> int:
        if not self.hint_used:
            self.score = max(0, self.score - self.rules["hint_penalty"])
            self.hint_used = True
        return self.score

    def evaluate_guess(self, user_choice: str, correct_title: str) -> dict:
        if user_choice == correct_title:
            earned = self.rules["points_with_hint"] if self.hint_used else self.rules["points_no_hint"]
            self.score += earned
            return {
                "is_correct": True,
                "round_over": True,
                "points_earned": earned,
                "total_score": self.score
            }
        
        self.attempts_left -= 1
        return {
            "is_correct": False,
            "round_over": self.attempts_left <= 0,
            "attempts_left": self.attempts_left,
            "total_score": self.score
        }

    def check_game_victory(self, max_possible_score: int) -> dict:
        won = self.score >= self.rules["win_threshold_score"]
        return {
            "won": won,
            "final_score": self.score,
            "threshold": self.rules["win_threshold_score"],
            "max_score": max_possible_score
        }