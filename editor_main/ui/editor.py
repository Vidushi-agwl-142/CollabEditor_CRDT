import tkinter as tk

class FileSystemEditor():
    def __init__(self, client) -> None:
        self.root = tk.Tk()
        self.client = client
        self.curr_file = ""
        self.files = []
        self.notebooks = {}
        self.file_index = 0
        if self.client is not None:
            Files = tk.Label(self.root, text="Files", width=10, height=5)
            Add = tk.Button(self.root, text="+", command= lambda: self.add_name(), width=10, height=5)
            Refresh = tk.Button(self.root, text="Refresh", command= lambda: self.refresh(), width=10, height=5)
            Connect = tk.Button(self.root, text="Connect", command= lambda: self.connect(), width=10, height=5)
            Files.grid(row = 0, column = 0)
            Add.grid(row = 0, column = 1)
            Refresh.grid(row = 0, column = 7)
            Connect.grid(row = 0, column = 6)
            self.client.attach_editor(self)
        
    def disconnect(self):
        # self.client.disconnect()
        Connect = tk.Button(self.root, text="Connect", command= lambda: self.connect(), width=10, height=5)
    
    def connect(self):
        # self.client.connect()
        Disconnect = tk.Button(self.root, text="Disconnect", command= lambda: self.disconnect(), width=10, height=5)

    def refresh(self):
        for peer in self.client.get_peers():
            self.client.sync(peer)
        self.render(self.curr_file)
    
    def add_name(self):
        file_name = tk.Entry(self.root, width=10)
        submit = tk.Button(self.root, text="submit", command=lambda: self.add_file(submit, file_name), width=10, height=5)
        file_name.grid(row=self.file_index+1, column = 0)
        submit.grid(row=self.file_index+1, column = 1)

    def add_file(self, submit, file_name):
        name = file_name.get()
        submit.destroy()
        file_name.destroy()
        self.files.append(name)
        self.file_index += 1
        self.notebooks[name]=[]
        self.curr_file = name
        new_file = tk.Button(self.root, text=name, width=10, height=5)
        delete = tk.Button(self.root, text="Delete", width=10, height=5)
        file = tk.Label(self.root, text=self.curr_file, width=10, height=5)
        file.grid(row= 0, column = 2)

        # if self.client is not None:
        #     self.client.create_file() 
        new_file.grid(row=self.file_index, column = 0)
        delete.grid(row=self.file_index, column = 1)
        self.add_cell()


    def add_cell(self, after=None):
        cell = self.create_cell_frame()
        # Figure out if where to insert or append the cell based on which cell the add
        # button was clicked
        if after in self.notebooks[self.curr_file]:
            index = self.notebooks[self.curr_file].index(after) + 1
        else:
            index = len(self.notebooks[self.curr_file])

        if index >= len(self.notebooks[self.curr_file]):
            self.notebooks[self.curr_file].append(cell)
            if self.client is not None:
                self.client.create_cell()
        else:
            self.notebooks[self.curr_file].insert(index, cell)
            if self.client is not None:
                self.client.create_cell(index)
        self.render()

    def create_cell_frame(self, after=None, initial_text='', depth=0):
        # Create the subframe to hold the cell widgets
        cell = tk.Frame(self.root)

        # Button to remove the cell
        remove = tk.Button(cell, text="X", command=lambda: self.remove_cell(cell), width=10, height=5)
        remove.grid(row=6*depth+1, column=7)
        
        # Text editor widget
        text = tk.Text(cell, wrap="char", highlightbackground="gray")
        text.grid(row=6*depth+1, column=2, columnspan = 5, rowspan = 5)
        text.insert("end", initial_text)
        text.bind("<KeyRelease>", self.edit_cell_callback)
        # text.pack(side="bottom")
        
        # Button to insert a new cell
        add = tk.Button(cell, text="+", command=lambda: self.add_cell(cell), width=10, height=5)
        add.grid(row=6*depth+6, column=7)
        return cell

    def edit_cell_callback(self, event):
        cell = event.widget.master
        if self.client is not None:
            # If a notebook client is attached, send the new text to the correct notebook cell
            self.client.update_cell(self.notebooks[self.curr_file].index(cell), event.widget.get("1.0", "end-1c"))

    def remove_cell(self, cell):
        if self.client is not None:
            self.client.remove_cell(self.notebooks[self.curr_file].index(cell))
        self.notebooks[self.curr_file].remove(cell)
        cell.destroy()

    # def sync(self, peer):
    #     self.client.sync(peer)
    #     self.render()

    def render(self):
        """
        Refresh the UI to reflect the current state of the notebook.
        """
        if self.client is not None:
            # Delete the current cells
            for cell in self.notebooks[self.curr_file]:
                cell.destroy()
            self.notebooks[self.curr_file] = []

            # Recreate all the cells with the client's current state
            cell_data = self.client.get_cell_data()
            index = 0
            for text in cell_data:
                cell = self.create_cell_frame(initial_text=text, depth=index)
                cell.grid(row=6*index+1, column=2, rowspan=5, columnspan=5)
                # cell.pack(side="top", fill="both", expand=True)
                self.notebooks[self.curr_file].append(cell)
                index+=1
        else:
            for cell in self.notebooks[self.curr_file]:
                cell.pack_forget()
            for cell in self.notebooks[self.curr_file]:
                cell.pack(side="top", fill="both", expand=True)

    def start(self):
        """
        Start the UI. Note that this method blocks until the UI is closed.
        """
        # self.add_cell()
        self.root.mainloop()

    


# class NotebookEditor():
#     """
#     NotebookEditor defines the UI for a simple notebook editor using tkinter. It
#     optionally takes a DistributedNotebook object as input to synchronize with.
#     """
#     def __init__(self, client=None):
#         self.root = tk.Tk()
#         self.root.title(client.name if client is not None else "Untitled Notebook")
#         self.client = client
#         self.cells = []
#         self.files = []
#         if self.client is not None:
#             # for peer in self.client.get_peers():
#                 # tk.Button(self.root, text="sync with {}".format(peer), command=lambda p=peer: self.sync(p)).pack(side="top")
#             Files = tk.Label(self.root, text="Files")
#             Add = tk.Button(self.root, text="+", command= lambda: self.add_name())
#             Refresh = tk.Button(self.root, text="Refresh")
#             Files.grid(row = 0, column = 0)
#             Add.grid(row = 0, column = 1)
#             Refresh.grid(row = 0, column = 7)
#             self.client.attach_editor(self)

#     def add_file(self, submit, file_name):
#         new_file = tk.Button(self.root, text=file_name.get())
#         submit.destroy()
#         file_name.destroy()
#         new_file.grid(column = 0)

#     def add_name(self):
#         file_name = tk.Entry(self.root, width=10, height=5)
#         submit = tk.Button(self.root, text="submit", command=lambda: self.add_file(submit, file_name))
#         file_name.grid(column = 0)
#         submit.grid(column = 1)

#     def add_cell(self, after=None):
#         cell = self.create_cell_frame()

#         # Figure out if where to insert or append the cell based on which cell the add
#         # button was clicked
#         if after in self.cells:
#             index = self.cells.index(after) + 1
#         else:
#             index = len(self.cells)

#         if index >= len(self.cells):
#             self.cells.append(cell)
#             if self.client is not None:
#                 self.client.create_cell()
#         else:
#             self.cells.insert(index, cell)
#             if self.client is not None:
#                 self.client.create_cell(index)
#         self.render()

#     def create_cell_frame(self, after=None, initial_text=''):
#         # Create the subframe to hold the cell widgets
#         cell = tk.Frame(self.root)

#         # Button to remove the cell
#         remove = tk.Button(cell, text="X", command=lambda: self.remove_cell(cell))
#         remove.grid(column=7)
        
#         # Text editor widget
#         text = tk.Text(cell, wrap="char", highlightbackground="gray")
#         text.grid(column=2, columnspan = 5, rowspan = 5)
#         text.insert("end", initial_text)
#         text.bind("<KeyRelease>", self.edit_cell_callback)
#         # text.pack(side="bottom")
        
#         # Button to insert a new cell
#         add = tk.Button(cell, text="+", command=lambda: self.add_cell(cell))
#         add.grid(column=7)
#         return cell

        

#     def edit_cell_callback(self, event):
#         cell = event.widget.master
#         if self.client is not None:
#             # If a notebook client is attached, send the new text to the correct notebook cell
#             self.client.update_cell(self.cells.index(cell), event.widget.get("1.0", "end-1c"))

#     def remove_cell(self, cell):
#         if self.client is not None:
#             self.client.remove_cell(self.cells.index(cell))
#         self.cells.remove(cell)
#         cell.destroy()

#     def sync(self, peer):
#         self.client.sync(peer)
#         self.render()

#     def render(self):
#         """
#         Refresh the UI to reflect the current state of the notebook.
#         """
#         if self.client is not None:
#             # Delete the current cells
#             for cell in self.cells:
#                 cell.destroy()
#             self.cells = []

#             # Recreate all the cells with the client's current state
#             cell_data = self.client.get_cell_data()
#             for text in cell_data:
#                 cell = self.create_cell_frame(initial_text=text)
#                 cell.grid(rowspan=5, columnspan=5)
#                 # cell.pack(side="top", fill="both", expand=True)
#                 self.cells.append(cell)
#         else:
#             for cell in self.cells:
#                 cell.pack_forget()
#             for cell in self.cells:
#                 cell.pack(side="top", fill="both", expand=True)

#     def start(self):
#         """
#         Start the UI. Note that this method blocks until the UI is closed.
#         """
#         self.add_cell()
#         self.root.mainloop()