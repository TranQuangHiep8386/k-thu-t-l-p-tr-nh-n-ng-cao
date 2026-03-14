import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
from calendar_logic import EventManager, Event

class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Lịch Cá Nhân")
        self.geometry("900x600")
        
        self.manager = EventManager()
        self.current_date = datetime.now()
        self.selected_date_str = self.current_date.strftime("%Y-%m-%d")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Left Panel: Calendar
        self.left_frame = ttk.Frame(self, padding="10")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Navigation
        nav_frame = ttk.Frame(self.left_frame)
        nav_frame.pack(fill="x", pady=5)
        
        ttk.Button(nav_frame, text="<<", command=self.prev_month).pack(side="left")
        self.lbl_month = ttk.Label(nav_frame, text="", font=("Arial", 14, "bold"))
        self.lbl_month.pack(side="left", expand=True)
        ttk.Button(nav_frame, text=">>", command=self.next_month).pack(side="left")
        
        # Calendar Grid
        self.cal_frame = ttk.Frame(self.left_frame)
        self.cal_frame.pack(fill="both", expand=True)
        
        # Right Panel: Events
        self.right_frame = ttk.Frame(self, padding="10", relief="sunken")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        ttk.Label(self.right_frame, text="Danh sách sự kiện", font=("Arial", 12, "bold")).pack(pady=5)
        self.lbl_selected_date = ttk.Label(self.right_frame, text="", font=("Arial", 10))
        self.lbl_selected_date.pack(pady=5)
        
        # Event List
        self.event_listbox = tk.Listbox(self.right_frame)
        self.event_listbox.pack(fill="both", expand=True, pady=5)
        self.event_listbox.bind('<<ListboxSelect>>', self.on_event_select)
        
        # Buttons
        btn_frame = ttk.Frame(self.right_frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Thêm Sự Kiện", command=self.add_event_dialog).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Thống kê", command=self.show_statistics).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa Sự Kiện", command=self.delete_event).pack(side="right", padx=5)
        
        self.draw_calendar()
        self.update_event_list()

    def draw_calendar(self):
        for widget in self.cal_frame.winfo_children():
            widget.destroy()
            
        year = self.current_date.year
        month = self.current_date.month
        
        self.lbl_month.config(text=f"Tháng {month} - {year}")
        
        # Weekday headers
        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        for i, day in enumerate(days):
            ttk.Label(self.cal_frame, text=day, anchor="center").grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            
        # Days
        cal = calendar.monthcalendar(year, month)
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    style = "TButton"
                    if date_str == self.selected_date_str:
                         # Just a simple way to highlight, not perfect in ttk without custom styles
                         # We'll use state or text change to indicate
                         pass
                    
                    btn = tk.Button(self.cal_frame, text=str(day), 
                                    command=lambda d=date_str: self.select_date(d))
                                    
                    # simple highlight for today
                    if date_str == datetime.now().strftime("%Y-%m-%d"):
                        btn.config(fg="blue", font=("Arial", 9, "bold"))
                        
                    # simple highlight for selected
                    if date_str == self.selected_date_str:
                        btn.config(bg="#e1e1e1", relief="sunken")

                    # Mark days with events
                    if date_str in self.manager.events and self.manager.events[date_str]:
                        btn.config(text=f"{day} •")

                    btn.grid(row=r+1, column=c, sticky="nsew", padx=1, pady=1)
                    
        # Make grid resizable
        for i in range(7):
            self.cal_frame.columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.cal_frame.rowconfigure(i, weight=1)

    def prev_month(self):
        month = self.current_date.month - 1
        year = self.current_date.year
        if month == 0:
            month = 12
            year -= 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self.draw_calendar()

    def next_month(self):
        month = self.current_date.month + 1
        year = self.current_date.year
        if month == 13:
            month = 1
            year += 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self.draw_calendar()

    def select_date(self, date_str):
        self.selected_date_str = date_str
        self.draw_calendar() # Re-draw to update selection highlight
        self.update_event_list()

    def update_event_list(self):
        self.event_listbox.delete(0, tk.END)
        self.lbl_selected_date.config(text=f"Ngày: {self.selected_date_str}")
        
        events = self.manager.get_events_for_date(self.selected_date_str)
        if not events:
            self.event_listbox.insert(tk.END, "(Không có sự kiện)")
        else:
            for event in events:
                display_text = f"[{event.time}] {event.title}"
                self.event_listbox.insert(tk.END, display_text)

    def add_event_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Thêm Sự Kiện")
        dialog.geometry("300x250")
        
        ttk.Label(dialog, text="Tiêu đề:").pack(pady=5)
        entry_title = ttk.Entry(dialog)
        entry_title.pack(fill="x", padx=10)
        
        ttk.Label(dialog, text="Giờ (HH:MM):").pack(pady=5)
        entry_time = ttk.Entry(dialog)
        entry_time.insert(0, "08:00")
        entry_time.pack(fill="x", padx=10)
        
        ttk.Label(dialog, text="Mô tả:").pack(pady=5)
        entry_desc = ttk.Entry(dialog)
        entry_desc.pack(fill="x", padx=10)
        
        def save():
            title = entry_title.get()
            time = entry_time.get()
            desc = entry_desc.get()
            
            if title:
                new_event = Event(title, self.selected_date_str, time, desc)
                self.manager.add_event(new_event)
                self.update_event_list()
                self.draw_calendar() # Update dot indicators
                dialog.destroy()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập tiêu đề!")

        ttk.Button(dialog, text="Lưu", command=save).pack(pady=10)

    def delete_event(self):
        selection = self.event_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sự kiện để xóa!")
            return
            
        index = selection[0]
        events = self.manager.get_events_for_date(self.selected_date_str)
        
        if not events:
            return

        event = events[index]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa '{event.title}'?"):
            if self.manager.delete_event(event.id, self.selected_date_str):
                self.update_event_list()
                self.draw_calendar()

    def on_event_select(self, event):
        # Optional: Show full details when selected
        pass

    def show_statistics(self):
        stats = self.manager.get_statistics()
        
        msg = f"""--- THỐNG KÊ HOẠT ĐỘNG ---
        
Tổng số sự kiện: {stats['total_events']}
Ngày bận rộn nhất: {stats['most_busy_date']} ({stats['max_events_on_busy_date']} sự kiện)
Số ngày có lịch: {stats['total_active_days']}
        """
        messagebox.showinfo("Thống Kê", msg)
