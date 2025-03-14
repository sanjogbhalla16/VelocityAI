from langchain.text_splitter import RecursiveCharacterTextSplitter

# Function to process scraped F1 content into Q&A format
def split_f1_data(input_text):
    """
    Splits F1-related scraped text into structured questions and answers.
    
    Args:
        input_text (dict): Dictionary with "title" and "content" keys.
    
    Returns:
        dict: Structured Q&A format.
    """
    output_dict = {"title": input_text["title"]}

    # Split content into lines
    all_lines = input_text["content"].split("\n")

    # Identify lines that contain questions
    question_lines = [i for i, line in enumerate(all_lines) if "?" in line]

    # Initialize lists for questions and answers
    questions = []
    paragraphs = []

    # If the first line is not a question, treat it as an intro
    if question_lines and question_lines[0] != 0:
        output_dict["first_paragraph"] = "\n".join(all_lines[:question_lines[0] - 1])
    else:
        output_dict["first_paragraph"] = None

    # Extract Q&A pairs
    for i in range(len(question_lines) - 1):
        question = all_lines[question_lines[i]].strip()
        answer = "\n".join(all_lines[question_lines[i] + 1: question_lines[i + 1]]).strip()

        if question and answer:
            questions.append(question)
            paragraphs.append(answer)

    # Handle last Q&A pair
    if question_lines:
        last_question = all_lines[question_lines[-1]].strip()
        last_answer = "\n".join(all_lines[question_lines[-1] + 1:]).strip()

        if last_question and last_answer:
            questions.append(last_question)
            paragraphs.append(last_answer)

    # If we have more paragraphs than questions, adjust
    if len(paragraphs) > len(questions):
        output_dict["first_paragraph"] = paragraphs[0]
        paragraphs.pop(0)

    output_dict["questions"] = questions
    output_dict["answers"] = paragraphs

    return output_dict
