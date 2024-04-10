import NLP_functions as nlp
from Controller import controller as AppController

def main():
    controller = AppController()
    
    #Load the file and select the characteristics
    ui = nlp.GUI_App()
    ui.mainloop()
    normalized_document= controller.normalize_text(ui.path)
    
    controller.local_test(ui, normalized_document)
    
    global_results = controller.global_test(normalized_document)
    print(f"--------Global-------\n{global_results}")


if __name__ == "__main__":
    main()