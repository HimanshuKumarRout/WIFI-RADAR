import os
import subprocess
import sys
import tkinter as tk

# Ensure the project root is on the import path when running init.py from any location.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Radar.main import RadarApp


def run_gui():
    root = tk.Tk()
    app = RadarApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


def run_scanner_script():
    scanner_script = os.path.join(BASE_DIR, "Radar", "scanner.py")
    print("\nRadar GUI closed. Running scanner.py now...\n")
    subprocess.run([sys.executable, scanner_script], check=False)


def main():
    run_gui()
    run_scanner_script()


if __name__ == "__main__":
    main()
