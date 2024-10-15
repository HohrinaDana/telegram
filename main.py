from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
class Post:
    def __init__(self, user: User, post: str):
        self.user = user
        self.post = post
        self.likes_count = 0
        self.comments = []
        self.timestamp = datetime.now()

    def add_like(self):
        self.likes_count += 1

    def add_comment(self, user: User, comment: str):
        self.comments.append(user.username + ': ' + comment)

    def __str__(self):
        return self.user.username + ': ' + self.post + '  ' + str(self.timestamp.strftime("%H:%M")) + ' ❤️' + str(self.likes_count) + ' Комментарии: ' + str(self.comments)

all_posts = []
current_user = None

def logIn():
    global current_user
    username = login_entry.get()
    password = password_entry.get()
    if username and password:
        current_user = User(username, password)
        messagebox.showinfo("Вход", "Вход выполнен как " + current_user.username)
        update_post()
        post_entry.config(state='normal')
        password_entry.delete(0, 'end') #удаление пароля
    else:
        messagebox.showinfo("Ошибка", "Введите логин и пароль")

def logOut():
    global current_user
    current_user = None
    post_entry.config(state='disabled')
    posts_listbox.delete(0, 'end')
    messagebox.showinfo("Выход", "Вы вышли из системы")

def publish_post():
    if current_user:
        new_post = Post(current_user, post_entry.get())
        all_posts.append(new_post)
        update_post()
        post_entry.delete(0, 'end')
    else:
        messagebox.showinfo("Ошибка", "Войдите в систему")

def update_post():
    posts_listbox.delete(0, 'end')
    for post in all_posts:
        posts_listbox.insert('end', str(post))

def like_post():
    post_index = posts_listbox.curselection() #кортеж с индексами выбранных элементов
    if post_index:
        all_posts[post_index[0]].add_like()
        update_post()
    else:
        messagebox.showinfo("Ошибка", "Выберите пост для лайка")

def comment_post():
    if current_user:
        post_index = posts_listbox.curselection()
        comment_text = comment_entry.get()
        if post_index and comment_text:
            all_posts[post_index[0]].add_comment(current_user, comment_text)
            comment_entry.delete(0, 'end')
            update_post()
        else:
            messagebox.showinfo("Ошибка", "Выберите пост и введите комментарий")
    else:
        messagebox.showinfo("Ошибка", "Войдите в систему")


root = Tk()
root.title('Telegramm')
root.geometry('600x700')
tab_control = ttk.Notebook(root) # вкладки

login_tab = ttk.Frame(tab_control)
tab_control.add(login_tab, text='Вход')

ttk.Label(login_tab, text='Логин:').pack()
login_entry = ttk.Entry(login_tab)
login_entry.pack()

ttk.Label(login_tab, text='Пароль:').pack()
password_entry = ttk.Entry(login_tab, show="*")
password_entry.pack()

ttk.Button(login_tab, text='Вход', command=logIn).pack()
ttk.Button(login_tab, text='Выход', command=logOut).pack()

post_tab = ttk.Frame(tab_control)
tab_control.add(post_tab, text='Посты')

ttk.Label(post_tab, text='Пост').pack()
post_entry = ttk.Entry(post_tab, width=50, state='disabled')
post_entry.pack()

ttk.Button(post_tab, text='Опубликовать', command=publish_post).pack()

ttk.Label(post_tab, text='Все посты:').pack()
posts_listbox = Listbox(post_tab, width=50, height=10)
posts_listbox.pack()

ttk.Button(post_tab, text='❤', command=like_post).pack()

ttk.Label(post_tab, text='Написать комментарий:').pack()
comment_entry = ttk.Entry(post_tab, width=50)
comment_entry.pack()

ttk.Button(post_tab, text='Комментировать', command=comment_post).pack()

tab_control.pack(expand=1, fill='both') # растягивает

root.mainloop()