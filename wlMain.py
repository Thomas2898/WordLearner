from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.widget import Widget

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
            
<SubjectScreen>:
    subject: subject
    BoxLayout:
        orientation: "vertical"
                
        BoxLayout:
            RecycleView:
                viewclass: 'SelectableLabel'
                data : [{'text': str(x)} for x in root.subjects]
                SelectableRecycleBoxLayout:
                    cols: 1
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    multiselect: True
                    touch_multiselect: True  
                    
        TextInput:
            id: subject
            multinline: False
            size_hint: 1, 0.2
        Button:
            text: 'Add Subject'
            size_hint: 1, 0.2
            on_press: root.addSubjectBtn()
''')

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


class SubjectScreen(RecycleView):
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

class myApp(App):
    def build(self):
        return SubjectScreen()

if __name__ == '__main__':
    myApp().run()