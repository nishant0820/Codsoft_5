from tkinter import *
from tkinter import ttk,messagebox
import pymysql
from tkinter import messagebox

class Contact:
    def __init__(self,root):
        self.root=root
        self.root.title("Contact Book | Nishant Gupta")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="black")
        
        title=Label(self.root,text="Contact Book",font=("times new roman",40,"bold"),bg="#010c48",fg="white").pack(side=TOP,fill=X)
        
        #----------- Variables -------------
        self.name=StringVar()
        self.phone=StringVar()
        self.email=StringVar()
        self.search_by=StringVar()
        self.search_txt=StringVar()
        
        #-------------- Contact Frame ---------------
        Contact_Frame=Frame(self.root,bd=4,relief=RIDGE)
        Contact_Frame.place(x=20,y=100,width=450,height=560)
        
        c_title=Label(Contact_Frame,text="Manage Contacts",font=("times new roman",30,"bold"))
        c_title.grid(row=0,columnspan=2,pady=20)
        
        lbl_name=Label(Contact_Frame,text="Name",font=("times new roman",20,"bold"))
        lbl_name.grid(row=1,column=0,pady=10,padx=20,sticky="w")
        
        txt_name=Entry(Contact_Frame,textvariable=self.name,font=("times new roman",15),bd=5,relief=GROOVE)
        txt_name.grid(row=1,column=1,pady=10,padx=20,sticky="w")
        
        lbl_phone=Label(Contact_Frame,text="Phone",font=("times new roman",20,"bold"))
        lbl_phone.grid(row=2,column=0,pady=10,padx=20,sticky="w")
        
        txt_phone=Entry(Contact_Frame,textvariable=self.phone,font=("times new roman",15),bd=5,relief=GROOVE)
        txt_phone.grid(row=2,column=1,pady=10,padx=20,sticky="w")
        
        email=Label(Contact_Frame,text="Email",font=("times new roman",20,"bold"))
        email.grid(row=3,column=0,pady=10,padx=20,sticky="w")
        
        txt_email=Entry(Contact_Frame,textvariable=self.email,font=("times new roman",15),bd=5,relief=GROOVE)
        txt_email.grid(row=3,column=1,pady=10,padx=20,sticky="w")
        
        lbl_address=Label(Contact_Frame,text="Address",font=("times new roman",20,"bold"))
        lbl_address.grid(row=4,column=0,pady=10,padx=20,sticky="w")
        
        self.txt_address=Text(Contact_Frame,width=30,height=10,font=("",10))
        self.txt_address.grid(row=4,column=1,pady=10,padx=20,sticky="w")
        
        #------------- Button Frame -------------------
        Btn_Frame=Frame(Contact_Frame,bd=4,relief=RIDGE,bg="black")
        Btn_Frame.place(x=10,y=460,width=430,height=70)
        
        add_btn=Button(Btn_Frame,text="Add",width=10,bd=0,cursor="hand2",command=self.add_contact).place(x=10,y=12,width=90,height=40)
        update_btn=Button(Btn_Frame,text="Update",width=10,bd=0,cursor="hand2",command=self.update_data).place(x=115,y=12,width=90,height=40)
        delete_btn=Button(Btn_Frame,text="Delete",width=10,bd=0,cursor="hand2",command=self.delete).place(x=215,y=12,width=90,height=40)
        clear_btn=Button(Btn_Frame,text="Clear",width=10,bd=0,cursor="hand2",command=self.clear).place(x=315,y=12,width=90,height=40)
        
        #------------- Details Frame -----------------
        Details_Frame=Frame(self.root,bd=4,relief=RIDGE)
        Details_Frame.place(x=500,y=100,width=800,height=560)
        
        lbl_search=Label(Details_Frame,text="Search By",font=("times new roman",20,"bold"))
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky="w")
        
        combo_search=ttk.Combobox(Details_Frame,textvariable=self.search_by,width=15,font=("times new roman",13,"bold"),state='readonly')
        combo_search['values']=("Name","Phone")
        combo_search.place(x=155,y=18)
        
        txt_search=Entry(Details_Frame,textvariable=self.search_txt,font=("times new roman",15),bd=5,relief=GROOVE)
        txt_search.place(x=330,y=18,width=175)
        
        Btn_Frame2=Frame(Details_Frame,bd=4,relief=RIDGE,bg="black")
        Btn_Frame2.place(x=525,y=10,width=260,height=45)
        
        showall_btn=Button(Btn_Frame2,text="Search",width=10,bd=0,cursor="hand2",command=self.searchby).place(x=10,y=3,width=110,height=30)
        search_btn=Button(Btn_Frame2,text="Show All",width=10,bd=0,cursor="hand2",command=self.fetch_data).place(x=130,y=3,width=110,height=30)
        
        #--------------------- Table Frame ----------------------
        Table_Frame=Frame(Details_Frame,bd=4,relief=RIDGE,bg="white")
        Table_Frame.place(x=10,y=70,width=760,height=470)
        
        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        
        self.Contact_Table=ttk.Treeview(Table_Frame,columns=("name","phone","email","address"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Contact_Table.xview)
        scroll_y.config(command=self.Contact_Table.yview)
        self.Contact_Table.heading("name",text="Name")
        self.Contact_Table.heading("phone",text="Phone No")
        self.Contact_Table.heading("email",text="Email")
        self.Contact_Table.heading("address",text="Address")
        self.Contact_Table['show']="headings"
        self.Contact_Table.column("name",width=200)
        self.Contact_Table.column("phone",width=200)
        self.Contact_Table.column("email",width=200)
        self.Contact_Table.column("address",width=200)
        self.Contact_Table.pack(fill=BOTH,expand=1)
        
        self.Contact_Table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    #--------------------- Funtions ------------------
    def add_contact(self):
        if self.name.get()=="":
            messagebox.showerror("Error","Name is required",parent=self.root)
        elif self.phone.get()=="":
            messagebox.showerror("Error","Phone no is required",parent=self.root)
        else:
            con=pymysql.connect(host="localhost",user="root",password="",database="contact")
            cur=con.cursor()
            cur.execute("insert into contact values(%s,%s,%s,%s)",(
                self.name.get(),
                self.phone.get(),
                self.email.get(),
                self.txt_address.get('1.0',END)
            ))
            con.commit()
            messagebox.showinfo("Success","Contact Added Successfully",parent=self.root)
            self.fetch_data()
            self.clear()
            con.close()
        
    def fetch_data(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="contact")
        cur=con.cursor()
        cur.execute("select * from contact")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.Contact_Table.delete(*self.Contact_Table.get_children())
            for row in rows:
                self.Contact_Table.insert('',END,values=row)
            con.commit()
        con.close()
        
    def clear(self):
        self.name.set("")
        self.phone.set("")
        self.email.set("")
        self.txt_address.delete("1.0",END)
        
    def get_cursor(self,ev):
        cursor_row=self.Contact_Table.focus()
        contents=self.Contact_Table.item(cursor_row)
        row=contents['values']
        self.name.set(row[0])
        self.phone.set(row[1])
        self.email.set(row[2])
        self.txt_address.delete("1.0",END)
        self.txt_address.insert(END,row[3])
        
    def update_data(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="contact")
        cur=con.cursor()
        cur.execute("update contact set name=%s,email=%s,address=%s where phone=%s",(
            self.name.get(),
            self.email.get(),
            self.txt_address.get('1.0',END),
            self.phone.get()
        ))
        con.commit()
        self.fetch_data()
        self.clear()
        con.close()
        
    def delete(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="contact")
        cur=con.cursor()
        op=messagebox.askyesno("Delete","Do you really want to delete this contact?",parent=self.root)
        if op==True:
            cur.execute("delete from contact where phone=%s",self.phone.get())
            con.commit()
            messagebox.showinfo("Delete","Contact deleted successfully",parent=self.root)
            self.fetch_data()
            self.clear()
            con.close()
        else:
            self.clear()
    
    def searchby(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="contact")
        cur=con.cursor()
        cur.execute("select * from contact where "+str(self.search_by.get())+" LIKE '%"+str(self.search_txt.get())+"%'")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.Contact_Table.delete(*self.Contact_Table.get_children())
            for row in rows:
                self.Contact_Table.insert('',END,values=row)
            con.commit()
        con.close()
    
        
    

root=Tk()
ob=Contact(root)
root.mainloop()