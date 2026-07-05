import customtkinter as ctk
from tkinter import ttk
import sqlite3
from datetime import datetime

# إعداد المظهر العام والتناسق
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Language dictionary
LANGUAGES = {
    "fr": {
        "app_title": "Système intelligent d'atelier - Réparation et vente d'appareils média et téléphones",
        "main_title": "Gestion intégrée de l'atelier de maintenance et des ventes",
        "tab_maintenance": "Maintenance et réparation",
        "tab_sales": "Vente d'appareils et accessoires",
        "tab_inventory": "Stock pièces détachées et marchandises",
        "cust_name": "Nom du client",
        "cust_phone": "Numéro de téléphone",
        "device_type": "Type d'appareil",
        "issue_desc": "Description de la panne (ex. : écran cassé, ne charge pas, flashage...)",
        "status": "Statut",
        "maint_cost": "Coût de maintenance",
        "btn_save_ticket": "Enregistrer un nouvel appareil",
        "btn_update_ticket": "Mettre à jour statut/coût",
        "btn_delete_ticket": "Supprimer la fiche",
        "btn_save_sale": "Enregistrer une vente",
        "btn_delete_sale": "Supprimer une vente",
        "btn_save_part": "Entrée en stock / Mise à jour",
        "btn_consume_part": "Consommer une pièce pour maintenance",
        "btn_delete_part": "Supprimer du stock",
        "sale_item": "Nom de l'article vendu (chargeur, smartphone, clé USB...)",
        "sale_qty": "Quantité",
        "sale_price": "Prix unitaire de vente",
        "part_name": "Nom de la pièce (écran iPhone 11, batterie S20...)",
        "part_qty": "Quantité disponible",
        "part_cost": "Prix d'achat",
        "maint_revenue": "Revenus maintenance",
        "sales_revenue": "Revenus ventes",
        "total_revenue": "Revenu net total",
        "col_id": "N°",
        "col_client": "Client",
        "col_phone": "Téléphone",
        "col_device": "Appareil",
        "col_issue": "Panne",
        "col_status": "Statut",
        "col_cost": "Coût (TND)",
        "col_date": "Date de réception",
        "col_sale_id": "N° vente",
        "col_item": "Article / Produit",
        "col_qty": "Quantité",
        "col_price": "Prix unitaire",
        "col_total": "Total (TND)",
        "col_sale_date": "Date de vente",
        "col_part_id": "ID pièce",
        "col_part_name": "Nom pièce / article",
        "col_part_qty": "Quantité disponible",
        "col_part_cost": "Prix d'achat (TND)",
        "col_inv_date": "Date d'inventaire",
        "status_waiting": "En attente",
        "status_repaired": "Réparé",
        "status_delivered": "Livré et validé",
        "msg_ticket_saved": "Appareil enregistré et planifié avec succès !",
        "msg_ticket_updated": "Données de maintenance et statut mis à jour avec succès !",
        "msg_ticket_deleted": "Fiche de maintenance supprimée avec succès.",
        "msg_sale_saved": "Vente enregistrée avec succès et tableau de bord mis à jour !",
        "msg_sale_deleted": "Vente supprimée et annulée.",
        "msg_part_saved": "Stock de pièces détachées approvisionné avec succès !",
        "msg_part_consumed": "Pièce liée, consommée et facture de maintenance mise à jour automatiquement !",
        "msg_part_deleted": "Article supprimé des registres de stock.",
        "msg_select_ticket": "Sélectionnez d'abord un appareil dans le tableau pour le modifier.",
        "msg_select_ticket_delete": "Sélectionnez la ligne à supprimer dans les registres de maintenance.",
        "msg_select_sale_delete": "Sélectionnez la vente à annuler.",
        "msg_select_part_delete": "Sélectionnez une pièce dans le tableau pour la supprimer.",
        "msg_select_ticket_part": "Attention : sélectionnez d'abord un appareil dans le tableau de maintenance pour lier la pièce !",
        "msg_fill_required": "Veuillez remplir le nom du client et la description de la panne.",
        "msg_fill_sale": "Veuillez remplir tous les champs de vente.",
        "msg_fill_part": "Veuillez saisir le nom de la pièce, la quantité et le coût.",
        "msg_cost_error": "Erreur dans la valeur du coût de maintenance.",
        "msg_numeric_error": "Erreur : veuillez saisir des nombres valides pour la quantité et le prix.",
        "msg_insufficient_stock": "Quantité insuffisante en stock",
        "msg_part_not_found": "Cette pièce n'existe pas en stock.",
        "msg_enter_part_name": "Veuillez saisir le nom de la pièce à déduire.",
        "language": "Langue"
    },
    "ar": {
        "app_title": "نظام الورشة الذكي - إصلاح وبيع الأجهزة الإعلامية والهواتف",
        "main_title": "الإدارة المتكاملة لورشة الصيانة والمبيعات",
        "tab_maintenance": "الصيانة والإصلاح",
        "tab_sales": "بيع الأجهزة والملحقات",
        "tab_inventory": "مخزون قطع الغيار والبضائع",
        "cust_name": "اسم العميل",
        "cust_phone": "رقم الهاتف",
        "device_type": "نوع الجهاز",
        "issue_desc": "وصف العطل (مثال: شاشة مكسورة، لا يشحن، فلاش...)",
        "status": "الحالة",
        "maint_cost": "تكلفة الصيانة",
        "btn_save_ticket": "تسجيل جهاز جديد",
        "btn_update_ticket": "تحديث الحالة/التكلفة",
        "btn_delete_ticket": "حذف الملف",
        "btn_save_sale": "تسجيل بيع",
        "btn_delete_sale": "حذف بيع",
        "btn_save_part": "إدخال للمخزون / تحديث",
        "btn_consume_part": "استهلاك قطعة للصيانة",
        "btn_delete_part": "حذف من المخزون",
        "sale_item": "اسم المادة المباعة (شاحن، هاتف، فلاشة...)",
        "sale_qty": "الكمية",
        "sale_price": "سعر البيع الوحدوي",
        "part_name": "اسم القطعة (شاشة iPhone 11، بطارية S20...)",
        "part_qty": "الكمية المتوفرة",
        "part_cost": "سعر الشراء",
        "maint_revenue": "إيرادات الصيانة",
        "sales_revenue": "إيرادات المبيعات",
        "total_revenue": "إجمالي الإيرادات الصافية",
        "col_id": "رقم",
        "col_client": "العميل",
        "col_phone": "الهاتف",
        "col_device": "الجهاز",
        "col_issue": "العطل",
        "col_status": "الحالة",
        "col_cost": "التكلفة (دينار)",
        "col_date": "تاريخ الاستلام",
        "col_sale_id": "رقم البيع",
        "col_item": "المادة / المنتج",
        "col_qty": "الكمية",
        "col_price": "السعر الوحدوي",
        "col_total": "المجموع (دينار)",
        "col_sale_date": "تاريخ البيع",
        "col_part_id": "رقم القطعة",
        "col_part_name": "اسم القطعة / المادة",
        "col_part_qty": "الكمية المتوفرة",
        "col_part_cost": "سعر الشراء (دينار)",
        "col_inv_date": "تاريخ الجرد",
        "status_waiting": "في الانتظار",
        "status_repaired": "تم الإصلاح",
        "status_delivered": "تم التسليم والتحقق",
        "msg_ticket_saved": "تم تسجيل الجهاز وتخطيطه بنجاح!",
        "msg_ticket_updated": "تم تحديث بيانات الصيانة والحالة بنجاح!",
        "msg_ticket_deleted": "تم حذف ملف الصيانة بنجاح.",
        "msg_sale_saved": "تم تسجيل البيع بنجاح وتحديث لوحة المعلومات!",
        "msg_sale_deleted": "تم حذف وإلغاء البيع.",
        "msg_part_saved": "تم تزويد مخزون قطع الغيار بنجاح!",
        "msg_part_consumed": "تم ربط القطعة واستهلاكها وتحديث فاتورة الصيانة تلقائياً!",
        "msg_part_deleted": "تم حذف المادة من سجلات المخزون.",
        "msg_select_ticket": "الرجاء تحديد جهاز من الجدول أولاً لتعديله.",
        "msg_select_ticket_delete": "الرجاء تحديد السطر المراد حذفه من سجلات الصيانة.",
        "msg_select_sale_delete": "الرجاء تحديد البيع المراد إلغاؤه.",
        "msg_select_part_delete": "الرجاء تحديد قطعة من الجدول لحذفها.",
        "msg_select_ticket_part": "تنبيه: الرجاء تحديد جهاز من جدول الصيانة أولاً لربط القطعة!",
        "msg_fill_required": "الرجاء ملء اسم العميل ووصف العطل.",
        "msg_fill_sale": "الرجاء ملء جميع حقول البيع.",
        "msg_fill_part": "الرجاء إدخال اسم القطعة والكمية والتكلفة.",
        "msg_cost_error": "خطأ في قيمة تكلفة الصيانة.",
        "msg_numeric_error": "خطأ: الرجاء إدخال أرقام صالحة للكمية والسعر.",
        "msg_insufficient_stock": "كمية غير كافية في المخزون",
        "msg_part_not_found": "هذه القطعة غير موجودة في المخزون.",
        "msg_enter_part_name": "الرجاء إدخال اسم القطعة المراد خصمها.",
        "language": "اللغة"
    },
    "en": {
        "app_title": "Intelligent Workshop System - Repair and Sales of Media Devices and Phones",
        "main_title": "Integrated Management of Maintenance Workshop and Sales",
        "tab_maintenance": "Maintenance and Repair",
        "tab_sales": "Device and Accessories Sales",
        "tab_inventory": "Spare Parts and Goods Inventory",
        "cust_name": "Customer Name",
        "cust_phone": "Phone Number",
        "device_type": "Device Type",
        "issue_desc": "Issue Description (e.g., broken screen, not charging, flashing...)",
        "status": "Status",
        "maint_cost": "Maintenance Cost",
        "btn_save_ticket": "Save New Device",
        "btn_update_ticket": "Update Status/Cost",
        "btn_delete_ticket": "Delete Record",
        "btn_save_sale": "Save Sale",
        "btn_delete_sale": "Delete Sale",
        "btn_save_part": "Stock Entry / Update",
        "btn_consume_part": "Consume Part for Maintenance",
        "btn_delete_part": "Delete from Stock",
        "sale_item": "Sold Item Name (charger, smartphone, USB drive...)",
        "sale_qty": "Quantity",
        "sale_price": "Unit Sale Price",
        "part_name": "Part Name (iPhone 11 screen, S20 battery...)",
        "part_qty": "Available Quantity",
        "part_cost": "Purchase Price",
        "maint_revenue": "Maintenance Revenue",
        "sales_revenue": "Sales Revenue",
        "total_revenue": "Total Net Revenue",
        "col_id": "No.",
        "col_client": "Customer",
        "col_phone": "Phone",
        "col_device": "Device",
        "col_issue": "Issue",
        "col_status": "Status",
        "col_cost": "Cost (TND)",
        "col_date": "Received Date",
        "col_sale_id": "Sale No.",
        "col_item": "Item / Product",
        "col_qty": "Quantity",
        "col_price": "Unit Price",
        "col_total": "Total (TND)",
        "col_sale_date": "Sale Date",
        "col_part_id": "Part ID",
        "col_part_name": "Part / Item Name",
        "col_part_qty": "Available Quantity",
        "col_part_cost": "Purchase Price (TND)",
        "col_inv_date": "Inventory Date",
        "status_waiting": "Pending",
        "status_repaired": "Repaired",
        "status_delivered": "Delivered and Verified",
        "msg_ticket_saved": "Device registered and scheduled successfully!",
        "msg_ticket_updated": "Maintenance data and status updated successfully!",
        "msg_ticket_deleted": "Maintenance record deleted successfully.",
        "msg_sale_saved": "Sale recorded successfully and dashboard updated!",
        "msg_sale_deleted": "Sale deleted and cancelled.",
        "msg_part_saved": "Spare parts stock replenished successfully!",
        "msg_part_consumed": "Part linked, consumed and maintenance invoice updated automatically!",
        "msg_part_deleted": "Item deleted from stock records.",
        "msg_select_ticket": "Please select a device from the table first to modify it.",
        "msg_select_ticket_delete": "Please select the row to delete from maintenance records.",
        "msg_select_sale_delete": "Please select the sale to cancel.",
        "msg_select_part_delete": "Please select a part from the table to delete it.",
        "msg_select_ticket_part": "Warning: Please select a device from the maintenance table first to link the part!",
        "msg_fill_required": "Please fill in the customer name and issue description.",
        "msg_fill_sale": "Please fill in all sales fields.",
        "msg_fill_part": "Please enter the part name, quantity and cost.",
        "msg_cost_error": "Error in maintenance cost value.",
        "msg_numeric_error": "Error: Please enter valid numbers for quantity and price.",
        "msg_insufficient_stock": "Insufficient quantity in stock",
        "msg_part_not_found": "This part does not exist in stock.",
        "msg_enter_part_name": "Please enter the part name to deduct.",
        "language": "Language"
    }
}

class WorkshopApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Language setting
        self.current_language = "fr"
        
        self.title(LANGUAGES[self.current_language]["app_title"])
        self.geometry("1150x850")
        self.minsize(1050, 700)
        
        # متغيرات التحكم والتعديل
        self.selected_ticket_id = None
        self.selected_sale_id = None
        self.selected_part_id = None
        
        # إنشاء وتحديث قاعدة البيانات
        self.init_db()
        
        # --- الحاوية الرئيسية القابلة للتمرير لحل مشكلة الافيشاج ---
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # العنوان الرئيسي
        self.title_label = ctk.CTkLabel(self.main_container, text=LANGUAGES[self.current_language]["main_title"], font=("Arial", 22, "bold"))
        self.title_label.pack(pady=10)
        
        # Language switcher
        control_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        control_frame.pack(pady=5, padx=10, fill="x")
        
        self.lang_combo = ctk.CTkComboBox(control_frame, values=["Français", "العربية", "English"], width=150, command=self.change_language)
        self.lang_combo.set("Français")
        self.lang_combo.pack(side="right", padx=5)
        
        lang_label = ctk.CTkLabel(control_frame, text=LANGUAGES[self.current_language]["language"] + ":", font=("Arial", 12))
        lang_label.pack(side="right", padx=5)
        
        # --- نظام التبويب الحديث ---
        self.tab_view = ctk.CTkTabview(self.main_container, width=1100)
        self.tab_view.pack(pady=5, padx=10, fill="both", expand=True)
        
        self.tab_maintenance = self.tab_view.add(LANGUAGES[self.current_language]["tab_maintenance"])
        self.tab_sales = self.tab_view.add(LANGUAGES[self.current_language]["tab_sales"])
        self.tab_inventory = self.tab_view.add(LANGUAGES[self.current_language]["tab_inventory"])
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # بناء الواجهات
        self.build_maintenance_tab()
        self.build_sales_tab()
        self.build_inventory_tab()
        
        # التنسيق اللوني للجداول وشحن البيانات
        self.adjust_treeview_theme()
        self.load_all_data()

    def init_db(self):
        conn = sqlite3.connect('workshop.db')
        cursor = conn.cursor()
        
        # 1. جدول الصيانة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_phone TEXT,
                device_type TEXT,
                issue_description TEXT,
                status TEXT DEFAULT 'En attente',
                cost REAL DEFAULT 0.0,
                date_received TEXT
            )
        ''')
        
        # 2. جدول المبيعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER,
                price REAL,
                total_price REAL,
                date_sold TEXT
            )
        ''')
        
        # 3. جدول مخزن قطع الغيار والسلع
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_name TEXT UNIQUE NOT NULL,
                quantity INTEGER DEFAULT 0,
                cost_price REAL,
                last_updated TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def change_language(self, choice):
        """Change the application language"""
        if choice == "Français":
            self.current_language = "fr"
        elif choice == "العربية":
            self.current_language = "ar"
        elif choice == "English":
            self.current_language = "en"
        
        # Update title
        self.title(LANGUAGES[self.current_language]["app_title"])
        
        # Update main title
        self.title_label.configure(text=LANGUAGES[self.current_language]["main_title"])
        
        # Destroy and recreate tabview with new language
        self.tab_view.destroy()
        
        self.tab_view = ctk.CTkTabview(self.main_container, width=1100)
        self.tab_view.pack(pady=5, padx=10, fill="both", expand=True)
        
        self.tab_maintenance = self.tab_view.add(LANGUAGES[self.current_language]["tab_maintenance"])
        self.tab_sales = self.tab_view.add(LANGUAGES[self.current_language]["tab_sales"])
        self.tab_inventory = self.tab_view.add(LANGUAGES[self.current_language]["tab_inventory"])
        
        # Rebuild interfaces
        self.build_maintenance_tab()
        self.build_sales_tab()
        self.build_inventory_tab()
        
        # Reload data
        self.load_all_data()

    def adjust_treeview_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            bg, fg, h_bg = "#2e2e2e", "white", "#1f1f1f"
        else:
            bg, fg, h_bg = "#ffffff", "black", "#ececec"
            
        self.style.configure("Treeview", font=("Arial", 11), rowheight=25, background=bg, foreground=fg, fieldbackground=bg)
        self.style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background=h_bg, foreground=fg)

    # =========================================================================
    # 1. واجهة قسم الصيانة والإصلاح
    # =========================================================================
    def build_maintenance_tab(self):
        form = ctk.CTkFrame(self.tab_maintenance)
        form.pack(pady=10, padx=10, fill="x")
        
        # السطر الأول
        r1 = ctk.CTkFrame(form, fg_color="transparent")
        r1.pack(fill="x", pady=5, padx=10)
        self.cust_name_entry = ctk.CTkEntry(r1, placeholder_text=LANGUAGES[self.current_language]["cust_name"], width=220)
        self.cust_name_entry.pack(side="right", padx=5)
        self.cust_phone_entry = ctk.CTkEntry(r1, placeholder_text=LANGUAGES[self.current_language]["cust_phone"], width=150)
        self.cust_phone_entry.pack(side="right", padx=5)
        
        self.device_combo = ctk.CTkComboBox(r1, values=["Téléphone Android", "iPhone", "Ordinateur portable (Laptop)", "Ordinateur de bureau (PC)", "Tablette", "Autre"], width=180)
        self.device_combo.pack(side="right", padx=5)
        
        # السطر الثاني
        r2 = ctk.CTkFrame(form, fg_color="transparent")
        r2.pack(fill="x", pady=5, padx=10)
        self.issue_entry = ctk.CTkEntry(r2, placeholder_text=LANGUAGES[self.current_language]["issue_desc"], width=400)
        self.issue_entry.pack(side="right", padx=5, expand=True, fill="x")
        
        self.status_combo = ctk.CTkComboBox(r2, values=[
            LANGUAGES[self.current_language]["status_waiting"],
            LANGUAGES[self.current_language]["status_repaired"],
            LANGUAGES[self.current_language]["status_delivered"]
        ], width=150)
        self.status_combo.pack(side="right", padx=5)
        
        self.maint_cost_entry = ctk.CTkEntry(r2, placeholder_text=LANGUAGES[self.current_language]["maint_cost"], width=100)
        self.maint_cost_entry.pack(side="right", padx=5)
        
        # الأزرار
        btn_f = ctk.CTkFrame(self.tab_maintenance, fg_color="transparent")
        btn_f.pack(pady=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_save_ticket"], command=self.save_ticket, fg_color="green").grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_update_ticket"], command=self.update_ticket, fg_color="#e67e22").grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_delete_ticket"], command=self.delete_ticket, fg_color="#c0392b").grid(row=0, column=2, padx=5)
        
        self.maint_status_lbl = ctk.CTkLabel(self.tab_maintenance, text="", font=("Arial", 13))
        self.maint_status_lbl.pack(pady=2)
        
        # الجدول
        t_frame = ctk.CTkFrame(self.tab_maintenance)
        t_frame.pack(pady=5, padx=10, fill="x")
        
        cols = ("id", "name", "phone", "device", "issue", "status", "cost", "date")
        self.tree_maint = ttk.Treeview(t_frame, columns=cols, show="headings", height=10)
        
        self.tree_maint.heading("id", text=LANGUAGES[self.current_language]["col_id"])
        self.tree_maint.heading("name", text=LANGUAGES[self.current_language]["col_client"])
        self.tree_maint.heading("phone", text=LANGUAGES[self.current_language]["col_phone"])
        self.tree_maint.heading("device", text=LANGUAGES[self.current_language]["col_device"])
        self.tree_maint.heading("issue", text=LANGUAGES[self.current_language]["col_issue"])
        self.tree_maint.heading("status", text=LANGUAGES[self.current_language]["col_status"])
        self.tree_maint.heading("cost", text=LANGUAGES[self.current_language]["col_cost"])
        self.tree_maint.heading("date", text=LANGUAGES[self.current_language]["col_date"])
        
        for c in cols: self.tree_maint.column(c, anchor="center", width=110)
        self.tree_maint.column("id", width=50)
        self.tree_maint.column("issue", width=180)
        
        self.tree_maint.pack(side="left", fill="both", expand=True)
        self.tree_maint.bind("<<TreeviewSelect>>", self.get_selected_ticket)
        
        sb = ttk.Scrollbar(t_frame, orient="vertical", command=self.tree_maint.yview)
        self.tree_maint.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    # =========================================================================
    # 2. واجهة قسم المبيعات
    # =========================================================================
    def build_sales_tab(self):
        form = ctk.CTkFrame(self.tab_sales)
        form.pack(pady=10, padx=10, fill="x")
        
        self.sale_item_entry = ctk.CTkEntry(form, placeholder_text=LANGUAGES[self.current_language]["sale_item"], width=300)
        self.sale_item_entry.pack(side="right", padx=10, pady=10)
        
        self.sale_qty_entry = ctk.CTkEntry(form, placeholder_text=LANGUAGES[self.current_language]["sale_qty"], width=100)
        self.sale_qty_entry.pack(side="right", padx=10, pady=10)
        
        self.sale_price_entry = ctk.CTkEntry(form, placeholder_text=LANGUAGES[self.current_language]["sale_price"], width=120)
        self.sale_price_entry.pack(side="right", padx=10, pady=10)
        
        btn_f = ctk.CTkFrame(self.tab_sales, fg_color="transparent")
        btn_f.pack(pady=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_save_sale"], command=self.save_sale, fg_color="green").grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_delete_sale"], command=self.delete_sale, fg_color="#c0392b").grid(row=0, column=1, padx=5)
        
        self.sales_status_lbl = ctk.CTkLabel(self.tab_sales, text="", font=("Arial", 13))
        self.sales_status_lbl.pack(pady=2)
        
        t_frame = ctk.CTkFrame(self.tab_sales)
        t_frame.pack(pady=5, padx=10, fill="x")
        
        cols = ("id", "item", "qty", "price", "total", "date")
        self.tree_sales = ttk.Treeview(t_frame, columns=cols, show="headings", height=10)
        
        self.tree_sales.heading("id", text=LANGUAGES[self.current_language]["col_sale_id"])
        self.tree_sales.heading("item", text=LANGUAGES[self.current_language]["col_item"])
        self.tree_sales.heading("qty", text=LANGUAGES[self.current_language]["col_qty"])
        self.tree_sales.heading("price", text=LANGUAGES[self.current_language]["col_price"])
        self.tree_sales.heading("total", text=LANGUAGES[self.current_language]["col_total"])
        self.tree_sales.heading("date", text=LANGUAGES[self.current_language]["col_sale_date"])
        
        for c in cols: self.tree_sales.column(c, anchor="center", width=150)
        self.tree_sales.column("id", width=60)
        self.tree_sales.pack(side="left", fill="both", expand=True)
        
        sb = ttk.Scrollbar(t_frame, orient="vertical", command=self.tree_sales.yview)
        self.tree_sales.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        
        # لوحة أرباح الورشة المجمعة في الأسفل
        self.dashboard = ctk.CTkFrame(self.tab_sales)
        self.dashboard.pack(pady=15, padx=10, fill="x")
        self.maint_revenue_lbl = ctk.CTkLabel(self.dashboard, text=f"{LANGUAGES[self.current_language]['maint_revenue']} : 0.000 TND", font=("Arial", 13, "bold"), text_color="#1e3799")
        self.maint_revenue_lbl.pack(side="right", expand=True, pady=10)
        self.sales_revenue_lbl = ctk.CTkLabel(self.dashboard, text=f"{LANGUAGES[self.current_language]['sales_revenue']} : 0.000 TND", font=("Arial", 13, "bold"), text_color="#27ae60")
        self.sales_revenue_lbl.pack(side="right", expand=True, pady=10)
        self.total_revenue_lbl = ctk.CTkLabel(self.dashboard, text=f"{LANGUAGES[self.current_language]['total_revenue']} : 0.000 TND", font=("Arial", 14, "bold"), text_color="#2ecc71")
        self.total_revenue_lbl.pack(side="right", expand=True, pady=10)

    # =========================================================================
    # 3. واجهة مخزن قطع الغيار والسلع
    # =========================================================================
    def build_inventory_tab(self):
        form = ctk.CTkFrame(self.tab_inventory)
        form.pack(pady=10, padx=10, fill="x")
        
        self.part_name_entry = ctk.CTkEntry(form, placeholder_text=LANGUAGES[self.current_language]["part_name"], width=280)
        self.part_name_entry.pack(side="right", padx=10, pady=10)
        
        self.part_qty_entry = ctk.CTkEntry(form, placeholder_text=LANGUAGES[self.current_language]["part_qty"], width=100)
        self.part_qty_entry.pack(side="right", padx=10, pady=10)
        
        self.part_cost_entry = ctk.CTkEntry(form, placeholder_text=LANGUAGES[self.current_language]["part_cost"], width=110)
        self.part_cost_entry.pack(side="right", padx=10, pady=10)
        
        btn_f = ctk.CTkFrame(self.tab_inventory, fg_color="transparent")
        btn_f.pack(pady=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_save_part"], command=self.save_part, fg_color="green").grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_consume_part"], command=self.consume_part, fg_color="#e67e22").grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_f, text=LANGUAGES[self.current_language]["btn_delete_part"], command=self.delete_part, fg_color="#c0392b").grid(row=0, column=2, padx=5)
        
        self.inv_status_lbl = ctk.CTkLabel(self.tab_inventory, text="", font=("Arial", 13))
        self.inv_status_lbl.pack(pady=2)
        
        t_frame = ctk.CTkFrame(self.tab_inventory)
        t_frame.pack(pady=5, padx=10, fill="x")
        
        cols = ("id", "name", "qty", "price", "date")
        self.tree_inv = ttk.Treeview(t_frame, columns=cols, show="headings", height=10)
        
        self.tree_inv.heading("id", text=LANGUAGES[self.current_language]["col_part_id"])
        self.tree_inv.heading("name", text=LANGUAGES[self.current_language]["col_part_name"])
        self.tree_inv.heading("qty", text=LANGUAGES[self.current_language]["col_part_qty"])
        self.tree_inv.heading("price", text=LANGUAGES[self.current_language]["col_part_cost"])
        self.tree_inv.heading("date", text=LANGUAGES[self.current_language]["col_inv_date"])
        
        for c in cols: self.tree_inv.column(c, anchor="center", width=180)
        self.tree_inv.column("id", width=80)
        self.tree_inv.column("name", width=250)
        self.tree_inv.pack(side="left", fill="both", expand=True)
        self.tree_inv.bind("<<TreeviewSelect>>", self.get_selected_part)
        
        sb = ttk.Scrollbar(t_frame, orient="vertical", command=self.tree_inv.yview)
        self.tree_inv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    # =========================================================================
    # العمليات البرمجية وقواعد البيانات (Backend Logic)
    # =========================================================================
    
    # دالات قسم الصيانة
    def save_ticket(self):
        name = self.cust_name_entry.get().strip()
        phone = self.cust_phone_entry.get().strip()
        device = self.device_combo.get()
        issue = self.issue_entry.get().strip()
        status = self.status_combo.get()
        cost = self.maint_cost_entry.get().strip() or "0.0"
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if name and issue:
            try:
                cost_val = float(cost)
                conn = sqlite3.connect('workshop.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO tickets (customer_name, customer_phone, device_type, issue_description, status, cost, date_received)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, phone, device, issue, status, cost_val, date_now))
                conn.commit()
                conn.close()
                self.clear_maint_entries()
                self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_ticket_saved"], text_color="green")
                self.load_all_data()
            except ValueError: self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_cost_error"], text_color="red")
        else: self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_fill_required"], text_color="orange")

    def get_selected_ticket(self, event):
        sel = self.tree_maint.focus()
        if sel:
            val = self.tree_maint.item(sel, 'values')
            if val:
                self.selected_ticket_id = val[0]
                self.cust_name_entry.delete(0, 'end'); self.cust_name_entry.insert(0, val[1])
                self.cust_phone_entry.delete(0, 'end'); self.cust_phone_entry.insert(0, val[2])
                self.device_combo.set(val[3])
                self.issue_entry.delete(0, 'end'); self.issue_entry.insert(0, val[4])
                self.status_combo.set(val[5])
                self.maint_cost_entry.delete(0, 'end'); self.maint_cost_entry.insert(0, val[6])

    def update_ticket(self):
        if not self.selected_ticket_id:
            self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_select_ticket"], text_color="orange")
            return
        status = self.status_combo.get()
        cost = self.maint_cost_entry.get().strip() or "0.0"
        name = self.cust_name_entry.get().strip()
        phone = self.cust_phone_entry.get().strip()
        device = self.device_combo.get()
        issue = self.issue_entry.get().strip()
        
        try:
            cost_val = float(cost)
            conn = sqlite3.connect('workshop.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tickets SET customer_name=?, customer_phone=?, device_type=?, issue_description=?, status=?, cost=? WHERE id=?
            ''', (name, phone, device, issue, status, cost_val, self.selected_ticket_id))
            conn.commit()
            conn.close()
            self.clear_maint_entries()
            self.selected_ticket_id = None
            self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_ticket_updated"], text_color="green")
            self.load_all_data()
        except ValueError: self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_cost_error"], text_color="red")

    def delete_ticket(self):
        sel = self.tree_maint.focus()
        if not sel:
            self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_select_ticket_delete"], text_color="orange")
            return
        t_id = self.tree_maint.item(sel, 'values')[0]
        conn = sqlite3.connect('workshop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE id=?", (t_id,))
        conn.commit()
        conn.close()
        self.clear_maint_entries()
        self.maint_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_ticket_deleted"], text_color="red")
        self.load_all_data()

    def clear_maint_entries(self):
        self.cust_name_entry.delete(0, 'end')
        self.cust_phone_entry.delete(0, 'end')
        self.issue_entry.delete(0, 'end')
        self.maint_cost_entry.delete(0, 'end')

    # دالات قسم المبيعات
    def save_sale(self):
        item = self.sale_item_entry.get().strip()
        qty = self.sale_qty_entry.get().strip()
        price = self.sale_price_entry.get().strip()
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if item and qty and price:
            try:
                q_val = int(qty)
                p_val = float(price)
                tot = q_val * p_val
                
                conn = sqlite3.connect('workshop.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sales (item_name, quantity, price, total_price, date_sold)
                    VALUES (?, ?, ?, ?, ?)
                ''', (item, q_val, p_val, tot, date_now))
                conn.commit()
                conn.close()
                
                self.sale_item_entry.delete(0, 'end')
                self.sale_qty_entry.delete(0, 'end')
                self.sale_price_entry.delete(0, 'end')
                self.sales_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_sale_saved"], text_color="green")
                self.load_all_data()
            except ValueError: self.sales_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_numeric_error"], text_color="red")
        else: self.sales_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_fill_sale"], text_color="orange")

    def delete_sale(self):
        sel = self.tree_sales.focus()
        if not sel:
            self.sales_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_select_sale_delete"], text_color="orange")
            return
        s_id = self.tree_sales.item(sel, 'values')[0]
        conn = sqlite3.connect('workshop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE id=?", (s_id,))
        conn.commit()
        conn.close()
        self.sales_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_sale_deleted"], text_color="red")
        self.load_all_data()

    # دالات قسم المخزن وقطع الغيار
    def save_part(self):
        name = self.part_name_entry.get().strip()
        qty = self.part_qty_entry.get().strip()
        cost = self.part_cost_entry.get().strip()
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if name and qty and cost:
            try:
                q_val = int(qty)
                c_val = float(cost)
                
                conn = sqlite3.connect('workshop.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO inventory (part_name, quantity, cost_price, last_updated)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(part_name) DO UPDATE SET
                    quantity = quantity + excluded.quantity,
                    cost_price = excluded.cost_price,
                    last_updated = excluded.last_updated
                ''', (name, q_val, c_val, date_now))
                conn.commit()
                conn.close()
                
                self.part_name_entry.delete(0, 'end')
                self.part_qty_entry.delete(0, 'end')
                self.part_cost_entry.delete(0, 'end')
                self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_part_saved"], text_color="green")
                self.load_all_data()
            except ValueError: self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_numeric_error"], text_color="red")
        else: self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_fill_part"], text_color="orange")

    def consume_part(self):
        """الربط الذكي: خصم قطعة غيار من المخزن وإدراجها فوراً لبيان الجهاز المفتوح بالصيانة"""
        name = self.part_name_entry.get().strip()
        qty = self.part_qty_entry.get().strip() or "1"
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if not self.selected_ticket_id:
            self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_select_ticket_part"], text_color="red")
            return
            
        if name:
            try:
                q_to_consume = int(qty)
                conn = sqlite3.connect('workshop.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT quantity, cost_price FROM inventory WHERE part_name=?", (name,))
                res = cursor.fetchone()
                
                if res:
                    curr_qty, cost_price = res[0], res[1]
                    if curr_qty >= q_to_consume:
                        # 1. خصم من المخزن
                        cursor.execute("UPDATE inventory SET quantity=? WHERE part_name=?", (curr_qty - q_to_consume, name))
                        
                        # 2. تعديل بيان الجهاز بالصيانة وزيادة السعر تلقائياً بناءً على سعر القطعة
                        cursor.execute("SELECT issue_description, cost FROM tickets WHERE id=?", (self.selected_ticket_id,))
                        t_res = cursor.fetchone()
                        old_desc, old_cost = t_res[0], t_res[1]
                        
                        new_desc = f"{old_desc} + [Installation de {q_to_consume} {name}]"
                        new_cost = old_cost + (cost_price * q_to_consume) # إضافة تكلفة القطعة لبيان الفاتورة
                        
                        cursor.execute("UPDATE tickets SET issue_description=?, cost=? WHERE id=?", (new_desc, new_cost, self.selected_ticket_id))
                        conn.commit()
                        self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_part_consumed"], text_color="green")
                    else:
                        self.inv_status_lbl.configure(text=f"{LANGUAGES[self.current_language]['msg_insufficient_stock']}, disponible : {curr_qty}", text_color="red")
                else:
                    self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_part_not_found"], text_color="red")
                conn.close()
                self.load_all_data()
            except ValueError: self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_numeric_error"], text_color="red")
        else: self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_enter_part_name"], text_color="orange")

    def get_selected_part(self, event):
        sel = self.tree_inv.focus()
        if sel:
            val = self.tree_inv.item(sel, 'values')
            if val:
                self.selected_part_id = val[0]
                self.part_name_entry.delete(0, 'end'); self.part_name_entry.insert(0, val[1])
                self.part_qty_entry.delete(0, 'end'); self.part_qty_entry.insert(0, val[2])
                self.part_cost_entry.delete(0, 'end'); self.part_cost_entry.insert(0, val[3])

    def delete_part(self):
        sel = self.tree_inv.focus()
        if not sel:
            self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_select_part_delete"], text_color="orange")
            return
        p_id = self.tree_inv.item(sel, 'values')[0]
        conn = sqlite3.connect('workshop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id=?", (p_id,))
        conn.commit()
        conn.close()
        self.inv_status_lbl.configure(text=LANGUAGES[self.current_language]["msg_part_deleted"], text_color="red")
        self.load_all_data()

    # شحن وحساب الإجماليات المالية
    def load_all_data(self):
        self.adjust_treeview_theme()
        
        # 1. شحن الصيانة
        for r in self.tree_maint.get_children(): self.tree_maint.delete(r)
        conn = sqlite3.connect('workshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer_name, customer_phone, device_type, issue_description, status, cost, date_received FROM tickets ORDER BY id DESC")
        m_rows = cursor.fetchall()
        sum_maint = 0.0
        for row in m_rows:
            sum_maint += row[6]
            self.tree_maint.insert("", "end", values=row)
            
        # 2. شحن المبيعات
        for r in self.tree_sales.get_children(): self.tree_sales.delete(r)
        cursor.execute("SELECT id, item_name, quantity, price, total_price, date_sold FROM sales ORDER BY id DESC")
        s_rows = cursor.fetchall()
        sum_sales = 0.0
        for row in s_rows:
            sum_sales += row[4]
            self.tree_sales.insert("", "end", values=row)
            
        # 3. شحن المخزن
        for r in self.tree_inv.get_children(): self.tree_inv.delete(r)
        cursor.execute("SELECT id, part_name, quantity, cost_price, last_updated FROM inventory ORDER BY quantity ASC")
        i_rows = cursor.fetchall()
        for row in i_rows:
            self.tree_inv.insert("", "end", values=row)
            
        conn.close()
        
        # تحديث لوحة الأرباح
        self.maint_revenue_lbl.configure(text=f"{LANGUAGES[self.current_language]['maint_revenue']} : {sum_maint:.3f} TND")
        self.sales_revenue_lbl.configure(text=f"{LANGUAGES[self.current_language]['sales_revenue']} : {sum_sales:.3f} TND")
        self.total_revenue_lbl.configure(text=f"{LANGUAGES[self.current_language]['total_revenue']} : {sum_maint + sum_sales:.3f} TND")

if __name__ == "__main__":
    app = WorkshopApp()
    app.mainloop()
