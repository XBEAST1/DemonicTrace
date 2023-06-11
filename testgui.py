import subprocess
import os
import glob
import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller, Key

window = tk.Tk()
window.title("Wi-Fi Probe Capture")
window.geometry("1000x800")
window.resizable(False, False)

output_text = tk.Text(window, height=20, width=100)
output_text.pack(pady=10)

iface = None  # Global variable to store the selected adapter

def capture_probes():
    global iface

    if os.name == "posix":
        os.system('airmon-ng check kill')  # Stop any interfering processes
        os.system(f'airmon-ng start {iface}')  # Start monitor mode on the selected adapter
        output_text.see(tk.END)
        window.update()

        # Start tcpdump process to capture probe requests
        check_iface = glob.glob('/sys/class/net/wlan*mon')

        if check_iface:
            # Get the first matching interface
            iface = os.path.basename(check_iface[0])
        process = subprocess.Popen(
            f'tcpdump -l -i {iface} -e -s 256 type mgt subtype probe-req | awk -f tcpdump.awk',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            universal_newlines=True
        )

        # Read the output of the tcpdump process and display it in the GUI
        for line in iter(process.stdout.readline, ''):
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
            window.update()

        process.wait()

        os.system(f'airmon-ng stop {iface}')  # Stop monitor mode
        os.system('service NetworkManager restart')  # Restart NetworkManager
    else:
        messagebox.showerror("Error", "This script is intended to run on a POSIX system (e.g., Linux).")


def get_wifi_adapters():
    try:
        # Execute the command 'iw dev' and capture the output
        output = subprocess.check_output(['iw', 'dev'], stderr=subprocess.STDOUT, universal_newlines=True)

        # Split the output into lines
        lines = output.split('\n')

        adapters = []

        # Iterate through each line
        for line in lines:
            # Check if the line contains the word 'Interface'
            if 'Interface' in line:
                # Split the line by spaces and get the last element, which is the adapter name
                adapter = line.split(' ')[-1]
                adapters.append(adapter)

        # Return the list of adapters
        return adapters
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with error: {e.output}")


def select_adapter():
    # Get the list of available Wi-Fi adapters
    wifi_adapters = get_wifi_adapters()

    if len(wifi_adapters) > 0:
        # Create a new window for selecting the adapter
        adapter_window = tk.Toplevel(window)
        adapter_window.title("Select Wi-Fi Adapter")

        # Function to confirm the selected adapter
        def confirm_selection():
            global iface
            # Get the index of the selected adapter from the listbox
            selection = adapter_listbox.curselection()

            if selection:
                # Retrieve the selected adapter from the list of adapters
                iface = wifi_adapters[selection[0]]
                messagebox.showinfo("Selection", f"Selected Wi-Fi adapter: {iface}")
                # Close the adapter selection window and start capturing probes
                adapter_window.destroy()
                capture_probes()
            else:
                messagebox.showwarning("Warning", "No adapter selected.")

        # Create a listbox to display the available adapters
        adapter_listbox = tk.Listbox(adapter_window)
        adapter_listbox.pack(pady=10)

        # Populate the listbox with the available adapters
        for adapter in wifi_adapters:
            adapter_listbox.insert(tk.END, adapter)

        # Create a button to confirm the adapter selection
        confirm_button = tk.Button(adapter_window, text="Confirm", command=confirm_selection)
        confirm_button.pack(pady=10)
    else:
        messagebox.showinfo("No Wi-Fi Adapters", "No Wi-Fi adapters found.")

def on_window_close():
    keyboard = Controller()

    # Simulate pressing 'Ctrl+C'
    with keyboard.pressed(Key.ctrl):
        keyboard.press('c')
        keyboard.release('c')
    os.system(f"airmon-ng stop {iface}")  # Stop monitor mode
    os.system("service NetworkManager restart")  # Restart NetworkManager
    window.destroy()


select_adapter_button = tk.Button(window, text="Select Wi-Fi Adapter", command=select_adapter)
select_adapter_button.pack(pady=10)

window.protocol("WM_DELETE_WINDOW", on_window_close)
window.mainloop()