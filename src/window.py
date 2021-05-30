# window.py
#
# Copyright 2021 Oliver Hust
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk


@Gtk.Template(resource_path='/org/trolliverpust/CounterPY/window.ui')
class SimpleCounterWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SimpleCounterWindow'

    # getting access to the GTK elements
    counter_display = Gtk.Template.Child()
    dec = Gtk.Template.Child()
    inc = Gtk.Template.Child()
    undo = Gtk.Template.Child()
    redo = Gtk.Template.Child()
    Grid1 = Gtk.Template.Child()
    zero = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.counter_value = 0          # modified value
        self.value_history = [0]        # saves values for undoing and redoing
                                        # things
        self.history_pointer = 0        # saves current position if moving
                                        # in history with undo / redo buttons
                                        # default value is pointing to the last
                                        # element in history list
        self.moving_in_history = False  # saves if we moved in history before

        self.inc.connect("clicked",self.increase)
        self.dec.connect("clicked",self.decrease)
        self.undo.connect("clicked",self.undo_action)
        self.redo.connect("clicked",self.redo_action)
        self.zero.connect("clicked",self.set_zero)

        # Overwriting the UI-File because
        # i didn't find the proper options
        # in Glade
        self.redo.set_sensitive(False)
        self.undo.set_sensitive(False)
        self.Grid1.set_row_spacing(5)
        self.Grid1.set_column_spacing(5)

    def set_value(self,value):
        """
        Changes the global value attribute to the given value,
        also updates label
        """
        self.counter_value = value
        self.counter_display.set_text(str(self.counter_value))
        self.update_buttons()

    def set_new_present(self):
        """
        is triggered iff user wants non-history action
        then the list of the past values is being cut at the
        current position of the history pointer
        """
        self.moving_in_history = False
        self.value_history = self.value_history[:self.history_pointer+1]
        self.history_pointer = len(self.value_history)-1

    def increase(self,args):
        """
        increases value by 1
        makes new entry in history
        """
        if self.moving_in_history:
            self.set_new_present()
        self.value_history.append(self.counter_value + 1)
        self.history_pointer = len(self.value_history)-1
        self.set_value(self.counter_value + 1)

    def decrease(self,args):
        """
        decreases value by 1
        makes new entry in history
        """
        if self.moving_in_history:
            self.set_new_present()
        self.value_history.append(self.counter_value - 1)
        self.history_pointer = len(self.value_history)-1
        self.set_value(self.counter_value - 1)

    def set_zero(self,args):
        """
        sets value to 0
        makes new entry in history
        """
        if self.moving_in_history:
            self.set_new_present()
        self.value_history.append(0)
        self.history_pointer = len(self.value_history)-1
        self.set_value(0)

    def update_buttons(self):
        """
        makes sure undo and redo buttons are only sensitive if necessary
        """
        if self.moving_in_history:
            self.undo.set_sensitive(self.history_pointer > 0)
            self.redo.set_sensitive(self.history_pointer < len(self.value_history)-1)
        else:
            self.undo.set_sensitive(True)
            self.redo.set_sensitive(False)

    def undo_action(self,args):
        """
        moves pointer of history to the next-early entry and applies
        this value for the displayed value
        """
        if not self.moving_in_history:
            self.moving_in_history = True
        self.history_pointer -= 1
        self.set_value(self.value_history[self.history_pointer])
        self.update_buttons()

    def redo_action(self,args):
        """
        moves pointer of history to the next-recent entry and applies
        this value for the displayed value
        """
        self.history_pointer += 1
        self.set_value(self.value_history[self.history_pointer])
        self.update_buttons()
