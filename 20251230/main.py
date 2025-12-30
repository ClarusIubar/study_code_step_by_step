import tkinter as tk

# init
root = tk.Tk()

# class
class Test_Data:
    def __init__(self, label_text, pady_value):
        self.label_text = label_text
        self.pady_value = pady_value
    
    def create_label(self):
        label = tk.Label(root, text=self.label_text)
        label.pack(pady=self.pady_value)

# instance
test_data = Test_Data("Hello, Tkinter!", 10)

# make 'n'
for _ in range(10):
    test_data.create_label()

# generate window
root.mainloop()