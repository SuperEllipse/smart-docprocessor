from copy import deepcopy
import re
import os
from docx import Document
from llm_proofer import *



def document_postprocessing(model_output):
    """
    Process the output from a language model to extract edited text and corrections.

    This function takes the raw output from a language model that has performed
    proofreading and editing tasks. It extracts the edited version of the text
    and a list of specific corrections made.

    Parameters:
    model_output (str): The raw string output from the language model.
                        Expected to contain sections for "Edited Text" and
                        itemized corrections.

    Returns:
    tuple: A tuple containing two elements:
           - edited_text (str): The extracted edited version of the text.
                                If no edited text is found, returns "No edited text found."
           - corrections (list): A list of strings, each representing a specific
                                 correction made by the model.

    Prints:
    - The extracted edited text.
    - A numbered list of corrections.

    Note:
    The function assumes a specific format in the model_output:
    - Edited text is enclosed in single quotes after "1. Edited Text:"
    - Corrections are listed with lowercase letters followed by parentheses.

    If the expected format is not found, the function may not extract information correctly.
    """

    # Extract Edited Text
    edited_text_match = re.search(r"Edited Text: '([^']*)'", model_output)
    edited_text = (
        edited_text_match.group(1) if edited_text_match else "No edited text found."
    )

    # Extract Corrections
    corrections_match = re.findall(r"(\b[a-z]\))(.+)", model_output)
    corrections = [correction.strip() for _, correction in corrections_match]

    # Print the results
    print("Edited Text:")
    print(edited_text)
    print("\nCorrections:")
    for i, correction in enumerate(corrections, 1):
        print(f"{i}. {correction}")

    return edited_text, corrections




def process_llm_output(response):
    """
    Process the output from a custom Large Language Model and extract
    the edited text and corrections.

    Parameters:
    llm_output (str): The raw output string from the LLM.

    Returns:
    tuple: A tuple containing two elements:
           - edited_text (str): The extracted edited text.
           - corrections (str): The extracted corrections, or "None needed." if no corrections.
    """
    # Extract Edited Text
    # Modify regex to capture edited text with or without quotes
    # edited_text_match = re.search(r"1\. Edited Text:\s*(.*)", response)
    edited_text_match = re.search(
        r"1\. Edited Text:\s*['\"]?(.*?)['\"]?\s*(?:\n|$)", response, re.DOTALL
    )
    edited_text = (
        edited_text_match.group(1).strip()
        if edited_text_match
        else "No edited text found."
    )

    # Extract the corrections
    corrections_match = re.search(r"2\. Corrections:\s*(.*)", response, re.DOTALL)
    corrections = (
        corrections_match.group(1).strip()
        if corrections_match
        else "No corrections found."
    )
    print("INSIDE process_llm_output")
    # Print the results
    print("Edited Text:")
    print(edited_text)
    print("\nCorrections:")
    print(corrections)
    print("DONE process_llm_output")
    return edited_text.strip(), corrections.strip()


def build_file_name_extensions(input_file_path, extension="temp"):
    """
    Extracts the file name from a given path and creates new paths with specified suffixes.

    Args:
        input_file_path (str): The path to the file.
        extension(str): name of the extension required

    Returns:
        tuple: A tuple containing the extracted file name, edited path, corrected path, and track changes path.

    ## USAGE
    orig_filename, new_filename, new_filename_with_path  = build_file_name_extensions("/home/cdsw/test.doc", "corrections") 
    print(orig_filename, new_filename, new_filename_with_path ) # returns test.doc, test_corrections.doc, /home/cdsw/test_corrections.doc
        
    """
    file_name = os.path.basename(input_file_path)
    file_name_wo_ext = os.path.splitext(file_name)[0]
    file_ext = os.path.splitext(file_name)[1]  # Get the file extension
    new_file_name = f"{file_name_wo_ext}_{extension}{file_ext}"
    new_file_path = os.path.join(os.path.dirname(input_file_path),new_file_name )
    return file_name, new_file_name, new_file_path

def create_track_changes_document(input_doc, edited_doc):
    doc = Document(input_doc)
    
    # need a temp compy because input gets deleted
    temp_doc = deepcopy(doc)
    _,_, temp_input_doc = build_file_name_extensions(input_doc, "temp")
    temp_doc.save(temp_input_doc)
    
    # need a temp copy of edit
    doc = Document(edited_doc)
    # need a temp compy because input gets deleted
    temp_doc = deepcopy(doc)
    _,_, temp_edited_doc = build_file_name_extensions(edited_doc, "temp")
    temp_doc.save(temp_edited_doc)
    
    # apply track changes
    
    from python_redlines.engines import XmlPowerToolsEngine
    wrapper = XmlPowerToolsEngine()

    output_trackchanges = wrapper.run_redline('Smartdoc Processor', temp_input_doc, temp_edited_doc)
    _,_, trackchanges_doc = build_file_name_extensions(edited_doc, "trackchanges")
    with open(trackchanges_doc, 'wb') as f:
        f.write(output_trackchanges[0])   
    
    return trackchanges_doc