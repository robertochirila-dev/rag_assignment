import json
import re
from typing import Dict, List, Tuple, Optional

class InputValidationError(Exception):
    pass

class MeasurementExtractionError(Exception):
    pass

class BraFittingRAG:
    def __init__(self):
        self.load_knowledge_base()
        self.similarity_threshold = 0.5  # Lowered for more flexible matching

    def load_knowledge_base(self):
        try:
            with open('app/data/bra_fitting_data.json', 'r') as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            self.knowledge_base = []

    def extract_measurements(self, query: str) -> Tuple[int, int]:
        # Look for patterns like "34 underbust", "38 bust", etc.
        underbust = bust = None
        matches = re.findall(r'(\d{2,3})\s*(underbust|under|band)', query.lower())
        if matches:
            underbust = int(matches[0][0])
        matches = re.findall(r'(\d{2,3})\s*(bust|over)', query.lower())
        if matches:
            bust = int(matches[0][0])
        # Fallback: try to extract two numbers if not labeled
        if underbust is None or bust is None:
            numbers = [int(s) for s in re.findall(r'\d{2,3}', query)]
            if len(numbers) >= 2:
                underbust, bust = numbers[0], numbers[1]
        if underbust is None or bust is None:
            raise MeasurementExtractionError("Could not extract both underbust and bust measurements.")
        if not (24 <= underbust <= 50 and 28 <= bust <= 60 and bust > underbust):
            raise InputValidationError("Measurements out of plausible range or bust not greater than underbust.")
        return underbust, bust

    def calculate_fit_similarity(self, query: str, context: Dict, user_issues: List[str]) -> float:
        # Extract context measurements from description
        try:
            context_underbust, context_bust = self.extract_measurements(context.get('description', ''))
            user_underbust, user_bust = self.extract_measurements(query)
        except Exception:
            return 0.0

        # Measurement similarity
        diff = abs(user_underbust - context_underbust) + abs(user_bust - context_bust)
        measurement_similarity = max(0, 1 - diff / 10)

        # Fit issue similarity
        context_issues = context.get('common_issues', [])
        issue_overlap = len(set(user_issues) & set(context_issues))
        issue_similarity = issue_overlap / max(1, len(set(user_issues + context_issues)))

        return 0.7 * measurement_similarity + 0.3 * issue_similarity

    def identify_fit_issues(self, query: str) -> List[str]:
        issues = []
        common_problems = {
            "riding up": "band_riding_up",
            "falling": "straps_falling",
            "digging": "straps_digging",
            "wrinkle": "cup_wrinkling",
            "overflow": "quadraboob",
            "quadraboob": "quadraboob",
            "gap": "cup_gaping",
            "tight": "band_too_tight",
            "loose": "band_too_loose"
        }
        for keyword, issue in common_problems.items():
            if keyword in query.lower():
                issues.append(issue)
        return issues

    def get_sister_sizes(self, size: str) -> List[str]:
        # Simple sister size logic for demonstration
        # e.g., 34C -> 32D, 36B
        import re
        match = re.match(r"(\d+)([A-Z]+)", size)
        if not match:
            return []
        band = int(match.group(1))
        cup = match.group(2)
        cup_order = "AA A B C D DD E F FF G GG H HH J JJ K".split()
        if cup not in cup_order:
            return []
        idx = cup_order.index(cup)
        sisters = []
        # Down band, up cup
        if band > 26 and idx + 1 < len(cup_order):
            sisters.append(f"{band-2}{cup_order[idx+1]}")
        # Up band, down cup
        if band < 48 and idx - 1 >= 0:
            sisters.append(f"{band+2}{cup_order[idx-1]}")
        return sisters

    def get_recommendation(self, query: str) -> Dict:
        try:
            if not query.strip():
                raise InputValidationError("Query is empty.")

            identified_issues = self.identify_fit_issues(query)
            self.extract_measurements(query)

            relevant_fits = []
            for context in self.knowledge_base:
                similarity = self.calculate_fit_similarity(query, context, identified_issues)
                if similarity > self.similarity_threshold:
                    relevant_fits.append({
                        'context': context,
                        'similarity': similarity
                    })

            if not relevant_fits:
                return {
                    "recommendation": None,
                    "confidence": 0.0,
                    "reasoning": "No close match found. Please check your measurements or try describing your fit issues differently.",
                    "fit_tips": "Consult our measurement guide or contact support.",
                    "identified_issues": identified_issues,
                    "sister_sizes": []
                }

            best_match = max(relevant_fits, key=lambda x: x['similarity'])
            rec_size = best_match['context']['recommendation']
            sister_sizes = self.get_sister_sizes(rec_size)

            return {
                "recommendation": rec_size,
                "confidence": round(best_match['similarity'], 2),
                "reasoning": best_match['context']['reasoning'],
                "fit_tips": best_match['context']['fit_tips'],
                "identified_issues": identified_issues,
                "sister_sizes": sister_sizes
            }

        except (InputValidationError, MeasurementExtractionError) as e:
            return {
                "error": str(e),
                "recommendation": None,
                "confidence": 0.0,
                "reasoning": str(e),
                "fit_tips": "Please provide valid measurements (e.g., '34 underbust, 38 bust').",
                "identified_issues": [],
                "sister_sizes": []
            }
        except Exception as e:
            return {
                "error": "Internal server error.",
                "recommendation": None,
                "confidence": 0.0,
                "reasoning": "An unexpected error occurred.",
                "fit_tips": "Please try again later.",
                "identified_issues": [],
                "sister_sizes": []
            }