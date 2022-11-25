import tkinter
import tkinter.filedialog



def prompt_file():
    
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

print(prompt_file())

