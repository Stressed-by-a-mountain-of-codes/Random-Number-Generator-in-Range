import tkinter as tk
from tkinter import messagebox
import random
import pyttsx3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

engine = pyttsx3.init()
histogram_data = []
job = None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def generate_number():
    global histogram_data, job

    try:
        low = int(entry_min.get())
        high = int(entry_max.get())
        if low > high:
            raise ValueError
        num = random.randint(low, high)
        histogram_data.append(num)

        result_label.config(text=f"Random Number: {num}", fg="darkgreen")
        speak(str(num))
        update_histogram()
        job = root.after(interval_ms.get(), generate_number)
    except ValueError:
        stop_auto()
        messagebox.showerror("Invalid Input", "Please enter valid integers (Min ≤ Max).")

def update_histogram():
    ax.clear()
    ax.hist(histogram_data, bins=range(min(histogram_data), max(histogram_data)+2), edgecolor='black')
    ax.set_title("Number Frequency")
    ax.set_xlabel("Number")
    ax.set_ylabel("Count")
    canvas.draw()

def start_auto():
    global job
    if job is None:
        generate_number()

def stop_auto():
    global job
    if job:
        root.after_cancel(job)
        job = None

def toggle_auto():
    if job:
        stop_auto()
        toggle_button.config(text="▶ Start Auto")
    else:
        start_auto()
        toggle_button.config(text="⏸ Stop Auto")

def reset_all():
    stop_auto()
    entry_min.delete(0, tk.END)
    entry_max.delete(0, tk.END)
    result_label.config(text="")
    histogram_data.clear()
    ax.clear()
    canvas.draw()
    toggle_button.config(text="▶ Start Auto")

root = tk.Tk()
root.title("Auto Random Number Generator with Voice & Histogram")
root.geometry("700x500")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Min:", font=("Arial", 11)).grid(row=0, column=0)
entry_min = tk.Entry(frame, width=8, font=("Arial", 12), justify="center")
entry_min.grid(row=0, column=1)

tk.Label(frame, text="Max:", font=("Arial", 11)).grid(row=0, column=2)
entry_max = tk.Entry(frame, width=8, font=("Arial", 12), justify="center")
entry_max.grid(row=0, column=3)
entry_max.bind("<Return>", lambda e: start_auto())

tk.Label(frame, text="Interval (ms):", font=("Arial", 11)).grid(row=0, column=4)
interval_ms = tk.IntVar(value=2000)
tk.Entry(frame, textvariable=interval_ms, width=8, font=("Arial", 12), justify="center").grid(row=0, column=5)

toggle_button = tk.Button(root, text="▶ Start Auto", font=("Arial", 12), command=toggle_auto)
toggle_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack()

tk.Button(root, text="Reset All", font=("Arial", 11), command=reset_all).pack(pady=5)

fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

entry_min.focus()
root.mainloop()
