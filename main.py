import os
import tkinter as tk
from tkinter import END, Label, Scrollbar, ttk
import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox
import sys
import sqlite3
from appdata import AppDataPaths
root = tk.Tk()
root.geometry('1130x600')
root.title('DogStar_database 0.0.3')
root.config(bg='black',cursor="hand2")

# Setting up database paths
paths = AppDataPaths('DogStar_db')
dir_path = '%s\\DogStar_db\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

file_path = '%sdata.db' % dir_path
sqlite3.connect(file_path)

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Set up background
background_image=ImageTk.PhotoImage(Image.open(resource_path("img/1bg.png")))
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.iconbitmap(resource_path('icon.ico'))

# Creating connection 
conn = sqlite3.connect(file_path)
c = conn.cursor()
# Creating customer table 
c.execute("""CREATE TABLE IF NOT EXISTS DogStar_Data (
    telefon UNIQUE,
    imie TEXT,
    nazwisko TEXT,
    rasa TEXT,
    ipsa TEXT,
    cena TEXT,
    opis TEXT
    )""")
# Creating history of customer table 
c.execute("""CREATE TABLE IF NOT EXISTS wizyty (
    telefon TEXT,
    Data TEXT,
    Godzina TEXT
    )""")
conn.commit()
conn.close()  

# Function for displaying the home page X
def home_page():
    tabs_size()

    # Function for entering customer data into the database
    def enter_data():

        # Connect to the SQLite database
        conn = sqlite3.connect(file_path)
        c = conn.cursor()

        # Select the data from the entry fields
        telefon = telefon_entry.get()
        if telefon:
            # Insert the data into the database
            c.execute("INSERT INTO DogStar_Data VALUES (:telefon, :imie, :nazwisko, :rasa, :ipsa, :cena, :opis)",
                {
                    'telefon': telefon_entry.get(),
                    'imie': imie_entry.get(),
                    'nazwisko': nazwisko_entry.get(),
                    'rasa': rasa_entry.get(),
                    'ipsa': ipsa_entry.get(),
                    'cena': pies_spinbox.get(),
                    'opis': desc_entry.get()
                })
            conn.commit()
            conn.close()
            tkinter.messagebox.showinfo(title="Gratulacje",message="Wprowadzono nowego klienta ")
        else:
            tkinter.messagebox.showwarning(title="Nie bądź leniwa",message="Wprowadź numer telefonu ")
    
        # Clear the text boxes
        imie_entry.delete(0,END)
        nazwisko_entry.delete(0,END)
        telefon_entry.delete(0,END)
        rasa_entry.delete(0,END)
        ipsa_entry.delete(0,END)
        pies_spinbox.delete(0,END)
        desc_entry.delete(0,END)

    # Create the home frame
    home_frame = tk.Frame(main_frame)
    lb = tk.Label(home_frame)

    # Create 1st section
    user_info_frame =tk.LabelFrame(main_frame, text="Dane Klienta",bg='black',fg='#FFFFFF',bd=0)
    user_info_frame.grid(row= 0, column=0,pady=(15,0))

    # Create labels and entry fields for user information information 1st section
    imie_label = tk.Label(user_info_frame , text="Imię klienta*",bg='black',fg='#FFFFFF')
    imie_label.grid(row= 2, column=0)
    imie_entry = tk.Entry(user_info_frame)
    imie_entry.grid(row= 3, column=0)
    nazwisko_label = tk.Label(user_info_frame , text="Nazwisko klienta*",bg='black',fg='#FFFFFF')
    nazwisko_label.grid(row=2, column=1)
    nazwisko_entry = tk.Entry(user_info_frame)
    nazwisko_entry.grid(row= 3, column=1)
    telefon_label = tk.Label(user_info_frame , text="Telefon",bg='black',fg='#FFFFFF')
    telefon_label.grid(row= 0, column=0)
    telefon_entry = tk.Entry(user_info_frame)
    telefon_entry.grid(row= 1, column=0)
    rasa_label = tk.Label(user_info_frame , text="Rasa psa",bg='black',fg='#FFFFFF')
    rasa_label.grid(row= 0, column=2)
    rasa_entry = tk.Entry(user_info_frame)
    rasa_entry.grid(row= 1, column=2)
    ipsa_label = tk.Label(user_info_frame , text="Imię psa",bg='black',fg='#FFFFFF')
    ipsa_label.grid(row= 0, column=1)
    ipsa_entry = tk.Entry(user_info_frame)
    ipsa_entry.grid(row= 1, column=1)

    for widget in user_info_frame.winfo_children():
        widget.grid_configure(padx=15, pady=5)

    # Create 2nd section
    opis_frame =tk.LabelFrame(main_frame, text="  Inne informacje",bg='black',fg='#FFFFFF',bd=0)
    opis_frame.grid(row= 4, column=0,sticky="news",pady=(15,0))

    # Create labels and entry fields for user information 2nd section
    pies_label = tk.Label(opis_frame ,text="Cena",bg='black',fg='#FFFFFF')
    pies_spinbox = tk.Spinbox(opis_frame, from_=0 ,to=1500,increment=10,)
    pies_label.grid(row= 4, column=0)
    pies_spinbox.grid(row=4,column=1)
    info_label = tk.Label(opis_frame ,text="* Pozycję nieobowiązkowe",bg='black',fg='#FFFFFF',font=('Bold',8))
    info_label.grid(row= 4, column=3)
    desc_label = tk.Label(opis_frame ,text="Opis",bg='black',fg='#FFFFFF')
    desc_label.grid(row= 5, column=0)
    desc_entry = tk.Entry(opis_frame)
    desc_entry.grid(row= 5, column=1) 
    for widget in opis_frame.winfo_children():
        widget.grid_configure(padx=15, pady=5)

    # Create a button to add the customer to the database
    sub = tk.Button(opis_frame,text="Dodaj klienta do bazy",command=enter_data,fg='#FFFFFF',bg='black',width=35, height=2)
    sub.grid(row=6,column=3)
    lb.pack()

# Function for displaying the wizyta page X
def dw_page():

    # Resize the tabs 
    tabs_size()

    def dict_factory(cursor, row):

        # Create a dictionary from the cursor description and row data
        return {col[0]:row[idx] for idx, col in enumerate(cursor.description)}
    
    # Connect to the database
    conn = sqlite3.connect(file_path)
    conn.row_factory = dict_factory
    c = conn.cursor()

    # Execute a SELECT
    c.execute('SELECT * FROM DogStar_Data')
    data = c.fetchall()

    c.close
    conn.close()

    # Function to get and save visit data
    def wizyta():

        # Get input data
        telefon = tel_entry.get()
        godzina = godz_entry.get()
        data = cal.get()
        if telefon:
            
            print("Telefon:", telefon, "     Godzina:", godzina)
            print("Rasa psa:",data,)
            print("------------------------------------------------")

            # Connect to the database
            conn = sqlite3.connect(file_path)

            # Insert the data into the wizyty table
            data_insert_query = '''INSERT INTO wizyty (telefon,godzina,data) VALUES
            (?,?,?)'''
            data_insert_tuple = (telefon, godzina,data)
            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()

            tkinter.messagebox.showinfo(title="Gratulacje",message="Zapisano nową wizytę ")
        else:
            tkinter.messagebox.showwarning(title="Brak wybranego numeru",message="Wybierz numer telefonu ")

    lista_frame =tk.LabelFrame(main_frame, text="Wybierz telefon klienta",bg='black',fg='#FFFFFF')
    lista_frame.pack(side='left',padx=20,pady=20)
    my_scrollbar = Scrollbar(lista_frame)
    my_scrollbar.pack(side='right',fill='y')

    
    def CurSelet(event):
        
        # Get the selected item from the listbox
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection[0])
        tel_entry.delete(0,END)
        tel_entry.insert(END,picked)
        
    listbox1=tkinter.Listbox(lista_frame,bg='black',fg='#FFFFFF')
    listbox1.pack(side='left')
    listbox1.bind('<<ListboxSelect>>',CurSelet)
    for rec in data:
        listbox1.insert(END, rec["telefon"])

    data_frame =tk.LabelFrame(main_frame, text="",bg='black',fg='#FFFFFF',padx=15,bd=0)
    data_frame.pack(side='right')

    tel_label = tk.Label(data_frame , text="Telefon",bg='black',fg='#FFFFFF')
    tel_label.grid(row= 0, column=0)
    tel_entry = tk.Entry(data_frame,width=12)
    tel_entry.grid(row= 1, column=0)
    tel_entry.insert(END, "")
    
    godzina_label = tk.Label(data_frame , text="Godzina",bg='black',fg='#FFFFFF')
    godzina_label.grid(row= 0, column=1)
    godz_entry = tk.Entry(data_frame,width=12)
    godz_entry.grid(row= 1, column=1)
    
    cal = tk.Entry(data_frame,width=10)
    cal.grid(row=1, column=2)
    cal1_label = tkinter.Label(data_frame , text="Data",bg='black',fg='#FFFFFF')
    cal1_label.grid(row= 0, column=2)


    sub = tk.Button(data_frame,text="Dodaj wizytę",fg='#FFFFFF',bg='black',width=15, height=1,command=wizyta)
    sub.grid(row=2,column=2)
    for widget in data_frame.winfo_children():
            widget.grid_configure(padx=1, pady=5)

# Function to displaying the customer list page X
def lk_page():
    table_size()
    lk_frame = tk.Frame(main_frame,bg='black')
    
    # Function to display visit history of a customer
    def historian_wizyt():
        editorr = tk.Tk()
        editorr.geometry('450x450')
        editorr.title('Historia wizyt')
        editorr.config(bg='black',cursor="hand2")
        editorr.iconbitmap(resource_path('icon.ico'))
        conn = sqlite3.connect(file_path)
        c = conn.cursor()
        record_id = id_entry.get()
        c.execute("SELECT * FROM DogStar_Data WHERE oid = " + record_id)
        records = c.fetchall()
        user_info_frame =tk.LabelFrame(editorr, text="Dane Klienta",bg='black',fg='#FFFFFF',pady=50,padx=20, font=('Bold',12))
        user_info_frame.pack()
        telefon_entry1 = tk.Entry(user_info_frame)

        for record in records:
            telefon_entry1.insert(0,record[0])  
        conn.commit()
        conn.close()
        
        # Function to display the visit records in a Treeview
        def show_rec():
            con2 = sqlite3.connect(file_path)

            cur2 = con2.cursor()

            cur2.execute("SELECT *,oid FROM wizyty WHERE telefon = ?", (telefon_entry1.get(),))

            rows = cur2.fetchall()    

            for row in rows:
                trev.insert("", tk.END, values=row)        

            con2.close()

        # Function to refresh and delete a visit record
        def refresh_del():
            tkinter.messagebox.showinfo(title="Gratulacje",message="Usunięto wizytę z listy")
            editorr.destroy()

        # Function to delete a visit record
        def visit_del():
            conn = sqlite3.connect(file_path)
            c = conn.cursor()
            c.execute("DELETE FROM wizyty WHERE oid = " + visit_id.get())
            conn.commit()
            conn.close()
            refresh_del()

        # Function to handle the click event on the Treeview
        def ClickTree(a):
            curItemm = trev.focus()
            detailss = trev.item(curItemm)
            idd = detailss.get("values")[3]
            visit_id.insert(END, idd)

        trev = ttk.Treeview(user_info_frame, column=("c1", "c2","c3"), show='headings')
        trev.bind('<ButtonRelease-1>',ClickTree)  
        trev.column("#1", anchor=tk.CENTER,width=100)
        trev.heading("#1", text="Telefon")
        trev.column("#2", anchor=tk.CENTER,width=100)
        trev.heading("#2", text="Data")
        trev.column("#3", anchor=tk.CENTER,width=100)
        trev.heading("#3", text="Godzina")
        trev.grid(row= 1, column=0,pady=25)
        inf = tk.Button(user_info_frame,text="Usuń wizytę",fg='#FFFFFF',bg='black',width=15, height=2,command=visit_del)
        inf.grid(row=2,column=0)

        visit_id = ttk.Entry(user_info_frame)
        show_rec()
        delete_pages()
        lk_page()
        
        editorr.mainloop()

    
    # Function handling the editing of customer profile
    def edit():
        if id_entry.get():
            editt()
        else:
            tkinter.messagebox.showwarning(title="Nie określono profilu klienta",message="Wybierz profil klienta do edycji ") 

    # Function opening the customer editing window        
    def editt():

        # Create a new window 
        editor = tk.Tk()
        editor.geometry('475x510')
        editor.title('Edytcja klienta')
        editor.config(bg='black',cursor="hand2")
        editor.iconbitmap(resource_path('icon.ico'))

        
        def sub_change(): 

            # Connect to the database
            conn = sqlite3.connect(file_path)
            c = conn.cursor()

            # Update the customer data
            c.execute("INSERT OR REPLACE INTO DogStar_Data VALUES (:telefon, :imie, :nazwisko, :rasa, :ipsa, :cena, :opis)",
            {
            'telefon': telefon_entry1.get(),
            'imie': imie_entryeditor.get(),
            'nazwisko': nazwisko1_entry.get(),
            'rasa': rasa1_entry.get(),
            'ipsa': ipsa1_entry.get(),
            'cena': pies1_entry.get(),
            'opis': desc1_entry.get()
            })
            conn.commit()
            conn.close()

            tkinter.messagebox.showinfo(title="Gratulacje",message="Zaktualizowano dane ")

            # Clear the pages and display the lk_page
            delete_pages()
            lk_page()

            # Close the editor window
            editor.destroy()
    
        conn = sqlite3.connect(file_path)
        c = conn.cursor()
        
        record_id = id_entry.get()

        # Select the customer data
        c.execute("SELECT * FROM DogStar_Data WHERE oid = " + record_id)
        records = c.fetchall()
        
        # Create a label frame for user information
        user_info_frame =tk.LabelFrame(editor, text="Dane Klienta",bg='black',fg='#FFFFFF',pady=50,padx=100, font=('Bold',12))
        user_info_frame.grid(row= 0, column=0)
        
        # Create labels and entry fields
        telefon_label = tk.Label(user_info_frame ,anchor='center', text="Telefon",bg='black',fg='#FFFFFF',pady=13,padx=13, font=('Bold',12))
        telefon_label.grid(row= 1, column=0)
        telefon_entry1 = tk.Entry(user_info_frame)
        telefon_entry1.grid(row= 1, column=1)


        imie_labeleditor = tk.Label(user_info_frame , text="Imię klienta",anchor='center',bg='black',fg='#FFFFFF',pady=13,padx=13, font=('Bold',12))
        imie_labeleditor.grid(row= 2, column=0)
        imie_entryeditor = tk.Entry(user_info_frame)
        imie_entryeditor.grid(row= 2, column=1)
        

        nazwisko_label = tk.Label(user_info_frame , text="Nazwisko klienta",anchor='center',bg='black',fg='#FFFFFF',pady=13,padx=13, font=('Bold',12))
        nazwisko_label.grid(row=3, column=0)
        nazwisko1_entry = tk.Entry(user_info_frame)
        nazwisko1_entry.grid(row= 3, column=1)


        rasa_label = tk.Label(user_info_frame , text="Rasa psa",bg='black',anchor='center',fg='#FFFFFF',pady=13,padx=13, font=('Bold',12))
        rasa_label.grid(row= 4, column=0)
        rasa1_entry = tk.Entry(user_info_frame)
        rasa1_entry.grid(row= 4, column=1)

        ipsa_label = tk.Label(user_info_frame , text="Imię psa",bg='black',anchor='center',fg='#FFFFFF',pady=13,padx=13, font=('Bold',12))
        ipsa_label.grid(row= 5, column=0)
        ipsa1_entry = tk.Entry(user_info_frame)
        ipsa1_entry.grid(row= 5, column=1)

        pies_label = tk.Label(user_info_frame ,text="Cena",bg='black',anchor='center',fg='#FFFFFF',pady=13,padx=13, font=('Bold',12))
        pies_label.grid(row= 6, column=0)
        pies1_entry = tk.Entry(user_info_frame)
        pies1_entry.grid(row=6,column=1)

        desc_label = tk.Label(user_info_frame ,text="Opis*",bg='black',anchor='center',fg='#FFFFFF',pady=13, padx=13,font=('Bold',12))
        desc_label.grid(row= 7, column=0)
        desc1_entry = tk.Entry(user_info_frame)
        desc1_entry.grid(row= 7, column=1) 

        # Insert the fetched data into the entry fields
        for record in records:
            telefon_entry1.insert(0,record[0])
            imie_entryeditor.insert(0,record[1])
            nazwisko1_entry.insert(0,record[2])
            rasa1_entry.insert(0,record[3])
            ipsa1_entry.insert(0,record[4])
            pies1_entry.insert(0,record[5])
            desc1_entry.insert(0,record[6])    
        conn.commit()
        conn.close()      
        
        sub = tk.Button(user_info_frame,text="Aktualizuj dane",fg='#FFFFFF',bg='black',width=15, height=2,command=sub_change)
        sub.grid(row=9,column=0)
        quio = tk.Button(user_info_frame,text="Anuluj",fg='#FFFFFF',bg='black',width=15, height=2,command=editor.destroy)
        quio.grid(row=9,column=1)
        telefon_entry1.configure(state=tk.DISABLED) 
        editor.mainloop()  
    def delete_data():

        # Check if the id_entry is not empty
        if id_entry.get():
            deletean_data()
        else:
            tkinter.messagebox.showwarning(title="Nie określono profilu klienta",message="Wybierz profil klienta do usunięcia ") 

    def historia_wizyt():

        # Check if the id_entry is not empty
        if id_entry.get():
            historian_wizyt()
        else:
            tkinter.messagebox.showwarning(title="Nie określono profilu klienta",message="Wybierz profil klienta w celu uzyskania historii wizyt ")

    def deletean_data():
        
        # Connect to the database
        conn = sqlite3.connect(file_path)
        c = conn.cursor()

        # Delete the customer
        c.execute("DELETE FROM DogStar_Data WHERE oid = " + id_entry.get())
        tkinter.messagebox.showinfo(title="Gratulacje",message="Usunięto klienta z listy")
        conn.commit()
        conn.close()

        # Clear the pages and display the lk_page
        delete_pages()
        lk_page()
    def View():

        # Connect to the database
        con2 = sqlite3.connect(file_path)
        cur2 = con2.cursor()

        # Select rows
        cur2.execute("SELECT *, oid FROM DogStar_data")
        rows = cur2.fetchall()    

        for row in rows:
            tree.insert("", tk.END, values=row)        
        con2.close()

    def CurSelect(a):

        # Get the currently selected item in the treeview
        curItem = tree.focus()

        # Get the details of the selected item
        details = tree.item(curItem)
        telefon0_item = details.get("values")[7]
        id_entry.delete(0,END)

        # Insert the value of telefon0_item into id_entry
        id_entry.insert(END, telefon0_item)
        telefon1_item = details.get("values"[1])
        telefon_entry.insert(END, telefon1_item)

    telefon_entry = tk.Entry(lk_frame)
    id_entry = tk.Entry(lk_frame,width=12)

    # Insert the value of telefon0_item into id_entry
    global tree
    tree = ttk.Treeview(main_frame, column=("c0","c1", "c2", "c3","c4","c5","c6","c7"), show='headings')

    # Configure the style of the treeview
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
        background="black",
        foreground="white",
        fieldbackground="black",
        rowheight=25,
    )
    style.map('Treeview',
        background=[('selected','#858585')]
    )

    # Bind the b event to the CurSelect
    tree.bind('<ButtonRelease-1>', CurSelect)

    # Configure columns and headings for the treeview
    tree.column("#1", anchor=tk.CENTER, width=150)
    tree.heading("#1", text="Telefon")

    tree.column("#2", anchor=tk.CENTER, width=150)
    tree.heading("#2", text="Imię klienta")

    tree.column("#3", anchor=tk.CENTER, width=150)
    tree.heading("#3", text="Naziwko klienta")

    tree.column("#4", anchor=tk.CENTER, width=150)
    tree.heading("#4", text="Rasa psa")

    tree.column("#5", anchor=tk.CENTER, width=150)
    tree.heading("#5", text="Imię psa")

    tree.column("#6", anchor=tk.CENTER, width=100)
    tree.heading("#6", text="Cena")

    tree.column("#7", anchor=tk.CENTER, width=250)
    tree.heading("#7", text="Opis")

    tree.column("#8", anchor=tk.CENTER, width=30)
    tree.heading("#8", text="ID")

    tree.pack()
    View()

    # Create a search entry widget
    search = tk.Entry(lk_frame)
    search.grid(row=0, column=4)

    # Create a function to perform dynamic search
    def perform_dynamic_search(event=None):
        lookup_record = search.get()
        # Remove rows displayed in treeview
        tree.delete(*tree.get_children())

        con2 = sqlite3.connect(file_path)
        cur2 = con2.cursor()

        if lookup_record:
            # Perform a dynamic search based on the lookup record
            cur2.execute("SELECT *, oid FROM DogStar_data WHERE telefon LIKE ?", ('%' + lookup_record + '%',))
        else:
            # Fetch all records if the lookup record is empty
            cur2.execute("SELECT *, oid FROM DogStar_data")

        rows = cur2.fetchall()

        if not rows:
            # If no matching records found, insert a special row with the message
            tree.insert("", tk.END, values=("", "", "", "Nie ma takiego klienta", "", "", "", ""))

        for row in rows:
            tree.insert("", tk.END, values=row)

        con2.close()

    # Bind the perform_dynamic_search function to the KeyRelease event on the search entry
    search.bind("<KeyRelease>", perform_dynamic_search)

    # Call the perform_dynamic_search function initially to display all records
    perform_dynamic_search()

    # Create an edit button
    sub = tk.Button(lk_frame, text="Edytuj", fg='#FFFFFF', bg='black', width=25, height=2, command=edit)
    sub.grid(row=0, column=0)

    # Create a delete button
    delete = tk.Button(lk_frame, text="Usuń", fg='#FFFFFF', bg='black', width=25, height=2, command=delete_data)
    delete.grid(row=0, column=2, padx=(0, 200))

    # Create a show button
    wizyty = tk.Button(lk_frame, text="Pokaż historie wizyt", fg='#FFFFFF', bg='black', width=25, height=2, command=historia_wizyt)
    wizyty.grid(row=0, column=1)

    lk_frame.pack()

# Deleting main pages 
def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy() 

# Configure hide indicators
def hide_indicators():
    home_indicate.config(bg='white')
    dw_indicate.config(bg='white')
    lk_indicate.config(bg='white')

# Changing indicators color
def indicate(lb, page):
    hide_indicators()
    lb.config(bg='#64afcc')
    delete_pages()
    page()

def mainscreen():
    pass


options_frame = tk.Frame(root,bg='black')

# Load image icons
my_image = ImageTk.PhotoImage(Image.open(resource_path("img/icon/icon-main.png")).resize((100,100)))
lk_image = ImageTk.PhotoImage(Image.open(resource_path("img/icon/list-icon.png")).resize((100,100)))
dw_image = ImageTk.PhotoImage(Image.open(resource_path("img/icon/visit-icon.png")).resize((100,100)))
home_image = ImageTk.PhotoImage(Image.open(resource_path("img/icon/add-icon.png")).resize((100,100)))
quit_image = ImageTk.PhotoImage(Image.open(resource_path("img/icon/quit-icon.png")).resize((100,100)))

# Create buttons
img = tk.Button(options_frame,image = my_image,bd=0,command=mainscreen, activebackground='black',bg='black')
img.pack()
img.grid(row=0,column=0,padx=(0,120))

home_btn = tk.Button(options_frame, image=home_image, font=('Bold',15),activebackground='black',bd=0,command=lambda: indicate(home_indicate,home_page),bg='black')
home_btn.grid(row=0,column=1)

home_indicate = tk.Label(options_frame ,text='',bg='white')
home_indicate.grid(row=1,column=1)

dw_btn = tk.Button(options_frame, image=dw_image, font=('Bold',15),bd=0,activebackground='black',command=lambda: indicate(dw_indicate, dw_page),bg='black')
dw_btn.grid(row=0,column=2)

dw_indicate = tk.Label(options_frame ,text='',bg='white',height=1)
dw_indicate.grid(row=1,column=2)

lk_btn = tk.Button(options_frame, image=lk_image, font=('Bold',15),activebackground='black',bd=0,command=lambda: indicate(lk_indicate, lk_page),bg='black')
lk_btn.grid(row=0,column=3)

lk_indicate = tk.Label(options_frame ,text='',bg='white')
lk_indicate.grid(row=1,column=3)
def wyjscie():
    sys.exit()

qu_btn = tk.Button(options_frame,image=quit_image, font=('Bold',15),bd=0,command=wyjscie,bg='black',activebackground='black')
qu_btn.grid(row=0,column=4,padx=(100,0))

options_frame.grid(row=0,column=0,padx=200,pady=10)
options_frame.configure(width=1600, height=500)

main_frame = tk.Frame(background_label,bg='black')
main_frame.place(x=550,y=200,width=500,height=300)

def table_size():
    main_frame.place(x=10,y=200,width=1100,height=315)
def tabs_size():
    main_frame.place(x=550,y=200,width=500,height=290)

sec_frame = tk.Frame(main_frame,bg='black')
sec_frame.place(x=0,y=0,width=500,height=300)

user_info_frame =tk.LabelFrame(sec_frame,bg='black',fg='#FFFFFF',bd=0)
user_info_frame.pack() 
user_info_frame.configure(width=500,height=300)

my_image1 = ImageTk.PhotoImage(Image.open(resource_path("img/dgb.png")).resize((500,90)))
img1 = Label(user_info_frame,image = my_image1,bd=0)
img1.pack()
img1.configure()

imie_label = tk.Label(user_info_frame , text="""  
Funkcje programu:
-Dodawanie klientów do bazy
-Dodawnie wizyt klientom 
-Edycja profilu klienta
-Możliwośc usunięcia profilu klienta
-Historia wizyt klienta
""",bg='black',fg='#FFFFFF')
imie_label.pack()

Frame = tk.Frame(root,bg='black')
Frame.grid()
#Last update 12/12/2022 12:59AM
root.mainloop()