# QR Code Generator for Tables

### 📋 Project Description

A Python desktop application for generating personalized QR codes for restaurant tables, events, or commercial establishments. Each QR code contains the table number in the center and redirects to a specific URL.

## ✨ Features

✅ Batch generation of multiple QR codes

✅ Customizable base URL

✅ Table number centered in the QR code

✅ User-friendly graphical interface (Tkinter)

✅ Custom font selection

✅ Real-time progress bar

✅ Support for different table quantities

✅ Choose destination folder for files


## 🛠️ System Requirements
Python
Python 3.6 or higher


## 📥 Installation & Environment Setup

Install Python

	Windows: Download from python.org

	Linux: sudo apt-get install python3 python3-pip (Ubuntu/Debian)

	Mac: brew install python or download from python.org


Clone or download the project

	git clone https://github.com/cristianosch/QR-CODE-PYTHON-INTERFACE.git


Using Virtual Environment (Recommended)

Windows

	# Create virtual environment
	python -m venv venv

	# Activate virtual environment
	venv\Scripts\activate

  
Linux/Mac	

	# Create virtual environment
	python3 -m venv venv

	# Activate virtual environment
	source venv/bin/activate



## Dependencies

	pip install -r requirements.txt


# Run the application

	python main.py


# Usage Instructions


	Fill in the fields:

	Base URL: URL where QR codes will redirect (e.g., https://myrestaurant.com/table/)

	Number of Tables: Quantity to generate (1-1000)

	Output Folder: Where PNG files will be saved

	Font: Font file for center number (TTF/OTF)

	Click "Generate QR Codes"
