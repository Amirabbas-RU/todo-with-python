import tkinter as tk
import argparse
import pygame
from tkinter import messagebox, ttk
from datetime import datetime, time as dt_time
import pickle
from tkcalendar import Calendar
from time import strftime

BG_COLOR = "#282a36"
FG_PINK = "#ff79c6"
FG_GREEN = "#50fa7b"
FG_YELLOW = "#f1fa8c"
FG_WHITE = "white"
ALERT_FILE = "alert.mp3"

class ToDoApp:
    def __init__(self, root, data_file="tasks.pkl"):
        self.root = root
        self.root.title("To-Do List App")
        self.root.configure(background=BG_COLOR)

        self.data_file = data_file
        self.tasks = []
        self.load_tasks()

        self.current_date_label = tk.Label(root, text="Current Date & Time:", background=BG_COLOR, foreground=FG_PINK, font=('calibri', 20, 'bold'))
        self.current_date_label.pack()

        self.clock_label = tk.Label(root, font=('calibri', 12, 'bold'), background='purple', foreground=FG_WHITE)
        self.clock_label.pack(anchor='n', pady=10)

        self.update_clock()

        self.current_date = datetime.now().date()
        self.date_text = tk.StringVar()
        self.date_text.set(self.current_date.strftime("%Y-%m-%d"))
        self.date_label = tk.Label(root, textvariable=self.date_text, foreground=FG_GREEN, background=BG_COLOR, font=('calibri', 12, 'bold'))
        self.date_label.pack()

        self.calendar_label = tk.Label(root, text="Select Date:", background=BG_COLOR, foreground=FG_PINK, font=('calibri', 15, 'bold'))
        self.calendar_label.pack()

        self.date_picker = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.date_picker.pack()

        self.entry_frame = tk.Frame(root, background=BG_COLOR)
        self.entry_frame.pack()

        self.task_label = tk.Label(self.entry_frame, text="Task:", background=BG_COLOR, foreground=FG_YELLOW, font=('calibri', 12, 'bold'))
        self.task_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.task_entry = tk.Entry(self.entry_frame)
        self.task_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.hour_label = tk.Label(self.entry_frame, text="Hour:", background=BG_COLOR, foreground=FG_YELLOW, font=('calibri', 12, 'bold'))
        self.hour_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.hour_entry = ttk.Combobox(self.entry_frame, values=[str(i).zfill(2) for i in range(1, 13)])
        self.hour_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.minute_label = tk.Label(self.entry_frame, text="Minute:", background=BG_COLOR, foreground=FG_YELLOW, font=('calibri', 12, 'bold'))
        self.minute_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.minute_entry = ttk.Combobox(self.entry_frame, values=[str(i).zfill(2) for i in range(60)])
        self.minute_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.am_pm_label = tk.Label(self.entry_frame, text="AM/PM:", background=BG_COLOR, foreground=FG_YELLOW, font=('calibri', 12, 'bold'))
        self.am_pm_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.am_pm_var = tk.StringVar()
        self.am_pm_var.set("AM")
        self.am_pm_entry = ttk.Combobox(self.entry_frame, values=["AM", "PM"], textvariable=self.am_pm_var)
        self.am_pm_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.priority_label = tk.Label(self.entry_frame, text="Priority:", background=BG_COLOR, foreground=FG_YELLOW, font=('calibri', 12, 'bold'))
        self.priority_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.priority_var = tk.StringVar()
        self.priority_var.set("Medium")
        self.priority_entry = ttk.Combobox(self.entry_frame, values=["Low", "Medium", "High"], textvariable=self.priority_var)
        self.priority_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.complete_button = tk.Button(self.button_frame, text="Mark Complete", command=self.mark_complete, bg="lightgreen")
        self.complete_button.pack(side=tk.LEFT, padx=10)

        self.task_listbox = tk.Listbox(root, font=("Helvetica", 14), height=10, width=80)
        self.task_listbox.pack()

        self.button_frame = tk.Frame(root, background=BG_COLOR)
        self.button_frame.pack()

        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, bg="lightblue")
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.start_button = tk.Button(self.button_frame, text="Start Timer", command=self.start_timer, bg="lightgreen")
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task, bg="orange")
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="lightcoral")
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Clear Tasks", command=self.clear_tasks, bg="lightyellow")
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.filter_frame = tk.Frame(root, background=BG_COLOR)
        self.filter_frame.pack(pady=5)

        self.filter_label = tk.Label(self.filter_frame, text="Search:", background=BG_COLOR, foreground=FG_PINK, font=('calibri', 12, 'bold'))
        self.filter_label.pack(side=tk.LEFT, padx=5)

        self.filter_entry = tk.Entry(self.filter_frame, width=30)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_entry.bind("<KeyRelease>", self.filter_tasks)

        self.update_task_list()

        self.start_timer()

    def load_tasks(self):
        try:
            with open(self.data_file, "rb") as f:
                self.tasks = pickle.load(f)
            self.tasks = [t if len(t) == 5 else (*t, "Medium", False) if len(t) == 4 else (*t, False) for t in self.tasks]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open(self.data_file, "wb") as f:
            pickle.dump(self.tasks, f)

    def update_clock(self):
        time_string = strftime('%H:%M:%S %p')
        self.clock_label.config(text=time_string)
        self.clock_label.after(1000, self.update_clock)

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task, time_obj, date_obj, priority, completed in self.tasks:
            status = "✓" if completed else "○"
            priority_tag = f"[{priority}]" if priority else "[Medium]"
            self.task_listbox.insert(tk.END, f"{status} {priority_tag} {task} - {time_obj.strftime('%I:%M %p')} - {date_obj}")

    def validate_inputs(self, task, hour_str, minute_str, am_pm, selected_date):
        errors = []
        if not task or not task.strip():
            errors.append("Task description is required.")
        if not hour_str or not hour_str.isdigit() or not (1 <= int(hour_str) <= 12):
            errors.append("Hour must be between 1 and 12.")
        if not minute_str or not minute_str.isdigit() or not (0 <= int(minute_str) <= 59):
            errors.append("Minute must be between 0 and 59.")
        if am_pm not in ("AM", "PM"):
            errors.append("Please select AM or PM.")
        if not selected_date:
            errors.append("Please select a date.")
        return errors

    def add_task(self):
        task = self.task_entry.get()
        hour_str = self.hour_entry.get()
        minute_str = self.minute_entry.get()
        am_pm = self.am_pm_var.get()
        selected_date = self.date_picker.get_date()

        errors = self.validate_inputs(task, hour_str, minute_str, am_pm, selected_date)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            hour = int(hour_str) if am_pm == "AM" else int(hour_str) + 12
            minute = int(minute_str)
            time_obj = dt_time(hour, minute)
            date_obj = selected_date
            priority = self.priority_var.get()
            self.tasks.append((task.strip(), time_obj, date_obj, priority, False))
            self.save_tasks()
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.hour_entry.set('')
            self.minute_entry.set('')
            self.am_pm_var.set("AM")
            self.priority_var.set("Medium")
            self.date_picker.set_date(self.current_date)
        except ValueError:
            messagebox.showerror("Error", "Invalid hour or minute.")

    def filter_tasks(self, event=None):
        query = self.filter_entry.get().lower()
        self.task_listbox.delete(0, tk.END)
        for task, time_obj, date_obj, priority, completed in self.tasks:
            status = "✓" if completed else "○"
            display = f"{status} [{priority}] {task} - {time_obj.strftime('%I:%M %p')} - {date_obj}"
            if not query or query in task.lower() or query in priority.lower() or query in date_obj:
                self.task_listbox.insert(tk.END, display)

    def mark_complete(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a task to mark.")
            return
        index = selected_index[0]
        if 0 <= index < len(self.tasks):
            task, time_obj, date_obj, priority, completed = self.tasks[index]
            self.tasks[index] = (task, time_obj, date_obj, priority, not completed)
            self.save_tasks()
            self.update_task_list()

    def clear_tasks(self):
        self.tasks = []
        self.save_tasks()
        self.update_task_list()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.tasks[index]
            self.save_tasks()
            self.update_task_list()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a task to edit.")
            return
        index = selected_index[0]
        if index < 0 or index >= len(self.tasks):
            messagebox.showerror("Error", "Please select a valid task to edit.")
            return

        updated_task = self.task_entry.get()
        updated_hour_str = self.hour_entry.get()
        updated_minute_str = self.minute_entry.get()
        updated_am_pm = self.am_pm_var.get()
        updated_date = self.date_picker.get_date()

        errors = self.validate_inputs(updated_task, updated_hour_str, updated_minute_str, updated_am_pm, updated_date)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            updated_hour = int(updated_hour_str) if updated_am_pm == "AM" else int(updated_hour_str) + 12
            updated_minute = int(updated_minute_str)
            updated_time_obj = dt_time(updated_hour, updated_minute)
            updated_date_obj = updated_date
            updated_priority = self.priority_var.get()
            self.tasks[index] = (updated_task.strip(), updated_time_obj, updated_date_obj, updated_priority, False)
            self.save_tasks()
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.hour_entry.set('')
            self.minute_entry.set('')
            self.am_pm_var.set("AM")
            self.priority_var.set("Medium")
            self.date_picker.set_date(self.current_date)
        except ValueError:
            messagebox.showerror("Error", "Invalid hour or minute.")

    def start_timer(self):
        def check_time():
            current_time = datetime.now().time()
            tasks_to_remove = []

            for task, time_obj, _, _ in self.tasks:
                if current_time >= time_obj:
                    if task not in tasks_to_remove:
                        tasks_to_remove.append(task)
                        pygame.mixer.init()
                        sound = pygame.mixer.Sound(ALERT_FILE)
                        sound.play()
                        messagebox.showinfo("Task Reminder", f"It's time to start '{task}'!")

            self.tasks = [(task, time_obj, date_obj, priority, completed) for task, time_obj, date_obj, priority, completed in self.tasks if task not in tasks_to_remove]
            self.root.after(60000, check_time)

        check_time()

def main():
    parser = argparse.ArgumentParser(
        prog="todo.py",
        description="A tkinter to-do list with timed reminders.",
    )
    parser.add_argument(
        "-d", "--data-file", default="tasks.pkl",
        help="path to the pickle file storing tasks (default: tasks.pkl)",
    )
    args = parser.parse_args()

    root = tk.Tk()
    app = ToDoApp(root, data_file=args.data_file)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Closing the window with Ctrl+C should exit quietly instead of
        # dumping a traceback onto the terminal.
        app.save_tasks()
        root.destroy()


if __name__ == "__main__":
    main()
