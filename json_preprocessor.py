import json

def convert_queries(input_json_path, output_json_path):
    # 读取输入 JSON
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    queries = data.get("queries", [])
    output_list = []

    for item in queries:
        # 提取所需字段
        task_id = item.get("id")
        filename = item.get("FileName")
        prompt = item.get("Question")
        answer = item.get("FinalAnswer")

        # 组织新结构
        converted = {
            "task_id": task_id,
            "spreadsheets": [filename] if filename else [],
            "prompt": prompt,
            "answer": answer
        }

        output_list.append(converted)

    # 写出到新 JSON 文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)

    print(f"转换完成！输出已保存到：{output_json_path}")


if __name__ == "__main__":
    convert_queries("QA_final.json", "QA_GRP.json")
