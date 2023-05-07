import tkinter
from tkinter import messagebox
from tkinter import *
import sqlite3
from tabulate import tabulate
from fpdf import FPDF

window = tkinter.Tk()
window.title("Login form")
window.geometry('340x440')
window.configure(bg='#333333')


def login():
    username = "admin"
    password = "admin"
    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="Login Success",
                            message="You successfully logged in.")
        main()
    else:
        messagebox.showerror(title="Error", message="Invalid login.")


frame = tkinter.Frame(bg='#333333')

# Creating widgets
login_label = tkinter.Label(
    frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tkinter.Label(
    frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
password_label = tkinter.Label(
    frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)


def main():
    root = Tk()
    root.title('Payroll Management System')

    label = Label(root, text="Payroll Management System",
                  bg="White", fg="Black", font="Arial")
    label.grid(row="0", column=1)
    root.geometry('400x400')
    root.resizable(False, False)

    # root.configure(bg='#333333')
    # creating the database
    conn = sqlite3.connect('payroll_management.db')
    # creating cursor
    c = conn.cursor()

    # c.execute("""CREATE TABLE payroll (
    #     name text,
    #     employee_id integer,
    #     employer text,
    #     address text,
    #     weekly_work_hours integer,
    #     hourly_pay integer,
    #     monthly_pay integer
    #     )""")

    def get_monthly_pay(weekly_work_hours, hourly_pay):
        weekly_work_hours = int(weekly_work_hours)
        hourly_pay = int(hourly_pay)

        overtime_hours = (weekly_work_hours - 40)
        overtime_pay = overtime_hours * hourly_pay * 1.5
        gross_pay = hourly_pay * weekly_work_hours

        if overtime_hours > 0:
            gross_pay = hourly_pay * weekly_work_hours + \
                overtime_pay - overtime_hours * hourly_pay

        tax = gross_pay * 4 * 0.2

        return (gross_pay * 4) - tax

    # creating edit window
    def editing_window():
        editing = Tk()
        editing.title('Select ID')
        editing.geometry('400x300')
        select_box_label = Label(editing, text="Select ID")
        select_box_label.grid(row=0, column=0, pady=5)
        select_box = Entry(editing, width=30)
        select_box.grid(row=0, column=1, padx=20, pady=5)
        # creating update button
        editing_btn = Button(editing, text="Edit Record",
                             command=lambda: edit())
        editing_btn.grid(row=1, column=0)
        # creating edit function

        def edit():
            global editor
            editor = Tk()
            editor.title('Update A Record')
            editor.geometry('400x300')
            # creating the database
            conn = sqlite3.connect('payroll_management.db')
            # creating cursor
            c = conn.cursor()

            record_id = select_box.get()
            c.execute("SELECT * FROM payroll WHERE oid = " + record_id)
            records = c.fetchall()

            print(tabulate(records, headers=["Name", "Emp ID", "Employer", "Address", "Weekly Work Hours",
                  "Hourly Pay", "Net Payable Salary", "Primary Key"], tablefmt="fancy_grid"))

            # creating global variables
            global name_editor
            global employee_id_editor
            global employer_editor
            global address_editor
            global weekly_work_hours_editor
            global hourly_pay_editor

            # creating text boxes
            name_editor = Entry(editor, width=30)
            name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
            employee_id_editor = Entry(editor, width=30)
            employee_id_editor.grid(row=1, column=1, padx=20)
            employer_editor = Entry(editor, width=30)
            employer_editor.grid(row=2, column=1, padx=20)
            address_editor = Entry(editor, width=30)
            address_editor.grid(row=3, column=1, padx=20)
            weekly_work_hours_editor = Entry(editor, width=30)
            weekly_work_hours_editor.grid(row=4, column=1, padx=20)
            hourly_pay_editor = Entry(editor, width=30)
            hourly_pay_editor.grid(row=5, column=1, padx=20)

            # creating text boxes labels
            name_label = Label(editor, text="Employee Name")
            name_label.grid(row=0, column=0, pady=(10, 0))
            employee_id_label = Label(editor, text="Employee ID")
            employee_id_label.grid(row=1, column=0)
            employer_label = Label(editor, text="Employer")
            employer_label.grid(row=2, column=0)
            address_label = Label(editor, text="Address")
            address_label.grid(row=3, column=0)
            weekly_work_hours_label = Label(editor, text="Weekly work hours")
            weekly_work_hours_label.grid(row=4, column=0)
            hourly_pay_label = Label(editor, text="Hourly pay")
            hourly_pay_label.grid(row=5, column=0)

            for record in records:
                name_editor.insert(0, record[0])
                employee_id_editor.insert(0, record[1])
                employer_editor.insert(0, record[2])
                address_editor.insert(0, record[3])
                weekly_work_hours_editor.insert(0, record[4])
                hourly_pay_editor.insert(0, record[5])

            # creating save button
            edit_btn = Button(editor, text="Save Record",
                              command=lambda: update())
            edit_btn.grid(row=6, column=0, columnspan=2,
                          pady=10, padx=10, ipadx=120)

            # creating update function
            def update():
                # creating the database
                conn = sqlite3.connect('payroll_management.db')
                # creating cursor
                c = conn.cursor()

                record_id = select_box.get()

                c.execute("""UPDATE payroll SET
                    name = :name,
                    employee_id = :employee_id,
                    employer = :employer,
                    address = :address,
                    weekly_work_hours = :weekly_work_hours,
                    hourly_pay = :hourly_pay
                    WHERE oid = :oid""",
                          {
                              'name': name_editor.get(),
                              'employee_id': employee_id_editor.get(),
                              'employer': employer_editor.get(),
                              'address': address_editor.get(),
                              'weekly_work_hours': weekly_work_hours_editor.get(),
                              'hourly_pay': hourly_pay_editor.get(),
                              'monthly_pay': get_monthly_pay(weekly_work_hours_editor.get(), hourly_pay_editor.get()),
                              'oid': record_id
                          })
                messagebox.showinfo(title="Update record",
                            message="You updated record successfully.")
                # commit changes
                conn.commit()
                # closing connection
                conn.close()
                editor.destroy()

    # creating delete_main function
    def delete_called():
        delete_window = Tk()
        delete_window.title('delete')
        delete_window.geometry('400x300')
        # creating the database
        conn = sqlite3.connect('payroll_management.db')
        # creating cursor
        c = conn.cursor()
        delete_box_final = Entry(delete_window, width=30)
        delete_box_final.grid(row=0, column=1, padx=20, pady=5)
        delete_box_final_label = Label(delete_window, text="Select ID")
        delete_box_final_label.grid(row=0, column=0, pady=5)

        def delete():
            # creating the database
            conn = sqlite3.connect('payroll_management.db')
            # creating cursor
            c = conn.cursor()

            c.execute("DELETE FROM payroll WHERE oid= " +
                      delete_box_final.get())
            messagebox.showinfo(title="Delete record",
                            message="You deleted record successfully.")
            # commit changes
            conn.commit()
            # closing connection
            conn.close()
            delete_window.destroy()
        delete_btn = Button(
            delete_window, text="Delete Record", command=delete)
        delete_btn.grid(row=2, column=0)

        # commit changes
        conn.commit()
        # closing connection
        conn.close()

    # creating submit function
    def submit():
        # creating the database
        conn = sqlite3.connect('payroll_management.db')
        # creating cursor
        c = conn.cursor()

        # insert into table
        c.execute("INSERT INTO payroll VALUES(:name, :employee_id, :employer, :address, :weekly_work_hours, :hourly_pay, :monthly_pay)",
                  {
                      'name': name.get(),
                      'employee_id': employee_id.get(),
                      'employer': employer.get(),
                      'address': address.get(),
                      'weekly_work_hours': weekly_work_hours.get(),
                      'hourly_pay': hourly_pay.get(),
                      'monthly_pay': get_monthly_pay(weekly_work_hours.get(), hourly_pay.get())
                  })
        messagebox.showinfo(title="Add record",
                            message="You added record successfully.")
        # commit changes
        conn.commit()
        # closing connection
        conn.close()

        # clearing textbox
        name.delete(0, END)
        employee_id.delete(0, END)
        employer.delete(0, END)
        address.delete(0, END)
        weekly_work_hours.delete(0, END)
        hourly_pay.delete(0, END)

    # creating query function
    def query():
        new_window = Tk()
        new_window.title('Record Table')
        new_window.geometry('800x400')
        # creating the database
        conn = sqlite3.connect('payroll_management.db')
        # creating cursor
        c = conn.cursor()
        # creating subheadings
        name_query_label = Label(new_window, text="Employee Name")
        name_query_label.grid(row=0, column=0, pady=(10, 0))
        employee_id_query_label = Label(new_window, text="Employee ID")
        employee_id_query_label.grid(row=0, column=1, pady=(10, 0))
        employer_query_label = Label(new_window, text="Employer")
        employer_query_label.grid(row=0, column=2, pady=(10, 0))
        address_query_label = Label(new_window, text="Address")
        address_query_label.grid(row=0, column=3, pady=(10, 0))
        weekly_work_hours_query_label = Label(
            new_window, text="Weekly work hours")
        weekly_work_hours_query_label.grid(row=0, column=4, pady=(10, 0))
        hourly_pay_query_label = Label(new_window, text="Hourly pay")
        hourly_pay_query_label.grid(row=0, column=5, pady=(10, 0))
        salary_query_label = Label(new_window, text="Net Salary")
        salary_query_label.grid(row=0, column=6, pady=(10, 0))
        oid_query_label = Label(new_window, text="OID")
        oid_query_label.grid(row=0, column=7, pady=(10, 0))
        pdf_btn = Button(new_window, text="Print All", command=pdf)
        pdf_btn.grid(row=0, column=10, padx=(10, 0), pady=(8, 0), ipadx=40)
        temp = c.execute("SELECT *,oid FROM payroll")
        # records = c.fetchall()
        i = 1
        for payroll in temp:
            for j in range(len(payroll)):
                e = Entry(new_window, width=10, fg='blue')
                e.grid(row=i, column=j, pady=(10, 0), padx=(10, 0))
                e.insert(END, payroll[j])
            i = i+1

        # commit changes
        conn.commit()
        # closing connection
        conn.close()

    def pdfsingle():
        print_window = Tk()
        print_window.title('Print Single Record')
        print_window.geometry('400x400')
        # creating the database
        conn = sqlite3.connect('payroll_management.db')
        # creating cursor
        c = conn.cursor()

        def printing():
            # creating the database
            conn = sqlite3.connect('payroll_management.db')
            # creating cursor
            c = conn.cursor()

            temp = c.execute(
                "SELECT *,oid FROM payroll WHERE oid =" + select_box_pdfsingle.get())
            records = c.fetchall()
            table = tabulate(records, headers=["Name", "Emp ID", "Employer", "Address", "Weekly Work Hours",
                             "Hourly", "Net Payable Salary", "Primary Key"], tablefmt="fancy_grid")
            print(table)

            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            headers = ["Name", "Emp ID", "Employer", "Address",
                       "Weekly Work Hours", "Hourly", "Net Payable Salary", "Primary Key"]

            for header in headers:
                # set font to bold and size 14 for headers
                pdf.set_font("Arial", 'B', size=7)
                pdf.cell(24, 10, header, 1, 0, "C")
            pdf.ln()
            for row in records:
                pdf.set_font("Arial", size=6)
                for item in row:
                    pdf.cell(24, 10, str(item), 1, 0, "C")
                pdf.ln()
            pdf.output("single.pdf")
            # commit changes
            conn.commit()
            # closing connection
            conn.close()
            print_window.destroy()

        select_box_pdfsingle_label = Label(print_window, text="Select ID")
        select_box_pdfsingle_label.grid(row=0, column=0, pady=5)
        select_box_pdfsingle = Entry(print_window, width=30)
        select_box_pdfsingle.grid(row=0, column=1, padx=20, pady=5)
        p_btn = Button(print_window, text="Print Record",
                       command=lambda: printing())
        p_btn.grid(row=1, column=0)

        # commit changes
        conn.commit()
        # closing connection
        conn.close()

    def pdf():
        # creating the database
        conn = sqlite3.connect('payroll_management.db')
        # creating cursor
        c = conn.cursor()

        temp = c.execute("SELECT *,oid FROM payroll")
        records = c.fetchall()
        table = tabulate(records, headers=["Name", "Emp ID", "Employer", "Address", "Weekly Work Hours",
                         "Hourly", "Net Payable Salary", "Primary Key"], tablefmt="fancy_grid")
        print(table)

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        headers = ["Name", "Emp ID", "Employer", "Address",
                   "Weekly Work Hours", "Hourly", "Net Payable Salary", "Primary Key"]

        for header in headers:
            # set font to bold and size 14 for headers
            pdf.set_font("Arial", 'B', size=7)
            pdf.cell(24, 10, header, 1, 0, "C")
        pdf.ln()
        for row in records:
            pdf.set_font("Arial", size=6)
            for item in row:
                pdf.cell(24, 10, str(item), 1, 0, "C")
            pdf.ln()
        pdf.output("table.pdf")

        # commit changes
        conn.commit()
        # closing connection
        conn.close()

    # creating text boxes
    name = Entry(root, width=30)
    name.grid(row=1, column=1, padx=20, pady=(10, 0))
    employee_id = Entry(root, width=30)
    employee_id.grid(row=2, column=1, padx=20)
    employer = Entry(root, width=30)
    employer.grid(row=3, column=1, padx=20)
    address = Entry(root, width=30)
    address.grid(row=4, column=1, padx=20)
    weekly_work_hours = Entry(root, width=30)
    weekly_work_hours.grid(row=5, column=1, padx=20)
    hourly_pay = Entry(root, width=30)
    hourly_pay.grid(row=6, column=1, padx=20)

    # creating text boxes labels
    name_label = Label(root, text="Employee Name")
    name_label.grid(row=1, column=0, pady=(10, 0))
    employee_id_label = Label(root, text="Employee ID")
    employee_id_label.grid(row=2, column=0)
    employer_label = Label(root, text="Employer")
    employer_label.grid(row=3, column=0)
    address_label = Label(root, text="Address")
    address_label.grid(row=4, column=0)
    weekly_work_hours_label = Label(root, text="Weekly work hours")
    weekly_work_hours_label.grid(row=5, column=0)
    hourly_pay_label = Label(root, text="Hourly pay")
    hourly_pay_label.grid(row=6, column=0)

    # creating submit button
    submit_btn = Button(root, text="Add Record", command=submit)
    submit_btn.grid(row=7, column=0)

    # creating query button
    query_btn = Button(root, text="Show Records", command=query)
    query_btn.grid(row=7, column=1)

    # creating delete button
    delete_btn = Button(root, text="Delete Record", command=delete_called)
    delete_btn.grid(row=9, column=0)

    # creating update button
    edit_btn = Button(root, text="Edit Record", command=editing_window)
    edit_btn.grid(row=9, column=1)

    pdf_btn = Button(root, text="Print Single Record", command=pdfsingle)
    pdf_btn.grid(row=10, column=0)

    # commit changes
    conn.commit()
 
    # closing connection
    conn.close()


frame.pack()

window.mainloop()
