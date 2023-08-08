import tkinter as tk
import winsound
import csv
import os

class TimerApp:
    def __init__(self, root, saveFile="timings.csv"):
        self.root = root
        self.root.title("Timer Application")
        self.saveFile = saveFile

        self.timer_value = 0
        self.is_running = False
        self.is_counting_down = False
        self.loop_number = 0
        self.bell_sound = '\a'  # Bell sound (may not work on all systems)

        self.timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 20))
        self.timer_label.pack(pady=20)

        self.button = tk.Button(root, text="Start", font=("Helvetica", 14), command=self.toggle_timer)
        self.button.pack()

        self.timings = []

    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
            self.button.config(text="Stop", bg="red")
        elif self.is_running and not self.is_counting_down:
            self.stop_timer()
            self.button.config(text="Wait...", bg="grey", state=tk.DISABLED)
            self.is_counting_down = True
            self.countdown_timer(self.timer_value // 5)
        else:
            self.button.config(state=tk.DISABLED)

    def start_timer(self):
        self.is_running = True
        self.button.config(bg="red")
        self.loop_number += 1
        self.update_timer()

    def stop_timer(self):
        self.is_running = False
        self.button.config(bg="green")

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
            self.timer_label.config(text="00:00:00")
            self.button.config(state=tk.NORMAL)
            self.play_bell_sound()
            self.save_timing()
            self.timer_value = 0
            self.is_counting_down = False
            self.toggle_timer()

    @staticmethod
    def format_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def play_bell_sound(self):
        winsound.PlaySound(r"gong-with-music.wav", winsound.SND_FILENAME)

    def save_timing(self):
        focus_time = self.timer_value
        break_time = self.timer_value // 5
        self.timings.append([focus_time, break_time])
        self.write_to_csv()

    def write_to_csv(self):
        file_exists = os.path.exists(self.saveFile)
        with open(self.saveFile, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if not file_exists:
                csvwriter.writerow(['Activity', 'Time'])
            for focus, break_time in self.timings:
                csvwriter.writerow([focus, break_time])

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
