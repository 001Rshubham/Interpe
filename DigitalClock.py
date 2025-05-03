# Importing necessary libraries
import tkinter as tk  # For GUI creation
from tkinter import ttk, messagebox, simpledialog, font  # For additional tkinter components
from datetime import datetime  # For working with date and time
import threading, time  # For handling multiple threads and time delays
import pytz  # For time zone handling
 

# === CONFIGURATION ===
TIME_ZONES = ['Asia/Kolkata','UTC', 'US/Eastern', 'Europe/London',  'Asia/Tokyo', 'Australia/Sydney']  # List of available time zones
THEMES = {
    'Dark': {'bg': '#000000', 'fg': '#00FFFF'},  # Dark theme with black background and cyan text
    'Light': {'bg': '#FFFFFF', 'fg': '#00008B'},  # Light theme with white background and dark blue text
    'Solarized': {'bg': '#002B36', 'fg': '#839496'},  # Solarized theme with a dark background and grayish text
}
FONTS = ['Courier New', 'Arial', 'Helvetica', 'Times New Roman', 'Digital-7']  # List of fonts available for selection


class DigitalClockApp(tk.Tk):  # Define the main application class
    def __init__(self):
        super().__init__()  # Initialize the parent class (Tk)
        self.title("Advanced Digital Clock")  # Set the window title
        self.geometry("650x250")  # Set the window size
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event

        # State variables
        self.current_tz = pytz.timezone('Asia/Kolkata')  # Default time zone is UTC
        self.theme_name = 'Dark'  # Default theme
        self.font_name = 'Courier New'  # Default font
        self.alarm_time = None  # Initially, no alarm set
        self.stopwatch_running = False  # Stopwatch not running initially
        self.timer_running = False  # Timer not running initially
    

        self.create_widgets()  # Create the widgets (buttons, labels, etc.)
        self.apply_theme()  # Apply the default theme
        self.update_time_loop()  # Start the time updating loop
         
    def create_widgets(self):
        # Create a top control frame for buttons and settings
        ctrl = ttk.Frame(self)
        ctrl.pack(fill='x', pady=5)  # Fill horizontally, with some vertical padding

        # Theme selection
        ttk.Label(ctrl, text="Theme:").pack(side='left')  # Label for Theme
        self.theme_cb = ttk.Combobox(ctrl, values=list(THEMES.keys()), state='readonly')  # Dropdown for theme selection
        self.theme_cb.set(self.theme_name)  # Set the default theme
        self.theme_cb.pack(side='left', padx=2)  # Pack the combobox with horizontal padding
        self.theme_cb.bind('<<ComboboxSelected>>', lambda e: self.change_theme())  # Bind selection change to theme change function

        # Font selection
        ttk.Label(ctrl, text="Font:").pack(side='left')  # Label for Font
        self.font_cb = ttk.Combobox(ctrl, values=FONTS, state='readonly')  # Dropdown for font selection
        self.font_cb.set(self.font_name)  # Set the default font
        self.font_cb.pack(side='left', padx=2)  # Pack the combobox with horizontal padding
        self.font_cb.bind('<<ComboboxSelected>>', lambda e: self.change_font())  # Bind selection change to font change function

        # Time zone selection
        ttk.Label(ctrl, text="Time Zone:").pack(side='left')  # Label for Time Zone
        self.tz_cb = ttk.Combobox(ctrl, values=TIME_ZONES, state='readonly')  # Dropdown for time zone selection
        self.tz_cb.set('Asia/Kolkata')  # Set the default time zone to UTC
        self.tz_cb.pack(side='left', padx=2)  # Pack the combobox with horizontal padding
        self.tz_cb.bind('<<ComboboxSelected>>', lambda e: self.change_timezone())  # Bind selection change to time zone change function

        # Fullscreen toggle button
        self.full_btn = ttk.Button(ctrl, text="Fullscreen", command=self.toggle_fullscreen)  # Button to toggle fullscreen mode
        self.full_btn.pack(side='right')  # Pack the button to the right side

        # Clock display labels
        self.time_lbl = ttk.Label(self, text="", font=(self.font_name, 48))  # Label for the time display
        self.time_lbl.pack(pady=5)  # Pack with vertical padding
        self.date_lbl = ttk.Label(self, text="", font=(self.font_name, 14))  # Label for the date display
        self.date_lbl.pack()  # Pack the date label
        self.weather_lbl = ttk.Label(self, text="", font=(self.font_name, 12))  # Label for the weather display
        self.weather_lbl.pack(pady=5)  # Pack with vertical padding

        # Bottom control buttons for alarm, stopwatch, and timer
        bottom = ttk.Frame(self)  # Frame for the bottom controls
        bottom.pack(fill='x', pady=5)  # Pack the frame horizontally with some vertical padding
        ttk.Button(bottom, text="Set Alarm", command=self.set_alarm).pack(side='left', padx=5)  # Button to set alarm
        ttk.Button(bottom, text="Stopwatch", command=self.open_stopwatch).pack(side='left')  # Button to open stopwatch
        ttk.Button(bottom, text="Timer", command=self.open_timer).pack(side='left')  # Button to open timer

    def apply_theme(self):
        th = THEMES[self.theme_name]  # Get the selected theme
        self.configure(bg=th['bg'])  # Set the window background color
        # Set the background and foreground colors for each label
        for w in [self.time_lbl, self.date_lbl, self.weather_lbl]:
            w.configure(background=th['bg'], foreground=th['fg'])

    def change_theme(self):
        self.theme_name = self.theme_cb.get()  # Get the selected theme from the combobox
        self.apply_theme()  # Apply the selected theme

    def change_font(self):
        self.font_name = self.font_cb.get()  # Get the selected font from the combobox
        # Apply the selected font to the time, date, and weather labels
        self.time_lbl.configure(font=(self.font_name, 48))
        self.date_lbl.configure(font=(self.font_name, 14))
        self.weather_lbl.configure(font=(self.font_name, 12))

    def change_timezone(self):
        self.current_tz = pytz.timezone(self.tz_cb.get())  # Change the time zone based on selection

    def toggle_fullscreen(self):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))  # Toggle fullscreen mode

    def update_time_loop(self):
        now = datetime.now(self.current_tz)  # Get the current time in the selected time zone
        self.time_lbl.config(text=now.strftime("%I:%M:%S %p"))  # Update the time label
        self.date_lbl.config(text=now.strftime("%A, %d %B %Y"))  # Update the date label
        # Check if it's time for the alarm
        if self.alarm_time and now.strftime("%I:%M %p") == self.alarm_time:
            messagebox.showinfo("Alarm", f"Alarm! {self.alarm_time}")  # Show an alarm message
            self.alarm_time = None  # Reset the alarm time
        self.after(200, self.update_time_loop)  # Update every 200 milliseconds

    def set_alarm(self):
        t = simpledialog.askstring("Set Alarm", "Enter alarm time (HH:MM AM/PM):")  # Ask for alarm time input
        if t:
            self.alarm_time = t  # Set the alarm time if valid

    def open_stopwatch(self):
        if hasattr(self, 'sw_win') and self.sw_win.winfo_exists(): return  # Avoid opening multiple stopwatch windows
        self.sw_win = tk.Toplevel(self)  # Create a new top-level window for the stopwatch
        self.sw_win.title("Stopwatch")  # Set the title for the stopwatch window
        lbl = ttk.Label(self.sw_win, text="00:00:00", font=(self.font_name, 24))  # Label for the stopwatch display
        lbl.pack(pady=10)  # Pack the label with vertical padding
        bk = {'running': False, 'start': 0, 'elapsed':0}  # Stopwatch state

        # Function to update stopwatch time
        def sw_loop():
            if bk['running']:
                bk['elapsed'] = time.time() - bk['start']  # Calculate elapsed time
                lbl.config(text=time.strftime('%H:%M:%S', time.gmtime(bk['elapsed'])))  # Update display
            self.sw_win.after(100, sw_loop)  # Update every 100 milliseconds

        # Control buttons: Start, Stop, Reset
        def start():
            if not bk['running']:
                bk['running'] = True
                bk['start'] = time.time() - bk['elapsed']  # Start or resume stopwatch
        def stop(): bk['running'] = False  # Stop the stopwatch
        def reset(): bk['running'] = False; bk['elapsed'] = 0; lbl.config(text='00:00:00')  # Reset the stopwatch

        # Button frame and buttons
        btnf = ttk.Frame(self.sw_win)
        btnf.pack()
        ttk.Button(btnf, text="Start", command=start).pack(side='left')  # Start button
        ttk.Button(btnf, text="Stop", command=stop).pack(side='left')  # Stop button
        ttk.Button(btnf, text="Reset", command=reset).pack(side='left')  # Reset button

        sw_loop()  # Start the stopwatch loop

    def open_timer(self):
        if hasattr(self, 'tm_win') and self.tm_win.winfo_exists(): return  # Avoid opening multiple timer windows
        self.tm_win = tk.Toplevel(self)  # Create a new top-level window for the timer
        self.tm_win.title("Timer")  # Set the title for the timer window
        lbl = ttk.Label(self.tm_win, text="00:00", font=(self.font_name, 24))  # Label for the timer display
        lbl.pack(pady=10)  # Pack the label with vertical padding
        entry = ttk.Entry(self.tm_win)  # Entry field for setting timer duration
        entry.insert(0, '00:01:00')  # Default time (1 minute)
        entry.pack()

        bk = {'running': False, 'remaining': 0}  # Timer state

        # Function to update timer time
        def tm_loop():
            if bk['running']:
                if bk['remaining'] > 0:
                    bk['remaining'] -= 1  # Decrease remaining time
                    lbl.config(text=time.strftime('%H:%M:%S', time.gmtime(bk['remaining'])))  # Update display
                else:
                    bk['running'] = False  # Stop timer when time runs out
                    messagebox.showinfo("Timer", "Time's up!")  # Show "time's up" message
            self.tm_win.after(1000, tm_loop)  # Update every second

        # Control buttons: Start, Stop, Reset
        def start():
            h, m, s = map(int, entry.get().split(':'))  # Parse the time input
            bk['remaining'] = h * 3600 + m * 60 + s  # Convert to seconds
            bk['running'] = True  # Start the timer
        def stop(): bk['running'] = False  # Stop the timer
        def reset(): bk['running'] = False; lbl.config(text='00:00:00')  # Reset the timer

        # Button frame and buttons
        frm = ttk.Frame(self.tm_win)
        frm.pack()
        ttk.Button(frm, text="Start", command=start).pack(side='left')  # Start button
        ttk.Button(frm, text="Stop", command=stop).pack(side='left')  # Stop button
        ttk.Button(frm, text="Reset", command=reset).pack(side='left')  # Reset button

        tm_loop()  # Start the timer loop

    def on_close(self):
        self.destroy()  # Cleanly close the application

# Run the application
if __name__ == '__main__':
    app = DigitalClockApp()  # Create an instance of the DigitalClockApp class
    app.mainloop()  # Start the tkinter main event loop
