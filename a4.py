import Profile
import ds_protocol
from pathlib import Path
import gui
import tkinter as tk
def main():
    print('Welcome to ICS32 Messages')  #Instructions

    root = tk.Tk()

    root.title("ICS32 Messages")
    app = gui.MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()