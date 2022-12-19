import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.inventory = [[None for i in range(7)] for j in range(15)]
        self.path = '/html/body/blockquote/table/tbody/tr[{}]/td[{}]/input'
        self.selected = []
        self.username = ''
        self.password = ''
        self.num = 0
        self.week = 0
        self.geometry("800x900")
        self.title(
            'Automatic laundry reservation for Lahden Talot student residents')
        self.resizable(0, 0)
        self.browser = None

        # status bar
        status = tk.Text(self, height=1, width=50)
        status.grid(column=0, row=21,
                    padx=5, pady=5, columnspan=8)
        status.tag_configure("center", justify='center')
        status.insert(tk.END, "READY")
        status.tag_add("center", 1.0, "end")

        def change_status(message):
            status.delete(1.0, tk.END)
            status.insert(tk.END, message)
            status.tag_add("center", 1.0, "end")

        def next_week(week):
            if week == 0:
                pass
            else:
                for j in range(week):
                    self.browser.find_element(
                        By.XPATH, '/html/body/blockquote/table/tbody/tr[1]/td[7]/input').click()

        # blank 3rd row
        for i in range(7):
            ttk.Label(self, text=" ").grid(
                column=i+1, row=3, padx=45, pady=10)

        # username
        username_label = ttk.Label(self, text="Username:")
        username_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        username_entry = ttk.Entry(self)
        username_entry.grid(column=1, row=1, sticky=tk.W,
                            padx=5, pady=5, columnspan=3)

        # password
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        password_entry = ttk.Entry(self,  show="*")
        password_entry.grid(column=1, row=2, sticky=tk.W,
                            padx=5, pady=5, columnspan=3)

        # labels
        user = ttk.Label(self, text="Username and Password will NOT be saved")
        user.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5, columnspan=5)
        days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i, day in enumerate(days):
            ttk.Label(self, text=day).grid(
                column=i+1, row=4, padx=5, pady=5)
        hours = ['7:00 - 8:00', '8:00 - 9:00', '9:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00',
                 '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00', '20:00 - 21:00', '21:00 - 22:00']
        for i, hour in enumerate(hours):
            ttk.Label(self, text=hour).grid(
                column=0, row=i+5, padx=5, pady=5)
        num_weeks = ttk.Label(self, text="Number of weeks to book:")
        num_weeks.grid(column=4, row=1, sticky=tk.W,
                       padx=5, pady=5, columnspan=2)
        num_entry = ttk.Entry(self, width=5)
        num_entry.grid(column=6, row=1, sticky=tk.W,
                       padx=5, pady=5)

        # each time slot has a button

        def book(i, j):
            if self.inventory[i][j]['text'] == 'Free':
                self.inventory[i][j]['text'] = 'Added'
                self.inventory[i][j]['bg'] = 'red'
                self.selected.append((i, j))
            else:
                self.inventory[i][j]['text'] = 'Free'
                self.inventory[i][j]['bg'] = 'green'
                self.selected.remove((i, j))
        for i in range(15):
            for j in range(7):
                self.inventory[i][j] = tk.Button(
                    self, text="Free", bg='green', command=lambda i=i, j=j: book(i, j))
                self.inventory[i][j].grid(column=j+1, row=i+5, padx=5, pady=5)

        # reset button

        def reset():
            for i in range(15):
                for j in range(7):
                    self.inventory[i][j]['text'] = 'Free'
                    self.inventory[i][j]['bg'] = 'green'
                    self.inventory[i][j]['state'] = 'normal'
            self.selected = []
            self.username = ''
            self.password = ''
            self.num = 0
            self.week = 0
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            num_entry.delete(0, 'end')
            change_status("READY")
            confirm['text'] = 'Confirm'
            confirm['state'] = 'disabled'
            start_button['state'] = 'normal'
        reset_button = tk.Button(
            self, text="RESET", command=reset, bg='red')
        reset_button.grid(column=4, row=2, sticky=tk.W, padx=5, pady=5)

        def start():
            self.username = username_entry.get()
            self.password = password_entry.get()
            try:
                self.num = int(num_entry.get())
            except ValueError:
                change_status("Please enter a valid number!")
                return
            if self.username == '' or self.password == '' or self.num == 0:
                change_status("Please fill in all the fields!")
            elif len(self.selected) == 0:
                change_status("Please select at least one time slot!")
            else:
                confirm['state'] = 'normal'
                change_status("Please confirm your booking!")
        start_button = tk.Button(
            self, text="START", command=start, bg='blue')
        start_button.grid(column=5, row=2, sticky=tk.W, padx=5, pady=5)

        def execute():
            self.browser = webdriver.Chrome()
            confirm['state'] = 'disabled'
            for i in range(15):
                for j in range(7):
                    self.inventory[i][j]['state'] = 'disabled'
            start_button['state'] = 'disabled'
            confirm['text'] = 'Working...'
            change_status("Logging in...")
            try:
                self.browser.get("http://extranet.oppilastalo.fi/")
            except Exception:
                change_status("Connection error.")
                confirm['text'] = "Error"
                return
            self.browser.find_element(By.XPATH,
                                      '/html/body/div/form/table/tbody/tr[3]/td[2]/input').send_keys(self.username)
            self.browser.find_element(By.XPATH,
                                      '/html/body/div/form/table/tbody/tr[4]/td[2]/input').send_keys(self.password)
            self.browser.find_element(By.XPATH,
                                      '/html/body/div/form/table/tbody/tr[5]/td[1]/input').click()
            try:
                self.browser.find_element(By.XPATH, '/html/body/center/div[1]')
            except Exception:
                pass
            else:
                change_status("Wrong username or password.")
                confirm['text'] = "Error"
                return
            change_status("Logged in.")
            self.browser.find_element(By.XPATH,
                                      '/html/body/code/a[4]').click()
            while self.week < self.num:
                for i in range(len(self.selected)):
                    change_status("Booking a slot...")
                    try:
                        self.browser.find_element(By.XPATH, self.path.format(
                            self.selected[i][0]+3, self.selected[i][1]+2)).click()
                        self.browser.find_element(By.XPATH,
                                                  '/html/body/blockquote/submenu/blockquote/input[1]').click()
                        change_status("Booking successful.")
                        self.browser.find_element(By.XPATH,
                                                  '/html/body/code/a[4]').click()
                        next_week(self.week)
                    except Exception:
                        change_status("Booking failed.")
                        continue
                self.week += 1
                next_week(1)
            self.browser.close()

        # confirm button
        confirm = tk.Button(self, text="Confirm", bg="yellow", command=execute)
        confirm['state'] = 'disabled'
        confirm.grid(column=0, row=22,
                     padx=5, pady=5, columnspan=8)


if __name__ == "__main__":
    app = App()
    app.mainloop()
