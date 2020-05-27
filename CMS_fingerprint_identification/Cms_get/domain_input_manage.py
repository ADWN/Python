import os,re 
class domain_input(object):
    def __init__(self):
        self.file_name  = (os.getcwd() + '/Domain_input/').replace('\\','/') + 'url.txt'  
        self.pattern    = re.compile(
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
        )        
        
    def insert_domain(self,domain): #添加域名  
        wirte_file  = open(self.file_name,'a',encoding='utf-8')
        wirte_file.write(domain + '\n')   
        wirte_file.close()
        insert_flag = 'True'
        
        return insert_flag
                
    def delete_domain(self,row_number): #删除域名
        if (row_number.isdigit()):    #输入行为纯数字（0或者正整数）
            read_file  = open(self.file_name,'r',encoding = 'utf-8')
            domain_get = read_file.readlines()
            read_file.close() 
            if (0 < int(row_number) <= len(domain_get)): #输入为数字且在范围内          
                domain_get.pop(int(row_number) - 1)               
                wirte_file = open(self.file_name,'w+',encoding = 'utf-8')
                wirte_file.writelines(domain_get) 
                wirte_file.close()
                delete_flag = 'True'       #成功删除域名
            else : 
                delete_flag = 'False2' #输入行数越界!\n输入行数为0或者超出域名总行数!
        else : 
            delete_flag = 'False1' #输入格式错误!\n输入行数不为纯数字!
        
        return delete_flag
            
            
    def update_domain(self,update_str):                                 #更新域名
        pattern = '.+\|.+'#只匹配XXX|XXX格式输入
        if (re.search(pattern, update_str) != None):                  #输入字符串格式正确
            update_value_list = update_str.split('|')
            row_number,domain = update_value_list[0],update_value_list[1]
            if (row_number.isdigit()):                            #输入行为纯数字（0或者正整数）
                read_file  = open(self.file_name,'r',encoding = 'utf-8')
                domain_get = read_file.readlines()
                read_file.close()    
                if (0 < int(row_number) <= len(domain_get)): #输入为数字且在范围内   
                    domain_get[int(row_number) - 1] = domain + '\n'
                    wirte_file = open(self.file_name,'w+',encoding = 'utf-8')
                    wirte_file.writelines(domain_get) 
                    wirte_file.close()
                    update_flag = 'True'      #函数运行正确
                else :
                    update_flag = 'False3' #输入行数越界!\n输入行数为0或者超出域名总行数!
            else :
                update_flag = 'False2' #输入格式错误!\n输入行数不为纯数字!
        else :
            update_flag = 'False1' #输入格式错误!\n输入格式不为number|domain!
            
        return update_flag
    
    def check_domain(self):  
        true_domain_count = 0
        fail_domain_list,check_result_list = [],[]
        try:
            file = open(self.file_name,'r',encoding = 'utf-8')
            domain_input = file.readlines()
            if(len(domain_input) != 0): #文件中有域名
                for i in range(len(domain_input)):
                    domain_input[i].replace("\n","")
                    if self.pattern.match(domain_input[i]):
                        true_domain_count = true_domain_count + 1
                    else:
                        fail_domain_list.append(i + 1)             #添加错误域名的列序号到列表
                check_result_list.append(len(domain_input))       #文件总域名数
                check_result_list.append(true_domain_count)      #文件正确域名数
                check_result_list.append(len(fail_domain_list)) #文件错误域名数
                if (len(fail_domain_list) == 0):               #不存在错误域名
                    check_result_list.append('0')             #文件错误域名所在行为0,所有域名输入正确!
                else :
                    check_result_list.append(str(fail_domain_list).replace('[','').replace(']','')) #文件错误域名所在行                           
            else : 
                check_result_list.append(0) 
                check_result_list.append(0)
                check_result_list.append(0) 
                check_result_list.append('Null') #文件为空,错误域名行为False    
        except IOError:
            print('打开文件:{}失败!\n程序找不到该文件!'.format(self.file_name ))
        finally:
            file.close()
            
        return check_result_list     
    
    
