import os
import tkinter as tk
from tkinter import filedialog, messagebox

def folder_path_generator(folder_path):
    num = ''
    count = 0
    folder_copy_path = f'{folder_path}_copy{num}'
    while os.path.exists(folder_copy_path):
        count += 1
        num = f'({count})'
        folder_copy_path = f'{folder_path}_copy{num}'
    return folder_copy_path

def file_path_generator(file_path):
    file_label, file_ext = os.path.splitext(file_path)
    num = ''
    count = 0
    file_copy_path = f'{file_label}_copy{num}{file_ext}'
    while os.path.exists(file_copy_path):
        count += 1
        num = f'({count})'
        file_copy_path = f'{file_label}_copy{num}{file_ext}'
    return file_copy_path

def copy(file_path, parent=''):
    try:
        file_name = os.path.basename(file_path)
        script_file_path = os.path.abspath(__file__)
        script_folder_path = os.path.dirname(script_file_path)

        if parent == '':
            file_copy_path = os.path.join(script_folder_path, file_name) 
        else:
            file_copy_path = parent
            
        if os.path.isdir(file_path):
            if parent == '':
                folder_copy_path = os.path.join(script_folder_path, file_name)
            else:
                folder_copy_path = parent
            if os.path.exists(folder_copy_path):
                folder_copy_path = folder_path_generator(folder_copy_path)

            os.mkdir(folder_copy_path)
            folder_file_names = os.listdir(file_path)

            for folder_file_name in folder_file_names:
                folder_file_path = os.path.join(file_path, folder_file_name)
                file_copy_path = os.path.join(folder_copy_path, folder_file_name)
            
                copy(folder_file_path, parent=file_copy_path)
        else:  
            if os.path.exists(file_copy_path):
                file_copy_path = file_path_generator(file_copy_path)

            with open(file_path, 'rb') as file_obj:
                file_data = file_obj.readlines()
            
            with open(file_copy_path, 'wb') as file_copy_obj:
                file_copy_obj.writelines(file_data)

            return True
    except PermissionError as e:
        print(e)

def GUI():
    window = tk.Tk()
    window.title('File/Folder Replicator')
    window.geometry('600x400')
    window.configure(bg='#f0f0f0')

    choice = tk.StringVar(value="file")

    def browse():
        if choice.get() == "file":
            path = filedialog.askopenfilename(initialdir=os.path.expanduser("~"))
        else:
            path = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
        if path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, path)

    def copy_file_or_folder():
        path = path_entry.get()
        num_copies = copies_scale.get()

        if not os.path.exists(path):
            messagebox.showerror("Path not found", "Please select a valid file or folder.")
            return

        for _ in range(num_copies):
            copy(path)
        if num_copies == 1:
            messagebox.showinfo("Success", f"Created {num_copies} copy of {path}.")
        else:
            messagebox.showinfo("Success", f"Created {num_copies} copies of {path}.")

    def copy_scale_intensity(value):
        colors = ['#ffffff', '#ffcece', '#ff9d9d', '#ff6c6c', '#ff3b3b', '#ff0000']
        copies_scale.config(troughcolor=colors[int(value)-1], fg='black')


    # UI Elements
    title_label = tk.Label(window, text="File/Folder Replicator", font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='black')
    title_label.pack(pady=20)

    choice_frame = tk.Frame(window, bg='#f0f0f0', bd=5)
    choice_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Label(choice_frame, text="Choose to copy a file or a folder:", font=('Arial', 14, 'bold'), fg='black', bg='#f0f0f0').pack(pady=5, anchor=tk.W)
    
    file_radio = tk.Radiobutton(choice_frame, text="File", variable=choice, value="file", font=('Arial', 12), bg='#f0f0f0', fg='#333', selectcolor='#f0f0f0')
    file_radio.pack(side=tk.LEFT, padx=20, anchor=tk.W)
    folder_radio = tk.Radiobutton(choice_frame, text="Folder", variable=choice, value="folder", font=('Arial', 12), bg='#f0f0f0', fg='#333', selectcolor='#f0f0f0')
    folder_radio.pack(side=tk.LEFT, padx=20, anchor=tk.W)

    path_frame = tk.Frame(window, bg='#f0f0f0', bd=5)
    path_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Label(path_frame, text="Path:", font=('Arial', 14), bg='#f0f0f0', fg='#333').pack(side=tk.LEFT, padx=5, anchor=tk.W)
    path_entry = tk.Entry(path_frame, width=30, font=('Arial', 14))
    path_entry.pack(side=tk.LEFT, padx=5, anchor=tk.W)
    browse_button = tk.Button(path_frame, text="Browse", command=browse, font=('Arial', 12), bg='#007BFF', fg='white')
    browse_button.pack(side=tk.LEFT, padx=5, anchor=tk.W)

    copies_frame = tk.Frame(window, bg='#f0f0f0', bd=5)
    copies_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Label(copies_frame, text="Number of copies:", font=('Arial', 14), bg='#f0f0f0', fg='#333').pack(side=tk.LEFT, padx=5, anchor=tk.W)
    copies_scale = tk.Scale(copies_frame, from_=1, to=5, orient=tk.HORIZONTAL, font=('Arial', 12), bg='#f0f0f0', fg='#333', command=copy_scale_intensity)
    copies_scale.pack(side=tk.LEFT, padx=5, anchor=tk.W)

    copy_button = tk.Button(window, text="Copy", command=copy_file_or_folder, font=('Arial', 16, 'bold'), bg='#007BFF', fg='white', padx=10, pady=5)
    copy_button.pack(pady=20)
    
    window.mainloop()

if __name__ == '__main__':
    GUI()
