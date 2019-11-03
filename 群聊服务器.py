# 123456

from socket import *
from pymysql import *
from threading import *
from time import sleep
import json

serve_ip = '192.168.42.29'
serve_port = 8090
database_pwd = 'llc1993'


def server_create():  # 接收数据
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.bind((serve_ip, serve_port))
    tcp_server_socket.listen(1000)
    while 1:
        c_con, cip = tcp_server_socket.accept()
        t = Thread(target=data_recv, args=(c_con, cip))
        t.start()


def server_send_to(cip, c_con, send_data):
    tcp_server_socket = socket(AF_INET, SOCK_DGRAM)
    tcp_server_socket.bind((serve_ip, serve_port))

    data = json.dumps(send_data)

    data_en = data.encode('utf8')

    # data_json = '123'.encode('utf8')
    c_con.sendto(data_en, cip)
    tcp_server_socket.close()


def login(uid):  # 登录
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()

    try:
        cursor.execute("SELECT pwd FROM userinf where uid = '{}'".format(uid))
        row = cursor.fetchall()
        pwd = row[-1][0]
        con.commit()
        cursor.close()
        con.close()
    except:
        pwd = False
    return pwd


def change_user_state(uid, command, uip, c_con):  # 用户状态
    print(c_con)
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()
    cursor.execute("UPDATE chatuserid SET state = '{}' WHERE uid = '{}'".format(command, uid))
    cursor.execute("""UPDATE chatuserid SET con = "{}" WHERE uid = '{}'""".format(c_con, uid))
    cursor.execute("UPDATE userinf SET uip = '{}' WHERE uid = '{}'".format(uip, uid))
    con.commit()
    cursor.close()
    con.close()


def register(password, qqid, uname):  # 添加用户信息
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()
    try:
        cursor.execute("insert into chatuserid(Null_) values(null)")
        cursor.execute('select uid from chatuserid')
        row = cursor.fetchall()
        uid = row[-1][0]

        cursor.execute("create table  {}friends(fid int, fname varchar(10) not null)".format(uid))
        cursor.execute(
            "insert into userinf(uid, pwd, qqid, uname) values('{}','{}','{}','{}')".format(uid, password, qqid,
                                                                                            uname))
        con.commit()
        cursor.close()
        con.close()
    except:
        uid = False
    return uid


def fotget_pwd1(qqid):  # 添加用户信息
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()
    try:
        cursor.execute("select uid from userinf where qqid = '{}'".format(qqid))
        row = cursor.fetchall()
        uid = row[0][0]
        print(uid)

        con.commit()
        cursor.close()
        con.close()
    except:
        uid = False
    return uid


def fotget_pwd2(pwd, uid):  # 添加用户信息
    print(type(uid))
    print(pwd)
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()
    try:
        cursor.execute("UPDATE userinf SET pwd = '{}' WHERE uid = '{}'".format(pwd, uid))
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        print(e)
        uid = False
    return uid


def add_friend_show(uid):
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()
    try:
        cursor.execute("select uid,uname from userinf where uid = '{}'".format(uid))
        row = cursor.fetchall()
        list_search_uid = row
        print(list_search_uid)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        print(e)
        list_search_uid = False
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()
    try:
        cursor.execute("select uid,uname from userinf where uname like '%{}%'".format(uid))
        row = cursor.fetchall()
        list_search_name = row
        print(list_search_name)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        print(e)
        list_search_name = False
    return list_search_name, list_search_uid


def add_friend(uid, fid, fname):  # 用户添加好友 好友id 好友备注
    try:
        con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
        cursor = con.cursor()
        cursor.execute("insert into {}friends(fid, fname) values('{}','{}')".format((uid), fid, fname))
        con.commit()
        cursor.close()
        con.close()
    except:
        fid = False
    return fid


def server_dispose(data, cip, c_con):
    data = json.loads(data.decode('utf8'))
    # data_dict = dict(data.decode('utf8'))
    if data['command'] == '1':
        pwd = login(data['uid'])
        if pwd == False:
            pass
        else:
            if pwd == data['pwd']:
                pwd = True
                change_user_state(data['uid'], '1', data['uip'], c_con)
            else:
                pwd = False
        send_data = {'command': '1', 'pwd': pwd}
        server_send_to(cip, c_con, send_data)
    elif data['command'] == '2':
        password = data['pwd']
        qqid = data['qqid']
        uname = data['uname']
        uid = register(password, qqid, uname)
        send_data = {'command': '2', 'uid': uid}
        server_send_to(cip, c_con, send_data)
    elif data['command'] == '3':
        qqid = data['qqid']
        uid = fotget_pwd1(qqid)
        data = {'command': '3', 'uid': uid}
        server_send_to(cip, c_con, data)
    elif data['command'] == '3.1':
        pwd = data['pwd']
        uid = data['uid']
        print(uid)
        uid = fotget_pwd2(pwd, uid)
        data = {'command': '3.1', 'pwd': pwd, 'uid': uid}
        server_send_to(cip, c_con, data)
    elif data['command'] == '4':
        fid = data['fid']
        user_list1, user_list2 = add_friend_show(fid)
        data = {'command': '4', 'f1': user_list1, 'f2': user_list2}
        server_send_to(cip, c_con, data)
    elif data['command'] == '4.1':
        fid = data['fid']
        uid = data['uid']
        fname = data['fname']
        fid = add_friend(uid, fid, fname)
        data = {'command': '4.1', 'fid': fid}
        server_send_to(cip, c_con, data)
    elif data['command'] == '5':
        uid = data['uid']
        uid = del_user(uid)
        data = {'command': '5', 'uid': uid}
        server_send_to(cip, c_con, data)


def data_recv(c_con, cip):  # 接受数据处理
    data = c_con.recv(1024)
    # data = data.decode('utf8')
    sleep(0.02)
    server_dispose(data, cip, c_con)
    # c_con.close()


server_create()


# data_recv(c_con, cip)


# inf_dict = {'uid': '12345678', 'command': '1', 'uname': '龙城', 'msg': '你好吗', 'pwd': '', 'qqid': '', 'fid': '',
#             'fname': ''}
# str_json = json.dumps(inf_dict)
# print(str_json)
# server_dispose(str_json.encode('utf8'), '1')


# server_send_to('1', '2', '3', '4', '5', '6', '7', '8', '9')


# create_user('12345678', '979746262', 'longcheng')


def del_user(uid):  # 用户添加好友
    try:
        con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
        cursor = con.cursor()
        cursor.execute("drop table if exists {}friends".format((uid)))
        cursor.execute("Delete  From userinf Where uid = '{}'".format(uid))
        con.commit()
        cursor.close()
        con.close()
    except:
        uid = False
    return uid


def del_friend(uid, fid):  # 删除好友
    con = connect(host='localhost', port=3306, user='root', passwd=database_pwd, db='pythonclass')
    cursor = con.cursor()
    cursor.execute("Delete  From {}friends Where fid = '{}'".format(uid, fid))
    cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()


# add_friend_show('long')
# add_friend('8', '7', '123')
# if __name__ == '__main__':
#     main()
