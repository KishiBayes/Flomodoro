import tkinter as tk
import winsound
import csv
from datetime import datetime
import sys

class TimerApp:
    def __init__(self, root, saveFile="timings.csv"):
        self.root = root
        self.root.title("Flowmodoro")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.geometry("+0+0")  # Position window in top-left corner
        self.root.attributes('-alpha', 0.5)  # Set initial transparency

        self.saveFile = saveFile

        self.timer_value = 0
        self.is_running = False
        self.is_counting_down = False
        self.loop_number = 0

        # Create a frame for the top bar
        self.top_bar = tk.Frame(root, bg="black")
        self.top_bar.pack(fill=tk.X)

        # Create the draggable dots
        self.drag_dots = tk.Label(self.top_bar, text="*\n*\n*", font=("Helvetica", 14), bg="black", fg="white")
        self.drag_dots.pack(side=tk.LEFT, padx=10)

        # Create the exit button
        self.exit_button = tk.Button(self.top_bar, text="X", font=("Helvetica", 14), bg="black", fg="white",
                                     command=self.exit_program)
        self.exit_button.pack(side=tk.RIGHT, padx=10)

        # Create a label to show the timer
        self.timer_label = tk.Label(self.top_bar, text="00:00:00", font=("Helvetica", 30), bg="black", fg="white")
        self.timer_label.pack(side=tk.LEFT, padx=20)

        # Create and bind the start/stop button
        self.button = tk.Button(self.top_bar, text="Start", font=("Helvetica", 14), command=self.toggle_timer)
        self.button.pack(side=tk.LEFT, padx=20)

        # Bind mouse hover events to show/hide window and change opacity
        self.root.bind("<Enter>", self.on_enter)
        self.root.bind("<Leave>", self.on_leave)

        self.timings = []

    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
            self.button.config(text="Stop", bg="red")
        elif self.is_running and not self.is_counting_down:
            self.stop_timer()
            self.button.config(text="Start", bg="green")
            self.is_counting_down = True
            self.countdown_timer(self.timer_value // 5)
        else:
            self.button.config(state=tk.DISABLED)

    def start_timer(self):
        self.is_running = True
        self.loop_number += 1
        self.update_timer()

    def stop_timer(self):
        self.is_running = False

    def update_timer(self):
        if self.is_running:
            self.timer_value += 1
            self.timer_label.config(text=self.format_time(self.timer_value))
            self.root.after(1000, self.update_timer)

    def countdown_timer(self, seconds):
        if seconds >= 0:
            self.timer_label.config(text=self.format_time(seconds))
            self.root.after(1000, lambda: self.countdown_timer(seconds - 1))
        else:
            self.save_timing()
            self.timer_value = 0
            self.is_counting_down = False
            self.toggle_timer()
            self.play_bell_sound()

    @staticmethod
    def format_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def save_timing(self):
        focus_time = self.timer_value
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.timings.append([current_date, focus_time])
        self.write_to_csv()

    def write_to_csv(self):
        with open(self.saveFile, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for row in self.timings:
                csvwriter.writerow(row)

    def play_bell_sound(self):
        winsound.PlaySound(r"bell.wav", winsound.SND_FILENAME)

    def exit_program(self):
        self.root.destroy()

    def on_enter(self, event):
        self.root.attributes('-alpha', 1.0)  # Set window to fully opaque

    def on_leave(self, event):
        self.root.attributes('-alpha', 0.5)  # Set window back to initial transparency

    # Allow dragging the window by clicking and dragging on the top bar
    def on_drag_start(self, event):
        self.root.x = event.x
        self.root.y = event.y

    def on_drag_motion(self, event):
        deltax = event.x - self.root.x
        deltay = event.y - self.root.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def on_drag_release(self, event):
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "timings.csv"

    root = tk.Tk()
    app = TimerApp(root, saveFile=csv_file)

    # Bind the drag events to the top bar and draggable dots
    app.top_bar.bind("<ButtonPress-1>", app.on_drag_start)
    app.top_bar.bind("<B1-Motion>", app.on_drag_motion)
    app.top_bar.bind("<ButtonRelease-1>", app.on_drag_release)

    app.drag_dots.bind("<ButtonPress-1>", app.on_drag_start)
    app.drag_dots.bind("<B1-Motion>", app.on_drag_motion)
    app.drag_dots.bind("<ButtonRelease-1>", app.on_drag_release)

    root.mainloop()