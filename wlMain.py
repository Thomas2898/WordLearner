from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.widget import Widget

#Where i learned how to get the labels selectable using a recycleview
#https://kivy.org/doc/stable/api-kivy.uix.recycleview.html
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, SubjectScreen, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            SubjectScreen, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            print("User Clicked")
            print(self.text)
            #rv.data.append({'text': str("Hello it works")})
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, SubjectScreen, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(SubjectScreen.data[index]))
            #print(rv.data.pop(index))
            #rv.data.pop(index)
        else:
            print("selection removed for {0}".format(SubjectScreen.data[index]))

class SubPopup(Popup):
    currentSub = ObjectProperty(None)
    newSub = ObjectProperty(None)

    def updateSubject(self):
        print("Entered updateSubject")
        print(self.currentSub.text)
        print(self.newSub.text)

    def deleteSubject(self):
        print("Entered deleteSubject")
        print(self.currentSub.text)

class SubjectScreen(Screen):
    subjects = ListProperty([])
    subject = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SubjectScreen, self).__init__(**kwargs)
        self.getSubjects()

    def getSubjects(self):
        self.subjects = [{'text': str(x)} for x in range(20)]
        #self.data.append({'text': str("Hello it works")})

    def addSubjectBtn(self):
        print(self.subject.text.upper())
        if self.subject.text in self.subjects:
            print("Already exists")
        else:
            self.subjects.append(self.subject.text)

    #Used to open a pop up window that will aloow the user to update and delete subjects
    def openSubPopup(self):
        pops = SubPopup()
        pops.open()


class TopicScreen(Screen):
    print("Moving to TopicScreen")

    def addTopicBtn(self):
        print("Add topic btn works")

    def getTopics(self):
        self.subjects = [{'text': str(x)} for x in range(20)]
        #self.data.append({'text': str("Hello it works")})
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class wlApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    wlApp().run()