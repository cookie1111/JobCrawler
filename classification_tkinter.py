import tkinter as tk
import pandas as pd
import webbrowser
import os

# Set the path to the folder containing the HTML files
folder_path = "C:\\Users\\Sebastjan\\PycharmProjects\\JobCrawler\\pages_ds\\2txt_de"

# Create an empty dataframe to store the classification results
df = pd.DataFrame(columns=['File', 'Class'])

# Create the main window
root = tk.Tk()
root.title('HTML Classifier')
root.wm_attributes('-topmost', True)

# Define a function to classify the current HTML file
def classify( event=None, btn = None):
    global df
    # Get the classification from the button that was pressed
    if btn is None:
        classification = event.char
    else:
        classification = btn
    print(classification)
    # Add the file name and classification to the dataframe
    df = df.append({'File': current_file, 'Class': classification}, ignore_index=True)
    # Clear the web browser widget and move to the next file
    #browser.reload()
    show_next_file()

# Define a function to display the contents of the next HTML file
def show_next_file():
    global current_file
    # Get the list of HTML files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    # If there are no more files, close the window and show the dataframe
    if len(files) == 0:
        root.destroy()
        print(df)
        return
    # Get the next file in the list
    current_file = files[0]
    # Display the file in the web browser widget
    file_url = 'file://' + os.path.join(folder_path, current_file)
    browser.open(file_url)
    # Remove the file from the list
    files.pop(0)

firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox"
# Create a web browser widget to render the HTML file
webbrowser.register(name='firefox',klass=None,instance=webbrowser.BackgroundBrowser(firefox_path))
browser = webbrowser.get('firefox')

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
