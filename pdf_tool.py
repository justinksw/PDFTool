import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
import tkinter.filedialog

w = 200
h = 100

cur_path = os.getcwd()


def combine_pdf():
    output = '_combined.pdf'
    folder = cur_path + "/to_combine"
    file_name_list = os.listdir(folder)

    if not file_name_list:
        popup_window('No file to combine!')
        return 0

    else:
        file_name_list.sort()
        file_path_list = [(folder + "/" + name) for name in file_name_list]
        pdf_writer = PdfFileWriter()
        for path in file_path_list:
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        with open(output, 'wb') as f:
            pdf_writer.write(f)
        popup_window('Done!')
        return 1


def split_pdf(path):
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output = os.getcwd() + "/splitted/_splitted_" + str(page) + ".pdf"
        with open(output, 'wb') as f:
            pdf_writer.write(f)
    popup_window('Done!')
    return 1


def add_encryption(path, password):
    if password == '':
        popup_window('Enter a password!')
        return 0

    else:
        output = cur_path + "/_encrypted.pdf"

        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(path)

        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
        pdf_writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)
        with open(output, 'wb') as f:
            pdf_writer.write(f)
        popup_window('Done!')
        return 1


class MainWindow:
    def __init__(self, root):
        self.master = root
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.frame = tk.Frame(self.master)
        self.merge_btn = tk.Button(text="Combine", width=20, command=combine_pdf)
        self.merge_btn.pack()
        self.split_btn = tk.Button(text="Split", width=20, command=self.do_split)
        self.split_btn.pack()
        self.encryption_btn = tk.Button(text="Encryption", width=20, command=self.do_encryption)
        self.encryption_btn.pack()
        # self.close_btn = tk.Button(text='Quit', width=20, command=self.destroy_app)
        # self.close_btn.pack()
        self.frame.pack()

    def do_split(self):
        split_window = tk.Toplevel(self.master)
        SplitWindow(split_window)

    def do_encryption(self):
        encryption_window = tk.Toplevel(self.master)
        EncryptionWindow(encryption_window)

    # def destroy_app(self):
    #     self.master.destroy()


class SplitWindow:
    def __init__(self, root):
        self.master = root
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.frame = tk.Frame(self.master)
        self.master.directory = tkinter.filedialog.askopenfilename(initialdir=cur_path,
                                                                   filetypes=[("PDF Files", "*.pdf")])
        split_pdf(self.master.directory)
        self.frame.pack()


class EncryptionWindow:
    def __init__(self, root):
        self.master = root
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.frame = tk.Frame(self.master)
        self.password_lb = tk.Label(self.master, text="Enter your Password to Encrypt")
        self.password_lb.pack()
        self.password_etr = tk.Entry(self.master)
        self.password_etr.pack()
        self.password = ''
        self.button = tk.Button(self.master, text="Enter", width=20, command=self.enter_pw)
        self.button.pack()
        self.frame.pack()

    def enter_pw(self):
        encryption_window2 = tk.Toplevel(self.master)
        self.password = self.password_etr.get()
        EncryptionWindow2(encryption_window2, self.password)


class EncryptionWindow2:
    def __init__(self, root, password):
        self.master = root
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.frame = tk.Frame(self.master)
        self.master.directory = tkinter.filedialog.askopenfilename(initialdir=cur_path,
                                                                   filetypes=[("PDF Files", "*.pdf")])
        add_encryption(self.master.directory, password)
        self.frame.pack()


def popup_window(msg):
    popup = tk.Tk()
    sw = popup.winfo_screenwidth()
    sh = popup.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    label = tk.Label(popup, text=msg, width=120, height=10)
    label.pack()
    tk.mainloop()


if __name__ == '__main__':
    root_ = tk.Tk()
    app = MainWindow(root_)
    tk.mainloop()


### Convert Img to PDF

#from PIL import Image
#from pathlib import Path
#
#cwd = Path.cwd()
#image_path = cwd / "913217751.jpg"
#pdf_path = cwd / "PDF.pdf"
#
#image = Image.open(image_path)
#pdf = image.convert("RGB")
#pdf.save(pdf_path)


### Rotate a PDF

#from pathlib import Path
#import PyPDF2
#
#name = "cuhk certificate KongShuWa"
#file_name = name + ".pdf"
#cwd = Path.cwd()
#file_path = cwd / file_name
#
#pdf_in = open(file_path, "rb")
#
#pdf_reader = PyPDF2.PdfFileReader(pdf_in)
#pdf_writer = PyPDF2.PdfFileWriter()
#
#page = pdf_reader.getPage(0)
#page.rotateClockwise(90)
#
#pdf_writer.addPage(page)
#
#pdf_out = open(cwd / "out.pdf", "wb")
#pdf_writer.write(pdf_out)
#
#pdf_out.close()
#pdf_in.close()
