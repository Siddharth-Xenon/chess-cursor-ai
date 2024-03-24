import openai
from typing import List
from config.firebase_config import get_openai_api_key
from models.insight import InsightModel


class OpenAIService:
    def __init__(self):
        self.openai_api_key = get_openai_api_key()
        openai.api_key = self.openai_api_key

    def analyze_game(self, pgn: str) -> List[InsightModel]:
        """
        Analyzes a chess game in PGN format and generates insights
        such as bad moves, excellent moves, and book moves.
        """
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=self._generate_prompt(pgn),
                temperature=0.7,
                max_tokens=150,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["\n"],
            )
            insights = self._parse_response(response.choices[0].text)
            return insights
        except Exception as e:
            print(f"Error analyzing game with OpenAI: {e}")
            return []

    def _generate_prompt(self, pgn: str) -> str:
        """
        Generates a prompt for the OpenAI API based on the PGN.
        """
        prompt = f"Given the following chess game in PGN format:\n{pgn}\n"
        prompt += "Identify any bad moves, excellent moves, and book moves. Provide insights for each identified move."
        return prompt

    def _parse_response(self, response: str) -> List[InsightModel]:
        """
        Parses the response from OpenAI into a list of InsightModel instances.
        """
        insights = []
        # This is a simplified parser. You might need a more sophisticated parser
        # depending on the complexity and format of the response from OpenAI.
        lines = response.split("\n")
        for line in lines:
            parts = line.split(":")
            if len(parts) == 2:
                move, insight_type = parts[0].strip(), parts[1].strip()
                insights.append(
                    InsightModel(move=move, insight_type=insight_type, description=line)
                )
        return insights


# Example usage
# openai_service = OpenAIService()
# insights = openai_service.analyze_game("Your PGN data here")
# for insight in insights:
#     print(insight)
