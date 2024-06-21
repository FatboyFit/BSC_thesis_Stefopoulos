import os
import pandas as pd
from docx import Document

def docx2csv(folder_path, output_file):
    # Read all the .docx files of all folders within a given folder
    docx_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.docx'):
                docx_files.append(os.path.join(root, file))

    # Define a list to store all data
    data = []
    
    # Extract the text from the .docx files and parse details
    for docx_file in docx_files:
        doc = Document(docx_file)
        full_text = '\n'.join([para.text for para in doc.paragraphs])
        
        # Extract metadata
        title = os.path.basename(docx_file).replace('.docx', '')
        journal = os.path.normpath(docx_file).split(os.sep)[1]  # Assumes 'data/{journal}/...' structure
        
        # Date extraction from core properties
        core_properties = doc.core_properties
        date = core_properties.created.strftime('%B %d, %Y') if core_properties.created else "No Date Found"

        # Classification text
        classification_index = full_text.find("Classification")
        classification_text = full_text[classification_index:].split('\n', 1)[1] if classification_index != -1 else "No Classification Found"

        # Append to data list
        data.append({
            'source': title,  # Only the file name without path
            'text': full_text,
            'title': title,
            'journal': journal,
            'date': date,
            'classification': classification_text.strip()  # Remove any leading/trailing whitespace
        })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame into a .csv file
    df.to_csv(output_file, index=False)

if __name__ == '__main__':
    folder_path = 'data/'
    output_file = 'output.csv'
    docx2csv(folder_path, output_file)
    print('Done')