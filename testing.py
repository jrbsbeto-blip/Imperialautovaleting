import time
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk


# Set window dark design matching slate-900 / slate-800
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CarWashDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Car Wash Management Dashboard")
        self.geometry("1100x650")
        self.configure(fg_color="#0f172a") # bg-slate-900

        # Memory store for active jobs
        self.vehicle_queue = []
        
        # Define comprehensive price index
        self.services_dict = {
            "Express Washes": [
                ("Express 1 Car", 35.00),
                            python "C:\Users\jrbsb\OneDrive\Test html\testing.py"    ("Express 1 Suv,Jeep", 45.00),
                ("Express 2 Car", 45.00),
                ("Express 2 Suv,Jeep", 55.00),
                ("Express 3 Car", 55.00),
                ("Express 3 Suv,Jeep", 65.00),
                ("Express 4 Car", 65.00),
                ("Express 4 Suv,Jeep", 75.00),
            ],
            "Valet Packages": [
                ("Valet 1 Car", 105.00),
                ("Valet 1 Suv,Jeep", 125.00),
                ("Valet 2 Car", 130.00),
                ("Valet 2 Suv,Jeep", 150.00),
                ("Valet 3 Car", 130.00),
                ("Valet 3 Suv,Jeep", 150.00),
            ],
            "extra packages": [
                ("Extra for express 7 seats", 5.00),
                ("extra for valet 7 seats", 10.00),
                ("Car seat wash 1", 10.00),
                ("Car seat wash 2", 15.00),
                ("Car seat wash 3", 20.00),
                ("Part of carpet wash 1", 5.00),
                ("Part of carpet wash 2", 10.00),
            ]
        }
        
        self.checkbox_variables = {}
        self.setup_ui()

    def setup_ui(self):
        # Configure layout split: Column 1 (Left panel) & Columns 2-3 (Right Panel)
        self.grid_columnconfigure(0, weight=4, minsize=380)
        self.grid_columnconfigure(1, weight=6, minsize=650)
        self.grid_rowconfigure(0, weight=1)

        # -------------------------------------------------------------
        # COLUMN 1: VEHICLE ENTRY & INTEGRATED ACTIONS
        # -------------------------------------------------------------
        left_panel = ctk.CTkFrame(self, fg_color="#1e293b", border_color="#334155", border_width=1, corner_radius=12)
        left_panel.grid(row=0, column=0, padx=20, py=20, sticky="nsew")
        
        lbl_title = ctk.CTkLabel(left_panel, text="🚗 1. Vehicle Entry & Actions", font=ctk.CTkFont(size=18, weight="bold"), text_color="#38bdf8")
        lbl_title.pack(anchor="w", padx=20, py=(20, 15))

        # Inputs
        ctk.CTkLabel(left_panel, text="License Plate", text_color="#94a3b8", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)
        self.txt_plate = ctk.CTkEntry(left_panel, placeholder_text="e.g. 123ABC", fg_color="#0f172a", border_color="#334155", text_color="white")
        self.txt_plate.pack(fill="x", padx=20, py=(0, 12))

        ctk.CTkLabel(left_panel, text="Vehicle Model", text_color="#94a3b8", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)
        self.txt_model = ctk.CTkEntry(left_panel, placeholder_text="e.g. Black Civic", fg_color="#0f172a", border_color="#334155", text_color="white")
        self.txt_model.pack(fill="x", padx=20, py=(0, 12))

        ctk.CTkLabel(left_panel, text="Customer Phone (Optional)", text_color="#94a3b8", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)
        self.txt_phone = ctk.CTkEntry(left_panel, placeholder_text="Not Provided", fg_color="#0f172a", border_color="#334155", text_color="white")
        self.txt_phone.pack(fill="x", padx=20, py=(0, 15))

        ctk.CTkLabel(left_panel, text="Select Services:", text_color="#94a3b8", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=20, py=(0, 5))

        # Scrollable Area for Service Selection
        scroll_container = ctk.CTkScrollableFrame(left_panel, fg_color="#0f172a", border_color="#334155", border_width=1, height=220)
        scroll_container.pack(fill="both", expand=True, padx=20, py=(0, 10))

        # Populate categories
        for category, service_items in self.services_dict.items():
            cat_color = "#38bdf8" if "Express" in category else "#c084fc"
            lbl_cat = ctk.CTkLabel(scroll_container, text=category.upper(), font=ctk.CTkFont(size=11, weight="bold"), text_color=cat_color)
            lbl_cat.pack(anchor="w", padx=5, py=(8, 2))
            
            for name, price in service_items:
                var = tk.BooleanVar()
                self.checkbox_variables[name] = (var, price)
                
                cb = ctk.CTkCheckBox(
                    scroll_container, 
                    text=f"{name} (€{price:.2f})", 
                    variable=var, 
                    command=self.calculate_live_total,
                    text_color="#cbd5e1",
                    font=ctk.CTkFont(size=12),
                    checkbox_width=18,
                    checkbox_height=18
                )
                cb.pack(anchor="w", padx=10, py=3)

        # Dynamic Pricing Summary Section
        summary_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        summary_frame.pack(fill="x", padx=20, py=10)
        
        ctk.CTkLabel(summary_frame, text="Total Price:", text_color="#94a3b8", font=ctk.CTkFont(size=13)).pack(side="left")
        self.lbl_live_total = ctk.CTkLabel(summary_frame, text="€0.00", text_color="#34d399", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_live_total.pack(side="right")

        # Submit Action
        btn_submit = ctk.CTkButton(left_panel, text="Add to Queue", command=self.add_vehicle, fg_color="#0284c7", hover_color="#0ea5e9", text_color="white", font=ctk.CTkFont(weight="bold"))
        btn_submit.pack(fill="x", padx=20, py=(0, 20))

        # -------------------------------------------------------------
        # COLUMNS 2 & 3: LIVE ACTIVE WASH QUEUE
        # -------------------------------------------------------------
        right_panel = ctk.CTkFrame(self, fg_color="#1e293b", border_color="#334155", border_width=1, corner_radius=12)
        right_panel.grid(row=0, column=1, padx=20, py=20, sticky="nsew")

        lbl_queue_title = ctk.CTkLabel(right_panel, text="📋 2. Active Queue", font=ctk.CTkFont(size=18, weight="bold"), text_color="#34d399")
        lbl_queue_title.pack(anchor="w", padx=20, py=20)

        # Scrollable Viewport simulating table tracking frame
        self.queue_container = ctk.CTkScrollableFrame(right_panel, fg_color="#0f172a", border_color="#334155", border_width=1)
        self.queue_container.pack(fill="both", expand=True, padx=20, py=(0, 20))
        
        self.render_queue()

    def calculate_live_total(self):
        total = 0.0
        for var, price in self.checkbox_variables.values():
            if var.get():
                total += price
        self.lbl_live_total.configure(text=f"€{total:.2f}")
        return total

    def add_vehicle(self):
        plate = self.txt_plate.get().strip().upper()
        model = self.txt_model.get().strip()
        phone = self.txt_phone.get().strip() or "Not Provided"
        
        selected_services = [name for name, (var, _) in self.checkbox_variables.items() if var.get()]
        
        if not plate or not model:
            messagebox.showwarning("Input Error", "Please provide both License Plate and Vehicle Model.")
            return
            
        if not selected_services:
            messagebox.showwarning("Selection Error", "Please select at least one active wash service package.")
            return

        total_price = self.calculate_live_total()

        # Add dictionary object structure
        vehicle_job = {
            "id": int(time.time() * 1000),
            "plate": plate,
            "model": model,
            "phone": phone,
            "services": ", ".join(selected_services),
            "total": total_price,
            "status": "Pending"
        }

        self.vehicle_queue.append(vehicle_job)
        self.render_queue()
        
        # Clear fields
        self.txt_plate.delete(0, tk.END)
        self.txt_model.delete(0, tk.END)
        self.txt_phone.delete(0, tk.END)
        for var, _ in self.checkbox_variables.values():
            var.set(False)
        self.calculate_live_total()

    def change_status(self, job_id, new_status):
        for job in self.vehicle_queue:
            if job["id"] == job_id:
                job["status"] = new_status
                break
        self.render_queue()

    def remove_job(self, job_id):
        self.vehicle_queue = [job for job in self.vehicle_queue if job["id"] != job_id]
        self.render_queue()

    def render_queue(self):
        # Clear current frame widgets inside container
        for widget in self.queue_container.winfo_children():
            widget.destroy()

        if not self.vehicle_queue:
            lbl_empty = ctk.CTkLabel(self.queue_container, text="No vehicles in queue.", font=ctk.CTkFont(slant="italic"), text_color="#64748b")
            lbl_empty.pack(pady=40)
            return

        # Render rows dynamically
        for job in self.vehicle_queue:
            row_frame = ctk.CTkFrame(self.queue_container, fg_color="#1e293b", corner_radius=6, border_color="#334155", border_width=1)
            row_frame.pack(fill="x", padx=5, py=4)

            # Details text column layout
            text_str = f"Plate: {job['plate']}  |  {job['model']}\nServices: {job['services']}\nPrice: €{job['total']:.2f}"
            lbl_info = ctk.CTkLabel(row_frame, text=text_str, justify="left", font=ctk.CTkFont(size=12), text_color="#e2e8f0")
            lbl_info.pack(side="left", padx=15, py=10)

            # Status Badge Styling Mapping
            status = job["status"]
            badge_color = "#f59e0b"  # Pending (Amber)
            if status == "In Progress":
                badge_color = "#38bdf8"  # (Sky Blue)
            elif status == "Completed":
                badge_color = "#34d399"  # (Emerald Green)

            lbl_status = ctk.CTkLabel(row_frame, text=status.upper(), text_color=badge_color, font=ctk.CTkFont(size=11, weight="bold"))
            lbl_status.pack(side="left", padx=20)

            # Action Buttons container setup
            btn_container = ctk.CTkFrame(row_frame, fg_color="transparent")
            btn_container.pack(side="right", padx=15)

            # Context flow buttons conditional mapping
            if status == "Pending":
                btn_start = ctk.CTkButton(
                    btn_container,
                    text="Start",
                    width=50,
                    height=24,
                    fg_color="#0369a1",
                    hover_color="#0284c7",
                    command=lambda j_id=job["id"]: self.change_status(j_id, "In Progress")
                )
                btn_start.pack(side="left", padx=2)
            elif status == "In Progress":
                btn_finish = ctk.CTkButton(
                    btn_container,
                    text="Finish",
                    width=50,
                    height=24,
                    fg_color="#047857",
                    hover_color="#059669",
                    command=lambda j_id=job["id"]: self.change_status(j_id, "Completed")
                )
                btn_finish.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(
                btn_container,
                text="✕",
                width=24,
                height=24,
                fg_color="#991b1b",
                hover_color="#dc2626",
                command=lambda j_id=job["id"]: self.remove_job(j_id)
            )
            btn_del.pack(side="left", padx=2)


if __name__ == "__main__":
    app = CarWashDashboard()
    app.mainloop()