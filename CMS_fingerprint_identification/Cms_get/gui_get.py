import re,random,os,sys,openpyxl
import tkinter as tk
from time import time
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
pwd = (os.getcwd() + '/Cms_get/').replace('\\','/')
sys.path.append(pwd) #添加路径
from Cms_get import user_function_manage,fingerprint_database_manage,domain_input_manage,fingerprint_identification

user_function = user_function_manage.user_function()
domain_input  = domain_input_manage.domain_input() #导入功能模块并实例化

class GUI(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.iconphoto(False, tk.PhotoImage(file = pwd + 'icon.gif')) #设置工具图标
        self.center_window(1000,500,self.window)#设置GUI主界面窗口大小
        self.window.title("CMS指纹识别工具1.0 Powered by AD.WN") #设置工具名称
        self.url_time_out  = 3                 #url连接超时默认设置为3s
        self.proxy_setting = 'off'             #代理功能默认设置为关闭
        self.association_number = 50           #协程池协程数默认设置为50 
        self.md5_finger_get= 'off'             #提取md5指纹功能默认设置为关闭 
        self.file_save_type_get = 'Txt'        #结果输出文件默认保存为txt格式
        self.domain_list   = []                #输入域名列表初始设置为空          
        self.creat_label_frame_show_messages() #创建工具动态显示栏
        self.creat_menu()                      #创建下拉菜单
        self.creat_label_frame_zero()          #创建操作区域框架
        self.creat_label_frame_one()           #创建指纹规则库管理框架
        self.creat_label_frame_two()           #创建域名输入框架
        self.creat_label_frame_three()         #创建指纹识别和运行结果显示框架
        self.window.mainloop()                 #主函数循环显示GUI界面
        
    def center_window(self,w,h,type): #使窗口屏幕居中
        ws = self.window.winfo_screenwidth() #获取屏幕的宽、高
        hs = self.window.winfo_screenheight()
        x = (ws/2) - (w/2)         # 计算 x, y 位置
        y = (hs/2) - (h/2)
        type.geometry('%dx%d+%d+%d' % (w, h, x, y))
        type.resizable(False, False) #禁止窗口缩放拉伸
    
    def creat_label_frame_show_messages(self): #设置方框-0-操作区域 
        label_frame_show_messages = tk.LabelFrame(self.window,text = '工具运行动态显示栏',width = 900,height = 50)
        label_frame_show_messages.place(x = 50,y = 10)
        self.output_data_label = Label(self.window,text='工具提示>>:工具运行成功!!!')
        self.output_data_label.config(fg = 'green')  
        self.output_data_label.place(x = 54,y = 30)        

    def creat_menu(self): #创建下拉选项菜单         
        menu = tk.Menu(self.window)  
        menu_about = tk.Menu(menu,tearoff = False)  
        menu.add_cascade(label='关于', menu = menu_about) #下拉选项菜单-关于
        def creat_menu_about_explain():  
            self.output_data_label['text'] = '工具动态>>:正在查看使用说明书...'
            self.output_data_label.config(fg = 'green')  
            self.output_data_label.update()             
            tkinter.messagebox.showinfo(title = '关于--使用说明书', message = '1.1.下拉菜单--说明:工具使用说明书\n'
            + '1.2.下拉菜单--设置:设置辅助功能\n'
            + '1.2.1.设置--超时:设置全局的URL请求的超时时间,默认为:3s\n'
            + '1.2.2.设置--代理:设置全局的URL请求的代理IP,默认为:off\n'
            + '1.2.3.设置--协程池:设置全局的协程池中的协程数量,默认为:50\n'
            + '1.2.5.设置--指纹提取:设置对已识别cms的MD5指纹提取,默认为:off\n'
            + '1.2.6.设置--文件保存:设置程序运行结果的保存文件格式,默认为:.txt\n'
            + '2.1.操作区域--域名输入:进行域名输入相关的操作\n'
            + '2.1.1.域名输入--新增域名:添加域名\n'
            + '2.1.2.域名输入--删除域名:删除域名\n'
            + '2.1.3.域名输入--更新域名:更新域名\n'
            + '2.1.4.域名输入--检查域名:判断输入的域名是否正确\n'
            + '2.1.5.域名输入--确认:确定域名输入,自行对输入域名进行正确判断\n'
            + '2.2.操作区域--指纹规则库查看:对指纹库进行增删查改操作\n'
            + '2.2.1.Banner指纹库--新增指纹:添加指纹到指纹库,输入格式为:data|data\n'
            + '2.2.1.Banner指纹库--删除指纹:删除指定的指纹,输入格式为:number\n'
            + '2.2.1.Banner指纹库--查询指纹:查询指定的指纹,输入格式为:number\n'
            + '2.2.1.Banner指纹库--更新指纹:更新指定的指纹,输入格式为:x|y|data\n'
            + '2.2.2.Cms指纹库--新增指纹:添加指纹到指纹库,输入格式为:data|data|data|data\n'
            + '2.2.2.Cms指纹库--删除指纹:删除指定的指纹,输入格式为:number\n'
            + '2.2.2.Cms指纹库--查询指纹:查询指定的指纹,输入格式为:number\n'
            + '2.2.2.Cms指纹库--更新指纹:更新指定的指纹,输入格式为:x|y|data\n'  
            + '2.3.操作区域--指纹识别:开始指纹识别模块的运行及工具退出\n'
            + '2.3.1.指纹识别--开始:开始进行Web指纹识别\n'
            + '2.3.2.指纹识别--退出:关闭并退出程序\n'
            + '3.结果输出:程序运行结果的输出展示\n'
            + '4.工具运行动态显示栏:向用户显示工具正在进行的操作\n'
            )     
            self.output_data_label['text'] = '工具动态>>:正在停留GUI主界面!'
            self.output_data_label.config(fg = 'green')  
            self.output_data_label.update()            
        menu_about.add_command(label='说明', command = creat_menu_about_explain)        
        menu_setting = tk.Menu(menu,tearoff = False)    
        menu.add_cascade(label='设置', menu = menu_setting) #下拉选项菜单-设置
        
        def creat_menu_setting_time_out():
            menu_setting_time_out_top = tk.Toplevel(menu_setting)
            self.center_window(400,200,menu_setting_time_out_top)
            self.output_data_label['text'] = '工具动态>>:正在进行URL连接超时自定义设置...' 
            self.output_data_label.config(fg = 'green')
            self.output_data_label.update()            
            menu_setting_time_out_top.title('设置--超时')  
            setting_time_out_label_frame = tk.LabelFrame(menu_setting_time_out_top,text = 'URL连接超时设置',width = 350,height = 150)
            setting_time_out_label_frame.place(x = 25,y = 25)
            menu_setting_time_out_top_la = tk.Label(menu_setting_time_out_top,text = '你选择的超时时间为:1s',width = 20,height = 2)
            menu_setting_time_out_top_la.place(x = 85,y = 40 )  
            def choose_time_out(time_out_number): #设置超时时间数
                menu_setting_time_out_top_la.config(text='你选择的超时时间为:{}s'.format(time_out_number))
                
            menu_setting_time_out_top_sc = tk.Scale(menu_setting_time_out_top,label = '左右滑动进行选择',from_ = 1,to = 10,
            orient = HORIZONTAL,length = 200,showvalue = 0,tickinterval = 1,resolution = 1,command = choose_time_out) #创建一个尺度滑条,长度200字符,从0开始10结束,以1为刻度,精度为1,触发调用choose_time_out函数
            menu_setting_time_out_top_sc.place(x = 90,y = 70 ) 
            
            def set_time_out():
                self.url_time_out = int(menu_setting_time_out_top_la.cget("text").replace('你选择的超时时间为:','').replace('s','')) #获取超时时间
                self.output_data_label['text'] = '工具动态>>:URL连接超时设置为:{}s'.format(self.url_time_out)
                self.output_data_label.config(fg = 'green')
                self.output_data_label.update()
                menu_setting_time_out_top.destroy()
                
            def set_time_out_quit():
                self.url_time_out = 3
                self.output_data_label['text'] = '工具提示>>:URL连接超时未自定义设置,默认值为3s!'
                self.output_data_label.config(fg = 'blue')  
                self.output_data_label.update()
                menu_setting_time_out_top.destroy()
                
            menu_setting_time_out_top_button_ok = tk.Button(menu_setting_time_out_top, text = '确认',width = 7,height = 1,command = set_time_out)
            menu_setting_time_out_top_button_ok.place(x = 80,y = 130)
            menu_setting_time_out_top_button_quit = tk.Button(menu_setting_time_out_top, text = '取消',width = 7,height = 1,command = set_time_out_quit)
            menu_setting_time_out_top_button_quit.place(x = 260,y = 130) 
        menu_setting.add_command(label='超时', command = creat_menu_setting_time_out)  #下拉选项菜单-设置-超时        
        
        def creat_menu_setting_proxy():
            menu_setting_proxy_top = tk.Toplevel(menu_setting)
            self.center_window(600,400,menu_setting_proxy_top)
            self.output_data_label['text'] = '工具动态>>:正在进行URL代理自定义设置...'
            self.output_data_label.config(fg = 'green')  
            self.output_data_label.update()            
            menu_setting_proxy_top.title('设置--代理--' + '路径:' + pwd + 'proxies.txt') 
            menu_setting_proxy_table = ttk.Treeview(menu_setting_proxy_top,show = "headings") #列表
            menu_setting_proxy_table["columns"]=("序号","代理IP")
            menu_setting_proxy_table.column("序号",width = 60)
            menu_setting_proxy_table.column("代理IP",width = 494)
            menu_setting_proxy_table.heading("序号",text = "序号") 
            menu_setting_proxy_table.heading("代理IP",text = "代理IP")    
            menu_setting_proxy_table.place(x = 20,y = 0)          
            yscrollbar = Scrollbar(menu_setting_proxy_top,orient = VERTICAL,command = menu_setting_proxy_table.yview) #Y滚动条
            menu_setting_proxy_table.configure(yscrollcommand = yscrollbar.set)
            yscrollbar.pack(side = RIGHT, fill = Y) 
            def menu_setting_proxy_table_update_value(file_name): #表格数据查看
                for item in menu_setting_proxy_table.get_children(): #清除表格已有内容,初始化表格
                    menu_setting_proxy_table.delete(item)                 
                try :
                    file = open(file_name,'r+',encoding = 'utf-8')
                    proxy_get = file.readlines()
                except IOError:                 
                    tkinter.messagebox.showerror(title = '查看代理--错误',message = '打开文件:{}\n失败!\n该文件不存在,请新建该文件!'.format(file_name))
                if ((len(proxy_get) == 0) and (file_name == pwd + 'proxies.txt')):
                    self.output_data_label['text'] = "工具提示>>:检查代理--结果;不存在有效代理IP,如果想使用自定义代理,可以将代理保存至文件:{}代理格式为:{'http':'http://ip:port','https':'https://ip:port'}'".format(file_name)
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()                 
                else : pass
                for i in range(len(proxy_get)):
                    proxy_get[i].strip()
                    menu_setting_proxy_table.insert('',i + 1,values=(i + 1,proxy_get[i]))   
                    
            menu_setting_proxy_table_update_value(pwd + 'proxies_from_xiciproxy.txt')
                   
            def refalsh_proxy():
                self.output_data_label['text'] = '工具提示>>:刷新代理--提示;指定从https://www.xicidaili.com/nn/获取多少页的代理IP,输入为:纯数字(1~4054)!'
                self.output_data_label.config(fg = 'blue')  
                self.output_data_label.update()
                input_value = StringVar()
                input_value.set('1')
                input_value_entry = tk.Entry(menu_setting_proxy_top,textvariable = input_value,width = 55)
                input_value_entry.place(x = 120,y = 230)             
                def get_proxy():
                    page_flag  = user_function.get_proxy_list(page = input_value_entry.get(),time_out = self.url_time_out,association_number = self.association_number)
                    if (page_flag == 'True'):
                        menu_setting_proxy_table_update_value(pwd + 'proxies_from_xiciproxy.txt') 
                        tkinter.messagebox.showinfo(title = '刷新代理--成功', message = '已成功刷新本地代理文件!')
                    elif (page_flag == 'False1'):
                        tkinter.messagebox.showerror(title = '刷新代理--错误', message = '输入格式错误!\n输入页数不为纯数字!')
                    else :
                        tkinter.messagebox.showerror(title = '刷新代理--错误', message = '输入页数越界!\n输入页数为0或者超出代理网页总页数!')
                    input_value_entry.destroy()
                    input_value_bt.destroy()    
                            
                input_value_bt = tk.Button(menu_setting_proxy_top,text = 'OK',width = 5,command =  get_proxy)
                input_value_bt.place(x = 531 , y = 230) 
                
            def check_proxy():
                proxies_num =  user_function.check_proxy(time_out = self.url_time_out,association_number = self.association_number)
                tkinter.messagebox.showinfo(title = '检查代理--结果', message = '有效代理数为:{}'.format(proxies_num))
                menu_setting_proxy_table_update_value(pwd + 'proxies.txt') 
            
            def open_proxy():
                self.proxy_setting = 'open' #打开代理
                proxies_num = user_function.check_proxy(time_out = self.url_time_out,association_number = self.association_number)
                self.output_data_label['text'] = '工具动态>>:URL代理已开启!'
                self.output_data_label.config(fg = 'green')  
                self.output_data_label.update()                  
                menu_setting_proxy_top.destroy()
                
            def close_proxy():
                self.proxy_setting = 'off' #关闭代理
                self.output_data_label['text'] = '工具提示>>:URL代理未自定义设置,默认值为off!'
                self.output_data_label.config(fg = 'blue')  
                self.output_data_label.update() 
                menu_setting_proxy_top.destroy()
             
            menu_setting_proxy_top_bt_refalsh = tk.Button(menu_setting_proxy_top,text  = '刷新代理',width = 10,height = 1,command = refalsh_proxy)
            menu_setting_proxy_top_bt_refalsh.place(x = 20,y = 230)             
            menu_setting_proxy_top_bt_check   = tk.Button(menu_setting_proxy_top,text  = '检查代理',width = 10,height = 1,command = check_proxy)
            menu_setting_proxy_top_bt_check.place(x = 20,y = 260)    
            menu_setting_proxy_top_bt_open    = tk.Button(menu_setting_proxy_top, text = '开启代理',width = 10,height = 1,command = open_proxy)
            menu_setting_proxy_top_bt_open.place(x = 20,y = 320)
            menu_setting_proxy_top_bt_close   = tk.Button(menu_setting_proxy_top, text = '关闭代理',width = 10,height = 1,command = close_proxy)
            menu_setting_proxy_top_bt_close.place(x = 20,y = 350) 
        menu_setting.add_command(label='代理', command = creat_menu_setting_proxy) #下拉选项菜单-设置-代理  
    
        def creat_menu_setting_association():
            menu_setting_association_top = tk.Toplevel(menu_setting)
            self.center_window(400,200,menu_setting_association_top)
            self.output_data_label['text'] = '工具动态>>:正在进行协程池协程数自定义设置...'
            self.output_data_label.config(fg = 'green')  
            self.output_data_label.update()              
            menu_setting_association_top.title('设置--协程池') 
            setting_association_label_frame = tk.LabelFrame(menu_setting_association_top,text = '协程数设置',width = 350,height = 150)
            setting_association_label_frame.place(x = 25,y = 25) 
            menu_setting_association_top_la = tk.Label(menu_setting_association_top,text = '你选择的协程数为:50',width = 20,height = 2)
            menu_setting_association_top_la.place(x = 85,y = 40 )  
            def choose_association(association_number): #设置协程数
                menu_setting_association_top_la.config(text='你选择的协程数为:' + association_number)

            menu_setting_association_top_sc = tk.Scale(menu_setting_association_top,label = '左右滑动进行选择',from_ = 50,to = 2300,
            orient = HORIZONTAL,length = 200,showvalue = 0,tickinterval = 450,resolution = 10,command = choose_association)
            menu_setting_association_top_sc.place(x = 90,y = 70 ) 
            def set_association():
                self.association_number = int(menu_setting_association_top_la.cget("text").replace('你选择的协程数为:','')) 
                self.output_data_label['text'] = '工具动态>>:协程池中协程数已设置为:{}!'.format(self.association_number)
                self.output_data_label.config(fg = 'green')  
                self.output_data_label.update()                 
                menu_setting_association_top.destroy()
                
            def set_association_quit():
                self.association_number = 50
                self.output_data_label['text'] = '工具提示>>:协程池中协程数未自定义设置,默认值为50!'
                self.output_data_label.config(fg = 'blue')  
                self.output_data_label.update()                 
                menu_setting_association_top.destroy()
                
            menu_setting_association_top_button_ok = tk.Button(menu_setting_association_top, text = '确认',width = 7,height = 1,command = set_association)
            menu_setting_association_top_button_ok.place(x = 80,y = 130)
            menu_setting_association_top_button_quit = tk.Button(menu_setting_association_top, text = '取消',width = 7,height = 1,command = set_association_quit)
            menu_setting_association_top_button_quit.place(x = 260,y = 130) 
        menu_setting.add_command(label='协程池', command = creat_menu_setting_association) #下拉选项菜单-设置-协程池
        
        def creat_menu_setting_md5_finger_get():
            menu_setting_md5_finger_get_top = tk.Toplevel(menu_setting)
            self.center_window(400,200,menu_setting_md5_finger_get_top)
            self.output_data_label['text'] = '工具动态>>:正在进行提取MD5指纹自定义设置...'
            self.output_data_label.config(fg = 'green')  
            self.output_data_label.update()              
            menu_setting_md5_finger_get_top.title('设置--提取MD5指纹') 
            setting_md5_finger_get_label_frame = tk.LabelFrame(menu_setting_md5_finger_get_top,text = 'md5文件指纹提取设置',width = 350,height = 150)
            setting_md5_finger_get_label_frame.place(x = 25,y = 25)                 
            def set_md5_finger_get():
                self.md5_finger_get = 'open' 
                self.output_data_label['text'] = '工具动态>>:MD5指纹提取已开启!'
                self.output_data_label.config(fg = 'green')  
                self.output_data_label.update() 
                menu_setting_md5_finger_get_top.destroy()
                
            def set_md5_finger_get_exit():
                self.md5_finger_get = 'off'
                self.output_data_label['text'] = '工具提示>>:MD5指纹提取未自定义设置,默认值为off!'
                self.output_data_label.config(fg = 'blue')  
                self.output_data_label.update() 
                menu_setting_md5_finger_get_top.destroy()
                
            menu_setting_md5_finger_get_top_button_ok = tk.Button(menu_setting_md5_finger_get_top, text = '开启指纹提取',width = 10,height = 1,command = set_md5_finger_get)
            menu_setting_md5_finger_get_top_button_ok.place(x = 100,y = 90)
            menu_setting_md5_finger_get_top_button_quit  = tk.Button(menu_setting_md5_finger_get_top, text = '取消',width = 10,height = 1,command = set_md5_finger_get_exit)
            menu_setting_md5_finger_get_top_button_quit.place(x = 240,y = 90) 
        menu_setting.add_command(label='指纹提取', command = creat_menu_setting_md5_finger_get) #下拉选项菜单-设置-指纹提取
        
        def creat_menu_setting_file_save():
            menu_setting_file_save_top = tk.Toplevel(menu_setting)
            self.center_window(400,200,menu_setting_file_save_top)
            self.output_data_label['text'] = '工具动态>>:正在进行工具运行结果保存格式自定义设置...'
            self.output_data_label.config(fg = 'green')  
            self.output_data_label.update()              
            menu_setting_file_save_top.title('设置--保存格式') 
            setting_file_save_label_frame = tk.LabelFrame(menu_setting_file_save_top,text = '结果输出文件保存类型设置',width = 350,height = 150)
            setting_file_save_label_frame.place(x = 25,y = 25)            
            choose_value = tk.StringVar()    # 定义一个var用来将radiobutton的值和Label的值联系在一起.
            def check_choose():
                if (choose_value.get() == 'CSV'):
                    self.file_save_type_get = 'Csv'
                    self.output_data_label['text'] = '工具动态>>:结果输出文件保存类型已设置为:*.csv!'
                    self.output_data_label.config(fg = 'green')  
                    self.output_data_label.update() 
                    menu_setting_file_save_top.destroy()
                elif (choose_value.get() == 'EXCEL'):
                    self.file_save_type_get = 'Excel'
                    self.output_data_label['text'] = '工具动态>>:结果输出文件保存类型已设置为:*.xls!'
                    self.output_data_label.config(fg = 'green')  
                    self.output_data_label.update() 
                    menu_setting_file_save_top.destroy()                    
                elif (choose_value.get() == 'TXT'):
                    self.file_save_type_get = 'Txt'
                    self.output_data_label['text'] = '工具动态>>:结果输出文件保存类型已设置为:*.txt!'
                    self.output_data_label.config(fg = 'green')  
                    self.output_data_label.update() 
                    menu_setting_file_save_top.destroy()   
                else : pass

            csv_rad   = tk.Radiobutton(menu_setting_file_save_top, text = 'Option CSV', variable = choose_value, value = 'CSV', command = check_choose)
            csv_rad.place(x = 160,y = 50)
            excel_rad = tk.Radiobutton(menu_setting_file_save_top, text = 'Option EXCEL', variable = choose_value, value = 'EXCEL', command = check_choose)
            excel_rad.place(x = 160,y = 90)
            txt_rad   = tk.Radiobutton(menu_setting_file_save_top, text = 'Option TXT', variable = choose_value, value = 'TXT', command = check_choose)
            txt_rad.place(x = 160,y = 130)            
        menu_setting.add_command(label='保存格式', command = creat_menu_setting_file_save) #下拉选项菜单-设置-结果输出文件保存类型   
        self.window.config(menu = menu) #添加下拉菜单控制
    
    
    def creat_label_frame_zero(self): #设置方框-0-操作区域 
        label_frame_zero = tk.LabelFrame(self.window,text = '操作区域',width = 900,height = 120)
        label_frame_zero.place(x = 49,y = 60)    
        
        
    def creat_label_frame_one(self) : #设置方框-1-指纹规则库
        label_frame_two = tk.LabelFrame(self.window,text = '指纹规则库管理',width = 110,height = 90)
        label_frame_two.place(x = 100,y = 80)
        warehouse_radio_input = tk.BooleanVar()
        fingerprint_manage = fingerprint_database_manage.fingerprint_database_manage() #实例化指纹规则库模块
        def check_choose():
            if (warehouse_radio_input.get() == False):
                banner_finger_top = tk.Toplevel(self.window)
                self.center_window(1000,400,banner_finger_top)
                self.output_data_label['text'] = '工具动态>>:正在查看Banner指纹库...'
                self.output_data_label.config(fg = 'green')  
                self.output_data_label.update()                 
                banner_finger_top.title('指纹库--Banner--' + '路径:' + pwd.replace('Cms_get','Fingerprint_database') + 'banner.xlsx')
                banner_finger_table = ttk.Treeview(banner_finger_top,show = "headings")
                banner_finger_table["columns"] = ("Num","Names","Keys")
                banner_finger_table.column("Num",width   = 50)
                banner_finger_table.column("Names",width = 480)
                banner_finger_table.column("Keys",width  = 427)
                banner_finger_table.heading("Num",text   = "Num") 
                banner_finger_table.heading("Names",text = "Names(y=1)") 
                banner_finger_table.heading("Keys",text  = "Keys(y=2)")
                banner_finger_table.place(x = 20 ,y = 20)
                yscrollbar = Scrollbar(banner_finger_top,orient = VERTICAL,command = banner_finger_table.yview)
                banner_finger_table.configure(yscrollcommand = yscrollbar.set)
                yscrollbar.pack(side = RIGHT, fill = Y) 
                def banner_finger_table_update_value(): #banner表数据显示
                    for item in banner_finger_table.get_children(): #清除表格已有内容,刷新表格
                        banner_finger_table.delete(item)            
                    workbook  = openpyxl.load_workbook(pwd.replace('Cms_get','Fingerprint_database') + 'banner.xlsx')
                    worksheet = workbook.active#获取表的banner表单(默认最活跃的即是第一个表)
                    finger_banner_get_col_name,finger_banner_get_col_keys =[],[]
                    for cell1,cell2 in zip(worksheet['A'][1:],worksheet['B'][1:]):
                        finger_banner_get_col_name.append(cell1.value)
                        finger_banner_get_col_keys.append(cell2.value)                    
                    workbook.close()
                    for i in range(len(finger_banner_get_col_name)):
                        banner_finger_table.insert('',i + 1 ,values=(i + 1,finger_banner_get_col_name[i],finger_banner_get_col_keys[i]))   
                
                banner_finger_table_update_value()
                
                def banner_finger_top_insert_value(): #banner表增
                    self.output_data_label['text'] = '工具提示>>:添加指纹;输入指纹格式为:Name|Key'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update() 
                    insert_value = tk.StringVar()
                    insert_value.set('Name|Key')
                    insert_value_entry = tk.Entry(banner_finger_top,textvariable = insert_value,width = 110)
                    insert_value_entry.place(x = 130,y = 270)                     
                    def insert_save():
                        insert_fingerprint = fingerprint_manage.banner_insert_fingerprint(insert_str = insert_value_entry.get())
                        if (insert_fingerprint == 'True'):
                            banner_finger_table_update_value() #刷新表格
                            tkinter.messagebox.showinfo(title = '添加指纹--成功',message = 'Banner指纹规则库已成功添加指纹!')
                        else :
                            tkinter.messagebox.showerror(title = '添加指纹--出错',message = '输入格式错误!\n输入格式不为Name|Key!')
                        insert_value_entry.destroy()
                        insert_value_save_bt.destroy()
   
                    insert_value_save_bt = tk.Button(banner_finger_top,text = 'OK',width = 5,command =  insert_save)
                    insert_value_save_bt.place(x = 935 , y = 260)
              
                def banner_finger_top_delete_value(): #banner表删
                    self.output_data_label['text'] = '工具提示>>:删除指纹;指定删除指纹表格第几行的指纹,输入为:纯数字(1~...)'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()                     
                    delete_value = StringVar()
                    delete_value.set('1')
                    delete_value_entry = tk.Entry(banner_finger_top,textvariable = delete_value,width = 110)
                    delete_value_entry.place(x = 130,y = 300)             
                    def delete_save():
                        delete_fingerprint = fingerprint_manage.banner_delete_fingerprint(row_number = delete_value_entry.get())
                        if (delete_fingerprint == 'True'):
                            banner_finger_table_update_value()    
                            tkinter.messagebox.showinfo(title = '删除指纹--成功',message = 'Banner指纹规则库已成功删除指纹!')
                        elif (delete_fingerprint == 'False1'):
                            tkinter.messagebox.showerror(title = '删除指纹--错误', message='输入格式错误!\n输入行数不为纯数字!')
                        else :
                            tkinter.messagebox.showerror(title = '删除指纹--错误', message='输入行数越界!\n输入行数为0或者超出Banner指纹规则库总行数!')
                        delete_value_entry.destroy()
                        delete_value_save_bt.destroy()  
                            
                    delete_value_save_bt = tk.Button(banner_finger_top,text = 'OK',width = 5,command =  delete_save)
                    delete_value_save_bt.place(x = 935 , y = 290)            
        
                def banner_finger_top_search_value(): #banner表查
                    self.output_data_label['text'] = '工具提示>>:查询指纹;指定查询指纹表格第几行指纹,输入为:纯数字(1~...)'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()  
                    search_value = StringVar()
                    search_value.set('1')
                    search_value_entry = tk.Entry(banner_finger_top,textvariable = search_value,width = 110)
                    search_value_entry.place(x = 130,y = 330)                    
                    def search():
                        search_flag,row_number,name,key = fingerprint_manage.banner_search_fingerprint(row_number = search_value_entry.get())
                        if (search_flag == 'True'):
                            tkinter.messagebox.showinfo(title = '查询指纹--结果--Banner指纹规则库第"{}"行'.format(row_number), message = 'Names:{}\nKeys:{}'.format(name,key))     
                        elif (search_flag == 'False1'):
                            tkinter.messagebox.showerror(title = '程序指纹--错误', message='输入格式错误!\n输入行数不为纯数字!')
                        else :
                            tkinter.messagebox.showerror(title = '查询指纹--错误', message='输入行数越界!\n输入行数为0或者超出Banner指纹规则库总行数')
                        search_value_entry.destroy()
                        search_bt.destroy()    
                            
                    search_bt = tk.Button(banner_finger_top,text = 'OK',width = 5,command =  search)
                    search_bt.place(x = 935 , y = 320)
                    
                def banner_finger_top_update_value(): #banner表改
                    self.output_data_label['text'] = '工具提示>>:更新指纹;更新指纹表格指纹,输入的坐标及更新后的数据格式为:x|y|data'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()  
                    update_value = StringVar()
                    update_value.set('x|y|data')
                    update_value_entry = tk.Entry(banner_finger_top,textvariable = update_value,width = 110)
                    update_value_entry.place(x = 130,y = 360)                    
                    def update_save(): 
                        update_fingerprint = fingerprint_manage.banner_update_fingerprint(update_str = update_value_entry.get())
                        if(update_fingerprint == 'True'):
                            banner_finger_table_update_value()
                            tkinter.messagebox.showinfo(title = '更新指纹--成功',message = 'Banner指纹规则库已成功更新指纹!')
                        elif (update_fingerprint == 'False1'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入格式错误!\n输入格式不为x|y|data!')
                        elif (update_fingerprint == 'False2'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入格式错误!\n输入的坐标x,y不都为纯数字!')
                        else :
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入行(列)数越界!\n输入的坐标中x(y)的值为0或者超过Banner指纹规则库总行(列)数!')
                        update_value_entry.destroy()
                        update_value_save_bt.destroy()                         
                    update_value_save_bt = tk.Button(banner_finger_top, text='OK', width = 5, command = update_save)
                    update_value_save_bt.place(x = 935 ,y = 350)
            
                banner_finger_table_insert_value_bt = tk.Button(banner_finger_top,text = '新增指纹',width = 10,command = banner_finger_top_insert_value)
                banner_finger_table_insert_value_bt.place(x = 20,y = 260)          
                banner_finger_table_delete_value_bt = tk.Button(banner_finger_top,text = '删除指纹',width = 10,command = banner_finger_top_delete_value)
                banner_finger_table_delete_value_bt.place(x = 20,y = 290)  
                banner_finger_table_search_value_bt = tk.Button(banner_finger_top,text = '查询指纹',width = 10,command = banner_finger_top_search_value)
                banner_finger_table_search_value_bt.place(x = 20,y = 320)          
                banner_finger_table_update_value_bt = tk.Button(banner_finger_top,text = '更新指纹',width = 10,command = banner_finger_top_update_value)
                banner_finger_table_update_value_bt.place(x = 20,y = 350)
                
            else :
                cms_finger_top = tk.Toplevel(self.window)
                self.center_window(1000,400,cms_finger_top)
                self.output_data_label['text'] = '工具动态>>:正在查看Cms指纹库...'
                self.output_data_label.config(fg = 'green')  
                self.output_data_label.update()                 
                cms_finger_top.title('指纹库--Cms--' + '路径:' + pwd.replace('Cms_get','Fingerprint_database') + 'cms.xlsx')
                cms_finger_table = ttk.Treeview(cms_finger_top,show = "headings")
                cms_finger_table["columns"] = ("Num","Cms","File_path","Match_pattern","Options","Hit")
                cms_finger_table.column("Num",width = 50)
                cms_finger_table.column("Cms",width = 175)
                cms_finger_table.column("File_path",width = 280)
                cms_finger_table.column("Match_pattern",width = 320)
                cms_finger_table.column("Options",width = 85)
                cms_finger_table.column("Hit",width = 55)
                cms_finger_table.heading("Num",text = "Num") 
                cms_finger_table.heading("Cms",text = "Cms(y=1)") 
                cms_finger_table.heading("File_path",text = "File_path(y=2)")
                cms_finger_table.heading("Match_pattern",text = "Match_pattern(y=3)")
                cms_finger_table.heading("Options",text = "Options(y=4)")
                cms_finger_table.heading("Hit",text = "Hit(y=5)")
                cms_finger_table.place(x = 20 ,y = 20)
                yscrollbar = Scrollbar(cms_finger_top,orient = VERTICAL,command = cms_finger_table.yview)
                cms_finger_table.configure(yscrollcommand = yscrollbar.set)
                yscrollbar.pack(side = RIGHT, fill = Y)         
                def cms_finger_table_update_value(): #cms表格数据显示
                    for item in cms_finger_table.get_children():#清除表格已有内容,初始化表格(刷新)
                        cms_finger_table.delete(item)            
                    workbook  = openpyxl.load_workbook(pwd.replace('Cms_get','Fingerprint_database') + 'cms.xlsx')
                    worksheet = workbook.active#获取表的cms表单(默认最活跃的即是第一个表)
                    finger_cms_get_col_cms,finger_cms_get_col_file_path,finger_cms_get_col_match_pattern,finger_cms_get_col_options,finger_cms_get_col_hit = [],[],[],[],[]
                    for cell1,cell2,cell3,cell4,cell5 in zip(worksheet['A'][1:],worksheet['B'][1:],worksheet['C'][1:],worksheet['D'][1:],worksheet['E'][1:]):#去掉列头,获取表中每一列的值
                        finger_cms_get_col_cms.append(cell1.value)
                        finger_cms_get_col_file_path.append(cell2.value)
                        finger_cms_get_col_match_pattern.append(cell3.value)
                        finger_cms_get_col_options.append(cell4.value)
                        finger_cms_get_col_hit.append(cell5.value)
                    workbook.close()
                    for i in range(len(finger_cms_get_col_cms)):
                        cms_finger_table.insert('',i + 1 ,values=(i + 1,finger_cms_get_col_cms[i],finger_cms_get_col_file_path[i],finger_cms_get_col_match_pattern[i],finger_cms_get_col_options[i],finger_cms_get_col_hit[i]))    
                
                cms_finger_table_update_value()
                
                def cms_finger_top_insert_value(): #cms增
                    self.output_data_label['text'] = '工具提示>>:添加指纹;输入指纹格式为:Cms_name|File_path(/...)|Match_pattern|Options(keyword/md5)'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()  
                    insert_value = StringVar()
                    insert_value.set('Cms_name|File_path(/...)|Match_pattern|Options(keyword/md5)')
                    insert_value_entry = tk.Entry(cms_finger_top,textvariable = insert_value,width = 110)
                    insert_value_entry.place(x = 130,y = 270)                    
                    def insert_save():
                        insert_fingerprint = fingerprint_manage.cms_insert_fingerprint(insert_str = insert_value_entry.get())
                        if (insert_fingerprint == 'True'):
                            cms_finger_table_update_value() #刷新表格
                            tkinter.messagebox.showinfo(title = '添加指纹--成功',message = 'Cms指纹规则库已成功添加指纹!')
                        elif (insert_fingerprint == 'False1'):
                            tkinter.messagebox.showerror(title = '添加指纹--错误',message = '输入格式错误!\n输入格式不为Cms_name|File_path(/...)|Match_pattern|Options(keyword/md5)!')
                        elif (insert_fingerprint == 'False2'):
                            tkinter.messagebox.showerror(title = '添加指纹--错误',message = '输入File_path错误!\n输入字符串指纹路径File_path中不含有字符"/"!')
                        elif (insert_fingerprint == 'False3'):
                            tkinter.messagebox.showerror(title = '添加指纹--错误',message = '输入File_path错误!\n输入字符串指纹路径File_path的第一个字符不为"/"!')
                        else :
                            tkinter.messagebox.showerror(title = '添加指纹--错误',message = '输入Options错误\n输入字符串指纹类型不为keyword或md5!')
                        insert_value_entry.destroy()
                        insert_value_save_bt.destroy()
                       
                    insert_value_save_bt = tk.Button(cms_finger_top,text = 'OK',width = 5,command =  insert_save)
                    insert_value_save_bt.place(x = 935 , y = 260)
      
                def cms_finger_top_delete_value(): #cms删
                    self.output_data_label['text'] = '工具提示>>:删除指纹;指定删除指纹表格第几行的指纹,输入为:纯数字(1~...)'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()
                    delete_value = StringVar()
                    delete_value.set('1')
                    delete_value_entry = tk.Entry(cms_finger_top,textvariable = delete_value,width = 110)
                    delete_value_entry.place(x = 130,y = 300)             
                    def delete_save():
                        delete_fingerprint = fingerprint_manage.cms_delete_fingerprint(row_number = delete_value_entry.get())
                        if (delete_fingerprint == 'True'):
                            cms_finger_table_update_value()    
                            tkinter.messagebox.showinfo(title = '删除指纹--成功',message = 'Cms指纹规则库已成功删除指纹!')
                        elif (delete_fingerprint == 'False1'):
                            tkinter.messagebox.showerror(title = '删除指纹--错误', message='输入格式错误!\n输入行数不为纯数字!')
                        else :
                            tkinter.messagebox.showerror(title = '删除指纹--错误', message='输入行数越界!\n输入行数为0或者超出Cms指纹规则库总行数!')
                        delete_value_entry.destroy()
                        delete_value_save_bt.destroy()  
                            
                    delete_value_save_bt = tk.Button(cms_finger_top,text = 'OK',width = 5,command =  delete_save)
                    delete_value_save_bt.place(x = 935 , y = 290)                       

                def cms_finger_top_search_value(): #cms查
                    self.output_data_label['text'] = '工具提示>>:查询指纹;指定查询指纹表格第几行指纹,输入为:纯数字(1~...)'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()                     
                    search_value = StringVar()
                    search_value.set('1')
                    search_value_entry = tk.Entry(cms_finger_top,textvariable = search_value,width = 110)
                    search_value_entry.place(x = 130,y = 330)                    
                    def search():
                        search_flag,row_number,Cms_name,File_path,Match_pattern,Options,Hit = fingerprint_manage.cms_search_fingerprint(row_number = search_value_entry.get())
                        if (search_flag == 'True'):
                            tkinter.messagebox.showinfo(title = '查询指纹--结果--Cms指纹规则库第"{}"行'.format(row_number), message = 'Cms_name:{}\nFile_path:{}\nMatch_pattern:{}\nOptions:{}\nHit:{}'.format(Cms_name,File_path,Match_pattern,Options,Hit))     
                        elif (search_flag == 'False1'):
                            tkinter.messagebox.showerror(title = '程序指纹--错误', message='输入格式错误!\n输入行数不为纯数字!')
                        else :
                            tkinter.messagebox.showerror(title = '查询指纹--错误', message='输入行数越界!\n输入行数为0或者超出Cms指纹规则库总行数')
                        search_value_entry.destroy()
                        search_bt.destroy()    

                    search_bt = tk.Button(cms_finger_top,text = 'OK',width = 5,command =  search)
                    search_bt.place(x = 935 , y = 320)
            
                def cms_finger_top_update_value(): #cms表格改
                    self.output_data_label['text'] = '工具提示>>:更新指纹;更新指纹表格指纹,输入的坐标及更新后的数据格式为:x|y|data'
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()  
                    update_value = StringVar()
                    update_value.set('x|y|data')
                    update_value_entry = tk.Entry(cms_finger_top,textvariable = update_value,width = 110)
                    update_value_entry.place(x = 130,y = 360)                    
                    def update_save(): 
                        update_fingerprint = fingerprint_manage.cms_update_fingerprint(update_str = update_value_entry.get())
                        if(update_fingerprint == 'True'):
                            cms_finger_table_update_value()
                            tkinter.messagebox.showinfo(title = '更新指纹--成功',message = 'Cms指纹规则库已成功更新指纹!')
                        elif (update_fingerprint == 'False1'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入格式错误!\n输入格式不为x|y|data!')
                        elif (update_fingerprint == 'False2'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入格式错误!\n输入的坐标x,y不都为纯数字!')
                        elif (update_fingerprint == 'False3'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入行(列)数越界!\n输入的坐标中x(y)的值为0或者超过Banner指纹规则库总行(列)数!')
                        elif (update_fingerprint == 'False4'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入更新值错误!\n更新指纹规则库的第二列的File_path,更新值不含有字符"/"!')
                        elif (update_fingerprint == 'False5'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入更新值错误!\n更新指纹规则库的第二列的File_path,更新值的第一个字符不为"/"!')
                        elif (update_fingerprint == 'False6'):
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入更新值错误!\n更新指纹规则库的第四列的Options,更新值不为"keyword"或"md5"!')
                        else:
                            tkinter.messagebox.showerror(title = '更新指纹--错误',message = '输入更新值错误!\n更新指纹规则库的第五列的Hit，更新值不为纯数字！')
                        update_value_entry.destroy()
                        update_value_save_bt.destroy()                                             
                     
                    update_value_save_bt = tk.Button(cms_finger_top, text='OK', width = 5, command = update_save)
                    update_value_save_bt.place(x = 935 ,y = 350)
            
                cms_finger_top_insert_value_bt = tk.Button(cms_finger_top,text = '新增指纹',width = 10,command = cms_finger_top_insert_value)
                cms_finger_top_insert_value_bt.place(x = 20,y = 260)          
                cms_finger_top_delete_value_bt = tk.Button(cms_finger_top,text = '删除指纹',width = 10,command = cms_finger_top_delete_value)
                cms_finger_top_delete_value_bt.place(x = 20,y = 290)  
                cms_finger_top_search_value_bt = tk.Button(cms_finger_top,text = '查询指纹',width = 10,command = cms_finger_top_search_value)
                cms_finger_top_search_value_bt.place(x = 20,y = 320)          
                cms_finger_top_update_value_bt = tk.Button(cms_finger_top,text = '更新指纹',width = 10,command = cms_finger_top_update_value)
                cms_finger_top_update_value_bt.place(x = 20,y = 350) 
                              
        warehouse_check_button_one = tk.Radiobutton(label_frame_two,text = 'Banner指纹库',variable = warehouse_radio_input,value = False,command = check_choose)
        warehouse_check_button_one.place(x = 0,y = 5)
        warehouse_check_button_two = tk.Radiobutton(label_frame_two,text = 'Cms指纹库',   variable = warehouse_radio_input,value = True, command = check_choose)
        warehouse_check_button_two.place(x = 0,y = 35)                  
    
    
    def creat_label_frame_two(self): #设置方框-2-域名输入 
        label_frame_one = tk.LabelFrame(self.window,text = '域名输入管理',width = 110,height = 90)
        label_frame_one.place(x = 430,y = 80)
        def creat_domain_input_top():
            self.domain_list = [] #进入就初始化self.domain_list
            domain_input_top = tk.Toplevel(label_frame_one)
            self.center_window(600,400,domain_input_top)
            self.output_data_label['text'] = '工具动态>>:正在进行域名输入...'
            self.output_data_label.config(fg = 'green')  
            self.output_data_label.update()              
            domain_input_top.title('域名输入--' + '路径:' + pwd.replace('Cms_get','Domain_input') + 'url.txt') 
            domain_input_table = ttk.Treeview(domain_input_top,show = "headings") #列表
            domain_input_table["columns"]=("序号","域名")
            domain_input_table.column("序号",width = 60)
            domain_input_table.column("域名",width = 494)
            domain_input_table.heading("序号",text = "序号") 
            domain_input_table.heading("域名",text = "域名")    
            domain_input_table.place(x = 20,y = 0)          
            yscrollbar = Scrollbar(domain_input_top,orient = VERTICAL,command = domain_input_table.yview) #Y滚动条
            domain_input_table.configure(yscrollcommand = yscrollbar.set)
            yscrollbar.pack(side = RIGHT, fill = Y) 
            def domain_input_table_update_value(): #表格数据刷新
                for item in domain_input_table.get_children(): #删除原有表格数据
                    domain_input_table.delete(item)
                try :
                    file_name = pwd.replace('Cms_get','Domain_input') + 'url.txt'
                    file      = open(file_name,'r+',encoding = 'utf-8')
                    domain_get = file.readlines()
                except IOError:
                    tkinter.messagebox.showerror(title = '查看域名--错误',message = '打开文件:{}失败!\n该文件不存在,请新建该文件!'.format(file_name))
                finally:
                    file.close()
                for i in range(len(domain_get)):
                    domain_get[i].rstrip()
                    domain_input_table.insert('',i + 1,values=(i + 1,domain_get[i]))  #表格插入数据
                if (len(domain_get) == 0):
                    self.output_data_label['text'] = '工具提示>>:如果想一次输入多个域名,可以将多个域名保存至文件:{}'.format(file_name)
                    self.output_data_label.config(fg = 'blue')  
                    self.output_data_label.update()                    
                else : pass
                
            domain_input_table_update_value()             
            
            def domain_input_top_insert_value(): #域名增
                self.output_data_label['text'] = '工具提示>>:新增域名;直接输入域名!'
                self.output_data_label.config(fg = 'blue')                  
                self.output_data_label.update() 
                insert_value = tk.StringVar()
                insert_value.set('www.baidu.com')
                insert_value_entry = tk.Entry(domain_input_top,textvariable = insert_value,width = 55)
                insert_value_entry.place(x = 110,y = 235)    
                def insert_save():
                    insert_domain = domain_input.insert_domain(domain = insert_value_entry.get())
                    domain_input_table_update_value() #刷新数据       
                    insert_value_entry.destroy()
                    insert_value_save_bt.destroy()
                insert_value_save_bt = tk.Button(domain_input_top,text = 'OK',width = 5,command =  insert_save)
                insert_value_save_bt.place(x = 532 , y = 230)
                
            def domain_input_top_delete_value(): #域名删
                self.output_data_label['text'] = '工具提示>>:删除域名;指定删除域名输入文件第几行的域名,输入为:纯数字(1~...)'
                self.output_data_label.config(fg = 'blue')                  
                self.output_data_label.update() 
                delete_value = tk.StringVar()
                delete_value.set('1')
                delete_value_entry = tk.Entry(domain_input_top,textvariable = delete_value,width = 55)
                delete_value_entry.place(x = 110,y = 263)    
                def delete_save():
                    delete_domain = domain_input.delete_domain(row_number = delete_value_entry.get())
                    if (delete_domain == 'True'):
                        domain_input_table_update_value()                      
                    elif (delete_domain == 'False1'):
                        tkinter.messagebox.showerror(title = '删除域名--错误', message='输入格式错误!\n输入行数不为纯数字!')
                    else :
                        tkinter.messagebox.showerror(title = '删除域名--错误', message='输入行数越界!\n输入行数为0或者超出域名总行数!')
                    delete_value_entry.destroy()
                    delete_value_save_bt.destroy()                                             
                delete_value_save_bt = tk.Button(domain_input_top,text = 'OK',width = 5,command =  delete_save)
                delete_value_save_bt.place(x = 532 , y = 260)         
            
            def domain_input_top_update_value(): #域名改
                self.output_data_label['text'] = '工具提示>>:更新域名;指定更新域名输入文件第几行的域名,输入为:number|domain'
                self.output_data_label.config(fg = 'blue')                                  
                self.output_data_label.update()
                update_value = tk.StringVar()
                update_value.set('1|www.baidu.com')
                update_value_entry = tk.Entry(domain_input_top,textvariable = update_value,width = 55)
                update_value_entry.place(x = 110,y = 300)                  
                def update_save():
                    update_domain = domain_input.update_domain(update_str = update_value_entry.get())
                    if (update_domain == 'True'):
                        domain_input_table_update_value()   
                    elif (update_domain == 'False1'):
                        tkinter.messagebox.showerror(title = '更新域名--错误', message='输入格式错误!\n输入格式不为number|domain!')
                    elif (update_domain == 'False2'):
                        tkinter.messagebox.showerror(title = '更新域名--错误', message='输入格式错误!\n输入行数不为纯数字!')
                    else :
                        tkinter.messagebox.showerror(title = '删除域名--错误', message='输入行数越界!\n输入行数为0或者超出域名总行数!')
                    update_value_entry.destroy()
                    update_value_save_bt.destroy()                                           
                update_value_save_bt = tk.Button(domain_input_top, text='OK', width=5, command = update_save)
                update_value_save_bt.place(x = 532 ,y = 295)        

            def domain_input_top_domain_check(): #域名检查             
                check_result_list = domain_input.check_domain() 
                tkinter.messagebox.showinfo(title = '域名检查--结果', message = '输入域名数:{}\n正确域名数:{}\n错误域名数:{}\n错误域名行:{}'.format(check_result_list[0],check_result_list[1],check_result_list[2],check_result_list[3]))
                
            def domain_input_top_ok(): #域名最终结果检查
                check_result_list = domain_input.check_domain() 
                if (check_result_list[3] == '0'): #域名全部正确
                    file_name = pwd.replace('Cms_get','Domain_input') + 'url.txt'
                    file = open(file_name,'r+',encoding = 'utf-8')
                    quchong_list = file.readlines()
                    file.close()
                    for i in range(len(quchong_list)):
                        quchong_list[i] = quchong_list[i].rstrip('\n')
                    self.domain_list = list(set(quchong_list))  #获取去重后的域名列表
                    self.domain_list.sort(key = quchong_list.index) #按照原有顺序排列
                    tkinter.messagebox.showinfo(title = '域名输入--提示',message = '所有域名输入正确!\n域名已成功输入!')
                    domain_input_top.destroy()
                    self.output_data_label['text'] = '工具动态>>:正在停留GUI主界面!'
                    self.output_data_label.config(fg = 'green')  
                    self.output_data_label.update()                     
                else:
                    tkinter.messagebox.showwarning(title = '域名输入--警告', message = '存在域名输入错误!\n域名未成功输入!') 
                
            def domain_input_top_quit():
                self.domain_list = []
                tkinter.messagebox.showwarning(title = '域名输入--警告', message = '域名未成功输入!') 
                domain_input_top.destroy()
                
            domain_input_top_insert_value_bt = tk.Button(domain_input_top,text  = '新增域名',width = 10,command = domain_input_top_insert_value)
            domain_input_top_insert_value_bt.place(x = 20,y = 230)             
            domain_input_top_delete_value_bt = tk.Button(domain_input_top,text  = '删除域名',width = 10,command = domain_input_top_delete_value)
            domain_input_top_delete_value_bt.place(x = 20,y = 260)
            domain_input_top_update_value_bt = tk.Button(domain_input_top,text  = '更新域名',width = 10,command = domain_input_top_update_value)
            domain_input_top_update_value_bt.place(x = 20,y = 290)
            domain_input_top_domain_check_bt = tk.Button(domain_input_top, text = '域名检查',width = 10,command = domain_input_top_domain_check)
            domain_input_top_domain_check_bt.place(x = 20,y = 320)
            domain_input_top_ok_bt   = tk.Button(domain_input_top, text = '确认',width = 10,command = domain_input_top_ok)
            domain_input_top_ok_bt.place(x= 20,y = 350)
            domain_input_top_quit_bt = tk.Button(domain_input_top, text = '取消',width = 10,command = domain_input_top_quit)
            domain_input_top_quit_bt.place(x = 498,y = 350)          
        domain_input_button = tk.Button(self.window,text = '输入域名',command = creat_domain_input_top)
        domain_input_button.place(x = 455,y =115)      
    
    
    def creat_label_frame_three(self): #设置方框-3-Web指纹识别
        label_frame_three = tk.LabelFrame(self.window,text = '指纹识别',width = 110,height = 90)
        label_frame_three.place(x = 790,y = 80)
        program_state_radio_input = tk.BooleanVar()  
        output_label_frame = tk.LabelFrame(self.window,text = '结果输出栏',width = 900,height = 280)
        output_label_frame.place(x = 50,y = 180)
        output_message = tk.StringVar()          
        output_table = ttk.Treeview(output_label_frame,show = "headings")
        output_table["columns"]=("序号","域名","标题","IP","CMS","Banner","操作系统","服务器","JS框架","开发语言")
        output_table.column("序号",width = 30)
        output_table.column("域名",width = 110)
        output_table.column("标题",width = 142)
        output_table.column("IP",width = 100)
        output_table.column("CMS",width = 80)
        output_table.column("Banner",width = 150)
        output_table.column("操作系统",width = 70)
        output_table.column("服务器",width = 70)
        output_table.column("JS框架",width = 70)
        output_table.column("开发语言",width = 70)
        output_table.heading("序号",text = "序号") 
        output_table.heading("域名",text = "域名")  
        output_table.heading("标题",text = "标题") 
        output_table.heading("IP",text = "IP") 
        output_table.heading("CMS",text = "CMS") 
        output_table.heading("Banner",text = "Banner") 
        output_table.heading("操作系统",text = "操作系统") 
        output_table.heading("服务器",text = "服务器") 
        output_table.heading("JS框架",text = "JS框架") 
        output_table.heading("开发语言",text = "开发语言") 
        output_table.place(x = 0,y = 10)    

        def check_choose():
            if (program_state_radio_input.get() == False):#序号,域名（URL）,title,IP,cms,banner,server,os,dev_language,所有的获取信息的列表的格式均是:[['url','message'],[...],[...]]
                self.output_data_label['text'] = '工具动态>>:正在查看工具配置信息...'
                self.output_data_label.config(fg = 'green')  
                self.output_data_label.update()                
                tkinter.messagebox.showinfo(title = '运行--配置信息', message = '域名输入数:{}\nURL连接超时:{}s\nURL代理状态:{}\n协程池协程数:{}\n指纹提取状态:{}\n文件保存格式:{}'
                .format(len(self.domain_list),self.url_time_out,self.proxy_setting,self.association_number,self.md5_finger_get,self.file_save_type_get))
                if (len(self.domain_list) != 0): #域名输入存在,程序运行
                    '''域名（URL）,title,IP,(cms,banner),os,server,js_frame,dev_language,输出列表的格式是:[['domain','title','iP','cms','banner','os','server','js_frame','dev_language'],[...],[...]]'''
                    for item in output_table.get_children():#清除表格已有内容,初始化表格
                        output_table.delete(item)
                    start = time()
                    self.output_data_label['text'] = '工具动态>>:正在进行Web指纹识别...'
                    self.output_data_label.config(fg = 'green')
                    self.output_data_label.update()
                    headers_list,proxy_list = user_function.get_headers_and_proxy_list(proxy_setting = self.proxy_setting,time_out = self.url_time_out,association_number = self.association_number)
                    result_list = fingerprint_identification.fingerprint_identification(domain_list = self.domain_list,headers_list = headers_list,proxy_list = proxy_list,time_out = self.url_time_out,association_number = self.association_number).get_result_dict()                
                    self.output_data_label['text'] = '工具动态>>:正在判断是否符合提取已识别Cms的MD5指纹条件...'
                    self.output_data_label.config(fg = 'green')
                    self.output_data_label.update() 
                    if (self.md5_finger_get == 'open'): #开启cms_md5指纹提取
                        identified_domain_list,identified_cms_name_list = [],[] #分别获取已识别cms的domain和cms名                  
                        for i in range(len(result_list)):
                            if ((result_list[i][3] != 'Not_found') and (',' not in result_list[i][3])):
                                identified_domain_list.append(result_list[i][0])
                                identified_cms_name_list.append(result_list[i][3]) 
                            else : pass

                        if (len(identified_domain_list) != 0): #存在cms被唯一识别时,对已识别的cms的文件MD5值指纹获取
                            self.output_data_label['text'] = '工具动态>>:符合条件，正在提取已识别Cms的MD5指纹...'
                            self.output_data_label.config(fg = 'green')
                            self.output_data_label.update() 
                            file_md5_list = user_function.get_file_md5_list(domain_list = identified_domain_list,cms_name_list = identified_cms_name_list,time_out = self.url_time_out,proxy_list = proxy_list,association_number = self.association_number) 
                            if (file_md5_list.count(['Not_found']) != len(file_md5_list)): #列表值不全是['Not_found']
                                self.output_data_label['text'] = '工具动态>>:已提取出已识别Cms的MD5指纹...'
                                self.output_data_label.config(fg = 'green')
                                self.output_data_label.update()                                  
                                file_md5_get_top = tk.Toplevel(self.window)
                                self.center_window(1000,400,file_md5_get_top)                              
                                file_md5_get_top.title('发现新指纹-MD5')
                                file_md5_get_table = ttk.Treeview(file_md5_get_top,show = "headings")
                                file_md5_get_table["columns"] = ("Num","Cms","File_path","Match_pattern","Options")
                                file_md5_get_table.column("Num",width = 50)
                                file_md5_get_table.column("Cms",width = 180)
                                file_md5_get_table.column("File_path",width = 300)
                                file_md5_get_table.column("Match_pattern",width = 342)
                                file_md5_get_table.column("Options",width = 85)
                                file_md5_get_table.heading("Num",text = "Num") 
                                file_md5_get_table.heading("Cms",text = "Cms(y=1)") 
                                file_md5_get_table.heading("File_path",text = "File_path(y=2)")
                                file_md5_get_table.heading("Match_pattern",text = "Match_pattern(y=3)")
                                file_md5_get_table.heading("Options",text = "Options(y=4)")
                                file_md5_get_table.place(x = 20 ,y = 20)
                                yscrollbar = Scrollbar(file_md5_get_top,orient = VERTICAL,command = file_md5_get_table.yview)
                                file_md5_get_table.configure(yscrollcommand = yscrollbar.set)
                                yscrollbar.pack(side = RIGHT, fill = Y)         
                                for item in file_md5_get_table.get_children():#清除表格已有内容,初始化表格
                                    file_md5_get_table.delete(item) 
                                for i in range(len(file_md5_list)): 
                                    if (file_md5_list[i] != ['Not_found']):
                                        file_md5_get_table.insert('',i + 1 ,values=(i + 1,file_md5_list[i][0],file_md5_list[i][1],file_md5_list[i][2],file_md5_list[i][3]))
                                    else : pass
                                        
                                def insert_value():
                                    insert_value = user_function.add_file_md5_to_cms_database(file_md5_list) #添加指纹到CMS指纹库
                                    tkinter.messagebox.showinfo(title = '添加指纹--提示',message = '已成功将指纹添加至CMS指纹库!')
                                    file_md5_get_top.destroy()
                                    
                                def insert_quit():
                                    tkinter.messagebox.showinfo(title = '添加指纹--提示',message = '未将指纹添加至CMS指纹库!')
                                    file_md5_get_top.destroy()
                                    
                                file_md5_get_table_insert_value_bt = tk.Button(file_md5_get_top,text = '添加指纹至CMS指纹库',width = 20,command = insert_value)
                                file_md5_get_table_insert_value_bt.place(x = 20,y = 350)  
                                file_md5_get_table_exit_bt = tk.Button(file_md5_get_top,text = '退出',width = 20,command = insert_quit)
                                file_md5_get_table_exit_bt.place(x = 830,y = 350) 
                                
                            else :
                                tkinter.messagebox.showinfo(title = '提取指纹--提示',message = '未从网页中找到MD5指纹!,指纹提取无效!')
                        else : 
                            self.output_data_label['text'] = '工具动态>>:判断出不符合提取指纹条件,未进行指纹提取！'
                            self.output_data_label.config(fg = 'green')
                            self.output_data_label.update() 
                            tkinter.messagebox.showinfo(title = '提取指纹--提示',message = '不存在已识别的Cms,指纹提取无效!')                            
                    else:pass
                    self.output_data_label['text'] = '工具动态>>:正在获取收集程序运行结果...'
                    self.output_data_label.config(fg = 'green')
                    self.output_data_label.update() 
                    for i in range(len(result_list)): #把程序得到的结果展示到表格中
                        output_table.insert('',i + 1,values = (i + 1 ,result_list[i][0],result_list[i][1],result_list[i][2],result_list[i][3],result_list[i][4],result_list[i][5],result_list[i][6],result_list[i][7],result_list[i][8]))                                                                     
                    
                    self.output_data_label['text'] = '工具动态>>:正在保存运行结果至文件路径"{}"下...'.format(pwd.replace('Cms_get','Result_output'))
                    self.output_data_label.config(fg = 'green')
                    self.output_data_label.update()  
                    output_file_save = user_function.output_save(result_list,self.file_save_type_get) #文件保存 
                    self.output_data_label['text'] = '工具动态>>:识别完成                          识别域名数:{}                          运行时间:{}s'.format(str(len(self.domain_list)),round(time() - start,2)) 
                    self.output_data_label.config(fg = 'green')
                    self.output_data_label.update()
                
                else :
                    tkinter.messagebox.showerror(title = '程序开始--错误', message = '域名未输入!')
                    self.output_data_label['text'] = '工具提示>>:域名未成功输入!'
                    self.output_data_label.config(fg = 'blue')
                    self.output_data_label.update()                                                 
            else : exit()     
                 
        program_state_check_button_one = tk.Radiobutton(label_frame_three,text = '开始',variable = program_state_radio_input,value = False,command = check_choose)
        program_state_check_button_one.place(x = 20,y = 5)
        program_state_check_button_two = tk.Radiobutton(label_frame_three,text = '退出',variable = program_state_radio_input,value = True,command = check_choose)
        program_state_check_button_two.place(x = 20,y = 35)    
        
        
if __name__=='__main__':
    GUI()        