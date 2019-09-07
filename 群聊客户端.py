from socket import *
from tkinter import *
import json
from time import sleep

serve_ip = '192.168.42.29'
serve_port = 8090


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


def login_root():  #
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
    global myid
    uip = getip()
    myid = uid_entry.get()
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
        send_data({'command': '2', 'qqid': QQ_entry2.get(), 'pwd': pwd_entry.get(), 'uname': uname_entry.get()})
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
    button_enter = Button(forget_pwd_root2, text='确认',
                          command=lambda: forget_pwd2(pwd_entry2.get(), pwd_entry3.get(), uid))
    button_enter.pack()
    button_cancel = Button(forget_pwd_root2, text='取消', command=exit_process)
    button_cancel.pack()
    mainloop()


def forget_pwd(qqid):
    print(qqid)
    data = {'qqid': qqid, 'command': '3'}
    send_data(data)


def forget_pwd2(pwd, pwd2, uid):
    if pwd == pwd2:
        data = {'pwd': pwd, 'command': '3.1', 'uid': uid}
        send_data(data)
    else:
        print('两次密码不一致!!')


def add_friend_root1():
    add_friend_root2 = Tk()
    add_friend_root2.geometry('600x800')
    uid_label = Label(add_friend_root2, text='id或昵称:')
    uid_label.pack()
    uid_entry = Entry(add_friend_root2)
    uid_entry.pack()
    button_enter = Button(add_friend_root2, text='确认',
                          command=lambda: add_friend_show(uid_entry.get()))
    button_enter.pack()
    button_cancel = Button(add_friend_root2, text='取消', command=exit_process)
    button_cancel.pack()
    mainloop()


def add_friend_show(fid):
    data = {'command': '4', 'fid': fid}
    send_data(data)


def add_friend(event):
    print(event.widget)
    fid = eval(event.widget['text'])[0]
    print(fid)

    add_friend_fname_root = Tk()
    add_friend_fname_root.geometry('100x100+100+100')
    entry_fname = Entry(add_friend_fname_root)
    entry_fname.pack()
    button_fname = Button(add_friend_fname_root, text='确定', command=lambda: add_friend_send_data(fid, entry_fname))
    button_fname.pack()
    mainloop()


def add_friend_send_data(fid, entry_fname):
    fname = entry_fname.get()
    uid = myid
    data = {'command': '4.1', 'fid': fid, 'uid': uid, 'fname': fname}
    send_data(data)


def change_friendadd():
    pass


def del_friendadd():
    pass


def del_user_inf():
    uid = myid
    data = {'command': '5', 'uid': uid}
    send_data(data)


def chat_main_root():
    chat_main_root2 = Tk()
    chat_main_root2.geometry('600x800+100+100')
    button_add_friendadd = Button(chat_main_root2, text='添加好友', command=lambda: add_friend_root1())
    button_add_friendadd.pack()
    button_del_friendadd = Button(chat_main_root2, text='注销账户', command=lambda: del_user_inf())
    button_del_friendadd.pack()



    mainloop()


def show_uid(uid):
    show_uid_root = Tk()
    label_uid = Label(show_uid_root, text=uid)
    label_uid.pack()
    button_show_uid = Button(show_uid_root, text='密码修改成功确认记住账号', command=lambda: show_uid_root.destroy())
    button_show_uid.pack()


def add_friend_show_root(show_list):
    add_friend_show_root2 = Tk()
    add_friend_show_root2.geometry('900x900+100+100')
    a = 0
    for i in show_list:
        print(i)
        print(type(i))
        if i[0] == str(myid):
            continue
        a += 1
        lable_show_add_friend = Label(add_friend_show_root2, text='{}'.format(i))
        lable_show_add_friend.bind('<ButtonRelease-1>', add_friend)
        lable_show_add_friend.place(x=20, y=20 * a)
    mainloop()


def send_data(data_send):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((serve_ip, serve_port))
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
    elif data['command'] == '4':
        if data['f1'] or data['f2']:
            list_show = list(data['f2'])
            for i in data['f1']:
                list_show.append(i)
        else:
            list_show = ''
        add_friend_show_root(list_show)
    elif data['command'] == '4.1':
        if data['fid']:
            print('添加成功!!')
        else:
            print('添加失败!!')
    elif data['command'] == '5':
        if data['uid']:
            print('账号已注销!!')
            sleep(1)
            exit_process()
    elif data['command'] =='6':
        pass


def data_processing(recv_data):
    print(recv_data)


# send_data({'command': '1'})


def exit_process():
    exit()


if __name__ == '__main__':
    main_root()
