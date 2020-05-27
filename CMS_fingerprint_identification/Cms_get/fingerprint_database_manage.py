import os,re,openpyxl 
import tkinter.messagebox


class fingerprint_database_manage(object):
    def __init__(self):
        self.banner_file_name = (os.getcwd() + '/Fingerprint_database/').replace('\\','/') + 'banner.xlsx'
        self.cms_file_name    = (os.getcwd() + '/Fingerprint_database/').replace('\\','/') + 'cms.xlsx'
        
    def banner_insert_fingerprint(self,insert_str):    #banner增
        pattern = '.+\|.+'                            #只匹配XXX|XXX格式输入
        if (re.search(pattern, insert_str) != None): #输入字符串格式正确
            insert_value_list = insert_str.split('|')
            workbook  = openpyxl.load_workbook(self.banner_file_name)
            worksheet = workbook.active    #获取表的banner表单(默认最活跃的即是第一个表)
            worksheet.append([insert_value_list[0], insert_value_list[1]])
            workbook.save(self.banner_file_name)
            workbook.close
            insert_flag = 'True'     #Banner指纹规则库已成功添加指纹!
        else :
            insert_flag = 'False' #输入格式错误!\n输入格式不为Name|Key!
            
        return insert_flag
    
    def cms_insert_fingerprint(self,insert_str): #cms增
        pattern = '.+\|.+\|.+\|.+'                                    #只匹配XXX|XXX|XXX|XXX格式输入,由于命中率为0,故不用输入,添加时程序自动添加该值
        if (re.search(pattern, insert_str) != None):                #输入字符串格式正确
            insert_value_list = insert_str.split('|')
            Cms_name,File_path,Match_pattern,Options = insert_value_list[0],insert_value_list[1],insert_value_list[2],insert_value_list[3]
            try :
                if (File_path.index('/') == 0 ):              #添加指纹路径字符串第一个字符必须为/
                    if ((Options.rstrip('\n') == 'keyword') or (Options.rstrip('\n') == 'md5')):
                        workbook  = openpyxl.load_workbook(self.cms_file_name)
                        worksheet = workbook.active      #获取表的cms表单(默认最活跃的即是第一个表)
                        worksheet.append([Cms_name, File_path,Match_pattern,Options,0])
                        workbook.save(self.cms_file_name)
                        workbook.close
                        insert_flag = 'True'      #Cms指纹规则库已成功添加指纹!
                    else :
                        insert_flag = 'False4' #输入Options错误\n输入字符串指纹类型不为keyword或md5!
                else :
                    insert_flag = 'False3' #输入File_path错误!\n输入字符串指纹路径File_path的第一个字符不为"/"!
            except :
                insert_flag = 'False2' #输入File_path错误!\n输入字符串指纹路径File_path中不含有字符"/"!
        else :
            insert_flag = 'False1' #输入格式错误!\n输入格式不为Cms_name|File_path(/...)|Match_pattern|Options(keyword/md5)!
            
        return insert_flag
    
    def banner_delete_fingerprint(self,row_number): #banner删
        if (row_number.isdigit()): #输入行为纯数字（0或者正整数）
            workbook  = openpyxl.load_workbook(self.banner_file_name)
            worksheet = workbook.active 
            if (0 < int(row_number) < worksheet.max_row):#输入为数字且在行数范围内       
                worksheet.delete_rows(int(row_number) + 1)
                workbook.save(self.banner_file_name)
                workbook.close
                delete_flag = 'True'      #Banner指纹规则库已成功删除指纹!
            else : 
                delete_flag = 'False2' #输入行数越界!\n输入行数为0或者超出Banner指纹规则库总行数
        else         : 
            delete_flag = 'False1' #输入格式错误!\n输入行数不为纯数字!
        
        return delete_flag

    def cms_delete_fingerprint(self,row_number): #cms删
        if (row_number.isdigit()): #输入行为纯数字（0或者正整数）
            workbook  = openpyxl.load_workbook(self.cms_file_name)
            worksheet = workbook.active 
            if (0 < int(row_number) < worksheet.max_row):#输入为数字且在行数范围内       
                worksheet.delete_rows(int(row_number) + 1)
                workbook.save(self.cms_file_name)
                workbook.close
                delete_flag = 'True'      #Cms指纹规则库已成功删除指纹!
            else : 
                delete_flag = 'False2' #输入行数越界!\n输入行数为0或者超出Cms指纹规则库总行数
        else         : 
            delete_flag = 'False1' #输入格式错误!\n输入行数不为纯数字!
        
        return delete_flag

    def banner_search_fingerprint(self,row_number): #banner查
        if (row_number.isdigit()):                           #输入行为纯数字（0或者正整数）
            workbook  = openpyxl.load_workbook(self.banner_file_name)
            worksheet = workbook.active 
            if (0 < int(row_number) < worksheet.max_row):#输入为数字且在行数范围内       
                name = worksheet[int(row_number) + 1][0].value
                key = worksheet[int(row_number) + 1][1].value
                workbook.close
                search_flag  = 'True'        #Banner指纹规则库已成功查询指纹!
            else : 
                search_flag  = 'False2'   #输入行数越界!\n输入行数为0或者超出Banner指纹规则库总行数
                name         = 'Not_found'
                key          = 'Not_found'
        else                 : 
            search_flag  = 'False1' #输入格式错误!\n输入行数不为纯数字!
            name         = 'Not_found'
            key          = 'Not_found'
            
        return search_flag,row_number,name,key
    
    def cms_search_fingerprint(self,row_number): #cms查
        if (row_number.isdigit()):                           #输入行为纯数字（0或者正整数）
            workbook  = openpyxl.load_workbook(self.cms_file_name)
            worksheet = workbook.active 
            if (0 < int(row_number) < worksheet.max_row):#输入为数字且在行数范围内       
                Cms_name      = worksheet[int(row_number) + 1][0].value
                File_path     = worksheet[int(row_number) + 1][1].value
                Match_pattern = worksheet[int(row_number) + 1][2].value
                Options       = worksheet[int(row_number) + 1][3].value
                Hit           = worksheet[int(row_number) + 1][4].value               
                name = worksheet[int(row_number) + 1][0].value
                key = worksheet[int(row_number) + 1][1].value
                workbook.close
                search_flag  = 'True'            #Cms指纹规则库已成功查询指纹!
            else : 
                search_flag  = 'False2'       #输入行数越界!\n输入行数为0或者超出Cms指纹规则库总行数
                Cms_name      = 'Not_found'
                File_path     = 'Not_found'
                Match_pattern = 'Not_found'
                Options       = 'Not_found'
                Hit           = 'Not_found'
        else                 : 
            search_flag   = 'False1' #输入格式错误!\n输入行数不为纯数字!
            Cms_name      = 'Not_found'
            File_path     = 'Not_found'
            Match_pattern = 'Not_found'
            Options       = 'Not_found'
            Hit           = 'Not_found'
            
        return search_flag,row_number,Cms_name,File_path,Match_pattern,Options,Hit
    
    def banner_update_fingerprint(self,update_str): #banner改
        pattern = '.+\|.+\|.+'#只匹配x|y|XXX格式输入
        if (re.search(pattern, update_str) != None):             #输入字符串格式正确
            update_value_list = update_str.split('|')
            x,y,update_data  = update_value_list[0],update_value_list[1],update_value_list[2]
            if ((x.isdigit()) and (y.isdigit())):           #判断输入的x,y是否为纯数字
                workbook  = openpyxl.load_workbook(self.banner_file_name)
                worksheet = workbook.active             #获取表的banner表单(默认最活跃的即是第一个表)
                if ((0 < int(x) < worksheet.max_row) and (0 < int(y) <= worksheet.max_column)): #输入x,y为纯数字且在表格行列数范围内
                    worksheet.cell(row = int(x) + 1,column = int(y),value = update_data)
                    workbook.save(self.banner_file_name)
                    workbook.close
                    update_flag = 'True'      #Banner指纹规则库已成功更新指纹!
                else :
                    update_flag = 'False3' #输入行(列)数越界!\n输入的坐标中x(y)的值为0或者超过Banner指纹规则库总行(列)数!
            else :
                update_flag = 'False2' #输入格式错误!\n输入的坐标x,y不都为纯数字!
        else :
            update_flag = 'False1' #输入格式错误!\n输入格式不为x|y|data!
            
        return update_flag
    
    def cms_update_fingerprint(self,update_str): #cms改
        pattern = '.+\|.+\|.+'#只匹配x|y|XXX格式输入
        if (re.search(pattern, update_str) != None):             #输入字符串格式正确
            update_value_list = update_str.split('|')
            x,y,update_data  = update_value_list[0],update_value_list[1],update_value_list[2]
            if ((x.isdigit()) and (y.isdigit())):           #判断输入的x,y是否为纯数字
                workbook  = openpyxl.load_workbook(self.cms_file_name)
                worksheet = workbook.active             #获取表的banner表单(默认最活跃的即是第一个表)
                if ((0 < int(x) < worksheet.max_row) and (0 < int(y) <= worksheet.max_column)): #输入x,y为纯数字且在表格行列数范围内
                    if (int(y) == 2):  #指定更新第二列File_path值，判断输入更新后的数据第一个字符串是否是/
                        try :
                            if (update_data.index('/') == 0 ):
                                worksheet.cell(row = int(x) + 1,column = int(y),value = update_data)
                                workbook.save(self.cms_file_name)
                                workbook.close
                                update_flag = 'True'      #Cms指纹规则库已成功更新指纹!
                            else :
                                update_flag = 'False5' #输入更新值错误!\n更新指纹规则库的第二列的File_path,更新值的第一个字符不为"/"!
                        except :
                            update_flag = 'False4' #输入更新值错误!\n更新指纹规则库的第二列的File_path,更新值不含有字符"/"!
                    elif (int(y) == 4):      
                        if((update_data == 'keyword') or (update_data == 'md5')):
                            worksheet.cell(row = int(x) + 1,column = int(y),value = update_data)
                            workbook.save(self.cms_file_name)
                            workbook.close
                            update_flag = 'True'      #Cms指纹规则库已成功更新指纹!
                        else :
                            update_flag = 'False6' #输入更新值错误!\n更新指纹规则库的第四列的Options,更新值不为"keyword"或"md5"!
                    elif (int(y) == 5):
                        if (update_data.isdigit()):
                            worksheet.cell(row = int(x) + 1,column = int(y),value = update_data)
                            workbook.save(self.cms_file_name)
                            workbook.close
                            update_flag = 'True'                  #Cms指纹规则库已成功更新指纹!
                        else :
                            update_flag = 'False7'            #输入更新值错误!\n更新指纹规则库的第五列的Hit，更新值不为纯数字！
                    else : 
                        worksheet.cell(row = int(x) + 1,column = int(y),value = update_data)
                        workbook.save(self.cms_file_name)
                        workbook.close
                        update_flag = 'True'       #Cms指纹规则库已成功更新指纹!
                else :
                    update_flag = 'False3' #输入行(列)数越界!\n输入的坐标中x(y)的值为0或者超过C指纹规则库总行(列)数!
            else :
                update_flag = 'False2' #输入格式错误!\n输入的坐标x,y不都为纯数字!
        else :
            update_flag = 'False1' #输入格式错误!\n输入格式不为x|y|data!
            
        return update_flag    
     
    
