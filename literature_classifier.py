import os
import shutil

# CHANGE THIS TO YOUR LOCAL FOLDER
BASE_DIR = "/Users/danielar/Desktop/Culture Book"

themes = {
    "Language_&_Interpreters": [("interpreter", 3), ("language", 2), ("spanish", 2), ("lep", 3), ("concordance", 2), ("translation", 2)],
    "Education_&_Curriculum": [("pedagogy", 3), ("curriculum reform", 3), ("programmatic assessment", 3), ("simulation", 2), ("module", 1)],
    "Empathy_&_Bias": [("empathy", 3), ("bias", 3), ("moral distress", 3), ("vr", 2), ("stigma", 2), ("prejudice", 2), ("compassion", 2)],
    "Humanities_&_Reflection": [("reflection", 3), ("humanities", 3), ("narrative", 2), ("ethics", 2), ("writing", 2), ("art", 2), ("story", 1)],
    "Frameworks_&_Models": [("kleinman", 3), ("campinha", 3), ("learn", 3), ("tset", 3), ("aacm", 3), ("canmeds", 3)],
    "Migrant_&_Global_Health": [("migrant", 3), ("refugee", 3), ("global", 2), ("diversity", 2), ("immigrant", 3), ("cross-cultural", 2), ("international", 2), ("disparity", 2)]
}

# Create folders
for folder in themes:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# Move files to their best-weighted match
for foldername, _, files in os.walk(BASE_DIR):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(foldername, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().lower()
            except:
                continue

            best_match = None
            best_score = 0
            for theme, kw_pairs in themes.items():
                score = sum(weight for keyword, weight in kw_pairs if keyword in content or keyword in filename.lower())
                if score > best_score:
                    best_match = theme
                    best_score = score

            # Avoid false matches for Frameworks
            if best_match == "Frameworks_&_Models" and best_score < 6:
                continue

            if best_match:
                dest_path = os.path.join(BASE_DIR, best_match, filename)
                if os.path.abspath(filepath) != os.path.abspath(dest_path):
                    shutil.move(filepath, dest_path)
