import tkinter as tk
import pandas as pd
import webview
from tkinterweb import HtmlFrame
import os
df_class_name = "overall_df.csv"
# Set the path to the folder containing the HTML files
folder_path = "C:\\Users\\Sebastjan\\PycharmProjects\\JobCrawler\\pages_ds"
folders = [f for f in os.listdir(folder_path)]
folder = folders.pop(0)
files = [f for f in os.listdir(os.path.join(folder_path,folder))]
current_file = files.pop()
current_df = pd.read_csv(os.path.join(os.path.join(folder_path,folder),"df.csv"))
row_idx = 0

# Create an empty dataframe to store the classification results
if os.path.exists(os.path.join(folder_path, df_class_name)):
    df = pd.read_csv(os.path.join(folder_path, df_class_name))
else:
    df = pd.DataFrame(columns=['File', 'Class'])

# Create the main window
root = tk.Tk()
root.title('HTML Classifier')
root.wm_attributes('-topmost', True)

# Define a function to classify the current HTML file
def classify( event=None, btn = None):
    global df
    global current_file
    global folder
    # Get the classification from the button that was pressed
    if btn is None:
        classification = event.char
    else:
        classification = btn
    print(classification)
    # Add the file name and classification to the dataframe
    df = df.append({'File': os.path.join(folder, current_file), 'Class': classification}, ignore_index=True)
    # Clear the web browser widget and move to the next file
    #browser.reload()
    show_next_file()

# Define a function to display the contents of the next HTML file
def show_next_file():
    global folder_path
    global current_file
    global folder
    global folders
    global files
    global current_df
    global row_idx
    global df
    # If there are no more files, close the window and show the dataframe
    if len(files) == 0:
        if len(folders) == 0:
            root.destroy()
            print(df)
            return
        else:
            folder = folders.pop(0)
            current_df = pd.read_csv(os.path.join(os.path.join(folder_path,folder),"df.csv"))
            files = [f"{i}.html"for i in range(len(current_df))]
            row_idx = 0

    # Get the next file in the list
    current_file = files.pop(0)
    if os.path.join(folder, current_file) in df["File"].values:
        row_idx = row_idx + 1
        show_next_file()

    # Display the file in the web browser widget
    file_url = 'file://' + os.path.join(os.path.join(folder_path,folder), current_file)
    frame.load_file(file_url)
    root.focus()
    root.title(f"{current_df.iloc[row_idx]['URL']} file:{current_file}")
    df.to_csv(os.path.join(folder_path, df_class_name))
    row_idx = row_idx+1

frame = HtmlFrame(root)
frame.pack()

# Create buttons to classify the file as belonging to either class
button1 = tk.Button(root, text='Class 1', command=lambda: classify(btn='1'))
button1.pack(side='left')
button2 = tk.Button(root, text='Class 2', command=lambda: classify(btn='2'))
button2.pack(side='left')

# Set the keyboard bindings to classify the file when a key is pressed
root.bind('<KeyPress-1>', classify)
root.bind('<KeyPress-2>', classify)

# Show the first HTML file
show_next_file()

# Run the main loop
root.mainloop()
