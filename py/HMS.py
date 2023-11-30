import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime 

def exit_application():
    root.destroy()


def register_patient():
    name = name_entry.get()
    age = age_entry.get()
    gender = "Male" if var_gender.get() == 1 else "Female"

    if name.strip() == '' or not age.isdigit():
        messagebox.showerror("Error", "Please enter valid information.")
        return

    # Write patient data to the file
    with open("patients.txt", "a") as file:
        file.write(f"Name:{name};Age:{age};Gender:{gender};Appointments:0\n")

    messagebox.showinfo("Success", f"Patient Registered:\nName: {name}\nAge: {age}\nGender: {gender}")


def display_schedule_input():
    global schedule_window
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Schedule Appointment")

    appointment_frame = tk.Frame(schedule_window)
    appointment_frame.pack(padx=20, pady=10)

    date_label = tk.Label(appointment_frame, text="Appointment Date:")
    date_label.grid(row=0, column=0, padx=5, pady=5)
    date_entry = tk.Entry(appointment_frame)
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    time_label = tk.Label(appointment_frame, text="Appointment Time:")
    time_label.grid(row=1, column=0, padx=5, pady=5)
    time_entry = tk.Entry(appointment_frame)
    time_entry.grid(row=1, column=1, padx=5, pady=5)

    am_pm_var = tk.StringVar()
    am_pm_var.set("AM")  # default value
    am_pm_label = tk.Label(appointment_frame, text="AM/PM:")
    am_pm_label.grid(row=1, column=2, padx=5, pady=5)
    am_pm_menu = tk.OptionMenu(appointment_frame, am_pm_var, "AM", "PM")
    am_pm_menu.grid(row=1, column=3, padx=5, pady=5)

    patient_name_label = tk.Label(appointment_frame, text="Patient's Name:")
    patient_name_label.grid(row=2, column=0, padx=5, pady=5)
    patient_name_entry = tk.Entry(appointment_frame)
    patient_name_entry.grid(row=2, column=1, padx=5, pady=5)

    schedule_button = tk.Button(appointment_frame, text="Schedule Appointment", command=lambda: schedule_appointment_action(date_entry.get(), time_entry.get(), am_pm_var.get(), patient_name_entry.get()))
    schedule_button.grid(row=3, columnspan=4, padx=5, pady=10)

def schedule_appointment_action(date, time, am_pm, patient_name):
    if date.strip() == '' or time.strip() == '' or patient_name.strip() == '':
        messagebox.showerror("Error", "Please enter valid appointment information.")
        return

    # Construct datetime object from the entered date, time, and AM/PM
    appointment_datetime_str = f"{date} {time} {am_pm}"
    try:
        appointment_datetime = datetime.strptime(appointment_datetime_str, "%d-%m-%Y %I:%M %p")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid date and time.")
        return

    # Read patient data from the file
    with open("patients.txt", "r") as file:
        lines = file.readlines()

    found = False
    updated_lines = []
    for line in lines:
        if line.startswith(f"Name:{patient_name}"):
            parts = line.strip().split(';')
            appointments = int(parts[-1].split(':')[-1]) + 1
            # Append appointment date and time to the patient's record
            updated_line = f"Name:{patient_name};{';'.join(parts[1:-1])};Appointments:{appointments};AppointmentDateTime:{appointment_datetime.strftime('%d-%m-%Y %I:%M %p')}\n"
            updated_lines.append(updated_line)
            found = True
        else:
            updated_lines.append(line)

    if found:
        # Update patient data in the file
        with open("patients.txt", "w") as file:
            file.writelines(updated_lines)

        messagebox.showinfo("Success", f"Appointment Scheduled:\nDate: {date}\nTime: {time} {am_pm}\nPatient: {patient_name}")
        display_patient_information_action(patient_name)  # Update displayed information
    else:
        messagebox.showerror("Error", f"Patient '{patient_name}' not found.")

def cancel_appointment():
    global cancel_window
    cancel_window = tk.Toplevel(root)
    cancel_window.title("Cancel Appointment")

    cancel_frame = tk.Frame(cancel_window)
    cancel_frame.pack(padx=20, pady=10)

    date_label = tk.Label(cancel_frame, text="Appointment Date:")
    date_label.grid(row=0, column=0, padx=5, pady=5)
    date_entry = tk.Entry(cancel_frame)
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    time_label = tk.Label(cancel_frame, text="Appointment Time:")
    time_label.grid(row=1, column=0, padx=5, pady=5)
    time_entry = tk.Entry(cancel_frame)
    time_entry.grid(row=1, column=1, padx=5, pady=5)

    am_pm_var = tk.StringVar()
    am_pm_var.set("AM")  # default value
    am_pm_label = tk.Label(cancel_frame, text="AM/PM:")
    am_pm_label.grid(row=1, column=2, padx=5, pady=5)
    am_pm_menu = tk.OptionMenu(cancel_frame, am_pm_var, "AM", "PM")
    am_pm_menu.grid(row=1, column=3, padx=5, pady=5)

    patient_name_label = tk.Label(cancel_frame, text="Patient's Name:")
    patient_name_label.grid(row=2, column=0, padx=5, pady=5)
    patient_name_entry = tk.Entry(cancel_frame)
    patient_name_entry.grid(row=2, column=1, padx=5, pady=5)

    cancel_button = tk.Button(cancel_frame, text="Cancel Appointment", command=lambda: cancel_appointment_action(date_entry.get(), time_entry.get(), am_pm_var.get(), patient_name_entry.get()))
    cancel_button.grid(row=3, columnspan=4, padx=5, pady=10)

def cancel_appointment_action(date, time, am_pm, patient_name):
    if date.strip() == '' or time.strip() == '' or patient_name.strip() == '':
        messagebox.showerror("Error", "Please enter valid appointment information.")
        return

    # Create the datetime string to match the format in the file
    appointment_datetime_str = f"{date} {time} {am_pm}"
    try:
        appointment_datetime = datetime.strptime(appointment_datetime_str, "%d-%m-%Y %I:%M %p")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid date and time.")
        return

    # Read patient data from the file
    with open("patients.txt", "r") as file:
        lines = file.readlines()

    found = False
    updated_lines = []
    for line in lines:
        if line.startswith(f"Name:{patient_name}"):
            parts = line.strip().split(';')
            appointments = int(parts[-2].split(':')[-1])  # Update to access the correct appointments count part
            if appointments > 0:
                appointments -= 1
                updated_lines.append(f"Name:{patient_name};{';'.join(parts[1:-2])};Appointments:{appointments}\n")
                found = True
            else:
                updated_lines.append(line)  # No appointments left, keep as is
                found = True
        else:
            updated_lines.append(line)

    if found:
        # Update patient data in the file
        with open("patients.txt", "w") as file:
            file.writelines(updated_lines)

        messagebox.showinfo("Success", f"Appointment Canceled:\nDate: {date}\nTime: {time} {am_pm}\nPatient: {patient_name}")
        display_patient_information_action(patient_name)  # Update displayed information
    else:
        messagebox.showerror("Error", f"No appointments found for patient '{patient_name}'.")

def display_patient_information():
    global display_window
    display_window = tk.Toplevel(root)
    display_window.title("Display Patient Information")

    display_frame = tk.Frame(display_window)
    display_frame.pack(padx=20, pady=10)

    patient_name_label = tk.Label(display_frame, text="Patient's Name:")
    patient_name_label.grid(row=0, column=0, padx=5, pady=5)
    patient_name_entry = tk.Entry(display_frame)
    patient_name_entry.grid(row=0, column=1, padx=5, pady=5)

    display_button = tk.Button(display_frame, text="Display Information", command=lambda: display_patient_information_action(patient_name_entry.get()))
    display_button.grid(row=1, columnspan=2, padx=5, pady=10)

def display_patient_information_action(patient_name):
    if patient_name.strip() == '':
        messagebox.showerror("Error", "Please enter a patient's name.")
        return

    # Read patient data from the file
    with open("patients.txt", "r") as file:
        lines = file.readlines()
    
    found = False
    for line in lines:
        if line.startswith(f"Name:{patient_name}"):
            parts = line.strip().split(';')
            age = parts[1].split(':')[-1]
            appointments = parts[3].split(':')[-1]
            messagebox.showinfo("Patient Information", f"Name: {patient_name}\nAge: {age}\nNumber of Appointments: {appointments}")
            found = True
            break
    
    if not found:
        messagebox.showerror("Error", f"Patient '{patient_name}' not found.")

def display_all_appointments():
    # Read all patient data from the file
    with open("patients.txt", "r") as file:
        lines = file.readlines()

    appointments_info = ""
    for line in lines:
        parts = line.strip().split(';')
        name = parts[0].split(':')[-1]
        appointments = parts[3].split(':')[-1]
        appointments_info += f"Patient: {name} - Appointments: {appointments}\n"

    if appointments_info:
        messagebox.showinfo("All Appointments", appointments_info)
    else:
        messagebox.showinfo("All Appointments", "No appointments scheduled.")

def search_patients_by_age():
    search_age = simpledialog.askinteger("Search by Age", "Enter Age:")
    if search_age is not None:
        # Read all patient data from the file
        with open("patients.txt", "r") as file:
            lines = file.readlines()

        matching_patients = ""
        for line in lines:
            parts = line.strip().split(';')
            name = parts[0].split(':')[-1]
            age = int(parts[1].split(':')[-1])
            if age == search_age:
                matching_patients += f"Name: {name} - Age: {age}\n"

        if matching_patients:
            messagebox.showinfo("Patients by Age", matching_patients)
        else:
            messagebox.showinfo("Patients by Age", f"No patients found with age {search_age}.")

def view_upcoming_appointments():
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    upcoming_appointments = ""

    with open("patients.txt", "r") as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) >= 5:
                name = parts[0].split(':')[-1]
                appointments = int(parts[3].split(':')[-1])
                if appointments > 0:
                    appointment_datetime_str = parts[4].split(':', 1)[-1].strip()  # Change here
                    try:
                        appointment_datetime = datetime.strptime(appointment_datetime_str, "%d-%m-%Y %I:%M %p")
                        appointment_date = appointment_datetime.date()
                        appointment_time = appointment_datetime.time()

                        if appointment_date > current_date or (appointment_date == current_date and appointment_time >= current_time):
                            upcoming_appointments += f"Patient: {name} - Appointment Date: {appointment_date.strftime('%d-%m-%Y')} - Time: {appointment_time.strftime('%I:%M %p')}\n"
                    except ValueError as e:
                        print(f"Error parsing date and time for patient {name}: {e}")
                        pass  # Skip if date format does not match

    if upcoming_appointments:
        messagebox.showinfo("Upcoming Appointments", upcoming_appointments)
    else:
        messagebox.showinfo("Upcoming Appointments", "No upcoming appointments.")

def update_patient_information():
    global update_window
    update_window = tk.Toplevel(root)
    update_window.title("Update Patient Information")

    update_frame = tk.Frame(update_window)
    update_frame.pack(padx=20, pady=10)

    patient_name_label = tk.Label(update_frame, text="Patient's Name:")
    patient_name_label.grid(row=0, column=0, padx=5, pady=5)
    patient_name_entry = tk.Entry(update_frame)
    patient_name_entry.grid(row=0, column=1, padx=5, pady=5)

    info_label = tk.Label(update_frame, text="Select Information to Update:")
    info_label.grid(row=1, column=0, padx=5, pady=5)

    var_info = tk.StringVar()
    var_info.set("Age")  # default value
    info_option = tk.OptionMenu(update_frame, var_info, "Age", "Gender")
    info_option.grid(row=1, column=1, padx=5, pady=5)

    update_button = tk.Button(update_frame, text="Update", command=lambda: update_patient_info_action(patient_name_entry.get(), var_info.get()))
    update_button.grid(row=2, columnspan=2, padx=5, pady=10)

def update_patient_info_action(patient_name, info_type):
    if patient_name.strip() == '':
        messagebox.showerror("Error", "Please enter a patient's name.")
        return

    # Read patient data from the file
    with open("patients.txt", "r") as file:
        lines = file.readlines()

    found = False
    updated_lines = []
    for line in lines:
        if line.startswith(f"Name:{patient_name}"):
            parts = line.strip().split(';')
            if info_type == "Age":
                new_age = simpledialog.askinteger("Update Age", "Enter New Age:")
                if new_age is not None:
                    parts[1] = f"Age:{new_age}"
                    updated_lines.append(';'.join(parts) + '\n')
            elif info_type == "Gender":
                new_gender = simpledialog.askstring("Update Gender", "Enter New Gender (Male/Female):")
                if new_gender is not None and new_gender in ["Male", "Female"]:
                    parts[2] = f"Gender:{new_gender}"
                    updated_lines.append(';'.join(parts) + '\n')
            found = True
        else:
            updated_lines.append(line)

    if found:
        # Update patient data in the file
        with open("patients.txt", "w") as file:
            file.writelines(updated_lines)
        messagebox.showinfo("Success", f"Patient information updated: {info_type} updated for {patient_name}.")
    else:
        messagebox.showerror("Error", f"Patient '{patient_name}' not found.")

def calculate_demographic_summary():
    total_patients = 0
    total_male_patients = 0
    total_female_patients = 0
    total_age = 0
    total_name_patients = set()

    # Read patient data from the file
    with open("patients.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(';')
        total_patients += 1

        name = parts[0].split(':')[-1]
        total_name_patients.add(name)

        gender = parts[2].split(':')[-1]
        if gender == "Male":
            total_male_patients += 1
        elif gender == "Female":
            total_female_patients += 1

        age = int(parts[1].split(':')[-1])
        total_age += age

    if total_patients > 0:
        average_age = total_age / total_patients
    else:
        average_age = 0

    messagebox.showinfo(
        "Demographic Summary",
        f"Total Patients: {total_patients}\n"
        f"Total Male Patients: {total_male_patients}\n"
        f"Total Female Patients: {total_female_patients}\n"
        f"Average Age: {average_age:.2f}"
    )

def generate_upcoming_appointment_report():
    current_datetime = datetime.now()  # Get current date and time
    upcoming_appointments = []

    # Read patient data from the file
    with open("patients.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(';')
        if len(parts) >= 5:
            name = parts[0].split(':')[-1]
            appointments = int(parts[3].split(':')[-1])
            if appointments > 0:
                appointment_datetime_str = parts[4].split(':', 1)[-1].strip()  # Extract appointment date and time
                try:
                    appointment_datetime = datetime.strptime(appointment_datetime_str, "%d-%m-%Y %I:%M %p")
                    if appointment_datetime >= current_datetime:
                        upcoming_appointments.append(f"Patient: {name} - Appointment Date: {appointment_datetime.strftime('%d-%m-%Y %I:%M %p')}")
                except ValueError as e:
                    print(f"Error parsing date and time for patient {name}: {e}")
                    pass  # Skip if date format does not match

    if upcoming_appointments:
        report_filename = "Upcoming_Appointment_Report.txt"
        with open(report_filename, 'w') as report_file:
            report_file.write("Upcoming Appointments Report\n\n")
            report_file.write("\n".join(upcoming_appointments))

        messagebox.showinfo("Report Generated", "Upcoming Appointment Report Generated Successfully.")
    else:
        messagebox.showinfo("No Appointments", "No upcoming appointments found.")

def main():
    global name_entry, age_entry, var_gender, root

    root = tk.Tk()
    root.title("Hospital Management System")

    menubar = tk.Menu(root)

    schedule_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Schedule Appointment", menu=schedule_menu)
    schedule_menu.add_command(label="Schedule", command=display_schedule_input)

    cancel_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Cancel Appointment", menu=cancel_menu)
    cancel_menu.add_command(label="Cancel", command=cancel_appointment)

    display_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Patient Info", menu=display_menu)
    display_menu.add_command(label="Display", command=display_patient_information)

    display_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="All Appointments", menu=display_menu)
    display_menu.add_command(label="Display All Appointments", command=display_all_appointments)

    display_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Search patients", menu=display_menu)
    display_menu.add_command(label="Search Patients by Age", command=search_patients_by_age)
   
    display_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Upcoming Appointments", menu=display_menu)
    display_menu.add_command(label="View Upcoming Appointments", command=view_upcoming_appointments)
    
    update_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Update Patient Info", menu=update_menu)
    update_menu.add_command(label="Update Information", command=update_patient_information)

    demographics_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Demographic Summary", menu=demographics_menu)
    demographics_menu.add_command(label="Display Summary in Window", command=calculate_demographic_summary)

    display_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Appointment Report", menu=display_menu)
    display_menu.add_command(label="Generate Upcoming Appointments Report", command=generate_upcoming_appointment_report)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=exit_application)

    menubar.add_cascade(label="Exit", menu=file_menu)
 
    root.config(menu=menubar)

    heading_label = tk.Label(root, text="Project Hospital", font=("Arial", 20))
    heading_label.pack(pady=10)

    sub_heading_label = tk.Label(root, text="Register Patient", font=("Arial", 14, "bold"))
    sub_heading_label.pack()

    registration_frame = tk.Frame(root)
    registration_frame.pack(pady=20)

    name_label = tk.Label(registration_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(registration_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    age_label = tk.Label(registration_frame, text="Age:")
    age_label.grid(row=1, column=0, padx=5, pady=5)
    age_entry = tk.Entry(registration_frame)
    age_entry.grid(row=1, column=1, padx=5, pady=5)

    var_gender = tk.IntVar()
    gender_label = tk.Label(registration_frame, text="Gender:")
    gender_label.grid(row=2, column=0, padx=5, pady=5)
    male_checkbox = tk.Checkbutton(registration_frame, text="Male", variable=var_gender, onvalue=1, offvalue=0)
    male_checkbox.grid(row=2, column=1, padx=5, pady=5)
    female_checkbox = tk.Checkbutton(registration_frame, text="Female", variable=var_gender, onvalue=0, offvalue=1)
    female_checkbox.grid(row=2, column=2, padx=5, pady=5)

    register_button = tk.Button(root, text="Register Patient", command=register_patient)
    register_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
