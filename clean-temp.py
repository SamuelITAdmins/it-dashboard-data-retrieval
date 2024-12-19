import shutil
import os

# Path to the temp folder
temp_folder = os.path.join(os.getcwd(), 'temp')

# Remove all contents of the temp folder
if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder)
    print(f"Temporary folder '{temp_folder}' cleaned up.")
