import tkinter as tk
from src.visual import CampusNavigator

def main():
    try:
        root = tk.Tk()
        app = CampusNavigator(root) 
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        root.quit()


if __name__ == "__main__":
    main()
