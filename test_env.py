from src.nlp.symptom_extractor import SymptomExtractor

extractor = SymptomExtractor()

tests = [
    "I have fever and cough",
    "Bukhar hai aur ulti ho rahi hai",
    "Repeated fever, loose motion and stomach infection",
    "Headache with body pain",
    "Food poisoning",
]

for text in tests:

    print("=" * 60)

    print(text)

    print()

    print(extractor.extract(text))