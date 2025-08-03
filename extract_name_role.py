import spacy
import re

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def extract_persons_and_roles(text):
    doc = nlp(text)
    results = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Search for a title or role nearby using token dependency
            person = ent.text
            role = None

            # Look to the right for appositional phrase or prepositional phrase
            for token in ent.root.rights:
                if token.dep_ in ("appos", "attr", "conj", "prep"):
                    role_span = [token]
                    role_span.extend([child for child in token.subtree])
                    role = " ".join(sorted({t.text for t in role_span}, key=lambda x: text.find(x)))
                    break

            # Look to the left for roles in patterns like "CEO John Smith"
            if not role:
                for token in ent.root.head.lefts:
                    if token.dep_ in ("compound", "amod", "nmod") and token.pos_ in ("NOUN", "PROPN"):
                        role = token.text
                        break

            results.append((person, role))

    return results

# Example usage
text = """When Germany was set to host UEFA Euro 2024 with DT as a main sponsor, the DTDL team expected an increase of up to 10 times in viewership and wanted OneTV to deliver an amazing viewing experience. “The brand reputation was at stake,” says Abhishek Srivastava, senior director of platform engineering at DTDL. “The intention was to provide smooth streaming, with minimal interruptions and downtime, to customers.”

During FIFA World Cup in 2022, there was a network issue with one of OneTV’s integrated streaming partners, though logged-in customers could access the live stream. The DTDL team wanted to avoid another such issue this time, so it planned meticulously to enhance the product. Various teams—product engineering, data engineering, security engineering, architecture, and platform—put their heads together to prepare for the spike in viewership. “Blending the best of these teams together and making them work as one was the trick that helped us tweak our architecture and optimize our backend services,” says Srivastava.
"""

for name, role in extract_persons_and_roles(text):
    print(f"Name: {name}, Role: {role}")

