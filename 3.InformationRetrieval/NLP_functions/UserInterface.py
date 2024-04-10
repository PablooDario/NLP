import tkinter as tk
from tkinter import filedialog
import pandas as pd

class GUI_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis de Similitud de Documentos")
        self.geometry("300x300")

        self.path = None
        self.vector_representation = tk.StringVar()
        self.features = tk.StringVar()
        self.element = tk.StringVar()
        
        self.load_document()

    def load_document(self):
        
        self.vector_representation.set("Vector Representation")
        self.features.set("Select Features")
        self.element.set("Select Element")
        
        # Para cargar el documento de prueba
        tk.Label(self, text="Cargar Documento de Prueba").grid(row=1, column=0)
        btn_load_document = tk.Button(self, text="Select File", command=lambda: self.load_test_text())
        btn_load_document.grid(row=2, column=0)
        vector_menu = tk.OptionMenu(self, self.vector_representation, "Frequency", "Binarized", "TF-IDF")
        vector_menu.grid(row=3, column=0)
        features_menu = tk.OptionMenu(self, self.features, "Unigrams", "Bigrams")
        features_menu.grid(row=4, column=0)
        element_menu = tk.OptionMenu(self, self.element, "Title", "Content", "Title+Content")
        element_menu.grid(row=5, column=0)
        btn_close =tk.Button(self, text="Cargar", command=self.destroy)
        btn_close.grid(row=6, column=3)
        
        '''
        btn_execute = tk.Button(self, text="Ejecutar", command=self.realizar_analisis_1)
        btn_execute.grid(row=1, column=4)
        '''

    def load_test_text(self):
        file_path = filedialog.askopenfilename(title=f"Seleccionar archivo de texto", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.path = file_path

    def realizar_analisis_1(self):
        #Esta es la tabla a mostrar
        resultado = pd.DataFrame() 
        #En las prácticas de Varinia yo usaba Pandas Databframes para imprimir las tablas, pero en su defecto se puede usar otro.
        self.mostrar_resultado(resultado)

    def mostrar_resultado(self, resultado):
        # Para mostrar el resultado en una ventana
        result_window = tk.Toplevel(self)
        result_table = tk.Label(result_window, text="Resultado")
        result_table.pack()

        result_text = tk.Text(result_window, height=12, width=50)
        result_text.pack()
        result_text.insert(tk.END, resultado.to_string())

if __name__ == "__main__":
    app = GUI_App()
    app.mainloop()