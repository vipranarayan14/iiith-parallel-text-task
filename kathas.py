import os
import re
from pathlib import Path


def format_title(title):
    return re.sub(r"\d+\.?", "", title).strip()


def format_sloka(sloka_lines):
    return " ".join([sloka_line.strip() for sloka_line in sloka_lines])


def read_file_lines(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.readlines()


def extract_sentences_with_positions(text, start_lineno):
    sentences = []
    buffer = []
    in_quote = False
    quote_buffer = []
    current_lineno = start_lineno

    for line in text:
        line = line.strip()
        if not line:
            current_lineno += 1
            continue

        for char in line:
            if char in ('"') and not in_quote:  # Open quote
                in_quote = True
                quote_buffer = [current_lineno]
                buffer.append(char)  # Store quotes
            elif char in ('"') and in_quote:  # Close quote
                in_quote = False
                quote_buffer.append(current_lineno)
                buffer.append(char)  # Store closing quote
                sentences.append(
                    ("".join(buffer).strip(), quote_buffer[0], quote_buffer[-1])
                )
                buffer = []
            elif in_quote:
                buffer.append(char)  # Store inside quotes without breaking
            elif char == "।":  # Sentence end
                buffer.append(char)
                sentences.append(
                    ("".join(buffer).strip(), current_lineno, current_lineno)
                )
                buffer = []
            else:
                buffer.append(char)

        print("sentences", sentences)

        if buffer and not in_quote:  # Add remaining text if line ends without danda
            sentences.append(("".join(buffer).strip(), current_lineno, current_lineno))
            buffer = []

        current_lineno += 1

    return sentences


def process_story_file(filepath):
    lines = read_file_lines(filepath)
    filename = Path(filepath).stem
    slno_base = f"130-stories_{filename}"

    output_data = []

    title_lineno = 16
    sloka_lineno = 17
    prose_start_lineno = 19
    questions_start_lineno = None

    # Extract different sections
    title = format_title(lines[title_lineno - 1])
    sloka = format_sloka(lines[sloka_lineno - 1 : sloka_lineno])

    prose_text = []
    questions = []

    for i, line in enumerate(lines[prose_start_lineno:], start=prose_start_lineno):
        if "प्रश्नाः" in line:
            questions_start_lineno = i + 1
            break
        prose_text.append(line.strip())

    print(filename, prose_text)

    prose_sentences = extract_sentences_with_positions(prose_text, prose_start_lineno)

    if questions_start_lineno:
        for i in range(questions_start_lineno, len(lines)):
            if "---" in lines[i]:
                break
            questions.append((lines[i].strip(), i + 1))

    # Append to output data with position tracking
    output_data.append([f"{slno_base}_{title_lineno}", "title", title, title_lineno])
    output_data.append([f"{slno_base}_{sloka_lineno}", "sloka", sloka, sloka_lineno])

    for i, (sentence, start_lineno, end_lineno) in enumerate(prose_sentences, start=1):
        output_data.append(
            [
                f"{slno_base}_{start_lineno}-{end_lineno}",
                "prose",
                sentence,
                start_lineno,
            ]
        )

    for i, (question, start_lineno) in enumerate(questions, start=1):
        output_data.append(
            [f"{slno_base}_{start_lineno}", "question", question, start_lineno]
        )

    return output_data


# Process all files
folder_path = "130-stories-proofed"
all_data = []

files = os.listdir(folder_path)[:3]

# print(files)

for filename in files:
    if filename.endswith(".txt"):  # Adjust if different file format
        filepath = os.path.join(folder_path, filename)
        all_data.extend(process_story_file(filepath))

# Write to output file as csv
output_filename = "130-stories-output.txt"
with open(output_filename, "w", encoding="utf-8") as file:
    for row in all_data:
        file.write("\t".join(map(str, row)) + "\n")
