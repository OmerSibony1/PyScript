import os
from pathlib import Path
import pdfplumber
import json
from tqdm import tqdm

encodings = ['utf-8', 'iso-8859-1', 'windows-1252', 'latin-1', 'cp1252']
desktop_path = Path.home() / "Desktop"
files_with_text_content = open(desktop_path / "files_with_text_content.txt", 'a',encoding='utf-8')
decodesFile = open(desktop_path / "decodeFiles.txt", 'a', encoding='utf-8')
excexptionDecodeFile = open(desktop_path / "excexptionDecodeFile.txt", 'a', encoding='utf-8')

"""GET FILES METHODS:"""

def getFilesDirYSubdir(path):
    path = Path(path)
    files = []
    for file in path.rglob("*"):
        if file.is_file():
            files.append(file)
            #print(file)
    return files


def getFilesFromDirectory(path):
    """Return:
    Dictonary with directory name as the key and list of files as the value"""
    files = []
    os.chdir(path)
    listdir = os.listdir(path)
    for d in listdir:
        #print(d)
        if os.path.isdir(d):
            continue
        if os.path.isfile(d):
            files.append(d)
    return files


"""FILES READERS"""

def search_text_in_binary_file(filename,text):
    """Search for text in a binary file by reading it in chunks"""
    try:
        with open(filename,'rb') as file:
            chunk_size = 1024*1024 # 1MB chunks
            while chunk := file.read(chunk_size):
                if text.encode('utf-8') in chunk:
                    return True
    except Exception as e:
        print(f"An error occured with file {filename}: {e}")
    return False


def search_text_in_file_line_by_line(filename, text):
    """Search for text in a file by reading it line-by-line"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if text in line:
                    return True
    except UnicodeDecodeError:
        print(f"Could not decode file: {filename}")
    except Exception as e:
        print(f"An error occurred with file {filename}: {e}")
    return False

def read_json_file(filename,text):
    try:
        with open(filename,'r',encoding='utf-8') as file:
            try:
                data = json.load(file)
                return text in str(data)
            except json.JSONDecodeError:
                print(f"Malformed JSON in {filename}")
                return False
    except UnicodeDecodeError:
        print(f"Unicode decode error in file: {filename}")
        return False
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return False
    except Exception as e:
        print(f"An error occurred while reading {filename}: {e}")
        return False


def read_pdf_file(filename, text):
    """Function Action:
     Read pdf file and return if the text is in it
     Returns:
         True if the text is exist at the file, False otherwise"""
    try:
        with pdfplumber.open(filename) as pdf:
            data = ''
            for page in pdf.pages:
                text_page = page.extract_text()
                if text_page:
                    data += text_page
            return text in data
    except Exception as e:
        print(f"Error reading PDF file {filename}: {e}")
        return False

"""DECODERS CHECK: """
def read_diff_decode(filename,text):
    """open the file with utf-8 encoding
    Returns:
         True if the text is exist at the file, False otherwise"""
    #decodesFile = open(desktop_path / "decodeFiles.txt",'a',encoding='utf-8')
    #excexptionDecodeFile = open(desktop_path / "excexptionDecodeFile.txt", 'a',encoding='utf-8')
    f=False
    for enc in encodings:
        try:
            with open(filename, encoding=enc) as f:  # Specify encoding
                chunk_size = 1024*1024 #1 MB chunk
                while chunk := f.read(chunk_size):
                    if text in chunk:
                        f=True
                        decodesFile.write(f"Could decode file: {filename} with {enc}\n")
                        break
                if f:
                    break
        except UnicodeDecodeError as ude: # exeption for wrong encode
            #print(f"Could not decode file: {filename} with {enc}")
            #print(f"{ude}")
            excexptionDecodeFile.write(f"Could not decode file: {filename} with {enc}\n")
            continue
        except Exception as e:
            excexptionDecodeFile.write(f"An error occurred with file {filename}: {e}\n")
    #decodesFile.close()
    #excexptionDecodeFile.close()
    return f



"""FIND TEXT IN FILES IN THE CURRENT DIRECTORY METHOD"""

def find_text_in_directory(files, dirname, text):
    """Get:
    files: Dictonary that contain the directory name and the files in it
     directory name : To look in specific directory
     text : The text that we are looking for
     Returns:
         list of every file that contain the text"""
    files_with_the_text = []
    directory_path = Path(dirname)  # Ensure dirname is a Path object
    for file in tqdm(files,desc="Proccesing files",unit="file"):
        filename = directory_path / file  # Combine path with file name
        #print(os.path.abspath(filename))
        if str(file).__contains__(".pdf"):
            if read_pdf_file(filename,text):
                files_with_the_text.append(str(filename))
        elif str(file).__contains__(".json"):
            if read_json_file(filename,text):
                files_with_the_text.append(str(filename))
        elif str(file).__contains__(".txt") or str(file).__contains__(".log"): # text files
            if search_text_in_file_line_by_line(filename,text):
                files_with_the_text.append(str(filename))
        else:
            if read_diff_decode(filename, text) or search_text_in_binary_file(filename,text):
                files_with_the_text.append(str(filename))


    return files_with_the_text if files_with_the_text else None



"""SEARCH METHODS"""

def search_current_directoty(path, text):
    #files_with_text_content = open(desktop_path / "files_with_text_content.txt",'a')
    files = getFilesFromDirectory(path)  # return dictonary that contain as a key the directory and value the list of files in it

    file_with_text = find_text_in_directory(files, path, text)
    if file_with_text == None:
        print(f"{text} not found in files in directory {path}")
        files_with_text_content.write(f"{text} not found in files in directory {path}\n")
    else:
        print(f"The files that contain '{text}' in it in {path}: ")
        files_with_text_content.write(f"The files that contain '{text}' in it in {path}: \n")
        for file in file_with_text:
            files_with_text_content.write(f"{Path(file).name}\n")
            print(Path(file).name)

    #files_with_text_content.close()

def search_in_subdirectories(path,text):
    files = getFilesDirYSubdir(Path(path))
    files_with_text = find_text_in_directory(files, path, text)
    files_with_text_content = open(desktop_path / f"files_with_{text}_content.txt", 'a')
    if files_with_text == None:
        print(f"None at the files in {path}")
    else:
        for file in files_with_text:
            print(Path(file))
            files_with_text_content.write(f"The files that contain '{text}' in it in {path}: {Path(file)}\n")
    #files_with_text_content.close()

"""MAIN METHOD"""

def menu():
    text = input("Input the text you want to look for in file names: ")
    path = input("Path: ")
    ans = input(f"Search only at the current {path} without subdirectories?(yes/no)\n"
                f"   yes- only current directory: {path}\n"
                f"   no- in subdirectories too\n ")
    while ans != "yes" or ans != "no":
        ans = input(f"your input wrong, plesae answer (1/2):\nSearch only at the current {path} without subdirectories?(yes/no)\n"
                    "   yes- only current directory: {path}\n"
                    "   no- in subdirectories too\n ")
        if ans == "yes" or ans == "no":
            break
    if ans == "yes":
        print(f"Ok start searching {text} in {path}")
        search_current_directoty(path,text)
    elif ans == "no":
        print(f"Ok start searching {text} in {path} and in his subdirectories too")
        search_in_subdirectories(path,text)
    decodesFile.close()
    excexptionDecodeFile.close()
    files_with_text_content.close()



if __name__ == '__main__':
    menu()
