from tkinter import *                # tkinter used for GUI
from tkinter import filedialog       # here filedialog used to browse the files
from art import text2art             # here art library used to write title name 
from termcolor import colored        # termcolor is used to add colors to title
from tkinter.font import Font       

zero = u'\u200B'                    
one = u'\u200C'                # these are the zero-width characters which not visible to user and used for hiding secret in cover text
beginning = u'\u200E'
end = u'\u200F'
divider = u'\u2060'

# encode function which takdes action to hide the secret information in cover text.
# here the secret information is conveted into binary format and hide into the cover text according to zero-width characters.
def encode():                    
    global beginning, end, zero, one
    # Get the secret text
    secret = secret_text.get("1.0", END).strip()

    stringlit = [str(format(ord(u), '08b')) for u in secret]

    # Get the cover text
    public_file_path = filedialog.askopenfilename(title="Select cover file")
    with open(public_file_path, "r") as public_file:
        public = public_file.read()

    public += beginning
    for digits in str(stringlit):
        if digits == '0':
            public += zero
        elif digits == '1':
            public += one

    public += end

    # Save the stego text to a file
    stego_file_path = filedialog.asksaveasfilename(title="Save stego file")
    with open(stego_file_path, "w") as output_file:
        output_file.write('{}'.format(public))

# decode function which takes action reverse to the encode,
#here the secret information revealed from stego file and stored in another file.
def decode():
    global beginning, end, zero, one

    # Get the stego text
    stego_file_path = filedialog.askopenfilename(title="Select stego file")
    with open(stego_file_path, "r") as input_file:
        text = input_file.read()

    starting = text.index(beginning) + 1
    ending = text.index(end)
    char = ''

    # Save the decrypted text to a file
    decrypted_file_path = filedialog.asksaveasfilename(title="Save decrypted file")
    with open(decrypted_file_path, "w") as output_file:
        output_file.write('Decrypted text: ')

        for t in range(len(range(starting, ending+1))//8):
            for u in text[starting:starting+8]:
                if u == zero:
                    char += '0'
                elif u == one:
                    char += '1'

            output_file.write(chr(int(char, 2)))
            char = ''
            starting += 8

        output_file.write('\n')
        
        
        # Display the decrypted output in the GUI
        decoded_output.delete("1.0", END)
        decoded_output.insert(END, "Decrypted text location: " + decrypted_file_path)
      

# Create the main window
root = Tk()
root.title("Text Steganography")

# Set window background color
root.configure(bg='light gray')

# Create the title label
title = Label(root, text=text2art('Steganography'), fg='dark blue', font=('Courier', 15,'bold'),bg='light gray')
title.pack(pady=20)


# Create the secret text input box
secret_text_label = Label(root, text="Secret text:", relief='solid',bg='dark blue',fg='white')
secret_text_label.pack()
secret_text = Text(root, height=5,relief='solid',bg='white smoke', fg='black')
secret_text.pack()

# Create the encode button
encode_button = Button(root, text="Encode", command=encode, relief='solid', bg='dark green', fg='white')
encode_button.pack(pady=10)

# Create the decode button
decode_button = Button(root, text="Decode", command=decode, relief='solid', bg='orange', fg='black')
decode_button.pack(pady=10)

# Create the decoded output box
decoded_output_label = Label(root, text="Decoded output:", relief='solid', bg='dark blue', fg='white')
decoded_output_label.pack()
decoded_output = Text(root, height=5, relief='solid', bg='white smoke', fg='black')
decoded_output.pack()

# Run the main loop
root.mainloop()

