# Define the file path and position
file_path = 'C:/GitRepos/Personal/Scripts/Python/Flask/flashcards_app/questions.json'
position = 23256

# Read the file in binary mode and get the byte at the specified position
with open(file_path, 'rb') as file:
    file.seek(position)
    byte = file.read(1)
    print(f"Byte at position {position}: {byte}")

# Convert the byte to its hexadecimal representation
hex_representation = byte.hex()
print(f"Hexadecimal representation: {hex_representation}")

# Try decoding the byte using 'latin-1' encoding
try:
    character = byte.decode('latin-1')
    print(f"Character at position {position} using 'latin-1': {character}")
except UnicodeDecodeError as e:
    print(f"Error decoding byte with 'latin-1': {e}")

# Read the entire file with 'latin-1' encoding and replace problematic characters
with open(file_path, 'r', encoding='latin-1', errors='replace') as file:
    content = file.read()

# Optionally, replace the problematic character with a placeholder
clean_content = content.replace('\x9d', '?')

# Save the cleaned content to a new file
output_path = 'C:/GitRepos/Personal/Scripts/Python/Flask/flashcards_app/questions.json'
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(clean_content)

print(f"Cleaned content saved to {output_path}")
