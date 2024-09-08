import chardet
import re
import uuid
import json

# Define the path to the markdown file and the output JSON file
markdown_file_path = './data/questions.md'
json_output_path = './questions.json'

# Detect the encoding of the markdown file
with open(markdown_file_path, 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Read the markdown file content with the detected encoding
with open(markdown_file_path, 'r', encoding=encoding, errors='replace') as file:
    markdown_content = file.readlines()

# Variables to track the current section and category
all_questions = []
questions = []
topic = ""
topic = {}
question = ""
answer = ""
answer_heading = ""

# Process each line in the markdown file
for line in markdown_content:

    # line = line.strip()
    # line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    # line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
    # line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)

    line = line.strip()
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Bold
    line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)  # Italic
    line = re.sub(r'\_(.*?)\_', r'<i>\1</i>', line)  # Italic
    line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)  # Links
    line = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', line)  # Images
    line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)  # Inline code
    line = re.sub(r'^```(.*?)```$', r'<pre><code>\1</code></pre>', line, flags=re.DOTALL)  # Code blocks
    line = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', line)  # Blockquotes
    
    if re.match(r"^## (.+)$", line):
        if topic and questions:
            obj = {
                "area_id": uuid.uuid4().urn.strip('urn:uuid:'), 
                "topic": topic,
                "questions": questions
                }
            all_questions.append(obj)
        topic = re.match(r"^## (.+)$", line).group(1).strip()
        print(f"Topic: {topic}")
        questions = []
    # Check if the line is a Level 2 heading
    elif re.match(r"^### (.+)$", line):
        if question and answer:
            answer = answer.strip()
            if IS_LIST:
                answer = f"{answer_heading}<ul>{answer}</ul>"
            obj = {
                "question_id": uuid.uuid4().urn.strip('urn:uuid:'), 
                "question": question,
                "answer": answer
                }
            questions.append(obj)
        question = re.match(r"^### (.+)$", line).group(1).strip()
        answer = ""
    else:
        if line:
            if re.match(r"^(\-|\d\.) (.+)$", line):
                IS_LIST = True
                answer += f"<li>{re.match(r"^(\-|\d\.) (.+)$", line).group(2).strip()}</li>"
            else:
                IS_LIST = False
                answer += f"{line.strip()}"

if topic and questions:
    obj = {
        "area_id": uuid.uuid4().urn.strip('urn:uuid:'), 
        "topic": topic,
        "questions": questions
        }
    all_questions.append(obj)
# Convert the dictionary to JSON and save it to a file
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_questions, json_file, ensure_ascii=False, indent=4)

print(f"JSON file created at: {json_output_path}")