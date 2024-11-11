import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file starting from the second page, filtering out page numbers.
    """
    text = []
    with fitz.open(pdf_path) as pdf:
        for page_num in range(1, len(pdf)):  # Start from the second page
            page = pdf[page_num]
            page_text = page.get_text("text")
            filtered_text = filter_out_page_numbers(page_text)
            text.append(filtered_text)
    return "\n".join(text)

def filter_out_page_numbers(page_text):
    """
    Removes lines that look like page numbers (e.g., 'Page 1', '1', 'Page 2').
    """
    lines = page_text.splitlines()
    filtered_lines = []
    
    for line in lines:
        # Remove lines that are just numbers or have "Page" followed by a number
        if re.match(r"^(Page\s*\d+|\d+)$", line.strip(), re.IGNORECASE):
            continue  # Skip page number lines
        filtered_lines.append(line)
    
    return "\n".join(filtered_lines)

def parse_screenplay_text(raw_text):
    """
    Parses raw screenplay text and formats it into a Tiny Shakespeare style.
    """
    parsed_lines = []
    lines = raw_text.splitlines()
    scene = None

    for line in lines:
        stripped_line = line.strip()

        # Identify and handle scene headers
        if stripped_line.startswith(("INT.", "EXT.")):
            scene = stripped_line
            parsed_lines.append(f"\n{scene}\n")
        
        # Identify and handle character names and dialogues
        elif stripped_line.isupper() and len(stripped_line.split()) <= 3:
            # Assume this is a character name
            character = stripped_line
            parsed_lines.append(f"{character}:")

        # If there's already a character set, assume this line is dialogue
        elif stripped_line and parsed_lines and parsed_lines[-1].endswith(":"):
            parsed_lines[-1] += f" {stripped_line}"

        # Else treat as generic line (for descriptions or actions)
        elif stripped_line:
            parsed_lines.append(stripped_line)

    return "\n".join(parsed_lines)

def convert_screenplay_to_tiny_shakespeare_format(pdf_path, output_path):
    """
    Converts a screenplay PDF to a Tiny Shakespeare-style text format, skipping the first page.
    """
    # Step 1: Extract text from the PDF, starting from the second page
    raw_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Parse and format the text
    formatted_text = parse_screenplay_text(raw_text)
    
    # Step 3: Write the formatted text to output file
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(formatted_text)

    print(f"Screenplay converted and saved to {output_path}")


# Example usage
pdf_path = "pdfs/thedarkknight-screenplay.pdf"
output_path = "thedarkknight-screenplay.txt"
convert_screenplay_to_tiny_shakespeare_format(pdf_path, output_path)
