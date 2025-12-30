import tkinter as tk

root = tk.Tk()

class Test_Data:
    def __init__(self, label_text, pady_value):
        self.label_text = label_text
        self.pady_value = pady_value

test_data = Test_Data("Hello, Tkinter!", 10)

label = tk.Label(root)

def create_label(text, pady):
    label = tk.Label(root, text=text)
    label.pack(pady=pady)

for _ in range(10):
    create_label(test_data.label_text, test_data.pady_value)

label.pack(pady=test_data.pady_value)

root.mainloop()