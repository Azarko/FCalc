# -*- coding: utf-8 -*-

"""
Freak Calc GUI.
App for calculate party payments.
"""

from Tkinter import *
from tkMessageBox import askyesno, showinfo, showerror
from tkSimpleDialog import askinteger
from core import FreakCore

__version__ = '0.9.1 beta'

# TODO: move to root folder.
# TODO: save, load
# TODO: title frame


class FreakGUI(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.__freaks = FreakCore()
        self.__freak_frames = []
        self.pack(expand=YES, fill=BOTH)
        self.master.title('Freak Calculator')
        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.create_menu_file()
        self.create_menu_about()

    def create_menu_file(self):
        menu = Menu(self.menu)
        menu.add_command(label='Save', command=self.not_ready)
        menu.add_command(label='Save as...', command=self.not_ready)
        menu.add_command(label='Load', command=self.not_ready)
        menu.add_separator()
        menu.add_command(label='Exit', command=self.quit)
        self.menu.add_cascade(label='File', underline=0, menu=menu)

    def create_menu_about(self):
        menu = Menu(self.menu)
        menu.add_command(label='Help', command=self.help)
        menu.add_command(label='About', command=self.about)
        self.menu.add_cascade(label='About', underline=0, menu=menu)

    def create_toolbar(self):
        toolbar = Frame(self)
        toolbar.pack(side=TOP, fill=X)
        self.calc_button = Button(toolbar, text='Calculate', cursor='hand2', command=self.calculate, state=DISABLED)
        self.calc_button.pack(side=LEFT)
        Button(toolbar, text='Add freak', cursor='hand2', command=self.add_freak).pack(side=LEFT)
        Button(toolbar, text='Add N freaks', cursor='hand2', command=self.add_n_freaks).pack(side=LEFT)
        Button(toolbar, text='Clear', cursor='hand2', command=self.clear).pack(side=LEFT)
        Button(toolbar, text='Delete all freaks', cursor='hand2', command=self.delete_all_freaks).pack(side=LEFT)
        self.edit_button = Button(toolbar, text='Edit', cursor='hand2', command=self.change_state, state=DISABLED)
        self.edit_button.pack(side=LEFT)
        self.toolbar = toolbar

    def add_freak(self):
        frame = Frame(self)
        self.__freaks.add_freak()
        freak_name = self.__freaks[-1].name
        name = Entry(frame, width=30)
        name.insert(0, freak_name)
        name.pack(side=LEFT)
        pay = Entry(frame, width=15)
        pay.insert(0, 0.0)
        pay.pack(side=LEFT)
        Label(frame, width=15, text='N/A').pack(side=LEFT)
        Button(frame, text='Del', command=lambda: self.delete_freak(frame)).pack(side=LEFT)
        frame.pack(side=TOP, )
        self.__freak_frames.append(frame)
        if self.calc_button['state'] == DISABLED:
            self.calc_button['state'] = NORMAL

    def add_n_freaks(self):
        n = askinteger('Enter count of freaks', 'Count of new freaks')
        if n is None:
            return
        elif n <= 0:
            showerror('Error!', 'Count must be positive integer!')
            raise ValueError('Count must be positive integer!')
        elif n > 15:
            showerror('Error!', 'Count too big! Please input value between 1 and 15')
            raise ValueError('Count too big!')
        for count in range(n):
            self.add_freak()
            self.update()

    def delete_freak(self, frame):
        self.__freaks.delete_freak_by_index(self.__freak_frames.index(frame))
        self.__freak_frames.remove(frame)
        frame.pack_forget()
        if not len(self.__freak_frames):
            self.calc_button['state'] = DISABLED

    def delete_all_freaks(self):
        if askyesno('Really delete', 'Are you really want to delete all members?'):
            for frame in self.__freak_frames:
                frame.pack_forget()
            self.__freaks.delete_all_freaks()
            self.calc_button['state'] = DISABLED

    def clear(self):
        if askyesno('Really clear', 'Are you really want to clear all payment information?'):
            for label in self.get_pay_entries():
                label.delete(0, len(label.get()))
                label.insert(0, 0.0)

    def get_pay_entries(self):
        return [frame.winfo_children()[1] for frame in self.__freak_frames]

    def get_mp_labels(self):
        return [frame.winfo_children()[2] for frame in self.__freak_frames]

    def calculate(self):
        for counter, pay_entry in enumerate(self.get_pay_entries()):
            freak_balance = float(pay_entry.get()) if pay_entry.get().isdigit() else 0.0
            self.__freaks[counter].set_balance(freak_balance)
        self.__freaks.calculate_payments()
        for freak, mp_label in zip(self.__freaks, self.get_mp_labels()):
            mp_label['text'] = '%.2f' % freak.need_to_pay
        self.change_state()

    def change_state(self):
        def change_element(element):
            if element['state'] == NORMAL:
                element['state'] = DISABLED
            else:
                element['state'] = NORMAL

        for element in self.toolbar.winfo_children():
            change_element(element)
        for frame in self.__freak_frames:
            for element in frame.winfo_children()[0:2] + [frame.winfo_children()[3]]:
                change_element(element)

    def not_ready(self):
        print 'Not ready'

    def help(self):
        text = '''
        How to use Freak Calculator:
         - press 'Add freak' for add new member;
         - set his name and pay-value;
         - repeat it for all you party-members;
         - press calculate and watch result;
         - if you need change something - press 'Edit'
        
        Press 'Clean' for reset all pays.
        Press 'Delete all freaks' for delete all members.
        Press 'Add N freaks' for add few members at same time.
        '''
        showinfo('FreakCalc version %s' % __version__, text)

    def about(self):
        text = 'FreakCalc ver. %s.\nApp for calculating party payments.\n2017.' % __version__
        showinfo('About FreakCalc', text)


if __name__ == '__main__':
    FreakGUI().mainloop()
