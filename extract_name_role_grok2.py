import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define a list of common titles
titles = ["Mr.", "Mrs.", "Ms.", "Miss", "Dr.", "Prof.", "Rev.", "St.", "Sir", "Lady"]

def extract_names(person_ent, titles):
    # Find the first token that is not a title
    i = 0
    while i < len(person_ent) and person_ent[i].text in titles:
        i += 1
    name_tokens = person_ent[i:]
    
    if len(name_tokens) == 0:
        return "", ""  # Unlikely, but handle just in case
    
    elif len(name_tokens) >= 2:
        # Multi-token name: all but last as first name, last as last name
        first_name = " ".join(t.text for t in name_tokens[:-1])
        last_name = name_tokens[-1].text
    
    else:  # len(name_tokens) == 1
        if i > 0:  # There was a title, so treat single token as last name
            first_name = ""
            last_name = name_tokens[0].text
        else:  # No title, so treat single token as first name
            first_name = name_tokens[0].text
            last_name = ""
    
    return first_name, last_name

# Example text
text = """
When Germany was set to host UEFA Euro 2024 with DT as a main sponsor, the DTDL team expected an increase of up to 10 times in viewership and wanted OneTV to deliver an amazing viewing experience. “The brand reputation was at stake,” says Abhishek Srivastava, senior director of platform engineering at DTDL. “The intention was to provide smooth streaming, with minimal interruptions and downtime, to customers.”

During FIFA World Cup in 2022, there was a network issue with one of OneTV’s integrated streaming partners, though logged-in customers could access the live stream. The DTDL team wanted to avoid another such issue this time, so it planned meticulously to enhance the product. Various teams—product engineering, data engineering, security engineering, architecture, and platform—put their heads together to prepare for the spike in viewership. “Blending the best of these teams together and making them work as one was the trick that helped us tweak our architecture and optimize our backend services,” says Srivastava.
"""

# Process the text
doc = nlp(text)

# Find appositional modifiers and link to PERSON entities
for token in doc:
    if token.dep_ == "appos":  # Check if the token is an appositional modifier
        head = token.head
        for ent in doc.ents:
            if head in ent and ent.label_ == "PERSON":
                # Extract first name and last name
                first_name, last_name = extract_names(ent, titles)
                # Extract role as before
                role_tokens = [t for t in token.subtree if t.pos_ != "PUNCT"]
                role = " ".join(t.text for t in role_tokens)
                print(f"First Name: {first_name}, Last Name: {last_name}, Role: {role}")
