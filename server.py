import sys

# Check if command-line arguments were provided
#sys.argv[0] is the script's name itself
if len(sys.argv) > 1:
    text = sys.argv[1]

    print(f"Received text from client: {text}")
    text=text.upper()
    print(text)

else:
    print("No text received.")