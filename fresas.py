import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pytz
import serial

class BombaAguaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Control de Bomba de Agua")
        self.geometry("400x400")

        self.reloj_label = tk.Label(self, text="", font=("Arial", 24))
        self.reloj_label.pack(pady=10)

        self.fecha_label = tk.Label(self, text="", font=("Arial", 12))
        self.fecha_label.pack(pady=5)

        self.hora_encendido_label = tk.Label(self, text="Hora de Encendido:", font=("Arial", 14))
        self.hora_encendido_label.pack(pady=5)

        self.hora_encendido_entry = tk.Entry(self, font=("Arial", 14))
        self.hora_encendido_entry.pack(pady=5)

        self.hora_apagado_label = tk.Label(self, text="Hora de Apagado:", font=("Arial", 14))
        self.hora_apagado_label.pack(pady=5)

        self.hora_apagado_entry = tk.Entry(self, font=("Arial", 14))
        self.hora_apagado_entry.pack(pady=5)

        self.aceptar_hora_button = tk.Button(self, text="Aceptar Hora", command=self.aceptar_hora)
        self.aceptar_hora_button.pack(pady=5)

        self.eliminar_hora_button = tk.Button(self, text="Eliminar Hora", command=self.eliminar_hora)
        self.eliminar_hora_button.pack(pady=5)

        self.encender_bomba_button = tk.Button(self, text="Encender Bomba", command=self.encender_bomba)
        self.encender_bomba_button.pack(pady=5)

        self.apagar_bomba_button = tk.Button(self, text="Apagar Bomba", command=self.apagar_bomba)
        self.apagar_bomba_button.pack(pady=5)

        self.estado_bomba_label = tk.Label(self, text="Estado de la Bomba: Apagada", font=("Arial", 14))
        self.estado_bomba_label.pack(pady=5)

        self.hora_encendido = None
        self.hora_apagado = None

        self.reloj_actualizar()

        # Configuración de la comunicación serial con Arduino
        self.arduino = serial.Serial('COM6', 9600, timeout=1)  # Ajusta el puerto COM según tu configuración

    def reloj_actualizar(self):
        fecha_actual = datetime.now(pytz.timezone('America/Mexico_City')).strftime('%d-%m-%y')
        hora_actual = datetime.now(pytz.timezone('America/Mexico_City')).strftime('%H:%M:%S')
        self.fecha_label.config(text=fecha_actual)
        self.reloj_label.config(text=hora_actual)
        if self.hora_encendido and self.hora_apagado:
            if self.hora_encendido <= datetime.now().time() <= self.hora_apagado:
                self.estado_bomba_label.config(text="Estado de la Bomba: Encendida")
                self.arduino.write(b'1')  # Envía '1' a Arduino para encender la bomba
            else:
                self.estado_bomba_label.config(text="Estado de la Bomba: Apagada")
                self.arduino.write(b'0')  # Envía '0' a Arduino para apagar la bomba
        self.after(1000, self.reloj_actualizar)

    def aceptar_hora(self):
        hora_encendido = self.hora_encendido_entry.get()
        hora_apagado = self.hora_apagado_entry.get()
        try:
            self.hora_encendido = datetime.strptime(hora_encendido, "%H:%M").time()
            self.hora_apagado = datetime.strptime(hora_apagado, "%H:%M").time()
            messagebox.showinfo("Hora Programada", f"Hora programada aceptada: Encendido: {hora_encendido}, Apagado: {hora_apagado}")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Por favor usa HH:MM")

    def eliminar_hora(self):
        self.hora_encendido = None
        self.hora_apagado = None
        self.hora_encendido_entry.delete(0, tk.END)  # Limpiar la entrada de la hora de encendido
        self.hora_apagado_entry.delete(0, tk.END)    # Limpiar la entrada de la hora de apagado
        messagebox.showinfo("Eliminar Hora", "Hora programada eliminada")

    def encender_bomba(self):
        self.estado_bomba_label.config(text="Estado de la Bomba: Encendida")
        self.arduino.write(b'1')  # Envía '1' a Arduino para encender la bomba

    def apagar_bomba(self):
        self.estado_bomba_label.config(text="Estado de la Bomba: Apagada")
        self.arduino.write(b'0')  # Envía '0' a Arduino para apagar la bomba


if __name__ == "__main__":
    app = BombaAguaApp()
    app.mainloop()