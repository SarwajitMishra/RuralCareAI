"""
Symptom Service for RuralCareAI

This module provides utility methods for working with symptoms:
1. Load symptoms from the trained model.
2. Convert machine names to display names.
3. Convert display names to machine names.
4. Search and retrieve symptoms.

Author: Sarwajit Kumar Mishra
"""

from pathlib import Path
import pickle


class SymptomService:
    """
    Service for handling symptom name conversions and retrieval.
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        model_dir = project_root / "models"

        with open(model_dir / "symptom_columns.pkl", "rb") as file:
            self.machine_symptoms = pickle.load(file)

        self.display_to_machine = {}
        self.machine_to_display = {}

        for symptom in self.machine_symptoms:
            display = self._machine_to_display(symptom)

            self.machine_to_display[symptom] = display
            self.display_to_machine[display] = symptom

    @staticmethod
    def _machine_to_display(symptom: str) -> str:
        """
        Convert machine name to human-readable name.

        Example:
            high_fever -> High Fever
        """
        return symptom.replace("_", " ").title()

    def get_machine_symptoms(self) -> list[str]:
        """
        Return all machine-readable symptom names.
        """
        return sorted(self.machine_symptoms)

    def get_display_symptoms(self) -> list[str]:
        """
        Return all display-friendly symptom names.
        """
        return sorted(self.display_to_machine.keys())

    def to_machine_name(self, display_name: str) -> str:
        """
        Convert display name to machine name.

        Example:
            High Fever -> high_fever
        """
        return self.display_to_machine.get(display_name)

    def to_display_name(self, machine_name: str) -> str:
        """
        Convert machine name to display name.

        Example:
            high_fever -> High Fever
        """
        return self.machine_to_display.get(machine_name)

    def to_machine_names(self, display_names: list[str]) -> list[str]:
        """
        Convert a list of display names to machine names.
        """
        return [
            self.display_to_machine[name]
            for name in display_names
            if name in self.display_to_machine
        ]

    def to_display_names(self, machine_names: list[str]) -> list[str]:
        """
        Convert a list of machine names to display names.
        """
        return [
            self.machine_to_display[name]
            for name in machine_names
            if name in self.machine_to_display
        ]

    def search(self, keyword: str) -> list[str]:
        """
        Search display names.

        Example:
            search("pain")
        """
        keyword = keyword.lower()

        return sorted([
            symptom
            for symptom in self.display_to_machine.keys()
            if keyword in symptom.lower()
        ])