#Nama   : DODI WIJAYA
#NIM    : F1D02310047
#Kelas  : Pemrograman Visual D

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame, QStackedWidget, 
                             QPushButton, QSizePolicy, QLineEdit, QDateEdit, 
                             QRadioButton, QMessageBox, QTextBrowser, QTextEdit,
                             QGridLayout)
from PySide6.QtCore import Qt, Signal, QDate, QObject

class FormSignals(QObject):
    step_changed = Signal(int)

global_signals = FormSignals()

class StepIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.steps = []
        self.init_ui()

    def init_ui(self):
        self.root_layout = QGridLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)

        self.line_container = QWidget()
        line_lay = QHBoxLayout(self.line_container)
        
        line_lay.setContentsMargins(60, 14, 60, 0) 
        line_lay.setSpacing(0)
        line_lay.setAlignment(Qt.AlignTop)
        
        self.prog_line = QFrame()
        self.prog_line.setFixedHeight(3)
        self.prog_line.setStyleSheet("background-color: #2ecc71; border: none;")
        self.prog_line.setFixedWidth(0)
        
        self.base_line = QFrame()
        self.base_line.setFixedHeight(3)
        self.base_line.setStyleSheet("background-color: #bdc3c7; border: none;")
        
        line_lay.addWidget(self.prog_line)
        line_lay.addWidget(self.base_line)
        self.root_layout.addWidget(self.line_container, 0, 0, Qt.AlignTop)

        top_widget = QWidget()
        top_widget.setStyleSheet("background: transparent;")
        self.steps_layout = QHBoxLayout(top_widget)
        self.steps_layout.setContentsMargins(30, 0, 30, 0)
        self.steps_layout.setAlignment(Qt.AlignTop)

        labels = ["Data Pribadi", "Kontak", "Akun"]
        for i, text in enumerate(labels):
            unit = QWidget()
            u_layout = QVBoxLayout(unit)
            u_layout.setContentsMargins(0, 0, 0, 0)
            u_layout.setSpacing(2)
            u_layout.setAlignment(Qt.AlignTop)

            circle = QLabel(str(i + 1))
            circle.setFixedSize(30, 30)
            circle.setAlignment(Qt.AlignCenter)
            circle.setStyleSheet("background-color: #bdc3c7; color: white; border-radius: 15px; font-weight: bold;")
            
            txt_label = QLabel(text)
            txt_label.setAlignment(Qt.AlignCenter)
            txt_label.setFixedWidth(60)
            txt_label.setStyleSheet("font-size: 10px; color: #7f8c8d; border: none;")

            u_layout.addWidget(circle, 0, Qt.AlignCenter)
            u_layout.addWidget(txt_label, 0, Qt.AlignCenter)
            
            self.steps_layout.addWidget(unit)
            self.steps.append((circle, txt_label))
            
            if i < len(labels) - 1:
                self.steps_layout.addStretch(1)

        self.root_layout.addWidget(top_widget, 0, 0, Qt.AlignTop)
        self.set_step(0)

    def set_step(self, index):
        total_w = self.width() - 120
        
        if index == 0: w = 0
        elif index == 1: w = total_w / 2
        else: w = total_w
        
        self.prog_line.setFixedWidth(max(0, int(w)))

        for i, (circle, txt) in enumerate(self.steps):
            if i < index: 
                circle.setText("✓")
                circle.setStyleSheet("background-color:#2ecc71; color:white; border-radius:15px; font-weight:bold;")
                txt.setStyleSheet("color:#2ecc71; font-weight:bold; font-size:10px;")
            elif i == index: 
                circle.setText(str(i+1))
                circle.setStyleSheet("background-color:#3498db; color:white; border-radius:15px; font-weight:bold;")
                txt.setStyleSheet("color:#3498db; font-weight:bold; font-size:10px;")
            else: 
                circle.setText(str(i+1))
                circle.setStyleSheet("background-color:#bdc3c7; color:white; border-radius:15px; font-weight:bold;")
                txt.setStyleSheet("color:#7f8c8d; font-size:10px;")

class BaseForm(QWidget):
    valid_changed = Signal(bool)
    def set_style(self, widget, status):
        color = "#2ecc71" if status == 'valid' else ("orange" if status == 'invalid' else "#dcdde1")
        widget.setStyleSheet(f"border: 2px solid {color}; padding: 4px; border-radius: 4px; color: black; background-color: white;")

class data_pribadi(BaseForm):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(2) 
        self.nama = QLineEdit(); self.nama.setPlaceholderText("Nama Lengkap")
        self.tgl = QDateEdit(QDate.currentDate()); self.tgl.setCalendarPopup(True)
        self.lk = QRadioButton("Laki-laki"); self.pr = QRadioButton("Perempuan")
        layout.addWidget(QLabel("<b>Step 1: Data Pribadi</b>"))
        layout.addWidget(QLabel("Nama:")); layout.addWidget(self.nama)
        layout.addWidget(QLabel("Tanggal Lahir:")); layout.addWidget(self.tgl)
        layout.addWidget(QLabel("Jenis Kelamin:")); layout.addWidget(self.lk); layout.addWidget(self.pr)
        layout.addStretch()
        self.nama.textChanged.connect(self.validate)
        self.lk.toggled.connect(self.validate); self.pr.toggled.connect(self.validate)

    def validate(self):
        ok = len(self.nama.text().strip()) > 0 and (self.lk.isChecked() or self.pr.isChecked())
        self.set_style(self.nama, 'valid' if len(self.nama.text()) > 0 else 'neutral')
        self.valid_changed.emit(ok); return ok

class kontak(BaseForm):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(2) 
        self.email = QLineEdit(); self.telp = QLineEdit(); self.addr = QTextEdit()
        self.email.setPlaceholderText("budi@email.com"); self.telp.setPlaceholderText("08123456")
        self.addr.setFixedHeight(30) 
        
        layout.addWidget(QLabel("<b>Step 2: Informasi Kontak</b>"))
        layout.addWidget(QLabel("Email")); layout.addWidget(self.email)
        layout.addWidget(QLabel("Telepon")); layout.addWidget(self.telp)
        
        self.warn = QLabel("⚠ Nomor minimal 10 digit")
        self.warn.setStyleSheet("color: orange; font-size: 9px;")
        self.warn.hide() 
        layout.addWidget(self.warn)
        
        layout.addWidget(QLabel("Alamat")); layout.addWidget(self.addr)
        layout.addStretch()
        
        self.email.textChanged.connect(self.validate)
        self.telp.textChanged.connect(self.validate)
        self.addr.textChanged.connect(self.validate)

    def validate(self):
        e_ok = "@" in self.email.text() and "." in self.email.text()
        t_ok = self.telp.text().isdigit() and len(self.telp.text()) >= 10
        a_ok = len(self.addr.toPlainText().strip()) > 5
        self.set_style(self.email, 'valid' if e_ok else ('invalid' if self.email.text() else 'neutral'))
        self.set_style(self.telp, 'valid' if t_ok else ('invalid' if self.telp.text() else 'neutral'))
        self.set_style(self.addr, 'valid' if a_ok else 'neutral')
        if len(self.telp.text()) == 0:
            self.warn.hide()
        elif len(self.telp.text()) < 10:
            self.warn.show()
        else:
            self.warn.hide()
        ok = e_ok and t_ok and a_ok
        self.valid_changed.emit(ok); return ok

class akun(BaseForm):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(2) 
        self.user = QLineEdit(); self.pw = QLineEdit(); self.cp = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password); self.cp.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("<b>Step 3: Akun</b>"))
        layout.addWidget(QLabel("Username")); layout.addWidget(self.user)
        layout.addWidget(QLabel("Password")); layout.addWidget(self.pw)
        layout.addWidget(QLabel("Konfirmasi Password")); layout.addWidget(self.cp)
        layout.addStretch()
        self.user.textChanged.connect(self.validate); self.pw.textChanged.connect(self.validate); self.cp.textChanged.connect(self.validate)

    def validate(self):
        u_ok = len(self.user.text()) >= 4; p_ok = len(self.pw.text()) >= 6
        c_ok = self.cp.text() == self.pw.text() and p_ok
        self.set_style(self.user, 'valid' if u_ok else 'neutral')
        self.set_style(self.pw, 'valid' if p_ok else 'neutral')
        self.set_style(self.cp, 'valid' if c_ok else ('invalid' if self.cp.text() else 'neutral'))
        ok = u_ok and p_ok and c_ok
        self.valid_changed.emit(ok); return ok

class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form Registrasi")
        self.setFixedSize(450, 350) 
        self.current_step = 0

        main_widget = QWidget(); self.setCentralWidget(main_widget)
        self.container_layout = QVBoxLayout(main_widget)
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container_layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(75) 
        header.setStyleSheet("background-color:#edf2f6; border-bottom:1px solid #dcdde1;")
        self.indicator = StepIndicator()
        h_lay = QVBoxLayout(header)
        h_lay.setContentsMargins(0, 10, 0, 0) 
        h_lay.addWidget(self.indicator)
        self.container_layout.addWidget(header)

        self.body_frame = QFrame()
        self.body_frame.setStyleSheet("background-color: white;")
        self.body_layout = QVBoxLayout(self.body_frame)
        self.body_layout.setContentsMargins(30, 10, 30, 0) 
        self.stack = QStackedWidget()
        self.s1, self.s2, self.s3, self.review = data_pribadi(), kontak(), akun(), QTextBrowser()
        for s in [self.s1, self.s2, self.s3, self.review]: self.stack.addWidget(s)
        self.body_layout.addWidget(self.stack)
        self.container_layout.addWidget(self.body_frame, 1)

        footer = QWidget()
        footer.setStyleSheet("background-color: white;")
        footer.setFixedHeight(45) 
        f_lay = QHBoxLayout(footer)
        f_lay.setContentsMargins(30, 0, 30, 5) 
        self.btn_back = QPushButton("← Kembali"); self.btn_next = QPushButton("Lanjut →")
        self.btn_next.setObjectName("primaryBtn") 
        f_lay.addWidget(self.btn_back); f_lay.addStretch(); f_lay.addWidget(self.btn_next)
        self.container_layout.addWidget(footer)

        self.info = QLabel()
        self.info.setText("Step 1 dari 3 — Lengkapi semua field untuk melanjutkan")
        self.info.setStyleSheet("color:#7f8c8d; font-size:10px; background-color:#edf2f6; padding: 5px 30px; border-top:1px solid #dcdde1;")
        self.container_layout.addWidget(self.info)

        self.btn_next.clicked.connect(self.go_next); self.btn_back.clicked.connect(self.go_back)
        self.s1.valid_changed.connect(self.btn_next.setEnabled)
        self.s2.valid_changed.connect(self.btn_next.setEnabled)
        self.s3.valid_changed.connect(self.btn_next.setEnabled)
        global_signals.step_changed.connect(self.handle_step_change)
        self.update_ui()

    def handle_step_change(self, index):
        self.stack.setCurrentIndex(index)
        self.indicator.set_step(index)
        self.btn_back.setEnabled(index > 0)
        self.info.setText(f"Step {min(index+1, 3)} dari 3 — Lengkapi semua field untuk melanjutkan")
        
        if index == 3:
            self.btn_next.setText("Submit")
            self.btn_next.setEnabled(True)
            
            jk = "Laki-laki" if self.s1.lk.isChecked() else "Perempuan"
            html_review = f"""
            <h4 style='color:#2c3e50; margin-top:0;'>Ringkasan Data</h4>
            <b>Nama Lengkap     :</b> {self.s1.nama.text()}<br>
            <b>Tanggal Lahir    :</b> {self.s1.tgl.date().toString('dd-MM-yyyy')}<br>
            <b>Jenis Kelamin    :</b> {jk}<br>
            <b>Email            :</b> {self.s2.email.text()}<br>
            <b>Telpon           :</b> {self.s2.telp.text()}<br>
            <b>Alamat           :</b> {self.s2.addr.toPlainText()}<br>
            <b>Username         :</b> {self.s3.user.text()}
            """
            self.review.setHtml(html_review)
        else:
            self.btn_next.setText("Lanjut →")
            self.btn_next.setStyleSheet("background-color:#3498db;")
            self.stack.currentWidget().validate()

    def update_ui(self): global_signals.step_changed.emit(self.current_step)
    
    def go_next(self):
        if self.current_step < 3: self.current_step += 1; self.update_ui()
        else: QMessageBox.information(self, "Selesai", "Data berhasil didaftarkan!"); self.close()
        
    def go_back(self):
        if self.current_step > 0: self.current_step -= 1; self.update_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet("""
        * {
            font-family: Arial, sans-serif;
            font-size: 11px;
            color: #2c3e50;
        }
        
        /* Bulatan Indikator */
        QLabel[state="done"] { background-color: #3498db; color: white; border-radius: 15px; font-weight: bold; }
        QLabel[state="active"] { background-color: #3498db; color: white; border-radius: 15px; font-weight: bold; }
        QLabel[state="pending"] { background-color: #bdc3c7; color: white; border-radius: 15px; font-weight: bold; }
        
        /* Teks Indikator */
        QLabel[state="done"] { color: #3498db; font-weight: bold; background: transparent;}
        QLabel[state="active"] { color: #3498db; font-weight: bold; background: transparent;}
        QLabel[state="pending"] { color: #bdc3c7; font-weight: normal; background: transparent;}

        /* Input Form */
        QLineEdit, QDateEdit, QTextEdit { 
            background-color: white; border: 1px solid #bdc3c7; border-radius: 4px; padding: 4px;
        }
        
        /* Radio Button */
        QRadioButton { background: transparent; }
        QRadioButton::indicator { width: 12px; height: 12px; border-radius: 6px; border: 1px solid #bdc3c7; background: white; }
        QRadioButton::indicator:checked { background: #3498db; border: 3px solid white; }
        
        /* Tombol Kembali */
        QPushButton { 
            padding: 6px 15px; border-radius: 4px; background-color: #f1f2f6; border: 1px solid #bdc3c7; 
        }
        QPushButton:hover { background-color: #e2e6ea; }
        QPushButton:disabled { background-color: #fafafa; color: #bdc3c7; border: 1px solid #eeeeee; }
    """)
    
    win = RegistrationWindow()
    win.show()
    sys.exit(app.exec())