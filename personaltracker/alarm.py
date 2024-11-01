import os
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import plyer
import sqlite3
import threading
import time

class Database:
    def __init__(self, db_name='user_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        
        # Create reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                description TEXT,
                time DATETIME,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Create tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                description TEXT,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()

    def register_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                           (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                       (username, password))
        return cursor.fetchone() is not None

    def add_reminder(self, user_id, title, description, reminder_time):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (user_id, title, description, time) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, title, description, reminder_time))
        self.conn.commit()

    def add_task(self, user_id, title, description):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (user_id, title, description) 
            VALUES (?, ?, ?)
        ''', (user_id, title, description))
        self.conn.commit()

class LoginScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        layout = BoxLayout(orientation='vertical', padding=50, spacing=10)
        
        self.username_input = TextInput(multiline=False, hint_text='Username')
        self.password_input = TextInput(multiline=False, hint_text='Password', password=True)
        
        login_button = Button(text='Login', on_press=self.login)
        register_button = Button(text='Register', on_press=self.register)
        
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(register_button)
        
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        
        if self.db.authenticate_user(username, password):
            # Switch to main app screen
            self.manager.current = 'main'
        else:
            # Show error (could use a popup in a real app)
            print("Login Failed")

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        
        if self.db.register_user(username, password):
            # Switch to main app screen or show success message
            self.manager.current = 'main'
        else:
            # Show error (could use a popup in a real app)
            print("Registration Failed")

class MainScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        layout = BoxLayout(orientation='vertical', padding=50, spacing=10)
        
        # Alarm Setting
        alarm_layout = BoxLayout(orientation='horizontal')
        self.alarm_input = TextInput(multiline=False, hint_text='Set Alarm Time (HH:MM)')
        set_alarm_button = Button(text='Set Alarm', on_press=self.set_alarm)
        alarm_layout.add_widget(self.alarm_input)
        alarm_layout.add_widget(set_alarm_button)
        layout.add_widget(alarm_layout)
        
        # Reminder Setting
        reminder_layout = BoxLayout(orientation='horizontal')
        self.reminder_title = TextInput(multiline=False, hint_text='Reminder Title')
        self.reminder_desc = TextInput(multiline=False, hint_text='Reminder Description')
        self.reminder_time = TextInput(multiline=False, hint_text='Reminder Time')
        add_reminder_button = Button(text='Add Reminder', on_press=self.add_reminder)
        reminder_layout.add_widget(self.reminder_title)
        reminder_layout.add_widget(self.reminder_desc)
        reminder_layout.add_widget(self.reminder_time)
        reminder_layout.add_widget(add_reminder_button)
        layout.add_widget(reminder_layout)
        
        # Task Setting
        task_layout = BoxLayout(orientation='horizontal')
        self.task_title = TextInput(multiline=False, hint_text='Task Title')
        self.task_desc = TextInput(multiline=False, hint_text='Task Description')
        add_task_button = Button(text='Add Task', on_press=self.add_task)
        task_layout.add_widget(self.task_title)
        task_layout.add_widget(self.task_desc)
        task_layout.add_widget(add_task_button)
        layout.add_widget(task_layout)
        
        self.add_widget(layout)
        
        # Start background notification thread
        threading.Thread(target=self.notification_thread, daemon=True).start()

    def set_alarm(self, instance):
        # Parse alarm time
        try:
            alarm_time = datetime.strptime(self.alarm_input.text, '%H:%M').time()
            # Schedule morning notification
            self.schedule_morning_notification(alarm_time)
        except ValueError:
            print("Invalid time format. Use HH:MM")

    def schedule_morning_notification(self, alarm_time):
        def send_morning_notification():
            plyer.notification.notify(
                title='Good Morning!',
                message='Have a wonderful day ahead!',
                timeout=10
            )

        def check_time():
            now = datetime.now().time()
            if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                send_morning_notification()
                # Additionally, check for breakfast notification at 11
                if now.hour == 11 and now.minute == 0:
                    plyer.notification.notify(
                        title='Breakfast Check',
                        message='I hope you have had breakfast!',
                        timeout=10
                    )

        # Schedule periodic check
        Clock.schedule_interval(lambda dt: check_time(), 60)  # Check every minute

    def add_reminder(self, instance):
        title = self.reminder_title.text
        desc = self.reminder_desc.text
        time = self.reminder_time.text
        
        # In a real app, you'd get the current user's ID
        user_id = 1  # Placeholder
        self.db.add_reminder(user_id, title, desc, time)
        
        # Optional: Send notification
        plyer.notification.notify(
            title='Reminder Added',
            message=f'{title}: {desc}',
            timeout=10
        )

    def add_task(self, instance):
        title = self.task_title.text
        desc = self.task_desc.text
        
        # In a real app, you'd get the current user's ID
        user_id = 1  # Placeholder
        self.db.add_task(user_id, title, desc)
        
        # Optional: Send notification
        plyer.notification.notify(
            title='Task Added',
            message=f'{title}: {desc}',
            timeout=10
        )

    def notification_thread(self):
        # This method can be expanded to handle more complex notification logic
        while True:
            time.sleep(60)  # Check every minute
            # Add any background notification checks here

class PersonalAssistantApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()

    def build(self):
        # Create screen manager
        sm = ScreenManager()
        
        # Create screens
        login_screen = LoginScreen(self.db, name='login')
        main_screen = MainScreen(self.db, name='main')
        
        # Add screens to screen manager
        sm.add_widget(login_screen)
        sm.add_widget(main_screen)
        
        return sm

if __name__ == '__main__':
    PersonalAssistantApp().run()