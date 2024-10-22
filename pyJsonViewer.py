import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, simpledialog

original_data = None

def load_json():
    global original_data
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            original_data = json.load(file)
        tree.delete(*tree.get_children())
        populate_tree(original_data)

def populate_tree(data, parent=''):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                node = tree.insert(parent, 'end', text=key, open=False)
                populate_tree(value, node)
            else:
                tree.insert(parent, 'end', text=f"{key}: {value}", open=False)
    elif isinstance(data, list):
        node = tree.insert(parent, 'end', text=f"Array ({len(data)} items)", open=False, tags=('array',))
        for i, item in enumerate(data):
            if isinstance(item, dict):
                name = item.get("Name", "")
                market_type = item.get("Markettype", {}).get("Name", "")
                text = f"[{i}]" + (f" - {name}" if name else "") + (f" ({market_type})" if market_type else "")
                child_node = tree.insert(node, 'end', text=text, open=False)
                populate_tree(item, child_node)
            elif isinstance(item, list):
                child_node = tree.insert(node, 'end', text=f"[{i}]", open=False)
                populate_tree(item, child_node)
            else:
                tree.insert(node, 'end', text=f"[{i}]: {item}", open=False)
    else:
        tree.insert(parent, 'end', text=str(data), open=False)

def filter_array(event):
    item = tree.focus()
    if 'array' in tree.item(item, 'tags'):
        parent = tree.parent(item)
        data = get_data_from_tree(item)
        property_name = simpledialog.askstring("Filtra Array", "Inserisci il nome della proprietà:")
        if property_name:
            filter_value = simpledialog.askstring("Filtra Array", f"Inserisci il valore per {property_name}:")
            if filter_value:
                filtered_data = [item for item in data if filter_value.lower() in str(item.get(property_name, '')).lower()]
                
                # Rimuovi i vecchi elementi
                tree.delete(item)
                
                # Popola con i dati filtrati
                new_node = tree.insert(parent, 'end', text=f"Filtered Array ({len(filtered_data)} items)", open=True, tags=('array', 'filtered'))
                populate_tree(filtered_data, new_node)
                
                # Abilita il pulsante per rimuovere i filtri
                remove_filter_button.config(state='normal')

def get_data_from_tree(item):
    data = []
    for child in tree.get_children(item):
        child_data = {}
        for grandchild in tree.get_children(child):
            text = tree.item(grandchild, 'text')
            if ':' in text:
                key, value = text.split(':', 1)
                child_data[key.strip()] = value.strip()
        data.append(child_data)
    return data

def remove_filters():
    global original_data
    if original_data:
        tree.delete(*tree.get_children())
        populate_tree(original_data)
        remove_filter_button.config(state='disabled')

def on_double_click(event):
    item = tree.selection()[0]
    tree.item(item, open=not tree.item(item)["open"])

def expand_all():
    for item in tree.get_children():
        tree.item(item, open=True)
        expand_children(item)

def expand_children(parent):
    for child in tree.get_children(parent):
        tree.item(child, open=True)
        expand_children(child)

def collapse_all():
    for item in tree.get_children():
        tree.item(item, open=False)
        collapse_children(item)

def collapse_children(parent):
    for child in tree.get_children(parent):
        tree.item(child, open=False)
        collapse_children(child)

# Creazione della finestra principale con tema scuro
root = ttk.Window(themename="darkly")
root.title("JSON Viewer")
root.geometry("800x600")

# Creazione dei pulsanti
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

load_button = ttk.Button(button_frame, text="Carica JSON", command=load_json, style='primary.TButton')
load_button.pack(side='left', padx=5)

expand_button = ttk.Button(button_frame, text="Espandi Tutto", command=expand_all, style='info.TButton')
expand_button.pack(side='left', padx=5)

collapse_button = ttk.Button(button_frame, text="Comprimi Tutto", command=collapse_all, style='info.TButton')
collapse_button.pack(side='left', padx=5)

remove_filter_button = ttk.Button(button_frame, text="Rimuovi Filtri", command=remove_filters, style='warning.TButton', state='disabled')
remove_filter_button.pack(side='left', padx=5)

# Creazione del widget Treeview
tree = ttk.Treeview(root, bootstyle="dark")
tree.pack(expand=True, fill='both')

# Gestione del doppio click per espandere/comprimere i nodi
tree.bind("<Double-1>", on_double_click)

# Gestione del click destro per filtrare gli array
tree.bind("<Button-3>", filter_array)

root.mainloop()