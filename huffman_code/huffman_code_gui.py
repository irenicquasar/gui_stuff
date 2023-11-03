import tkinter as tk
from tkinter import filedialog
from huffman_code import count_occurence, prob_occ, construct, generate_huffman_codes, display_huffman_code

def open_file():
    filepath = filedialog.askopenfilename()
    with open(filepath, 'r') as file:
        text = file.read()
    return text

def generate_and_display_huffman_code():
    dictionary = count_occurence(text)
    dictionary = prob_occ(dictionary, text)
    dictionary, node_dict = construct(dictionary)
    root = next(iter(node_dict.values()))
    huffman_code = generate_huffman_codes(root)
    output_text = display_huffman_code(text, huffman_code)
    output_text_widget.delete(1.0, tk.END)  # Clear the Text widget
    output_text_widget.insert(tk.END, output_text)  # Insert the new text

root = tk.Tk()

text = ''  # Initialize text variable

def open_file_button_clicked():
    global text  # Use the global text variable
    text = open_file()  # Update text when the "Open File" button is clicked

open_button = tk.Button(root, text="Open File", command=open_file_button_clicked)
open_button.pack()

generate_button = tk.Button(root, text="Generate Huffman Code", command=generate_and_display_huffman_code)
generate_button.pack()

output_text_widget = tk.Text(root, wrap=tk.WORD)  # Create a Text widget with word wrapping
output_text_widget.pack()

root.mainloop()