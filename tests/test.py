import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


file_path = filedialog.askopenfilename(
        title="파일을 선택하세요",
        filetypes=[("모든 파일", "*.png, *.jpg")]
    )

print(file_path)