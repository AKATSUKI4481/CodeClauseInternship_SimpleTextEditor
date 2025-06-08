# 📝 This is a super basic text editor made using tkinter in Python.
# I added features like bold, italic, font size, alignment, etc.
# It's a beginner-friendly but functional editor!

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import tkinter.font as tkfont
import keyword
import re

# 🧱 Main Window
window = tk.Tk()
window.title("Srinjoy's Text Editor")
window.geometry("800x600")

# 🖋️ Default font
font_name = "Arial"
font_size = 12
my_font = tkfont.Font(family=font_name, size=font_size)

# 📄 Text Widget
text_box = tk.Text(window, wrap='word', undo=True, font=my_font)
text_box.pack(expand=True, fill='both')

# ✨ Configure alignment styles
text_box.tag_configure("left", justify='left')
text_box.tag_configure("center", justify='center')
text_box.tag_configure("right", justify='right')

# 🔷 Syntax highlighting styles
text_box.tag_configure("keyword", foreground="blue")
text_box.tag_configure("string", foreground="darkgreen")
text_box.tag_configure("comment", foreground="grey")

# 📊 Word Counter
word_counter = tk.Label(window, text="Words: 0", anchor='e')
word_counter.pack(fill='x', side='bottom')

# ➕ Update word count
def count_words(event=None):
    full_text = text_box.get(1.0, 'end-1c')
    word_list = full_text.split()
    total_words = len(word_list)
    word_counter.config(text="Words: " + str(total_words))

# 🎨 Syntax Highlighting
def highlight_syntax(event=None):
    text = text_box.get("1.0", "end-1c")

    # Remove old tags
    for tag in text_box.tag_names():
        if tag not in ("left", "center", "right", "bold", "italic", "underline"):
            text_box.tag_remove(tag, "1.0", "end")

    # Highlight Python keywords
    for kw in keyword.kwlist:
        for match in re.finditer(r'\b' + re.escape(kw) + r'\b', text):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            text_box.tag_add("keyword", start, end)

    # Highlight strings
    for match in re.finditer(r'(\".*?\"|\'.*?\')', text):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        text_box.tag_add("string", start, end)

    # Highlight comments
    for match in re.finditer(r'#.*', text):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        text_box.tag_add("comment", start, end)

# Bind both syntax and word count
text_box.bind('<KeyRelease>', lambda e: (count_words(), highlight_syntax()))

# 📁 File Operations
def make_new_file():
    text_box.delete(1.0, tk.END)
    window.title("Untitled - My First Text Editor")
    count_words()

def open_existing_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Python Files", "*.py"), ("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_box.delete(1.0, tk.END)
            text_box.insert(1.0, content)
        window.title(file_path + " - My First Text Editor")
        count_words()
        highlight_syntax()

def save_my_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_box.get(1.0, tk.END))
        window.title(file_path + " - My First Text Editor")

def close_window():
    window.quit()

# 💅 Styling (Bold, Italic, Underline)
def make_style(style_type):
    try:
        current_tags = text_box.tag_names("sel.first")
        if style_type in current_tags:
            text_box.tag_remove(style_type, "sel.first", "sel.last")
        else:
            text_box.tag_add(style_type, "sel.first", "sel.last")
    except:
        messagebox.showwarning("Oops!", "Select some text first!")

bold_font = tkfont.Font(text_box, text_box.cget("font"))
bold_font.configure(weight="bold")
text_box.tag_configure("bold", font=bold_font)

italic_font = tkfont.Font(text_box, text_box.cget("font"))
italic_font.configure(slant="italic")
text_box.tag_configure("italic", font=italic_font)

underline_font = tkfont.Font(text_box, text_box.cget("font"))
underline_font.configure(underline=True)
text_box.tag_configure("underline", font=underline_font)

# 🔤 Font Changes
def change_font_name():
    global font_name
    new_font = simpledialog.askstring("Font Change", "Type font name (like Arial, Courier):")
    if new_font:
        font_name = new_font
        my_font.config(family=font_name)

def change_font_size():
    global font_size
    new_size = simpledialog.askinteger("Font Size", "Enter font size (like 12, 16):")
    if new_size:
        font_size = new_size
        my_font.config(size=font_size)

# 🔃 Text Alignment
def align_text(alignment):
    try:
        text_box.tag_remove("left", "sel.first", "sel.last")
        text_box.tag_remove("center", "sel.first", "sel.last")
        text_box.tag_remove("right", "sel.first", "sel.last")
        text_box.tag_add(alignment, "sel.first", "sel.last")
    except:
        messagebox.showwarning("Oops!", "Select some text first!")

# 🧾 Menus
menu_bar = tk.Menu(window)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=make_new_file)
file_menu.add_command(label="Open", command=open_existing_file)
file_menu.add_command(label="Save", command=save_my_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=close_window)
menu_bar.add_cascade(label="File", menu=file_menu)

# Format Menu
style_menu = tk.Menu(menu_bar, tearoff=0)
style_menu.add_command(label="Bold", command=lambda: make_style("bold"))
style_menu.add_command(label="Italic", command=lambda: make_style("italic"))
style_menu.add_command(label="Underline", command=lambda: make_style("underline"))
style_menu.add_separator()
style_menu.add_command(label="Change Font", command=change_font_name)
style_menu.add_command(label="Change Size", command=change_font_size)
menu_bar.add_cascade(label="Format", menu=style_menu)

# Align Menu
align_menu = tk.Menu(menu_bar, tearoff=0)
align_menu.add_command(label="Left Align", command=lambda: align_text("left"))
align_menu.add_command(label="Center Align", command=lambda: align_text("center"))
align_menu.add_command(label="Right Align", command=lambda: align_text("right"))
menu_bar.add_cascade(label="Align", menu=align_menu)

# Set Menu Bar
window.config(menu=menu_bar)

# ⌨️ Shortcuts
window.bind('<Control-n>', lambda event: make_new_file())
window.bind('<Control-o>', lambda event: open_existing_file())
window.bind('<Control-s>', lambda event: save_my_file())
window.bind('<Control-q>', lambda event: close_window())

window.bind('<Control-b>', lambda event: make_style("bold"))
window.bind('<Control-i>', lambda event: make_style("italic"))
window.bind('<Control-u>', lambda event: make_style("underline"))

# 🚀 Start
window.mainloop()

