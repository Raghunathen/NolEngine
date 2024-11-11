import os

def merge_text_files(input_folder, output_file):
    """
    Merges all text files in a specified folder into a single output file, separated by new lines.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                
                # Add a newline separator after each file's content
                outfile.write("\n")

    print(f"All text files from '{input_folder}' have been merged into '{output_file}'.")

# Example usage
input_folder = "txts"
output_file = "NOLAAAAN.txt"
merge_text_files(input_folder, output_file)
