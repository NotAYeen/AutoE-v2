import threading
import time
import keyboard
import tkinter as tk
from tkinter import messagebox
import requests

# ---------- CONFIGURACIÓN ----------
VERSION_ACTUAL = "1.0.0"
running = False
modo_compacto = False

root = tk.Tk()
root.title("AutoE v.2")
root.geometry("300x450")
root.configure(bg="#C0C0C0")  # Fondo clásico XP
root.resizable(False, False)

# ---------- FUNCIONALIDAD ----------
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
    intervalo = int(intervalo_entry.get()) / 1000
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
        estado_label.config(text="Activo", fg="green")

def detener():
    global running
    running = False
    estado_label.config(text="Suspendido", fg="red")

def alternar_modo_compacto():
    global modo_compacto
    modo_compacto = not modo_compacto
    if modo_compacto:
        intervalo_label.pack_forget()
        intervalo_entry.pack_forget()
        root.geometry("300x230")
        btn_compacto.config(text="Expandir opciones")
    else:
        if modo_rutina.get() == "solo_e":
            intervalo_label.pack(anchor="w", pady=(10,0), padx=20)
            intervalo_entry.pack(anchor="w", pady=(0,10), padx=20)
        root.geometry("300x400")
        btn_compacto.config(text="Modo compacto")

def actualizar_intervalo(*args):
    if modo_rutina.get() == "solo_e":
        if not intervalo_label.winfo_ismapped():
            intervalo_label.pack(anchor="w", pady=(10,0), padx=20)
        if not intervalo_entry.winfo_ismapped():
            intervalo_entry.pack(anchor="w", pady=(0,10), padx=20)
    else:
        if intervalo_label.winfo_ismapped():
            intervalo_label.pack_forget()
        if intervalo_entry.winfo_ismapped():
            intervalo_entry.pack_forget()

# ---------- COMPROBAR ACTUALIZACIÓN ----------
def comprobar_actualizacion():
    url = "https://raw.githubusercontent.com/usuario/repositorio/main/version.txt"  # Cambia esta URL
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            version_remota = respuesta.text.strip()
            if version_remota != VERSION_ACTUAL:
                status_version_label.config(text=f"Update: {version_remota}", fg="orange")
                messagebox.showinfo(
                    "Actualización disponible",
                    f"Hay una nueva versión disponible: {version_remota}\nTu versión: {VERSION_ACTUAL}"
                )
            else:
                status_version_label.config(text="Actualizado ✅", fg="green")
        else:
            status_version_label.config(text="Error versión", fg="red")
    except Exception as e:
        print("Error al comprobar actualización:", e)
        status_version_label.config(text="Error conexión", fg="red")

# ---------- INTERFAZ VISUAL ----------
fuente_titulo = ("Tahoma", 18, "bold")
fuente_normal = ("Tahoma", 11)
fuente_negrita = ("Tahoma", 11, "bold")

titulo = tk.Label(root, text="AutoE v.2", font=fuente_titulo, bg="#C0C0C0", fg="#000000")
titulo.pack(pady=10)

estado_label = tk.Label(root, text="Suspendido", fg="red", bg="#C0C0C0", font=("Tahoma", 12, "bold"))
estado_label.pack()

btn_iniciar = tk.Button(root, text="▶ Iniciar", command=iniciar, font=fuente_negrita,
                        bg="#E0E0E0", width=12, height=2, relief="raised")
btn_iniciar.pack(pady=(10,5))

btn_detener = tk.Button(root, text="⏹ Detener", command=detener, font=fuente_negrita,
                        bg="#E0E0E0", width=12, height=2, relief="raised")
btn_detener.pack(pady=(5,10))

btn_compacto = tk.Button(root, text="Modo compacto", command=alternar_modo_compacto,
                         font=fuente_normal, bg="#D9D9D9", width=18, relief="raised")
btn_compacto.pack(pady=5)

modo_label = tk.Label(root, text="Modo de rutina:", font=fuente_negrita, bg="#C0C0C0")
modo_label.pack(anchor="w", pady=(10,0), padx=20)

modo_rutina = tk.StringVar(value="solo_e")
modo_rutina.trace_add("write", actualizar_intervalo)

radio1 = tk.Radiobutton(root, text="Solo E", variable=modo_rutina, value="solo_e",
                        font=fuente_normal, bg="#C0C0C0", activebackground="#C0C0C0")
radio1.pack(anchor="w", padx=40, pady=3)

radio2 = tk.Radiobutton(root, text="E + A + D", variable=modo_rutina, value="e_ad",
                        font=fuente_normal, bg="#C0C0C0", activebackground="#C0C0C0")
radio2.pack(anchor="w", padx=40, pady=3)

intervalo_label = tk.Label(root, text="Intervalo entre pulsaciones (ms):", font=fuente_normal, bg="#C0C0C0")
intervalo_entry = tk.Entry(root, width=8, font=fuente_normal)
intervalo_entry.insert(0, "200")

root.after(100, actualizar_intervalo)

# ---------- LABEL DE VERSIÓN (esquina inferior derecha) ----------
status_version_label = tk.Label(root, text="Comprobando versión...", font=("Tahoma", 9),
                                bg="#C0C0C0", fg="black")
status_version_label.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

# ---------- INICIO ----------
root.after(800, comprobar_actualizacion)
root.mainloop()
