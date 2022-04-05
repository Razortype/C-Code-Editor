from tkinter import Checkbutton, OptionMenu, Tk ,Toplevel
from tkinter import Canvas, Frame, Menu
from tkinter import Label, Text, Entry, Button, messagebox, Listbox
from tkinter import END, TOP, RIGHT, LEFT, N, W, S, BOTH, VERTICAL, Y, E, NO
from tkinter import StringVar, INSERT, IntVar
from tkinter.ttk import Treeview
from tkinter import filedialog
from tkinter.constants import ANCHOR, CENTER
import threading, time
import GUI.constants as c
import GUI.functions as f

class EditPage(Toplevel):
    def __init__(self,parent, folder_name, file_name, file_path):
        super().__init__(parent)

        self.folder_name = folder_name
        self.file_name = file_name
        self.file_path = file_path
        self.init_source_data = ""
        self.last_source_data = ""
        self.protocol("WM_DELETE_WINDOW", self.quit_text)

        self.title(f'Editing: "{self.folder_name.upper()}" => "{self.file_name}"')
        self.iconbitmap(c.EDITPAGE_ICON_PATH)
        self.resizable(width=False, height=False)

        self.main_canvas = Canvas(self, height=450, width=750, bg=c.EDIT_CANVAS_BG)
        self.main_canvas.pack()

        # file menu
        self.top_menu = Menu(self)
        self.config(menu=self.top_menu)

        self.file_menu = Menu(self.top_menu, tearoff=False)
        self.top_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_text, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Exit",command=self.quit_text, accelerator="Ctrl+Q")

        self.tools_menu = Menu(self.top_menu, tearoff=False)
        self.top_menu.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Undo",command=self.undo_text,accelerator="Ctrl+Z")
        self.tools_menu.add_command(label="Redo",command=self.redo_text,accelerator="Ctrl+Y")
        self.tools_menu.add_separator()
        self.tools_menu.add_command(label="Copy",command=self.copy_text,accelerator="Ctrl+C")
        self.tools_menu.add_command(label="Paste", accelerator="Ctrl+V")
        self.tools_menu.add_command(label="Reset",command=self.reset_text, accelerator="F5")

        self.text_frame = Frame(self.main_canvas, bg=c.TEXT_FRAME_BG)
        self.text_frame.place(relx=0.01,rely=0.02, relwidth=0.98,relheight=0.96)

        # text frame
        self.code_source = Text(self.text_frame, bg=c.LABEL_BG, fg=c.LABEL_FG, undo=True)
        self.code_source.pack(expand=True, fill='both')
        self.code_source.focus()

        self.init_text()

        self.code_source.bind('<Control-z>', self.undo_text)
        self.code_source.bind('<Control-y>', self.redo_text)
        self.code_source.bind('<Control-s>', self.save_text)
        self.code_source.bind('<Control-q>', self.quit_text)
        self.code_source.bind('<Control-c>', self.copy_text)
        self.code_source.bind('<F5>', self.reset_text)
        self.code_source.bind('<Tab>', self.tab_pressed)

    def init_text(self):
        with open(self.file_path,"r") as source:
            data = source.read()

        self.init_source_data = data.rstrip()
        self.code_source.insert(END, data)

    def save_text(self, event=None):
        source = self.code_source.get('1.0', END).rstrip()
        if not (self.init_source_data.rstrip() == source or self.last_source_data.rstrip() == source):
            answer = messagebox.askyesno("Save Code", "Do you want to save unsaved data?")
            if answer:
                self.last_source_data = source
                f.save_source_code(self.file_path,source)

    def quit_text(self, event=None):
        source = self.code_source.get('1.0', END).rstrip()
        if not (self.init_source_data.rstrip() == source or self.last_source_data.rstrip() == source):
            answer = messagebox.askyesno("Safe Quit", "Unsaved data has been found!\n\nDo you want to save before exit?", icon="warning")
            if answer:
                self.last_source_data = source
                f.save_source_code(self.file_path,source)
        self.destroy()

    def copy_text(self, event=None):
        text = self.code_source.selection_get()
        f.copy_text(text)

    def reset_text(self, event=None):
        self.code_source.delete('1.0', END)
        self.code_source.insert(END, self.init_source_data)

    def undo_text(self, event=None):
        self.code_source.edit_undo()

    def redo_text(self, event=None):
        self.code_source.edit_redo()

    def tab_pressed(self, event=None):
        self.code_source.insert("insert", " "*4)
        return "break"

class SettingPage(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.title("Settings")
        self.iconbitmap(c.SETTING_ICON_PATH)
        self.resizable(width=False, height=False)

        self.main_canvas = Canvas(self, height=450, width=750, bg=c.SETTING_CANVAS_BG)
        self.main_canvas.pack()

        self.ifl_canvas = Canvas(self.main_canvas, height=100, width=600, bg=c.SETTING_CANVAS_ROWS_BG)
        self.ifl_canvas.pack()
        
        self.ar_table_canvas = Canvas(self.main_canvas, height=100, width=600, bg=c.SETTING_CANVAS_ROWS_BG)
        self.ar_table_canvas.pack(pady=20)

        self.log_prop_canvas = Canvas(self.main_canvas, height=100, width=600, bg=c.SETTING_CANVAS_ROWS_BG)
        self.log_prop_canvas.pack()

        # Initial Directory Canvas

        self.path_values_canvas = Canvas(self.ifl_canvas, bg=c.SETTING_CANVAS_ROWS_BG,width=600,height=200)
        self.path_values_canvas.pack()

        self.current_path = Label(self.path_values_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, font=c.PARAG_FONT, text=f.get_init_path(), width=80)
        self.path_input = Text(self.path_values_canvas, height=1, width=80, bg=c.LABEL_BG, fg=c.LABEL_FG)
        
        Label(self.path_values_canvas, bg=c.LABEL_BG, fg=c.LABEL_FG, font=c.PARAG_FONT, text="Current Location:").grid(row=0,column=0)
        self.current_path.grid(row=0,column=1)
        Label(self.path_values_canvas, bg=c.LABEL_BG, fg=c.LABEL_FG, font=c.PARAG_FONT, text="New Location:").grid(row=1,column=0)
        self.path_input.grid(row=1,column=1)

        self.ifl_button_canvas = Canvas(self.ifl_canvas, bg=c.SETTING_CANVAS_ROWS_BG, width=400, height=25)
        
        self.ifl_button_canvas.pack()

        self.select_from_button = Button(self.ifl_button_canvas, font=c.PARAG_FONT, text="Select From", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=10, command=self.get_folder)
        self.save_input_button = Button(self.ifl_button_canvas, font=c.PARAG_FONT, text="Save Input", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=10, command=self.save_path_input)

        self.select_from_button.grid(row=0, column=0, padx=5, pady=10)
        self.save_input_button.grid(row=0, column=1, padx=5, pady=10)

        # Add/Remove Table Canvas

        self.left_title = Label(self.ar_table_canvas, bg=c.LABEL_BG, fg=c.LABEL_FG, font=c.PARAG_FONT, text="Properties")
        self.right_title = Label(self.ar_table_canvas, bg=c.LABEL_BG, fg=c.LABEL_FG, font=c.PARAG_FONT, text="Refills")

        self.left_listbox = Listbox(self.ar_table_canvas,bg=c.LABEL_BG,fg=c.LABEL_FG)
        self.right_listbox = Listbox(self.ar_table_canvas,bg=c.LABEL_BG,fg=c.LABEL_FG)

        self.left_button = Button(self.ar_table_canvas,bg=c.BUTTON_BG,fg=c.BUTTON_FG, text="remove", command=self.remove_prop)
        self.right_button = Button(self.ar_table_canvas,bg=c.BUTTON_BG,fg=c.BUTTON_FG, text="add", command=self.add_prop)

        self.left_title.grid(row=0,column=0, padx=20)
        self.right_title.grid(row=0,column=1,pady=5, padx=20)
        self.left_listbox.grid(row=1,column=0, padx=20)
        self.right_listbox.grid(row=1,column=1,pady=5, padx=20)
        self.left_button.grid(row=2,column=0, padx=20)
        self.right_button.grid(row=2,column=1,pady=5, padx=20)

        # Log canvas

        self.log_switch_canvas = Canvas(self.log_prop_canvas, bg=c.SETTING_CANVAS_ROWS_BG)
        self.log_switch_canvas.pack()
        Label(self.log_switch_canvas,bg=c.LABEL_BG,fg=c.LABEL_FG,font=c.PARAG_FONT,text="Save logs:").grid(row=0,column=0)
        self.log_bool_val = Label(self.log_switch_canvas,bg=c.LABEL_BG,fg=c.LABEL_FG,font=c.PARAG_FONT,text="")
        self.switch_log_button = Button(self.log_switch_canvas,bg=c.BUTTON_BG,fg=c.BUTTON_FG,font=c.PARAG_FONT,text="Flip",command=self.flip_log_val)

        self.log_bool_val.grid(row=0,column=1,padx=10,pady=5)
        self.switch_log_button.grid(row=0,column=2,padx=50,pady=5)

        self.log_values_canvas = Canvas(self.log_prop_canvas, bg=c.SETTING_CANVAS_ROWS_BG,width=600,height=200)
        self.log_values_canvas.pack(pady=10)

        self.current_log_path = Label(self.log_values_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, font=c.PARAG_FONT, text=f.get_log_path(), width=40)
        self.log_path_input = Text(self.log_values_canvas, height=1, width=40, bg=c.LABEL_BG, fg=c.LABEL_FG)
        
        Label(self.log_values_canvas, bg=c.LABEL_BG, fg=c.LABEL_FG, font=c.PARAG_FONT, text="Log Path:").grid(row=0,column=0)
        self.current_log_path.grid(row=0,column=1)
        Label(self.log_values_canvas, bg=c.LABEL_BG, fg=c.LABEL_FG, font=c.PARAG_FONT, text="New:").grid(row=1,column=0)
        self.log_path_input.grid(row=1,column=1,pady=5)

        self.log_button_canvas = Canvas(self.log_prop_canvas, bg=c.SETTING_CANVAS_ROWS_BG, width=400, height=25)
        
        self.log_button_canvas.pack()

        self.select_log_from_button = Button(self.log_button_canvas, font=c.PARAG_FONT, text="Select From", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=10, command=self.get_log_folder)
        self.save_log_input_button = Button(self.log_button_canvas, font=c.PARAG_FONT, text="Save Input", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=10, command=self.save_log_path_input)

        self.select_log_from_button.grid(row=0, column=0, padx=5, pady=10)
        self.save_log_input_button.grid(row=0, column=1, padx=5, pady=10)

        ####

        self.save_data_button = Button(self.main_canvas,bg=c.BUTTON_BG,fg=c.BUTTON_FG,text="SAVE DATA", command=self.save_data)
        self.save_data_button.pack(pady=10)

        self.insert_initial_values()

    def get_folder(self):
        currentpath = f.get_init_path()
        folder_path = filedialog.askdirectory(initialdir=currentpath)
        self.current_path.configure(text=folder_path)
        self.path_input.delete('1.0',END)
        self.path_input.insert('1.0',folder_path)

    def save_path_input(self):
        given_path = self.path_input.get("1.0",END)[:-1]
        print(given_path)
        if f.check_exists(given_path):
            self.current_path.config(text=given_path)
        else:
            messagebox.showerror("Path ERROR!",f"There is no path such: {given_path}")
    
    def remove_prop(self):
        selected_item = self.left_listbox.curselection()
        if len(selected_item) != 0:
            data = self.left_listbox.get(selected_item)
            self.left_listbox.delete(selected_item)
            self.right_listbox.insert(END,data)
        else:
            messagebox.showerror("Item ERROR","There is no selected item.")

    def add_prop(self):
        selected_item = self.right_listbox.curselection()
        if len(selected_item) != 0:
            data = self.right_listbox.get(selected_item)
            self.right_listbox.delete(selected_item)
            self.left_listbox.insert(END,data)
        else:
            messagebox.showerror("Item ERROR","There is no selected item.")

    def get_log_folder(self):
        currentpath = f.get_log_path()
        folder_path = filedialog.askdirectory(initialdir=currentpath)
        self.current_log_path.configure(text=folder_path)
        self.log_path_input.delete('1.0',END)
        self.log_path_input.insert('1.0',folder_path)
    
    def save_log_path_input(self):
        given_path = self.log_path_input.get("1.0",END)[:-1]
        print(given_path)
        if f.check_exists(given_path):
            self.current_log_path.config(text=given_path)
    
    def flip_log_val(self):
        val = self.log_bool_val.cget("text")
        if val == "False":
            self.log_bool_val.config(text="True")
            self.log_path_input.config(state="normal")
            self.select_log_from_button.config(state="normal")
            self.save_log_input_button.config(state="normal")
        else:
            self.log_path_input.config(state="disabled")
            self.select_log_from_button.config(state="disabled")
            self.save_log_input_button.config(state="disabled")
            self.log_bool_val.config(text="False")

    def insert_initial_values(self):
        init_path = f.get_data("IP")
        props = f.get_data("PI")
        refills = f.get_data("RI")
        logval = f.get_data("LV")
        log_val = "False" if len(logval)==0 else logval
        logpath = f.get_data("LP")
        log_path = "PATH TO LOG" if len(logpath)==0 else logpath

        self.current_path.config(text=init_path)
        self.path_input.insert("1.0",init_path)

        for prop in props:
            if prop:
                self.left_listbox.insert(END, prop)

        for refill in refills:
            if refill:
                self.right_listbox.insert(END, refill)

        self.log_bool_val.config(text=log_val)
        self.current_log_path.config(text=log_path)
        self.log_path_input.insert("1.0",log_path)

        if log_val=="False":
            self.log_path_input.config(state="disabled")
            self.select_log_from_button.config(state="disabled")
            self.save_log_input_button.config(state="disabled")

    def save_data(self):
        init_path = self.current_path.cget("text")
        prop_items = list(self.left_listbox.get(0,END))
        refill_items = list(self.right_listbox.get(0,END))
        log_val = self.log_bool_val.cget("text")
        log_path = self.current_log_path.cget("text")

        if f.check_exists(init_path) and f.check_exists(log_path):
            f.save_data(init_path,prop_items,refill_items,log_val,log_path)
            messagebox.showinfo("Succes","Settings succesfully saved to application.")
        else:
            messagebox.showerror("Directory Error", "Initial and log file directory must be declared.")

class App(Tk):
    def __init__(self):
        super().__init__()
        self.choosed_directory = None
        self.bind('<Control-f>', self.fetch_data)
        self.bind('<F5>', self.refresh_window)
        
        self.resizable(width=c.RESIZE_X, height=c.RESIZE_Y)
        self.title(c.APP_TITLE)
        self.iconbitmap(c.MAIN_ICON_PATH)

        # MAIN CANVAS
        self.main_canvas = Canvas(self, height=550, width=900, bg=c.MAIN_CANVAS_BG)
        self.main_canvas.pack()

        # Frames
        self.frame_folder = Frame(self, bg=c.F_FOLDER_BG)
        self.frame_folder.place(relx=0, rely=0, relwidth=0.77, relheight=0.25)

        self.frame_table = Frame(self, bg=c.F_TABLE_BG)
        self.frame_table.place(relx=0, rely=0.25, relwidth=0.77, relheight=0.75)

        self.frame_detail = Frame(self, bg=c.F_DETAIL_BG)
        self.frame_detail.place(relx=0.77, rely=0, relwidth=0.23, relheight=1)

        # FOLDER FRAME
        Label(self.frame_folder, fg=c.LABEL_FG, bg=c.LABEL_BG, text=c.MAIN_TITLE, font=c.TITLE_FONT).pack(pady=7)

        self.folder_canvas = Canvas(self.frame_folder, height=100, width=200, bg=c.FOLDER_CANVAS_BG)
        self.folder_canvas.pack()
        
        self.path_label = Label(self.folder_canvas, width=60, fg=c.LABEL_FG, bg=c.LABEL_BG, text=c.INITIAL_FOLDER_PATH, font=c.PARAG_FONT)
        
        self.button_canvas = Canvas(self.folder_canvas, width=20, height=20, bg=c.FOLDER_BUTTON_CANVAS_BG)

        self.folder_button = Button(self.button_canvas, font=c.PARAG_FONT, text="Select", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=6, command=self.choose_folder)
        self.fetch_button = Button(self.button_canvas, font=c.PARAG_FONT, text="Fetch", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=6, command=self.fetch_data)

        self.path_label.grid(row=0, column=0, pady=10, padx=17)
        self.button_canvas.grid(row=0, column=1, pady=10, padx=17)
        self.folder_button.pack()
        self.fetch_button.pack()

        # DETAIL FRAME
        Label(self.frame_detail, fg=c.LABEL_FG, bg=c.LABEL_BG, text="PROPERTIES", font=c.TITLE_2_FONT).pack(pady=20)

        # details items -----------------
        self.detail_canvas = Canvas(self.frame_detail, bg=c.DETAIL_CANVAS_BG)
        self.detail_canvas.pack()
        self.init_props()

        self.start_canvas = Frame(self.frame_detail, bg=c.START_FRAME_BG)
        self.start_canvas.place(relx=0.03,rely=0.83,relwidth=0.95,relheight=0.16)

        self.selections = ["RUN","COMPILE","BOTH", "EDIT"]
        self.var = StringVar()
        self.bind('<Key>', self.change_option)
        self.bind('<Control-r>', self.start_code)

        self.selection_box = OptionMenu(self.start_canvas,self.var,*self.selections)
        self.var.set("RUN")
        self.start_button = Button(self.start_canvas, font=c.PARAG_FONT, text="START", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=6, command=self.start_code)
        self.setting_page_button = Button(self.start_canvas, font=c.PARAG_FONT, text="Settings", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=6, command=self.open_setting_page)
        self.compile_all_button = Button(self.start_canvas, font=c.PARAG_FONT, text="All", fg=c.BUTTON_FG, bg=c.BUTTON_BG, height=1, width=6, command=self.compile_all)
        
        self.selection_box.grid(row=1,column=1, padx=10, pady=5)
        self.start_button.grid(row=1,column=2, padx=10, pady=5)
        self.setting_page_button.grid(row=2,column=2, padx=10, pady=5)
        self.compile_all_button.grid(row=2,column=1, padx=10, pady=5)

        # TABLE FRAME
        Label(self.frame_table, fg=c.LABEL_FG, bg=c.LABEL_BG, text="ALL SEARCHED DATA", font=c.TITLE_FONT).pack(pady=10)

        self.file_data_canvas = Canvas(self.frame_table, bg=c.TABLE_CANVAS_BG)
        self.file_data_canvas.pack()

        self.data_tree = Treeview(self.file_data_canvas)
        self.data_tree.pack(expand=True, fill='both')
        self.data_tree.bind("<Double-1>", self.import_data)
        self.data_tree.bind("<Button-3>", self.open_folder)
        self.data_tree.bind("<Return>", self.import_data)

        self.data_tree['columns'] = ("ID","Folder Name","Name","Last Edited","file_path","comp_bef","last_compiled_time")

        self.data_tree.column("#0", width=0, stretch=NO)
        self.data_tree.column("ID", anchor=CENTER, width=40)
        self.data_tree.column("Folder Name", anchor=W, width=160)
        self.data_tree.column("Name", anchor=W, width=120)
        self.data_tree.column("Last Edited", anchor=W, width=120)
        self.data_tree.column("file_path", width=0, stretch=NO)
        self.data_tree.column("comp_bef", width=0, stretch=NO)
        self.data_tree.column("last_compiled_time", width=0, stretch=NO)

        self.data_tree.heading("#0",text="Label", anchor=W)
        self.data_tree.heading("ID", text="ID", anchor=CENTER)
        self.data_tree.heading("Folder Name", text="Folder Name", anchor=W)
        self.data_tree.heading("Name", text="Name", anchor=W)
        self.data_tree.heading("Last Edited", text="Last Edited", anchor=W)
        self.data_tree.heading("file_path", text="file_path",anchor=W)
        self.data_tree.heading("comp_bef", text="comp_bef",anchor=W)
        self.data_tree.heading("last_compiled_time", text="lct",anchor=W)

        Label(self.frame_table, fg=c.INFO_LABEL_FG, bg=c.F_TABLE_BG, text="(the item must be imported with double clicking it)", font=c.INFO_FONT).pack()


        self.search_canvas = Canvas(self.frame_table, bg = c.F_TABLE_BG)
        self.search_canvas.pack(pady=30)

        self.search_text = Text(self.search_canvas, height=1, width=40, bg=c.LABEL_BG, fg=c.LABEL_FG)
        self.search_text.grid(row=0,column=0,padx=10)
        self.search_text.bind('<Return>',self.search_data)

        self.search_button = Button(self.search_canvas, text="search", fg=c.BUTTON_FG, bg=c.BUTTON_BG, font=c.PARAG_FONT, height=1, width=10, command=self.search_data)
        self.search_button.grid(row=0,column=1)

    def refresh_window(self, event=None):
        self.destroy()
        self.__init__()

    def search_data(self, event=None):
        key_word = self.search_text.get('1.0', END).lower().strip("\n")
        self.search_text.delete('1.0', END)
        tree_data = []
        for item in self.data_tree.get_children():
            given_data = self.data_tree.item(item)['values']
            data = {"id":0,"folder_name":None,"name":None,"last_edited":None,"file_path":None,"comp_bef":None,"last_compiled_time":None}

            for index,key in enumerate(data.keys()):
                data[key] = given_data[index]

            tree_data.append(data)
        
        results = [item for item in tree_data if key_word in item.get("folder_name").lower()]
        
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        for index,res in enumerate(results):
            values = (index+1,*list(res.values())[1:])
            self.data_tree.insert(parent='', index='end', iid=index, text="Parent", values=values)

    def change_option(self, event=None):
        try:
            if event.char in "1234":
                self.var.set(self.selections[int(event.char)-1])
        except Exception:
            pass

    def choose_folder(self):
        folder_path = filedialog.askdirectory(initialdir=c.INITIAL_FOLDER_PATH)
        self.path_label.configure(text=folder_path)

    def fetch_data(self, event=None):
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)

        given_dir = self.path_label.cget("text")
        files = f.search_files(given_dir)
        
        cfiles = [i for i in files if i.endswith(".c")]

        for index,file_dir in enumerate(cfiles):
            folder_name,file_name,file_modified_time,comp_before,last_compiled_time= f.get_file_data(file_dir)
            values = (index+1,folder_name,file_name,file_modified_time,file_dir,comp_before,last_compiled_time)
            self.data_tree.insert(parent='', index='end', iid=index, text="Parent", values=values)

    def open_folder(self, event=None):
        cur_item = self.data_tree.identify_row(event.y)
        if cur_item:
            self.data_tree.selection_set(cur_item)
            given_data = self.data_tree.item(cur_item)['values']
            path = given_data[4]
            f.open_folder_dir(path)

    def import_data(self, event=None):
        cur_item = self.data_tree.focus()
        if len(cur_item) != 0:
            given_data = self.data_tree.item(cur_item)['values']
            data = {"ID":0,"Folder Name":None,"Name":None,"Last Edited":None,"file_path":None,"comp_bef":None,"last_compiled_time":None}
            
            for index,key in enumerate(data.keys()):
                data[key] = given_data[index]
            
            try:
                self.d_name.config(text=data.get("Folder Name","None"))
            except Exception:
                pass
            try:
                self.d_f_name.config(text=data.get("Name","None"))
            except Exception:
                pass
            try:
                self.d_lmt.config(text=data.get("Last Edited","None"))
            except Exception:
                pass
            try:
                self.d_comp.config(text=data.get("comp_bef","None"))
            except Exception:
                pass
            try:
                self.d_lct.config(text=data.get("last_compiled_time"))
            except Exception:
                pass
            try:
                self.d_fd.config(text=data.get("file_path","None"))
            except Exception:
                pass

            self.choosed_directory = data.get("file_path",None)
        else:
            messagebox.showerror("Select ERROR", "No such value has selected!")

    def open_setting_page(self):
        setting_page = SettingPage(self)
        setting_page.grab_set()

    def start_code(self, event=None):
        file_directory = self.choosed_directory
        if file_directory:
            state = self.selection_box.cget("text")
            comp_before = self.d_comp.cget("text")
        else:
            messagebox.showwarning("File","An item must be imported from table!")
            return

        if state == "RUN":
            if comp_before != "False":
                con = f.check_run_suit(file_directory)
                if con:
                    f.run_compile_both(file_directory,state)
                else:
                    answer = messagebox.askyesno("Process Suitabilty","There is a possibility that the file does not match the exe.\n\nDo you still want to continue?")
                    if answer:
                        f.run_compile_both(file_directory,state)
            else:
                messagebox.showerror("File ERROR", "No such directory has found to run (.exe)")
        elif state == "COMPILE" or state == "BOTH":
            exception = f.run_compile_both(file_directory,state)
            if exception:
                messagebox.showerror("Runtime Error", f"An error occured\n\nERROR:\n{exception}")
            else:
                messagebox.showinfo("Compiler info", "Process completed succesfully!")
            try:
                self.d_comp.config(text="True")
            except Exception:
                pass
        elif state == "EDIT":
            self.open_edit_page()
    
    def compile_all(self):
        if self.data_tree.get_children():
            rows = []
            for item in self.data_tree.get_children():
                data = self.data_tree.item(item)['values']
                f.compile_file(data[-3])

                rows.append("     - {} ({})".format(data[-6],data[-5]))

            messagebox.showinfo("Success", "All file have been compiled succesfully!\n\n{}".format("\n".join(rows)))
        else:
            messagebox.showwarning("File","Fetch data with given directory!")
    
    def open_edit_page(self):
        folder_name = self.d_name.cget("text")
        file_name = self.d_f_name.cget("text")
        file_path = self.d_fd.cget("text")
        edit_page = EditPage(self, folder_name, file_name, file_path)
        edit_page.grab_set()

    def copy_dir_data(self, event=None):
        file_dir = self.d_fd.cget("text")
        if file_dir != "copied!":
            f.copy_text(file_dir)
            self.d_fd.config(text="copied!")
            time.sleep(1)
            self.d_fd.config(text=file_dir)

    def init_props(self):

        data = f.get_data()
        prop_items = [i.lower() for i in data.get("prop_items")]
        index = 0

        if "name" in prop_items:
            Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="NAME:").grid(row=0-index, column=0, pady=10,padx=5)
            self.d_name = Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="")
            self.d_name.grid(row=index, column=1, pady=10, padx=5)
            index += 1

        if "folder name" in prop_items:
            Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="FILE NAME:").grid(row=index, column=0, pady=10,padx=5)
            self.d_f_name = Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="")
            self.d_f_name.grid(row=index, column=1, pady=10, padx=5)
            index += 1

        if "last modified time" in prop_items:
            Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="LAST MODIFIED TIME:", wraplength=80).grid(row=index, column=0, pady=10,padx=5)
            self.d_lmt = Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="")
            self.d_lmt.grid(row=index, column=1, pady=10, padx=5)
            index += 1

        if "compiled" in prop_items:
            Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="COMPILED:").grid(row=index, column=0, pady=10,padx=5)
            self.d_comp = Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="")
            self.d_comp.grid(row=index, column=1, pady=10, padx=5)
            index += 1

        if "last compiled time" in prop_items:
            Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="LAST COMPILED TIME:", wraplength=80).grid(row=index, column=0, pady=10,padx=5)
            self.d_lct = Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="")
            self.d_lct.grid(row=index, column=1, pady=10, padx=5)
            index += 1

        if "file directory" in prop_items:
            Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="Directory:").grid(row=index, column=0, pady=10,padx=5)
            self.d_fd = Label(self.detail_canvas, fg=c.LABEL_FG, bg=c.LABEL_BG, text="", anchor=W, wraplength=100)
            self.d_fd.grid(row=index, column=1, pady=10, padx=5)
            self.d_fd.bind('<Button-1>', lambda event:threading.Thread(target=self.copy_dir_data).start())