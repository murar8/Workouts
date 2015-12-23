# -*- coding: utf-8 -*-
#
#  DataBaseUtils.py
#
#  Copyright 2015 Lorenzo Murarotto <lnzmrr@gmail.com>

#!python2.7

from database.DataBase import WoDataBase
from utils.GtkUtils import GtkUtils
from gi.repository import Gtk


class FrameView(Gtk.Frame):
        
        def __init__(self):
                super(FrameView, self).__init__()
                
                builder.add_from_file("main/layout/view.glade")
                builder.connect_signals(self)
                
                box=builder.get_object("box")
                self.add(box)
                
                self.listStore=builder.get_object("listStore")
                self.treeviewSelection=builder.get_object("treeviewSelection")
                self.comboBoxExcercise=builder.get_object("comboBoxExcercise")
                self.listExcercises=builder.get_object("listExcercises")
                self.calendarFrom=builder.get_object("calendarFrom")
                self.calendarTo=builder.get_object("calendarTo")

                allEntries=[[exc] for exc in woDataBase.retrieve_excercises()]
                gtkUtils.update_store(self.listExcercises,allEntries)
                gtkUtils.update_store(self.listStore,woDataBase.retrieve_all())

        def on_buttonShowAll_clicked(self,button):
                """show all entries on screen"""
                self.listStore.clear()
                gtkUtils.update_store(self.listStore,woDataBase.retrieve_all())         
                window.statusBar.push(0,"Showing ALL entries")
        
        def on_buttonDelete_clicked(self, button):
                """deletes selected items"""
                listStore,paths=self.treeviewSelection.get_selected_rows()
                
                if not paths:
                        window.statusBar.push(0,"No IDs removed")
                        return
                        
                iters=[listStore.get_iter(row) for row in paths]
                ids=[listStore.get_value(value,0) for value in iters]
                
                try:
                        [woDataBase.delete(Id) for Id in ids]
                        gtkUtils.update_store(listStore,woDataBase.retrieve_all())
                        message="successfully removed #"+str(len(ids))+" IDs!"
                        window.statusBar.push(0,message)
                except:
                        window.statusBar.push(0,"Error in removing IDs!!!")

        def on_comboBoxExcercise_changed(self,combo):
                """filters the database by the selected excercise"""
                path=combo.get_child().get_displayed_row()
                if not path: return
                iter_=self.listExcercises.get_iter(path)
                selected=self.listExcercises.get_value(iter_,0)
                excercises=woDataBase.retrieve_by_excercise(selected)
                gtkUtils.update_store(self.listStore,excercises)
                window.statusBar.push(0,"Showing Excercises for: "+selected)
        
                
        def on_calendar_day_selected(self,calendar):
                """updates the tree's store to display entries between the two dates"""
                dateFrom=gtkUtils.date_to_string(self.calendarFrom.get_date())
                dateTo=gtkUtils.date_to_string(self.calendarTo.get_date())
                
                if gtkUtils.is_later(dateFrom,dateTo):
                        self.calendarTo.select_month(int(dateFrom[5:7])-1,int(dateFrom[0:4]))
                        self.calendarTo.select_day(int(dateFrom[8:11]))
                
                if dateFrom==dateTo:
                        gtkUtils.update_store(
                                self.listStore,
                                woDataBase.retrieve_by_date(dateFrom))
                else:
                        gtkUtils.update_store(
                                self.listStore,
                                woDataBase.retrieve_by_interval(dateFrom,dateTo))

                message="Showing excercises from:  "+dateFrom+"  To:  "+dateTo
                window.statusBar.push(0,message)
                
class FrameAdd(Gtk.Frame):
        
        def __init__(self):
                super(FrameAdd, self).__init__()
                
                builder = Gtk.Builder()
                builder.add_from_file("main/layout/add.glade")
                builder.connect_signals(self)
                
                box=builder.get_object("box")
                self.add(box)
                
                self.listExcercisesAdd=builder.get_object("listExcercisesAdd")
                self.comboBoxExcerciseAdd=builder.get_object("comboBoxExcerciseAdd")
                self.entryExcercise=builder.get_object("entryExcercise")
                self.entryNotes=builder.get_object("entryNotes")
                self.spinbuttonSets=builder.get_object("spinbuttonSets")
                self.spinbuttonReps=builder.get_object("spinbuttonReps")
                self.spinbuttonWeight=builder.get_object("spinbuttonWeight")
                self.calendar=builder.get_object("calendar")
                self.buttonAdd=builder.get_object("buttonAdd")
                
                gtkUtils.update_store(
                        self.listExcercisesAdd,
                        [[exc] for exc in woDataBase.retrieve_excercises()])
                        
        def on_comboBoxExcerciseAdd_changed(self,combo):
                """loads the last known configuartion from selected excercise"""
                path=combo.get_child().get_displayed_row()
                if not path: return
                iter_=self.listExcercisesAdd.get_iter(path)
                if not iter_: return
                selected=self.listExcercisesAdd.get_value(iter_,0)
                last=woDataBase.retrieve_last_workout_by_excercise(selected)
                
                self.entryNotes.set_text(last[6])
                self.spinbuttonSets.set_value(last[3])
                self.spinbuttonReps.set_value(last[4])
                self.spinbuttonWeight.set_value(last[5])
                
                window.statusBar.push(0,"Showing last entry for given excercise")
                
        def on_buttonAdd_clicked(self,button):
                """adds the entry into the database"""
                excercise=self.entryExcercise.get_text()
                
                if not excercise:
                        path=self.comboBoxExcerciseAdd.get_child().get_displayed_row()
                        if path:
                                iter_=self.listExcercisesAdd.get_iter(path)
                                excercise=self.listExcercisesAdd.get_value(iter_,0)
                        else:
                                message="ERROR: no excercise selected"
                                window.statusBar.push(0,message)
                                return
                                
                date=gtkUtils.date_to_string(self.calendar.get_date())
                sets=self.spinbuttonSets.get_value_as_int()
                reps=self.spinbuttonReps.get_value_as_int()
                weight=self.spinbuttonWeight.get_value_as_int()
                notes=self.entryNotes.get_text()
                
                try:
                        woDataBase.add(date,excercise,sets,reps,weight,notes)
                        message="Succesfully added: "
                        for val in(date,excercise,sets,reps,weight,notes):
                                message+=str(val)+" "
                        window.statusBar.push(0,message)
                        
                except AssertionError:
                        message="ERROR: something is wrong with the values"
                        window.statusBar.push(0,message)
                
class Window(Gtk.Window):
        
        def __init__(self):
                super(Window, self).__init__(
                        title="WokoutsHistory",
                        default_height=800,
                        default_width=600)
                
                self.frameView=FrameView()
                self.frameAdd=FrameAdd()
                self.box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                self.stack=Gtk.Stack()
                self.stackSwitcher=Gtk.StackSwitcher()
                self.statusBar=Gtk.Statusbar()
                
                self.stack.add_titled(self.frameView,"frameView","View")
                self.stack.add_titled(self.frameAdd,"frameAdd","Add")
                self.stackSwitcher.set_stack(self.stack)
                self.box.pack_start(self.stackSwitcher,False,False,0)
                self.box.pack_start(self.stack,True,True,1)
                self.box.pack_end(self.statusBar,False,False,0)
                self.add(self.box)
                
                self.connect("delete-event",Gtk.main_quit)
                self.show_all()
                
if __name__ == "__main__":
        builder=Gtk.Builder()
        gtkUtils=GtkUtils()
        woDataBase=WoDataBase()
        window=Window()
        Gtk.main()


