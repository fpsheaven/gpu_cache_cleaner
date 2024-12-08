import subprocess
import re
import os
import time

def detect_gpu():
    try:
        result = subprocess.run(
            ['powershell', 'Get-CimInstance Win32_VideoController | Select-Object Name'],
            capture_output=True, text=True, shell=True
        )
        gpu_name = result.stdout.strip()
        
        if re.search(r'NVIDIA', gpu_name, re.IGNORECASE):
            print("I found NVIDIA.")
            time.sleep(2)
            create_batch_file("NVIDIA", r'%USERPROFILE%\AppData\LocalLow\NVIDIA\PerDriverVersion\DXCache\*')
        
        elif re.search(r'AMD', gpu_name, re.IGNORECASE):
            print("I found AMD.")
            time.sleep(2)
            create_batch_file("AMD", r'%USERPROFILE%\AppData\LocalLow\AMD\DXCache\*')
        
        else:
            print("GPU not detected or unsupported.")
    except Exception as e:
        print(f"Error detecting GPU: {e}")

def create_batch_file(brand, path):
    startup_path = os.path.join(
        os.environ['APPDATA'], 
        r'Microsoft\Windows\Start Menu\Programs\Startup\gpu_cache_cleaner.bat'
    )

    if os.path.exists(startup_path):
        print(f"Batch file already exists at {startup_path}. Running it now...")
        execute_batch_file(startup_path)
        ask_remove_file(startup_path)
        return
    else:
        print("Creating a batch file. One moment...")

    try:
        command = f'del /Q /F /S "{path}"\nexit'
        
        # Write the batch file
        with open(startup_path, 'w') as batch_file:
            batch_file.write(f"@echo off\n:: Clean DX Cache for {brand}\n{command}")
        
        print(f"{brand} cleanup batch file created at {startup_path}. Executing it.")
        execute_batch_file(startup_path)
        ask_remove_file(startup_path)
    except Exception as e:
        print(f"Error creating batch file: {e}")

def execute_batch_file(batch_file_path):
    try:
        subprocess.run(f'start cmd /c "{batch_file_path}"', shell=True)
    except Exception as e:
        print(f"Error executing batch file: {e}")

def ask_remove_file(file_path):
    user_input = input("Do you want to remove the batch file? (y/n): ").strip().lower()
    if user_input in ['y', 'yes']:
        try:
            os.remove(file_path)
            print("Batch file removed successfully.")
        except Exception as e:
            print(f"Error removing batch file: {e}")
    else:
        print("Batch file kept.")

if __name__ == "__main__":
    detect_gpu()
