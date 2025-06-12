import argostranslate.package
import argostranslate.translate
import os

# Step 1: Get available packages online
available_packages = argostranslate.package.get_available_packages()

# Step 2: Find Hindi → English package
for pkg in available_packages:
    if pkg.from_code == "hi" and pkg.to_code == "en":
        print("Downloading Hindi to English package...")
        download_path = pkg.download()
        argostranslate.package.install_from_path(download_path)
        print("Model installed successfully.")
        break
else:
    print("Hindi to English translation package not found.")
