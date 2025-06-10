import tkinter as tk

class KeyboardShortcuts:
    def __init__(self, root):
        self.root = root
        self.bindings = {}
        self.allow_in_inputs = set()  # atalhos permitidos mesmo em campos de entrada
        root.bind_all('<Key>', self._handle_event, add='+')

    def add_shortcut(self, key_combo, callback, allow_in_input=False):
        """Registra um atalho"""
        normalized = self._normalize_combo(key_combo)
        try:
            if not callable(callback):
                self.state = "Callback deve ser uma função."
                raise ValueError("Callback deve ser uma função.")
            self.bindings[normalized] = callback
            if allow_in_input:
                self.allow_in_inputs.add(normalized)
            self.state = f"Atalho '{normalized}' adicionado com sucesso."
            return True
        
        except Exception as e:
            self.state = f"Erro ao adicionar atalho '{normalized}': {e}"
            return False
        
    def _handle_event(self, event):
        widget = event.widget
        
        # Ignora teclas em campos de entrada, a menos que permitido
        
        if isinstance(widget, (tk.Entry, tk.Text)) and not self._is_allowed_in_input(event):
            return

        combo = self._event_to_combo(event)
        if combo in self.bindings:
            if isinstance(self.bindings[combo], str):
                print(f"Erro: Callback para '{combo}' é uma string, esperado função.")
                return
            self.bindings[combo]()  # Executa callback

    def _event_to_combo(self, event):
        keys = []
        
        special_keys = {
            'Return': 'Enter',
            'Escape': 'Esc',
            'BackSpace': 'Backspace',
            'Delete': 'Delete',
            'Tab': 'Tab',
            'space': 'Space',
        }
        keySym = event.keysym
        # F1-F12 suporte
        if "_" in keySym:
            key = keySym.split('_')[0]
            keys.append(key.capitalize())
        else:
            if keySym.startswith('F') and keySym[1:].isdigit():
                keys.append(event.keysym.upper())
            else:
                key = special_keys.get(keySym, keySym.capitalize())
                keys.append(key)
        
        return '+'.join(keys)

    def _normalize_combo(self, combo):
        parts = combo.lower().split('+')
        keys = sorted([p.capitalize() for p in parts])
        return '+'.join(keys)

    def _is_allowed_in_input(self, event):
        combo = self._event_to_combo(event)
        return combo in self.allow_in_inputs
    
'''Example usage:
    shortcuts.add_shortcut("Control+S", lambda: print("Salvar"))
    shortcuts.add_shortcut("Control+Shift+Q", lambda: print("Sair"))
    shortcuts.add_shortcut("F1", lambda: print("Ajuda"))
    shortcuts.add_shortcut("Enter", lambda: print("Tecla Enter pressionada fora de input"))

    # Atalho ENTER dentro do Entry (liberado via allow_in_input=True)
    shortcuts.add_shortcut("Enter", lambda: print("Enter no campo de entrada"), allow_in_input=True)
'''
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("PDV")
    root.geometry("400x300")

    entry = tk.Entry(root)
    entry.pack(pady=10)

    label = tk.Label(root, text="Foque no campo acima e pressione Enter")
    label.pack()

    shortcuts = KeyboardShortcuts(root)

    # Atalhos gerais
    shortcuts.add_shortcut("Control", lambda: print("Salvar"))
    #shortcuts.add_shortcut("Control+Shift+Q", lambda: print("Sair"))
    shortcuts.add_shortcut("F1", lambda: print("Ajuda"))
    #shortcuts.add_shortcut("Enter", lambda: print("Tecla Enter pressionada fora de input"))

    # Atalho ENTER dentro do Entry (liberado via allow_in_input=True)
    shortcuts.add_shortcut("Enter", lambda: print("Enter no campo de entrada"), allow_in_input=True)

    root.mainloop()

if __name__ == "__main__":
    main()
