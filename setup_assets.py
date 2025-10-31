import os
import requests
import zipfile
import sys
from tqdm import tqdm

# --- config ---
ASSETS_URL = "https://github.com/zziruhuang/vispils-flask-app/releases/download/v1.1.0/assets-v1.1.0.zip"
ASSETS_ZIP_NAME = "assets-v1.1.0.zip"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def download_file(url, destination):
    """show download progress bar while downloading a file from a URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  
        
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc="Downloading Assets")
        with open(destination, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("Error: Something went wrong during download.")
            return False
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

def unzip_file(zip_path, extract_to):
    """unzip the zip file to a specified directory"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            print(f"Unzipping {zip_path} to {extract_to}...")
            zip_ref.extractall(extract_to)
            print("Unzipping complete.")
        return True
    except zipfile.BadZipFile:
        print(f"Error: {zip_path} is not a valid zip file.")
        return False
    except Exception as e:
        print(f"An error occurred during unzipping: {e}")
        return False

def main():
    """main function"""
    print("--- Setting up required assets for the project ---")

    # Check if required libraries are installed
    try:
        import requests
        from tqdm import tqdm
    except ImportError:
        print("Required packages 'requests' and 'tqdm' are not installed.")
        print("Please run: pip install requests tqdm")
        sys.exit(1)

    # Target ZIP file path
    zip_file_path = os.path.join(PROJECT_ROOT, ASSETS_ZIP_NAME)

    # 1. Download assets package
    if not download_file(ASSETS_URL, zip_file_path):
        sys.exit(1)

    # 2. Unzip assets package to project root
    if not unzip_file(zip_file_path, PROJECT_ROOT):
        sys.exit(1)

    # 3. Clean up downloaded ZIP file
    try:
        print(f"Cleaning up {zip_file_path}...")
        os.remove(zip_file_path)
        print("Cleanup complete.")
    except OSError as e:
        print(f"Error removing file: {e}")

    print("\n--- Assets setup complete! ---")
    print("You can now proceed with installing other dependencies and running the application.")

if __name__ == "__main__":
    main()
