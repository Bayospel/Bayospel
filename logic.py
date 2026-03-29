from fuzzywuzzy import process

# Bayospel's "Skill Map"
KNOWN_COMMANDS = {
    "scan network": ["scan", "network scan", "recon", "check ports"],
    "open whatsapp": ["whatsapp", "open chat", "messages"],
    "lock laptop": ["lock", "secure computer", "laptop lock"],
    "mobile data": ["data on", "internet on", "turn on data"]
}

def correct_command(spoken_text):
    # 1. Flatten the dictionary to a list of all variations
    all_variations = [item for sublist in KNOWN_COMMANDS.values() for item in sublist]
    
    # 2. Find the closest match (Scoring out of 100)
    best_match, score = process.extractOne(spoken_text.lower(), all_variations)
    
    # 3. Decision Logic
    if score > 85:
        # High confidence: Just do it
        return best_match, True
    elif score > 50:
        # Low confidence: Ask the user
        return best_match, False
    else:
        # No clue what was said
        return None, False

