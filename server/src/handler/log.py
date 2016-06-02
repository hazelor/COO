#!/usr/bin/python
#-*-coding:utf-8-*-
from base import base_handler
import tcelery
import tasks
import tornado


# tcelery.setup_nonblocking_producer()

class login_handler(base_handler):
    def get(self):
        self.render('login.html',
                    username_warning = '',
                    password_warning = '',
                    login_warning = '',
                    page_name = 'login')

    # @tornado.web.asynchronous
    def post(self):
        # self.set_secure_cookie("username", self.get_argument("username"))
        # self.redirect("/")

        # authentication operation
        username = self.get_argument('username')
        if username == '':
            self.render('login.html',
                    username_warning = '用户名不能为空',
                    password_warning = '',
                    login_warning = '',
                    page_name = 'login')
        else:
            password = self.get_argument('password')
            if password == '':
                self.render('login.html',
                        username_warning = '',
                        password_warning = '密码不能为空',
                        login_warning = '',
                        page_name = 'login')
            else:
                # tasks.user_check.apply_async(args=[username, password], callback=self.on_query_device)
                response = tasks.user_check(username, password)
                self.on_query_device(response)

    # def on_query_device(self, resp):
    #     if resp.result:
    #         username = self.get_argument('username')
    #         tasks.device_query.apply_async(args=[username], callback=self.on_success)
    #     else:
    #         self.render('login.html',
    #                 username_warning = '',
    #                 password_warning = '',
    #                 login_warning = '用户名或密码错误',
    #                 page_name = 'login')
    #         # print 'yes'
    #     # self.finish()
    def on_query_device(self, resp):
        if resp:
            username = self.get_argument('username')
            response = tasks.device_query(username)
            self.on_success(response)
        else:
            self.render('login.html',
                    username_warning = '',
                    password_warning = '',
                    login_warning = '用户名或密码错误',
                    page_name = 'login')
    # def on_success(self, resp):
    #     user_macaddress_member = ''
    #     for i in xrange(0,len(resp.result)):
    #         if i!=len(resp.result)-1:
    #             user_macaddress_member+=resp.result[i][0]+','
    #         else:
    #             user_macaddress_member+=resp.result[i][0]
    #     self.set_secure_cookie('username', user_macaddress_member)
    #     # print self.current_user
    #     self.redirect('/')
    def on_success(self, resp):
        user_macaddress_member = ''
        for i in xrange(0,len(resp)):
            if i!=len(resp)-1:
                user_macaddress_member+=resp[i][0]+','
            else:
                user_macaddress_member+=resp[i][0]
        self.set_secure_cookie('username', user_macaddress_member)
        # print self.current_user
        self.redirect('/')
    def on_connection_close(self):
        print 'login on_connection_close method called'


class logout_handler(base_handler):
    def get(self):
        pass
    def post(self):
        pass
