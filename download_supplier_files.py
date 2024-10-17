import os
import requests

# Base URL of the Frappe instance
base_url = "http://127.0.0.1:8005"

# API keys or session authentication for accessing the Frappe API
headers = {
    "Authorization": "token ecbf384e69573b2:9835dc590b98754"
}

# Fetch files related to a specific supplier and DocType
def fetch_supplier_files(supplier_name, doctype):
    file_api_url = f"{base_url}/api/resource/File"
    
    # Define the filters to fetch files related to a supplier and attached to a specific DocType
    params = {
        'filters': f'[["attached_to_name", "=", "{supplier_name}"], ["attached_to_doctype", "=", "{doctype}"]]',
        'fields': '["*"]'  # Fetch all fields
    }


    # Make the request to get the list of files for the supplier
    response = requests.get(file_api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Failed to fetch files for {supplier_name}. Status code: {response.status_code}")
        return []

# Download a file using the file manager download API
def download_file(file_url, file_name, supplier_name):
    download_url = f"{base_url}/api/method/download_file"
    params = {'file_url': file_url}

    # Send GET request to download the file
    response = requests.get(download_url, headers=headers, params=params)

    if response.status_code == 200:
        # Create supplier directory if it doesn't exist
        if not os.path.exists(supplier_name):
            os.makedirs(supplier_name)

        # Construct the full file path using the provided file name
        filepath = os.path.join(supplier_name, file_name)

        # Save the file to the supplier's folder
        with open(filepath, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {file_name} for {supplier_name}")
    else:
        print(response.json())
        print(f"Failed to download {file_url}. Status code: {response.status_code}")

# Main function to get files for each supplier and download them
def download_supplier_files(suppliers, doctype):
    for supplier in suppliers:
        print(f"Fetching files for supplier: {supplier}")
        files = fetch_supplier_files(supplier, doctype)
        
        for file in files:
            file_url = file.get("file_url")
            file_name = file.get("file_name")  # Get the file name from the API response
            if file_url and file_name:
                download_file(file_url, file_name, supplier)

# List of suppliers to fetch files for
suppliers = ["ABC FG"]

# The specific DocType to which the files are attached (e.g., "Supplier")
doctype = "Supplier"

# Run the script
download_supplier_files(suppliers, doctype)
