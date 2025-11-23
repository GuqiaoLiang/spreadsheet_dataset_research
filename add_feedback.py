import json
import random

INPUT_FILE = "QA_GRP.json"             # Your original tasks
OUTPUT_FILE = "QA_GRP_with_feedback.json"   # Output file with auto feedback
RULES_FILE = "feedback_rules.json"          # The rule list


def load_rules(path):
    """Load rule definitions from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tasks(path):
    """Load task list to be enriched with feedback."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_matching_rule(prompt, rules):
    """
    Return the best-matching feedback template from rules.
    - Case-insensitive keyword matching
    - Scores rules by number of matched keywords
    - Randomly selects one feedback item from the rule's feedback list
    """
    p = prompt.lower()
    best_rule = None
    best_score = 0

    for rule in rules:
        score = sum(1 for kw in rule["keywords"] if kw.lower() in p)
        if score > best_score:
            best_score = score
            best_rule = rule

    if best_rule and best_score > 0:
        return random.choice(best_rule["feedback"])  # pick one natural variant

    return None


def generate_feedback(prompt, rules):
    """
    Generate a feedback message using rules.
    Uses the best matching rule (via find_matching_rule).
    Falls back to a general clarification message.
    """
    feedback = find_matching_rule(prompt, rules)

    if feedback:
        return feedback

    # General fallback
    fallback_feedbacks = [
        "Could you clarify how ambiguous or missing information should be handled in this task?",
        "Some details seem unspecified—how would you prefer the agent to address unclear values?",
        "Would you like to specify how edge cases or incomplete data should be managed?",
        "Should the agent make assumptions when the instructions are unclear, or ask for confirmation first?"
    ]

    return random.choice(fallback_feedbacks)


def main():
    print("Loading rules...")
    rules = load_rules(RULES_FILE)

    print("Loading tasks...")
    tasks = load_tasks(INPUT_FILE)

    print("Processing tasks...")
    updated = []
    for task in tasks:
        fb = generate_feedback(task["prompt"], rules)
        task["feedback"] = fb
        updated.append(task)

    print("Saving output...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=4, ensure_ascii=False)

    print(f"Done! Processed {len(updated)} tasks.")
    print(f"Output written to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
