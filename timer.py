"""
A counter to turn off the PC after a set time.
Latest update: 16.08.2023
A desktop application to turn off your PC at a specified time.
"""

# Import necessary modules
import win32gui  
import win32con  
import time  
import subprocess  
import threading  
import importlib
import sys

# Install necessary modules
required_modules = ['wx']

missing_modules = []

for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    for module in missing_modules:
        try:
            subprocess.check_call([f"pip install {module}"])
        except subprocess.CalledProcessError as e:
            print(f'Start failed. Program will break in 5s')
            time.sleep(5)
            sys.exit()

# Import necessary modules
import wx 

# Hide the console window
win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)

# Define the CountdownApp class, derived from wx.App
class CountdownApp(wx.App):
    def OnInit(self):
        # Initialize the application
        self.frame = CountdownFrame(None, title="Timer")  # Create an instance of CountdownFrame
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# Define the CountdownFrame class, derived from wx.Frame
class CountdownFrame(wx.Frame):
    def __init__(self, parent, title):
        # Initialize the frame
        super(CountdownFrame, self).__init__(parent, title=title, size=(300, 200))
        
        # Create a panel within the frame
        self.panel = wx.Panel(self)
        
        # Create GUI components: labels, text controls, and buttons
        self.seconds_label = wx.StaticText(self.panel, label="Za ile sekund wyłączyć komputer?")
        self.seconds_textctrl = wx.TextCtrl(self.panel)
        self.start_button = wx.Button(self.panel, label="Start")
        self.stop_button = wx.Button(self.panel, label="Stop")
        
        # Bind button events to methods
        self.start_button.Bind(wx.EVT_BUTTON, self.start_countdown)
        self.stop_button.Bind(wx.EVT_BUTTON, self.stop_countdown)
        
        # Set up sizer to organize GUI components
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()  
        sizer.Add(self.seconds_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        sizer.Add(self.seconds_textctrl, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.start_button, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        sizer.Add(self.stop_button, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        sizer.AddStretchSpacer() 
        
        # Apply the sizer to the panel
        self.panel.SetSizer(sizer)
        
        # Initialize attributes for countdown
        self.countdown_thread = None
        self.running = False
        
    def start_countdown(self, event):
        # Start the countdown thread when the Start button is clicked
        if not self.running:
            try:
                seconds = int(self.seconds_textctrl.GetValue())
                if seconds < 0:
                    # Display an error message for negative input
                    wx.MessageBox("Podaj wartość większą lub równą 0.", "Błąd", wx.OK | wx.ICON_ERROR)
                    return
                self.running = True
                self.start_button.Disable()
                self.stop_button.Enable()
                self.seconds_textctrl.Disable()
                self.countdown_thread = threading.Thread(target=self.run_countdown, args=(seconds,))
                self.countdown_thread.start()
            except ValueError:
                # Display an error message for invalid input
                wx.MessageBox("Wprowadź poprawną liczbę sekund.", "Błąd", wx.OK | wx.ICON_ERROR)
    
    def stop_countdown(self, event):
        # Stop the countdown when the Stop button is clicked
        if self.running:
            self.running = False
            self.start_button.Enable()
            self.stop_button.Disable()
            self.seconds_textctrl.Enable()
    
    def run_countdown(self, seconds):
        # Run the countdown and update the display
        for i in range(seconds, 0, -1):
            if not self.running:
                break
            wx.CallAfter(self.update_display, i)
            time.sleep(1)
        if self.running:
            wx.CallAfter(self.complete_countdown)
        
    def update_display(self, remaining_seconds):
        # Update the text control with the remaining seconds
        self.seconds_textctrl.SetValue(str(remaining_seconds))
        
    def complete_countdown(self):
        # Perform actions when the countdown completes (e.g., shutdown)
        self.seconds_textctrl.SetValue("0")
        subprocess.Popen('shutdown /s /t 0', shell=True)
        self.running = False
        self.start_button.Enable()
        self.seconds_textctrl.Enable()
        self.stop_button.Disable()

# Run the application if this script is the main module
if __name__ == '__main__':
    app = CountdownApp()
    app.MainLoop()
