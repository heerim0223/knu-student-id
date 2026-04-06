def main():
    import tkinter as tk
    from ui.app import GymApp

    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()