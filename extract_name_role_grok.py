import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Your example text
text = """
When Germany was set to host UEFA Euro 2024 with DT as a main sponsor, the DTDL team expected an increase of up to 10 times in viewership and wanted OneTV to deliver an amazing viewing experience. “The brand reputation was at stake,” says Abhishek Srivastava, senior director of platform engineering at DTDL. “The intention was to provide smooth streaming, with minimal interruptions and downtime, to customers.”

During FIFA World Cup in 2022, there was a network issue with one of OneTV’s integrated streaming partners, though logged-in customers could access the live stream. The DTDL team wanted to avoid another such issue this time, so it planned meticulously to enhance the product. Various teams—product engineering, data engineering, security engineering, architecture, and platform—put their heads together to prepare for the spike in viewership. “Blending the best of these teams together and making them work as one was the trick that helped us tweak our architecture and optimize our backend services,” says Srivastava.
"""

# Process the text
doc = nlp(text)

# Iterate over tokens and find appositional modifiers
for token in doc:
    if token.dep_ == "appos":  # Check if the token is an appositional modifier
        head = token.head
        # Check if the head of the appositional modifier is part of a PERSON entity
        for ent in doc.ents:
            if head in ent and ent.label_ == "PERSON":
                person = ent.text
                # Extract the role as the subtree of the appositional modifier, excluding punctuation
                role_tokens = [t for t in token.subtree if t.pos_ != "PUNCT"]
                role = " ".join(t.text for t in role_tokens)
                print(f"Person: {person}, Role: {role}")
