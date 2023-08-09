import tkinter as tk
import winsound
import csv
import os
from datetime import datetime
import sys
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class TimerApp:
    def __init__(self, root, saveFile="timings.csv"):
        self.root = root
        self.root.title("Flowmodoro")
        self.root.geometry("300x150")
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

        self.plot_button = tk.Button(root, text="Track Work Time", font=("Helvetica", 14), command=self.open_plot)
        self.plot_button.pack()

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, root)
        self.plot_canvas.get_tk_widget().pack()

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
        winsound.PlaySound(r"bell.wav", winsound.SND_FILENAME)

    def save_timing(self):
        focus_time = self.timer_value
        break_time = self.timer_value // 5
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.timings.append([current_date, focus_time, break_time])
        self.write_to_csv()

    def write_to_csv(self):
        file_exists = os.path.exists('timings.csv')
        with open('timings.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if not file_exists:
                csvwriter.writerow(['Date', 'Activity', 'Time'])
            for row in self.timings:
                csvwriter.writerow(row)

    def open_plot(self):
        dates = []
        counts = []

        with open(self.saveFile, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip the header row
            for row in csvreader:
                dates.append(row[0])  # Assuming dates are in the first column
                counts.append(int(row[1]))  # Assuming activity counts are in the second column

        plot_window = tk.Toplevel(self.root)
        plot_window.title("Track Work Time")
        plot_window.geometry("800x600")  # Set a smaller plot window size

        figure = Figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111)

        sns.lineplot(x=dates, y=counts, marker='x', ax=ax, label='Focus Time')
        sns.lineplot(x=dates, y=[sum(counts[:i + 1]) for i in range(len(counts))], marker='x', ax=ax,
                     label='Total Time')

        ax.set_xlabel('Date')
        ax.set_ylabel('Time')
        ax.set_title('Focus Time and Total Focus by Date')
        ax.tick_params(axis='x', rotation=45)
        ax.legend()

        canvas = FigureCanvasTkAgg(figure, master=plot_window)
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        canvas.get_tk_widget().pack()

        plot_window.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "timings.csv"

    root = tk.Tk()
    app = TimerApp(root, saveFile=csv_file)
    root.mainloop()
