import threading
import time
import keyboard
import requests
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar, BooleanVar
import os
from PIL import Image
import numpy as np
import webbrowser
import sys


if getattr(sys, 'frozen', False):  
    base_path = sys._MEIPASS
else:  
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, "E2.ico")  

VERSION_ACTUAL = "1.0.0"
GITHUB_URL = "https://github.com/NotAYeen/AutoE-v2"
running = False
modo_compacto = False

NOISE_INTENSITY = 35 
NOISE_FPS = 20
NOISE_FRAME_DELAY = 1000 // NOISE_FPS
NOISE_SCALE_FACTOR = 4
MIN_WIDTH = 280
MIN_HEIGHT_COMPACT = 290 
MIN_HEIGHT_FULL = 480 

FONT_FAMILY = "Courier New"
fuente_titulo = (FONT_FAMILY, 18, "bold")
fuente_normal = (FONT_FAMILY, 12, "bold")
fuente_pequena = (FONT_FAMILY, 10, "bold")

COLOR_FONDO = "
COLOR_TEXTO = "
COLOR_WIDGET_FONDO = "
COLOR_BORDE = "
COLOR_HOVER = "

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("AutoE v.2")


if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

root.configure(fg_color=COLOR_FONDO) 
root.resizable(True, True) 
root.minsize(MIN_WIDTH, MIN_HEIGHT_FULL)
root.attributes("-topmost", True)

bg_noise_label = ctk.CTkLabel(root, text="", fg_color="transparent")
bg_noise_label.place(x=0, y=0, relwidth=1, relheight=1)



def generar_ruido_dinamico():
    global bg_noise_label
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    if current_width <= 1 or current_height <= 1:
        root.after(NOISE_FRAME_DELAY, generar_ruido_dinamico)
        return

    small_width = current_width // NOISE_SCALE_FACTOR
    small_height = current_height // NOISE_SCALE_FACTOR
    
    if small_width < 1 or small_height < 1:
        root.after(NOISE_FRAME_DELAY, generar_ruido_dinamico)
        return

    noise_array = np.random.randint(0, NOISE_INTENSITY, 
                                    (small_height, small_width), 
                                    dtype=np.uint8)
    
    noise_pil_img = Image.fromarray(noise_array, mode='L')
    full_size_img = noise_pil_img.resize((current_width, current_height), 
                                         Image.Resampling.NEAREST)
    noise_ctk_img = ctk.CTkImage(light_image=full_size_img, 
                                 size=(current_width, current_height))
    bg_noise_label.configure(image=noise_ctk_img)
    bg_noise_label.image = noise_ctk_img 
    root.after(NOISE_FRAME_DELAY, generar_ruido_dinamico)

def presionar_tecla(tecla, tiempo):
    keyboard.press(tecla)
    time.sleep(tiempo)
    keyboard.release(tecla)

def rutina_e_ad():
    global running
    while running:
        for _ in range(100):
            if not running: return
            keyboard.press('e')
            time.sleep(0.1)
            keyboard.release('e')
        if not running: return
        presionar_tecla('a', 1.25)
        for _ in range(100):
            if not running: return
            keyboard.press('e')
            time.sleep(0.1)
            keyboard.release('e')
        if not running: return
        presionar_tecla('d', 1.25)

def rutina_solo_e():
    global running
    try:
        intervalo = int(intervalo_entry.get()) / 1000
    except ValueError:
        intervalo = 0.2
    while running:
        keyboard.press('e')
        time.sleep(intervalo)
        keyboard.release('e')
        time.sleep(intervalo)

def iniciar():
    global running
    if not running:
        running = True
        modo = modo_rutina.get()
        if modo == "solo_e":
            threading.Thread(target=rutina_solo_e, daemon=True).start()
        else:
            threading.Thread(target=rutina_e_ad, daemon=True).start()
        estado_label.configure(text="ACTIVO", text_color="

def detener():
    global running
    running = False
    estado_label.configure(text="SUSPENDIDO", text_color="

def alternar_modo_compacto():
    global modo_compacto
    modo_compacto = not modo_compacto
    if modo_compacto:
        frame_rutina.pack_forget()
        check_on_top.pack_forget() 
        root.minsize(MIN_WIDTH, MIN_HEIGHT_COMPACT) 
        btn_compacto.configure(text="EXPANDIR OPCIONES")
    else:
        check_on_top.pack(pady=10, fill="x", padx=20) 
        frame_rutina.pack(pady=5, fill="x", padx=20)
        root.minsize(MIN_WIDTH, MIN_HEIGHT_FULL) 
        btn_compacto.configure(text="MODO COMPACTO")

def toggle_on_top():
    estado = on_top_var.get()
    root.attributes("-topmost", estado)

def actualizar_intervalo(*args):
    if modo_rutina.get() == "solo_e":
        if not modo_compacto: 
            if not intervalo_label.winfo_ismapped():
                intervalo_label.pack(anchor="w", pady=(10,0), padx=10)
            if not intervalo_entry.winfo_ismapped():
                intervalo_entry.pack(anchor="w", pady=(0,10), padx=10)
    else:
        if intervalo_label.winfo_ismapped():
            intervalo_label.pack_forget()
        if intervalo_entry.winfo_ismapped():
            intervalo_entry.pack_forget()

def safe_toggle_script():
    if running:
        detener()
    else:
        iniciar()

def on_hotkey_press():
    root.after(0, safe_toggle_script)

def comprobar_actualizacion():
    url = "https://raw.githubusercontent.com/NotAYeen/AutoE-v2/main/version.txt"
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            version_remota = respuesta.text.strip()
            if version_remota != VERSION_ACTUAL:
                status_version_label.configure(text=f"UPDATE: {version_remota}", text_color="orange")
                msg = CTkMessagebox(
                    title="Actualización disponible",
                    message=f"Hay una nueva versión disponible: {version_remota}\nTu versión: {VERSION_ACTUAL}",
                    icon="info",
                    font=fuente_normal,
                    option_1="Descargar",  
                    option_2="Más tarde"    
                )
                respuesta_usuario = msg.get()
                if respuesta_usuario == "Descargar":
                    webbrowser.open_new_tab(GITHUB_URL)
            else:
                status_version_label.configure(text="ACTUALIZADO", text_color="
        else:
            status_version_label.configure(text="ERROR VERSION", text_color="red")
    except Exception as e:
        print("Error al comprobar actualización:", e)
        status_version_label.configure(text="ERROR CONEXION", text_color="red")



button_style = {
    "font": fuente_normal,
    "text_color": COLOR_TEXTO,
    "fg_color": COLOR_WIDGET_FONDO,
    "border_color": COLOR_BORDE,
    "hover_color": COLOR_HOVER,
    "border_width": 2,
    "corner_radius": 0, 
}

label_style = {
    "font": fuente_normal,
    "text_color": COLOR_TEXTO,
    "fg_color": "transparent" 
}

frame_style = {
    "fg_color": COLOR_WIDGET_FONDO,
    "border_color": COLOR_BORDE,
    "border_width": 2,
    "corner_radius": 0,
}

radio_inside_style = {
    "font": fuente_normal,
    "text_color": COLOR_TEXTO,
    "fg_color": COLOR_BORDE, 
    "hover_color": COLOR_HOVER,
    "bg_color": "transparent" 
}

check_style = radio_inside_style.copy() 
check_style["font"] = (FONT_FAMILY, 11, "bold")



titulo = ctk.CTkLabel(root, text="AutoE v.2", font=fuente_titulo, 
                      text_color=COLOR_TEXTO, fg_color="transparent")
titulo.pack(pady=10, fill="x", padx=20) 

estado_label = ctk.CTkLabel(root, text="SUSPENDIDO", text_color="red", 
                            font=(FONT_FAMILY, 14, "bold"), fg_color="transparent")
estado_label.pack(fill="x", padx=20)

btn_iniciar = ctk.CTkButton(root, text="▶ INICIAR", command=iniciar, height=40, **button_style)
btn_iniciar.pack(pady=(10,5), fill="x", padx=20)

btn_detener = ctk.CTkButton(root, text="⏹ DETENER", command=detener, height=40, **button_style)
btn_detener.pack(pady=(5,10), fill="x", padx=20)

compact_button_style = button_style.copy()
compact_button_style['font'] = fuente_pequena 

btn_compacto = ctk.CTkButton(root, text="MODO COMPACTO", command=alternar_modo_compacto,
                           height=25, **compact_button_style)
btn_compacto.pack(pady=5, fill="x", padx=20)

on_top_var = BooleanVar(value=True) 
check_on_top = ctk.CTkCheckBox(root, text="SIEMPRE VISIBLE", 
                               command=toggle_on_top,
                               variable=on_top_var,
                               onvalue=True, offvalue=False,
                               **check_style)
check_on_top.pack(pady=10, fill="x", padx=20) 

frame_rutina = ctk.CTkFrame(root, **frame_style)
frame_rutina.pack(pady=5, fill="x", padx=20)

modo_label = ctk.CTkLabel(frame_rutina, text="MODO DE RUTINA:", **label_style)
modo_label.pack(anchor="w", pady=(10,0), padx=10) 

modo_rutina = StringVar(value="solo_e")
modo_rutina.trace_add("write", actualizar_intervalo)

radio1 = ctk.CTkRadioButton(frame_rutina, text="SOLO E", variable=modo_rutina, 
                            value="solo_e", **radio_inside_style)
radio1.pack(anchor="w", padx=30, pady=3) 

radio2 = ctk.CTkRadioButton(frame_rutina, text="E + A + D", variable=modo_rutina, 
                            value="e_ad", **radio_inside_style)
radio2.pack(anchor="w", padx=30, pady=3) 

intervalo_label = ctk.CTkLabel(frame_rutina, text="INTERVALO (MS):", **label_style)
intervalo_entry = ctk.CTkEntry(frame_rutina, width=80, font=fuente_normal,
                               fg_color=COLOR_WIDGET_FONDO,
                               border_color=COLOR_BORDE,
                               text_color=COLOR_TEXTO,
                               border_width=2,
                               corner_radius=0)
intervalo_entry.insert(0, "200")

root.after(100, actualizar_intervalo)

status_version_label = ctk.CTkLabel(root, text="COMPROBANDO...", font=fuente_pequena,
                                    text_color=COLOR_TEXTO, fg_color="transparent")
status_version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)



root.after(500, comprobar_actualizacion) 
root.after(100, generar_ruido_dinamico)

keyboard.add_hotkey('ctrl+f1', on_hotkey_press)

root.mainloop()
