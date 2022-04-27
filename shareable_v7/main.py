#assemble todays list
#UI today's list
#output today's list
from modules.tag import Main as Tags
from datetime import date,timedelta,datetime
class Main():
    def __init__(self) -> None:
        #self.get_mind_dump()
        self.tags = Tags()
        self.completed = 0
        self.done=[]
        self.filename = "list.txt"
        self.outputfile = "done.txt"
        self.today = date.today().strftime('%Y-%m-%d')
        self.max_tasks_to_show=5
        self.low_priority_tag_name='-LOW PRIORITY'
        self.run()
    def start_done_file(self):
        lines=False
        isToday=False
        with open(self.outputfile,'r') as f:
            lines=f.readlines()
        todayLines=0
        for line in lines:
            x=line.strip('\n')
            y=False
            if x and x[0]=='2':
                y=x
                x=''
            if isToday and x:
                todayLines+=1
            if y==str(self.today):
                isToday=True
        if isToday:
            self.completed=todayLines
        else:
            with open(self.outputfile,'a') as f:
                f.write('\n'+self.today+'\n')
    def get_mind_dump(self):
        #currently not being called because I don't need it
        x=input('\nWhat tasks are on your mind? (type a comma-separated list and press enter. Press enter immediately if you have no tasks to add.)')
        mind_dump = ['-MIND DUMP FOR TODAY']+x.split(',')
        filename='list.txt'
        with open(filename,'a') as f:
            f.write('\n')
            for line in mind_dump:
                f.write(line.strip())
                f.write('\n')
        return mind_dump
    def display_options(self,options,limit=False):
        if len(options)==0:
            print('-no options provided-')
        the_range = len(options)
        if limit != False and limit<the_range:
            the_range = limit
        for i in range(the_range):
            print(f"{i}. {options[i].strip()}")
    def get_option(self,options,option_name='option',limit=False,allow_multiselect=False):
        if allow_multiselect:
            while True:
                self.display_options(options,limit)
                x=input(f'Select index(es) of desired {option_name}: (comma-separated list) ')
                try:
                    x=x.split(',')
                    output = []
                    for index in x:
                        index=int(index)
                        selection=options[index]
                        output.append(selection)
                    return output
                except:
                    print(f'\nINVALID SELECTION(S)--must select a number(s) between 0 and {len(options)-1} to indicate the {option_name}(s) you wish to select')
        while True:
            self.display_options(options,limit)
            x=input(f'Select index of desired {option_name}: ')
            try:
                x=int(x)
                y=options[x]
                return y
            except:
                print(f'\nINVALID SELECTION--must select a number between 0 and {len(options)-1} to indicate the {option_name} you wish to select')
    def run_tasks_menu(self):
        back = 'go back to tags'
        changeLimit = 'edit the number of tasks shown at a time'
        removeLimit = 'show all tasks'
        moveToLowPriority = 'move some tasks to low priority'
        addTasks = 'add tasks to this list'
        menu = [back,changeLimit,removeLimit,moveToLowPriority,addTasks]
        print('\n')
        option = self.get_option(menu)
        if option == back:
            self.run_tags()
            return False
        if option == changeLimit:
            while True:
                y = self.max_tasks_to_show
                if not y:
                    y='SHOW ALL'
                x = input(f'How many tasks do you want to show at once? (current value is {y}) ')
                try:
                    self.max_tasks_to_show=int(x)
                    return True
                except:
                    print('\nINVALID SELECTION--must input a positive integer number')
        if option == removeLimit:
            self.max_tasks_to_show=False
            return True
        if option == moveToLowPriority:
            self.select_and_move_tasks_to_low_priority()
            return True
        if option == addTasks:
            self.addNewTasks()
            return True
    def addNewTasks(self):
        x=input('\nWhat tasks are on your mind? (type a comma-separated list and press enter. Press enter immediately if you have no tasks to add.)')
        x=x.split(',')
        self.tags.tags[self.current_tag]=x+self.tags.tags[self.current_tag]
        return x
    def select_and_move_tasks_to_low_priority(self):
        print('\n\n')
        tasks = self.tags.tags[self.current_tag]
        options = self.get_option(options=tasks,allow_multiselect=True)
        if self.low_priority_tag_name not in self.tags.tags:
            self.tags.tags[self.low_priority_tag_name]=[]
        self.tags.tags[self.low_priority_tag_name]+=options
        for option in options:
            tasks.remove(option)
        self.tags.tags[self.current_tag] = tasks
        return False
    def handle_done(self):
        with open(self.outputfile, 'a') as f:
            for item in self.done:
                f.write(item)
                f.write('\n')
        self.done=[]
        self.tags.tags[self.current_tag]=self.current_tasks
        self.tags.update_mainlist_file()
    def run_tasks(self,tasks):
        while True:
            if len(tasks)==0:
                self.run_tags()
                return False
            menu='menu'
            x=[menu]+tasks
            print('\n')
            print(f'You have completed {self.completed} tasks today.')
            if self.max_tasks_to_show:
                y=self.get_option(x,'task',limit=self.max_tasks_to_show+1)
            else:
                y=self.get_option(x,'task')
            if y==menu:
                cont = self.run_tasks_menu()
                if cont:
                    continue
                return False
            tasks.remove(y)
            self.completed=self.completed+1
            self.done.append(y)
            print('')
            self.current_tasks=tasks
            self.handle_done()
            self.current_tasks=[]
    def run_tags(self):
        self.tags.clear_empty()
        if len(self.tags.tags)==0:
            print(f'Congrats! You\'re done! You completed {self.completed} tasks!')
            return False
            
        print('\n')
        print(f'You have completed {self.completed} tasks today.')
        quit="quit program"
        tag_names = list(self.tags.tags.keys())
        tag_names.sort()
        x=[quit]+tag_names
        y=self.get_option(x,'task categories')
        if y==quit:
            return False
        self.current_tag=y
        self.run_tasks(self.tags.tags[y])
    def run(self):
        self.start_done_file()
        self.run_tags()
        


if __name__ == "__main__":
    Main()