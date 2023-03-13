ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.xlsx', '.xls', '.csv'}
import pathlib # to get the file extension

# Function to check if the file extension is allowed
def allowed_file(filename):
    return pathlib.Path(filename).suffix in ALLOWED_EXTENSIONS