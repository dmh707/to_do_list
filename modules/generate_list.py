'''
This file needs to take the sublists and add the items in the sublists to the list if and only if I have not run the program since the list should have been updated
This file will return a python list of tasks or tags, which will then be processed by tags.py
'''
import os
import abc
from datetime import date,timedelta,datetime
import re
def get_last_checked(test = False):
    last_checked_filename='.\last_checked.txt'
    last_checked =''
    with open(last_checked_filename,'r') as f:
        x=f.readline()
        x=x.strip()
        last_checked=x
    if not test:
        today = date.today()
        with open(last_checked_filename,'w') as f:
            f.write(str(today))
    format = "%Y-%m-%d"
    last_checked = datetime.strptime(last_checked, format).date()
    return last_checked
last_checked = get_last_checked()

class Main:
    def __init__(self) -> None:
        self.mainlist_filename = '.\list.txt'
        self.sublist_filenames = self.get_sublists_filenames()
        self.list = self.get_list()
        self.update_mainlist_file()
    def update_mainlist_file(self):
        output = []
        for line in self.list:
            output.append(line+'\n')
        with open(self.mainlist_filename,'w') as f:
            f.writelines(output)
    def get_sublists_filenames(self):
        files = os.listdir('.\sublists')
        return files
    def get_repeat_type(self,filename):
        repeat_types={
            'daily':Daily,
            'weekly':Weekly,
            'monthly':Monthly
        }
        return repeat_types[filename.removesuffix('.txt').split('-')[0]]
    def get_list(self):
        lysts = []
        for s in self.sublist_filenames:
            lysts.append(self.get_repeat_type(s)(s))
        first_list = []
        with open(self.mainlist_filename,'r') as f:
            first_list=f.readlines()
        untagged_str = '-UNTAGGED'
        output_list=[]
        if untagged_str not in first_list[0]:
            output_list=[untagged_str]
        output_list+=first_list
        for lyst in lysts:
            if len(lyst.list):
                if untagged_str not in lyst.list[0]:
                    output_list.append(untagged_str)
                output_list+=lyst.list
        filtered_output_list=[]
        if '' in output_list:
            output_list.remove('')
        for line in output_list:
            if line != '' and (line[0] == '-' or line not in filtered_output_list):
                filtered_output_list.append(line.strip())
        return filtered_output_list


class Repeat_Type(abc.ABC):
    def __init__(self,filename) -> None:
        super().__init__()
        self.filename_small = filename
        self.filename = f'.\sublists\{filename}'
        self.repeat_days = self.get_repeat_day()
        self.list=[]
        self.need_list_bool = self.need_list()
        if self.need_list_bool:
            self.get_list()
    @abc.abstractmethod
    def need_list(self):
        pass
    def renew_check(self,renewal):
        global last_checked
        if renewal>last_checked:
            return True
        return False
    def get_list(self):
        list=[]
        with open(self.filename,'r') as f:
            list=f.readlines()
        for line in list:
            self.list.append(line.strip())
    def get_repeat_day(self):
        f=self.filename_small.removesuffix('.txt')
        f_list=f.split('-')
        if len(f_list)>1:
            return f_list[1]
        return False
            
class Daily(Repeat_Type):
    def __init__(self, filename) -> None:
        super().__init__(filename)
    def need_list(self):
        today = date.today()
        return self.renew_check(today)

class Weekly(Repeat_Type):
    def __init__(self, filename) -> None:
        super().__init__(filename)
    def need_list(self):
        days_dict = {
            'M':'Monday',
            'T':'Tuesday',
            'W':'Wednesday',
            'H':'Thursday',
            'F':'Friday',
            'A':'Saturday',
            'S':'Sunday'}
        days = []
        for day in self.repeat_days:
            days.append(self.get_last_date_of_weekday(days_dict[day]))
        days.sort()
        renewal = days[-1]
        return self.renew_check(renewal)
    def get_last_date_of_weekday(self,weekday):
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        x=days.index(weekday)
        today = date.today()
        offset = (today.weekday() - x) % 7
        last_date = today - timedelta(days=offset)
        return last_date
class Monthly(Repeat_Type):
    def __init__(self, filename) -> None:
        super().__init__(filename)
    def need_list(self):
        repeat_days_list = self.get_repeat_days_list()
        days = []
        for day in repeat_days_list:
            days.append(self.get_last_date_of_monthday(int(day)))
        days.sort()
        renewal = days[-1]
        return self.renew_check(renewal)
    def get_last_date_of_monthday(self,day_of_month):
        today = date.today()
        day_this_month = today.replace(day=day_of_month)
        output = day_this_month
        if day_this_month > today:
            last_month = (today.replace(day=1) - timedelta(days=1)).month
            day_last_month = today.replace(day=day_of_month,month=last_month)
            output = day_last_month
        return output
    def get_repeat_days_list(self):
        x=self.repeat_days
        output_list=[]
        while len(x)!=0:
            output_list.append(x[0:2])
            if len(x)>1:
                x=x[2:]
            else:
                x=[]
        return output_list

if __name__ == '__main__':
    Main()