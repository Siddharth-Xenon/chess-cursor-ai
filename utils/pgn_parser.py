import re
from typing import List, Dict


class PGNParser:
    """
    A simple PGN (Portable Game Notation) parser to extract game moves and metadata from a PGN formatted string.
    """

    def __init__(self, pgn_data: str):
        self.pgn_data = pgn_data

    def parse(self) -> Dict[str, List[str]]:
        """
        Parses the PGN data and returns a dictionary with game metadata and moves.

        Returns:
            Dict[str, List[str]]: A dictionary containing 'metadata' and 'moves' keys.
        """
        metadata = self._extract_metadata()
        moves = self._extract_moves()
        return {"metadata": metadata, "moves": moves}

    def _extract_metadata(self) -> Dict[str, str]:
        """
        Extracts metadata from the PGN data.

        Returns:
            Dict[str, str]: A dictionary of metadata key-value pairs.
        """
        metadata_pattern = re.compile(r'\[(\w+)\s+"([^"]+)"\]')
        metadata_matches = metadata_pattern.findall(self.pgn_data)
        return {key: value for key, value in metadata_matches}

    def _extract_moves(self) -> List[str]:
        """
        Extracts the list of moves from the PGN data.

        Returns:
            List[str]: A list of moves in standard algebraic notation.
        """
        # Remove line breaks and metadata to isolate the moves string
        moves_str = re.sub(r"\n", " ", self.pgn_data)
        moves_str = re.sub(r'\[(\w+)\s+"([^"]+)"\]', "", moves_str).strip()

        # Split the moves string into individual moves, ignoring move numbers and game result
        moves = re.findall(r"\d+\.\s*([^\s]+)\s+([^\s]+)?", moves_str)
        flattened_moves = [move for pair in moves for move in pair if move]
        return flattened_moves


# Example usage
if __name__ == "__main__":
    example_pgn = """
    [Event "F/S Return Match"]
    [Site "Belgrade, Serbia JUG"]
    [Date "1992.11.04"]
    [Round "29"]
    [White "Fischer, Robert J."]
    [Black "Spassky, Boris V."]
    [Result "1/2-1/2"]

    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6
    """
    parser = PGNParser(example_pgn)
    parsed_data = parser.parse()
    print("Metadata:", parsed_data["metadata"])
    print("Moves:", parsed_data["moves"])
