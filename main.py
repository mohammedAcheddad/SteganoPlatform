import threading
import time
import numpy as np
import pywt
from tkinter import Tk
from PIL import Image
from customtkinter import *
from tkinterdnd2 import TkinterDnD, DND_ALL
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
import cv2

set_appearance_mode("dark")
set_default_color_theme("FlipperZeroTheme.json")

class SteganographyApp(TkinterDnD.DnDWrapper, CTk, Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

def show_error(message):
    showerror("ERROR", message)

def process_drag_and_drop(event):
    if event.data.lower().endswith(".png"):
        encode_or_decode(event.data)
    else:
        show_error("Expected a PNG image but received another file")

def encode_img(img, transform_method='dct'):
    global progressbar
    progressbar.stop()
    for x in range(0, 101):
        progressbar.set(x/100)
        root.update()
    time.sleep(0.5)
    for widget in frame.winfo_children():
        widget.destroy()
    save_btn = CTkButton(frame, text="Click Here to Download the Image", font=("HaxrCorp4089", 30), command=lambda: save(img))
    save_btn.place(anchor="center", relx=0.5, rely=0.5)
    go_back = CTkButton(frame, text="< Go Back", font=("HaxrCorp4089", 30), command=home)
    go_back.place(anchor="nw", x=20, y=20)
    save(img)

def save(img):
    file = asksaveasfilename()
    if file != "":
        if not file.lower().endswith(".png"):
            file += ".png"
        cv2.imwrite(file, img)

def encode(text, transform_method='dct'):
    global progressbar
    for widget in frame.winfo_children():
        widget.destroy()
    description = CTkLabel(frame, text="Working On It.....", font=("HaxrCorp4089", 50), anchor="w")
    description.pack(fill="x", pady=20, padx=20)
    progressbar = CTkProgressBar(frame, height=50, corner_radius=3)
    progressbar.pack(expand=True, fill="x", padx=20)
    progressbar.start()

    if transform_method == 'dct':
        t1 = threading.Thread(target=encode_img_dct, args=(text,))
    elif transform_method == 'dwt':
        t1 = threading.Thread(target=encode_img_dwt, args=(text,))
    else:
        raise ValueError("Invalid transform method")
    t1.start()

def encode_img_dct(message):
    image = cv2.imread(FILE)
    ycbcr_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    binary_data = ''.join(format(ord(char), '08b') for char in message)

    height, width, _ = ycbcr_image.shape
    data_index = 0

    for y in range(0, height, 8):
        for x in range(0, width, 8):
            block = ycbcr_image[y:y+8, x:x+8, 0]
            dct_block = cv2.dct(np.float32(block))

            for i in range(8):
                for j in range(8):
                    if data_index < len(binary_data):
                        dct_block[i, j] = (dct_block[i, j].astype(np.int32) & ~1) | int(binary_data[data_index])
                        data_index += 1

            modified_block = cv2.idct(dct_block)
            ycbcr_image[y:y+8, x:x+8, 0] = np.clip(modified_block, 0, 255)

    modified_image = cv2.cvtColor(ycbcr_image, cv2.COLOR_YCrCb2BGR)
    encode_img(modified_image, transform_method='dct')

def encode_img_dwt(message):
    img = cv2.imread(FILE, cv2.IMREAD_GRAYSCALE)
    coeffs = pywt.dwt2(img, 'haar')
    cA, (cH, cV, cD) = coeffs

    message_bin = ''.join(format(ord(char), '08b') for char in message)
    message_idx = 0

    for c in [cA, cH, cV, cD]:
        for i in range(c.shape[0]):
            for j in range(c.shape[1]):
                if message_idx < len(message_bin):
                    c[i, j] = round(c[i, j] / 2) * 2 + int(message_bin[message_idx])
                    message_idx += 1

    stego_coeffs = cA, (cH, cV, cD)
    stego_img = pywt.idwt2(stego_coeffs, 'haar')

    stego_img_bgr = cv2.cvtColor(stego_img.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    encode_img(stego_img_bgr, transform_method='dwt')

def encode_ui():
    for widget in frame.winfo_children():
        widget.destroy()
    data = CTkTextbox(frame, height=300, font=("HaxrCorp4089", 50))
    data.pack(expand=True, fill="both", padx=20, pady=20)

    encode_btn_dct = CTkButton(frame, font=("HaxrCorp4089", 30), text=" Encode with DCT", anchor="w",
                               command=lambda: encode(data.get(0.0, "end"), transform_method='dct'))
    encode_btn_dct.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    encode_btn_dwt = CTkButton(frame, font=("HaxrCorp4089", 30), text=" Encode with DWT", anchor="w",
                               command=lambda: encode(data.get(0.0, "end"), transform_method='dwt'))
    encode_btn_dwt.pack(expand=True, fill="both", padx=20, pady=(0, 20))

def decode_ui():
    for widget in frame.winfo_children():
        widget.destroy()
    try:
        stego_image = cv2.imread(FILE)
        data_dwt = dwt_steganography_extract(stego_image)
        text_dwt = CTkLabel(frame, text=data_dwt, font=("HaxrCorp4089", 30), wraplength=700, fg_color="transparent", bg_color="transparent")
        text_dwt.place(anchor="center", relx=0.5, rely=0.5)

        go_back = CTkButton(frame, text="< Go Back", font=("HaxrCorp4089", 30), command=home)
        go_back.place(anchor="nw", x=20, y=20)

    except Exception as e:
        show_error("Error: " + str(e))
        go_back = CTkButton(frame, text="< Go Back", font=("HaxrCorp4089", 30), command=home)
        go_back.place(anchor="nw", x=20, y=20)

def dct_steganography_extract(modified_image):
    ycbcr_image = cv2.cvtColor(modified_image, cv2.COLOR_BGR2YCrCb)
    height, width, _ = ycbcr_image.shape
    binary_data = ""

    for y in range(0, height, 8):
        for x in range(0, width, 8):
            block = ycbcr_image[y:y+8, x:x+8, 0]
            dct_block = cv2.dct(np.float32(block))

            for i in range(8):
                for j in range(8):
                    binary_data += str(int(dct_block[i, j].astype(np.int32)) & 1)

    string_data = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
    decoded_string = string_data
    print(decoded_string[:100])
    return decoded_string

def dwt_steganography_extract(stego_image):
    stego_gray = cv2.cvtColor(stego_image, cv2.COLOR_BGR2GRAY)
    coeffs = pywt.dwt2(stego_gray, 'haar')
    cA, (cH, cV, cD) = coeffs

    extracted_message_bin = ''
    for c in [cA, cH, cV, cD]:
        for i in range(c.shape[0]):
            for j in range(c.shape[1]):
                extracted_message_bin += str(c[i, j] % 2)

    extracted_message = ''.join([chr(int(extracted_message_bin[i:i+8], 2)) for i in range(0, len(extracted_message_bin), 8)])
    print(extracted_message)
    return extracted_message

def encode_or_decode(file):
    global FILE
    for widget in frame.winfo_children():
        widget.destroy()
    FILE = file

    encodeOption = CTkFrame(frame)
    encodeOption.pack(padx=20, pady=30, expand=True, fill="both", side="left")
    encodeOption.bind("<Enter>", lambda e: encodeOption.configure(fg_color="#814007"))
    encodeOption.bind("<Leave>", lambda e: encodeOption.configure(fg_color="#000000"))
    encodeOption.bind("<Button-1>", lambda e: encode_ui())

    description = CTkLabel(encodeOption, text="Add data to the image   ", font=("HaxrCorp4089", 30), anchor="w")
    description.pack(side="bottom", fill="x", pady=20, padx=20)
    description.bind("<Enter>", lambda e: encodeOption.configure(fg_color="#814007"))
    description.bind("<Leave>", lambda e: encodeOption.configure(fg_color="#000000"))
    description.bind("<Button-1>", lambda e: encode_ui())

    title = CTkLabel(encodeOption, text="Encode", font=("HaxrCorp4089", 30), anchor="w")
    title.pack(side="bottom", fill="x", pady=0, padx=20)
    title.bind("<Enter>", lambda e: encodeOption.configure(fg_color="#814007"))
    title.bind("<Leave>", lambda e: encodeOption.configure(fg_color="#000000"))
    title.bind("<Button-1>", lambda e: encode_ui())

    decodeOption = CTkFrame(frame)
    decodeOption.pack(padx=20, pady=30, expand=True, fill="both", side="left")
    decodeOption.bind("<Enter>", lambda e: decodeOption.configure(fg_color="#814007"))
    decodeOption.bind("<Leave>", lambda e: decodeOption.configure(fg_color="#000000"))
    decodeOption.bind("<Button-1>", lambda e: decode_ui())

    description = CTkLabel(decodeOption, text="Decode data in the image", font=("HaxrCorp4089", 30), anchor="w")
    description.pack(side="bottom", fill="x", pady=20, padx=20)
    description.bind("<Enter>", lambda e: decodeOption.configure(fg_color="#814007"))
    description.bind("<Leave>", lambda e: decodeOption.configure(fg_color="#000000"))
    description.bind("<Button-1>", lambda e: decode_ui())

    title = CTkLabel(decodeOption, text="Decode", font=("HaxrCorp4089", 30), anchor="w")
    title.pack(side="bottom", fill="x", pady=0, padx=20)
    title.bind("<Enter>", lambda e: decodeOption.configure(fg_color="#814007"))
    title.bind("<Leave>", lambda e: decodeOption.configure(fg_color="#000000"))
    title.bind("<Button-1>", lambda e: decode_ui())

def choose_file():
    file = askopenfilename()
    if file != "":
        if file.lower().endswith(".png"):
            encode_or_decode(file)
        else:
            show_error("Selected file is not a PNG image")

root = SteganographyApp()
root.geometry("900x500")
root.title("Hide Data")

def home():
    global frame
    if frame is not None:
        frame.destroy()

    frame = CTkFrame(root)
    frame.pack(padx=20, pady=20, expand=True, fill="both")
    text = CTkLabel(frame, text="Drag and Drop the Image or Choose the File", font=("HaxrCorp4089", 30))
    text.pack(pady=20)
    dnd_frame = CTkFrame(frame)
    dnd_frame.pack(padx=30, pady=(10, 30), expand=True, fill="both")
    dnd_frame.drop_target_register(DND_ALL)
    dnd_frame.dnd_bind("<<Drop>>", process_drag_and_drop)
    lbl = CTkButton(dnd_frame, text="Click to choose the file or Drag and Drop the File", font=("HaxrCorp4089", 30), hover=False, fg_color="transparent", command=choose_file)
    lbl.pack(expand=True, fill="both")

home()

root.mainloop()
