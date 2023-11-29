import tkinter as tk
from posture import PostureWatcher

class Application:

    def __init__(self, root):
        self.root = root
        self.root.title("Posture Watcher")
        self.pw = PostureWatcher()
        self.base_posture_label = tk.Label(root, text="⚠️ Please set your base posture.")
        self.base_posture_label.pack()
        self.quit_button = tk.Button(root, text="Quit", command=self.quit)
        self.quit_button.pack()
        self.update_title()

    def set_base_posture(self):
        self.pw.set_base_posture()

    def clear_base_posture(self):
        self.pw.base_posture = None

    def quit(self):
        self.pw.stop()
        self.root.quit()

    def update_title(self):
        if not self.pw.base_posture:
            self.base_posture_label.config(text="⚠️ Please set your base posture.")
        else:
            cd = self.pw.deviation.current_deviation
            if cd < 25:
                self.base_posture_label.config(text="✅ Great posture!")
            elif cd < 35:
                self.base_posture_label.config(text=f"⚠️ Improve your posture! ({cd}%)")
            else:
                self.base_posture_label.config(text=f"⛔️ Fix your posture! ({cd}%)")
        self.root.after(1000, self.update_title)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
