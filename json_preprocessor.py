import json

def extract_topic(filename):
    """
    Extracts the topic from the FileName field.
    Example: 'employment-table01' → 'Employment'
    """
    if not filename:
        return "Unknown"
    prefix = filename.split("-")[0]
    return prefix.capitalize()


def generate_title(item):
    """
    Generates a title based on FileName and QuestionType.
    Example: Employment + Fact Checking → 'Employment Fact Checking'
    """
    topic = extract_topic(item.get("FileName"))
    qtype = item.get("QuestionType", "").strip()

    if not qtype:
        qtype = "General Task"

    return f"{topic} {qtype}"


def convert_queries(input_json_path, output_json_path):
    """
    Convert the structured QA dataset into a simplified task list.

    Input fields:
        - id
        - FileName
        - Question
        - FinalAnswer

    Output fields:
        - task_id
        - title (auto-generated)
        - spreadsheets
        - prompt
        - answer
    """
    # Load input JSON
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    queries = data.get("queries", [])
    output_list = []

    for item in queries:
        task_id = item.get("id")
        filename = item.get("FileName")
        prompt = item.get("Question")
        answer = item.get("FinalAnswer")

        # Generate title automatically
        title = generate_title(item)

        # Construct output entry
        converted = {
            "task_id": task_id,
            "title": title,
            "spreadsheets": [filename] if filename else [],
            "prompt": prompt,
            "answer": answer
        }

        output_list.append(converted)

    # Write output JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)

    print(f"Conversion completed! Output saved to: {output_json_path}")


if __name__ == "__main__":
    convert_queries("QA_final.json", "QA_GRP.json")

