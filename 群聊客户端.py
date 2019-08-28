from socket import *
from tkinter import *
import json


def getip():
    myname = getfqdn(gethostname())
    myaddr = gethostbyname(myname)
    return myaddr


def main_root():  # 主界面
    # get_ip_mac()
    root_main = Tk()
    root_main.geometry('500x500')
    button_login = Button(text='登录', command=login_root)
    button_login.pack()
    button_user_register = Button(text='用户注册', command=user_register_root)
    button_user_register.pack()
    button_forget_pwd = Button(text='忘记密码', command=forget_pwd_root)
    button_forget_pwd.pack()
    button_exit = Button(text='退出', command=exit_process)
    button_exit.pack()
    mainloop()


def login_root():  # 创建群聊界面
    login_root1 = Tk()
    login_root1.geometry('500x500')
    uid_label = Label(login_root1, text='账号:')
    uid_label.pack()
    uid_entry = Entry(login_root1)
    uid_entry.pack()
    pwd_label = Label(login_root1, text='密码:')
    pwd_label.pack()
    pwd_entry = Entry(login_root1)
    pwd_entry.pack()
    button_enter = Button(login_root1, text='确认',
                          command=lambda: login(uid_entry, pwd_entry))
    button_enter.pack()
    button_cancel = Button(login_root1, text='取消', command=exit_process)
    button_cancel.pack()
    mainloop()
    # print(cname, uip)


def login(uid_entry, pwd_entry):
    uip = getip()
    send_data({'uip': uip, 'command': '1', 'uid': uid_entry.get(), 'pwd': pwd_entry.get()})


def user_register_root():
    root_register1 = Tk()
    root_register1.geometry('500x500')
    name_label = Label(root_register1, text='昵称:')
    name_label.pack()
    uname_entry = Entry(root_register1)
    uname_entry.pack()
    pwd_label = Label(root_register1, text='密码:')
    pwd_label.pack()
    pwd_entry = Entry(root_register1)
    pwd_entry.pack()
    pwd_label2 = Label(root_register1, text='再次输入密码:')
    pwd_label2.pack()
    pwd_entry2 = Entry(root_register1)
    pwd_entry2.pack()
    QQ_label2 = Label(root_register1, text='QQ号码:')
    QQ_label2.pack()
    QQ_entry2 = Entry(root_register1)
    QQ_entry2.pack()
    button_enter = Button(root_register1, text='确认',
                          command=lambda: register(uname_entry, pwd_entry, pwd_entry2, QQ_entry2))
    button_enter.pack()
    button_cancel = Button(root_register1, text='取消', command=exit_process)
    button_cancel.pack()
    mainloop()


def register(uname_entry, pwd_entry, pwd_entry2, QQ_entry2):
    if pwd_entry.get() == pwd_entry2.get():
        send_data({'command': '2', 'qqid': QQ_entry2.get(), 'pwd': pwd_entry.get(), 'uname': '龙成'})
    else:
        print('两次密码不一致!!!')


def forget_pwd_root():
    forget_pwd_root1 = Tk()
    forget_pwd_root1.geometry('500x500')
    QQ_label2 = Label(forget_pwd_root1, text='QQ号码:')
    QQ_label2.pack()
    QQ_entry2 = Entry(forget_pwd_root1)
    QQ_entry2.pack()
    button_enter = Button(forget_pwd_root1, text='确认', command=lambda: forget_pwd(QQ_entry2.get()))
    button_enter.pack()
    button_cancel = Button(forget_pwd_root1, text='取消', command=exit_process)
    button_cancel.pack()
    mainloop()


def forget_pwd_root2(uid):
    forget_pwd_root2 = Tk()
    forget_pwd_root2.geometry('500x500')
    pwd_label2 = Label(forget_pwd_root2, text='新密码:')
    pwd_label2.pack()
    pwd_entry2 = Entry(forget_pwd_root2)
    pwd_entry2.pack()
    pwd_label3 = Label(forget_pwd_root2, text='再次输入密码:')
    pwd_label3.pack()
    pwd_entry3 = Entry(forget_pwd_root2)
    pwd_entry3.pack()
    button_enter = Button(forget_pwd_root2, text='确认', command=lambda: forget_pwd2(pwd_entry2.get(), pwd_entry3.get(),uid))
    button_enter.pack()
    button_cancel = Button(forget_pwd_root2, text='取消', command=exit_process)
    button_cancel.pack()
    mainloop()


def forget_pwd(qqid):
    print(qqid)
    data = {'qqid': qqid, 'command': '3'}
    send_data(data)


def forget_pwd2(pwd, pwd2,uid):
    if pwd == pwd2:
        data = {'pwd': pwd, 'command': '3.1','uid':uid}
        send_data(data)
    else:
        print('两次密码不一致!!')


def add_friend():
    pass


def change_friendadd():
    pass


def del_friendadd():
    pass


def chat_main_root():
    chat_main_root2 = Tk()
    chat_main_root2.geometry('600x800+100+100')
    button_add_friendadd = Button(chat_main_root2, text='添加好友', command=lambda: add_friend())
    button_add_friendadd.pack()
    button_del_friendadd = Button(chat_main_root2, text='删除好友', command=lambda: del_friendadd())
    button_del_friendadd.pack()
    button_change_friendadd = Button(chat_main_root2, text='修改备注', command=lambda: change_friendadd())
    button_change_friendadd.pack()
    mainloop()


def show_uid(uid):
    show_uid_root = Tk()
    label_uid = Label(show_uid_root, text=uid)
    label_uid.pack()
    button_show_uid = Button(show_uid_root, text='密码修改成功确认记住账号', command=lambda: show_uid_root.destroy())
    button_show_uid.pack()


def send_data(data_send):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('192.168.42.214', 8090))
    data = json.dumps(data_send)
    data_en = data.encode('utf8')
    client_socket.send(data_en)
    recv_data1 = client_socket.recv(1024)
    recv_data = recv_data1.decode()
    data = json.loads(recv_data)
    print(data)
    client_socket.close()
    if data['command'] == '1':
        pwd = data['pwd']
        if pwd:
            print('成功登录!!')
            chat_main_root()
        else:
            print('账号密码错误!!')
    elif data['command'] == '2':
        uid = data['uid']
        if uid:
            print('注册成功!!')

            show_uid(uid)
        else:
            print('注册信息有误!!')
    elif data['command'] == '3':
        if data['uid']:
            print('验证成功!!')
            uid = data['uid']
            forget_pwd_root2(uid)
        else:
            print('验证失败!!')
    elif data['command'] == '3.1':
        if data['pwd']:
            print('密码修改成功!!')
            print(data)
            uid = data['uid']
            show_uid(uid)
        else:
            print('修改失败!!')


def data_processing(recv_data):
    print(recv_data)


# send_data({'command': '1'})


def exit_process():
    exit()


if __name__ == '__main__':
    main_root()
