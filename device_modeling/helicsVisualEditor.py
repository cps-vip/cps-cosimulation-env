import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import os
import json
from graphVisual import map_all_devices, SRC_DIR

#TODO: Create templates for adding devices
class JSONEditor(tk.Toplevel):
    def __init__(self, master, config_path, all_publications=None, template=None):
        super().__init__(master)
        self.title("HELICS Config Editor")
        self.config_path = config_path
        self.all_publications = all_publications or {}
        self.publications = []
        self.subscriptions = []
        self.confirm = False
        if config_path and os.path.exists(config_path): 
            if  not template:
                with open(config_path, 'r') as f:
                    self.config_data = json.load(f)
            else:
                self.config_data = template 

            self.publications = self.config_data.get("publications", [])
            self.subscriptions = self.config_data.get("subscriptions", [])

            self.create_widgets()
            self.update_dropdowns()
            self.grab_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Core Configuration
        ttk.Label(main_frame, text="Core Configuration").grid(row=0, column=0, sticky=tk.W)
        core_frame = ttk.Frame(main_frame)
        core_frame.grid(row=1, column=0, sticky=tk.EW)
        
        ttk.Label(core_frame, text="Core Name:").grid(row=0, column=0)
        self.core_name = ttk.Entry(core_frame)
        self.core_name.insert(0, self.config_data.get("coreName", ""))
        self.core_name.grid(row=0, column=1)
        
        ttk.Label(core_frame, text="Core Type:").grid(row=1, column=0)
        self.core_type = ttk.Combobox(core_frame, values=["zmq", "tcp", "udp"])
        self.core_type.set(self.config_data.get("coreType", "zmq"))
        self.core_type.grid(row=1, column=1)
        
        # Publications Section
        pub_frame = ttk.LabelFrame(main_frame, text="Publications")
        pub_frame.grid(row=2, column=0, sticky=tk.EW, pady=5)
        
        self.pub_combobox = ttk.Combobox(pub_frame, state="readonly", width=35)
        self.pub_combobox.pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(pub_frame)
        btn_frame.pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Edit", command=self.edit_publication).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Add New", command=self.add_publication).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_publication).pack(side=tk.LEFT, padx=2)

        # Subscriptions Section
        sub_frame = ttk.LabelFrame(main_frame, text="Subscriptions")
        sub_frame.grid(row=3, column=0, sticky=tk.EW, pady=5)
        
        self.sub_combobox = ttk.Combobox(sub_frame, state="readonly", width=35)
        self.sub_combobox.pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(sub_frame)
        btn_frame.pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Edit", command=self.edit_subscription).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Add New", command=self.add_subscription).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_subscription).pack(side=tk.LEFT, padx=2)

        # Control Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, pady=10)
        ttk.Button(btn_frame, text="Save", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def update_dropdowns(self):
        # Update publications dropdown
        pub_names = [f"{p.get('name', 'Unnamed')} ({p.get('key', 'no key')})" 
                    for p in self.publications]
        self.pub_combobox['values'] = pub_names
        self.pub_combobox.set('' if not pub_names else pub_names[0])
        
        # Update subscriptions dropdown
        sub_names = [f"{s.get('name', 'Unnamed')} ({s.get('key', 'no key')})" 
                    for s in self.subscriptions]
        self.sub_combobox['values'] = sub_names
        self.sub_combobox.set('' if not sub_names else sub_names[0])

    def edit_publication(self):
        selected_idx = self.pub_combobox.current()
        if selected_idx == -1:
            messagebox.showwarning("No Selection", "Please select a publication to edit", master=self)
            return
        self.edit_entry(self.publications[selected_idx], "publications", selected_idx)

    #TODO: Finish confirm box for delete
    def delete_publication(self):
        selected_idx = self.pub_combobox.current()
        if selected_idx == -1:
            messagebox.showwarning("No Selection", "Please select a publication to delete", master=self)
            return
        confirm_box()
        if self.confirm:
            del self.publications[selected_idx]
        self.update_dropdowns()

    def edit_subscription(self):
        selected_idx = self.sub_combobox.current()
        if selected_idx == -1:
            messagebox.showwarning("No Selection", "Please select a subscription to edit", master=self)
            return
        self.edit_entry(self.subscriptions[selected_idx], "subscriptions", selected_idx)

    #TODO: Finish confirm box for delete
    def delete_subscription(self):
        selected_idx = self.sub_combobox.current()
        if selected_idx == -1:
            messagebox.showwarning("No Selection", "Please select a subscription to delete", master=self)
            return

        confirm_box()
        if self.confirm:
            del self.subscriptions[selected_idx]
        self.update_dropdowns()

    def edit_entry(self, data, category, index):
        edit_win = tk.Toplevel(self)
        edit_win.title(f"Edit {category[:-1]}")
        
        fields = ["name", "key", "type", "unit"]
        if category == "publications":
            fields += ["global", "tolerance"]
        else:
            fields += ["required", "tolerance", "default"]
        
        entries = {}
        for row, field in enumerate(fields):
            ttk.Label(edit_win, text=f"{field.title()}:").grid(row=row, column=0, sticky=tk.W)
            entries[field] = ttk.Entry(edit_win)
            value = str(data.get(field, ""))
            if field in ['global', 'required']:
                value = str(data.get(field, False)).lower()
            entries[field].insert(0, value)
            entries[field].grid(row=row, column=1, sticky=tk.EW)
        #TODO: Fix window levels on save and messages 
        ttk.Button(edit_win, text="Save", 
                 command=lambda: self.save_edit(edit_win, entries, data, category, index)
                 ).grid(row=len(fields)+1, columnspan=2)

    #TODO: Add some logic to make sure pubs and subs conform to helics standards
    def save_edit(self, window, entries, original_data, category, index):
        for field, entry in entries.items():
            value = entry.get()
            if field in ['global', 'required']:
                value = value.lower() in ['true', '1', 'yes']
            elif field == 'tolerance' and value:
                try: value = float(value)
                except: value = 0.0
            elif field == 'default' and value:
                try: value = json.loads(value)
                except: value = value
            original_data[field] = value
        
        if category == "publications":
            self.publications[index] = original_data
        else:
            self.subscriptions[index] = original_data
        
        window.destroy()
        self.update_dropdowns()
        messagebox.showinfo("Updated", f"{category[:-1]} updated successfully", master=self)

    def add_publication(self):
        pub_win = tk.Toplevel(self)
        pub_win.title("New Publication")
        
        fields = [("name", "Name:"), ("key", "Key:"), ("type", "Type:"),
                 ("unit", "Unit:"), ("global", "Global (true/false):"),
                 ("tolerance", "Tolerance:")]
        entries = {}
        
        for row, (field, label) in enumerate(fields):
            ttk.Label(pub_win, text=label).grid(row=row, column=0)
            entries[field] = ttk.Entry(pub_win)
            entries[field].grid(row=row, column=1)
        
        ttk.Button(pub_win, text="Save", command=lambda: self.save_new_entry(
            pub_win, entries, "publications")).grid(row=len(fields), columnspan=2)

    def add_subscription(self):
        sub_win = tk.Toplevel(self)
        sub_win.title("New Subscription")
        
        main_frame = ttk.Frame(sub_win)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Publication selection
        ttk.Label(main_frame, text="Available Publications:").grid(row=0, column=0, sticky=tk.W)
        pub_listbox = tk.Listbox(main_frame, width=50, height=6)
        pub_listbox.grid(row=1, column=0, columnspan=2, sticky=tk.EW)
        
        for device, (pubs, _) in self.all_publications.items():
            for pub in pubs:
                pub_listbox.insert(tk.END, f"{device}: {pub['key']}")
        
        ttk.Button(main_frame, text="Use Selected", 
                  command=lambda: self.use_selected_pub(pub_listbox)).grid(row=2, column=0, pady=5)
        
        # Subscription fields
        fields = [("key", "Key:"), ("type", "Type:"), ("unit", "Unit:"),
                 ("required", "Required:"), ("tolerance", "Tolerance:"),
                 ("default", "Default Value:")]
        self.entries = {}
        
        for row, (field, label) in enumerate(fields, start=3):
            ttk.Label(main_frame, text=label).grid(row=row, column=0)
            self.entries[field] = ttk.Entry(main_frame)
            self.entries[field].grid(row=row, column=1)
        
        ttk.Button(main_frame, text="Save", 
                  command=lambda: self.save_new_entry(sub_win, self.entries, "subscriptions")
                  ).grid(row=len(fields)+3, columnspan=2)

    def use_selected_pub(self, listbox):
        selection = listbox.curselection()
        if not selection: return
        
        selected = listbox.get(selection[0])
        device, key = selected.split(": ", 1)
        
        for pub_device, (pubs, _) in self.all_publications.items():
            if pub_device == device:
                for pub in pubs:
                    if pub['key'] == key:
                        self.entries['key'].delete(0, tk.END)
                        self.entries['key'].insert(0, key)
                        self.entries['type'].delete(0, tk.END)
                        self.entries['type'].insert(0, pub.get('type', ''))
                        self.entries['unit'].delete(0, tk.END)
                        self.entries['unit'].insert(0, pub.get('unit', ''))
                        return

    #TODO: Add some logic to make sure pubs and subs conform to helics standards
    def save_new_entry(self, window, entries, category):
        data = {}
        for field, entry in entries.items():
            value = entry.get()
            if field in ['global', 'required']:
                value = value.lower() in ['true', '1', 'yes']
            elif field == 'tolerance' and value:
                try: value = float(value)
                except: value = 0.0
            elif field == 'default' and value:
                try: value = json.loads(value)
                except: value = value
            data[field] = value
        
        if category == "publications":
            self.publications.append(data)
        else:
            self.subscriptions.append(data)
        
        window.destroy()
        self.update_dropdowns()

    def save_config(self):
        self.config_data.update({
            "coreName": self.core_name.get(),
            "coreType": self.core_type.get(),
            "publications": self.publications,
            "subscriptions": self.subscriptions
        })
        
        if self.config_path:
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=4)
            messagebox.showinfo("Success", "Configuration saved successfully", master=self)
            self.destroy()

    def confirm_box(self):
        self.confirm = False
        confirm_win = tk.TopLevel(self)
        confirm_win.title("Confirm Delete?")

        main_frame = tk.Frame(confirm_win)
        main_frame.pack()

        tk.Label(main_frame, text="Are you sure you want to delete this?").pack(side=tk.TOP)
        tk.Button(main_frame, text="Yes", command= lambda: set_confirm(confirm_win, True))).pack(side=tk.LEFT)
        tk.Button(main_frame, text="No", command= lambda: set_confirm(confirm_win, False)).pack(side=tk.RIGHT)
        
        self.grab_set()
        self.wait_window(confirm_win)

    def set_confirm(self, window, value):
        window.destroy()
        self.confirm = value


class GraphEditorApp:
    def __init__(self, master):
        self.master = master
        self.device_map = {}
        self.current_selection = None
        self.config_dir = os.path.join(SRC_DIR, "")
        self.all_publications = {}
        
        self.master.title("HELICS Network Visualizer")
        self.master.geometry("1200x800")
        
        self.create_widgets()
        self.refresh_graph()

    def create_widgets(self):
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.refresh_btn = ttk.Button(control_frame, text="Refresh Graph", command=self.refresh_graph)
        self.refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.add_btn = ttk.Button(control_frame, text="Add New Device", command=self.add_device)
        self.add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.edit_btn = ttk.Button(control_frame, text="Edit Selected", command=self.edit_device, state=tk.DISABLED)
        self.edit_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_btn = ttk.Button(control_frame, text="Delete Selected", command=self.delete_device, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.fig = plt.figure(figsize=(16, 12))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def refresh_graph(self):
        self.fig.clf()
        self.device_map = map_all_devices(self.config_dir)
        self.all_publications = self.device_map
        
        self.G = nx.DiGraph()
        self.G.add_nodes_from(self.device_map.keys())
        
        devices = list(self.device_map.items())
        for pub_dev, (pubs, _) in devices:
            for sub_dev, (_, subs) in devices:
                if pub_dev != sub_dev and set(s['key'] for s in subs) & set(p['key'] for p in pubs):
                    self.G.add_edge(pub_dev, sub_dev)
        
        ax = self.fig.add_subplot(111)
        self.node_positions = nx.kamada_kawai_layout(self.G)
        nx.draw(self.G, self.node_positions, ax=ax, with_labels=True,
               node_size=2500, node_color='lightblue', font_size=10, arrowsize=20)
        
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.draw()

    def on_click(self, event):
        if not event.inaxes: return
        
        click_point = (event.xdata, event.ydata)
        min_dist = float('inf')
        closest = None
        
        for node, pos in self.node_positions.items():
            dist = (pos[0]-click_point[0])**2 + (pos[1]-click_point[1])**2
            if dist < min_dist:
                min_dist = dist
                closest = node
        
        if min_dist < 0.01:
            self.current_selection = closest
            self.edit_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            self.highlight_node(closest)
        else:
            self.current_selection = None
            self.edit_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)

    def highlight_node(self, node):
        ax = self.fig.gca()
        ax.clear()
        node_colors = ['orange' if n == node else 'lightblue' for n in self.G.nodes()]
        nx.draw(self.G, self.node_positions, ax=ax, with_labels=True,
               node_color=node_colors, node_size=2500, font_size=10, arrowsize=20)
        self.canvas.draw()
    
    #TODO: Add more templates for devices
    def add_device(self):
        empty_template = {
                "coreName": "",
                "coreType": "zmq",
                "name": "",
                "publications": [],
                "subscriptions": []
            }

        name_win = tk.Toplevel(self.master)
        name_win.title = "Name File"
        ttk.Label(name_win, text="File Name: ").pack(side=tk.LEFT)
        entry = ttk.Entry(name_win)
        entry.pack(side=tk.LEFT, padx=5, pady=10)
        ttk.Button(name_win, text="Create new file", 
                 command=lambda: self.create_file(entry, name_win, empty_template)
                 ).pack(side=tk.LEFT)
        name_win.grab_set()

   #TODO: Check entry.get() for illegal characters that may mess up file creation 
    def create_file(self, entry, window, template):
        name = "config/" + entry.get() + "_config.json"
        try:
            f = open(name, "x")
            f.write(json.dumps(template))
            f.close()
            window.destroy()
            JSONEditor(self.master, config_path=name, all_publications=self.all_publications, template=template)
            self.refresh_graph()
        except FileExistsError:
            messagebox.showwarning("File Already Exists", "Please select a different file name")
        except Exception as e:
            messagebox.showwarning("Error", f"Could not create file: {e}")


    def edit_device(self):
        if not self.current_selection: return
        
        target_file = self.find_config_file()
        if target_file:
            JSONEditor(self.master, target_file, self.all_publications)
            self.refresh_graph()
        else:
            messagebox.showerror("Error", f"No config found for {self.current_selection}:{target_file}")
    
    def delete_device(self):
        if not self.current_selection: return
        target_file = self.find_config_file()
        try:
            os.remove(target_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete {self.current_selection}:{e}")
        self.refresh_graph()

    def find_config_file(self):
        target = self.current_selection.lower().replace(' ', '')
        for root, _, files in os.walk(self.config_dir):
            for file in files:
                if file.endswith('.json'):
                    base = os.path.splitext(file)[0].replace('_config', '')
                    clean_base = base.lower().replace(' ', '')
                    if clean_base == target:
                        return os.path.join(root, file)
        return None

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphEditorApp(root)
    app.run()
