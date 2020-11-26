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


class SelectableLabelSubjectScreen(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, subjectscreen, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabelSubjectScreen, self).refresh_view_attrs(
            SubjectScreen, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabelSubjectScreen, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, subjectscreen, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("User Clicked " + format(self.text))
            #Used to pass the value of the label that the user clicked
            SubjectScreen.subjectSelected(self.text)


class SelectableLabelTopicScreen(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, topicscreen, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabelTopicScreen, self).refresh_view_attrs(
            TopicScreen, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabelTopicScreen, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, topicscreen, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("User Clicked " + format(self.text))
            #Used to pass the value of the label that the user clicked
            TopicScreen.topicSelected(self.text)


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
        

class SubjectScreen(RecycleView, Screen):
    subjects = ListProperty([])
    subject = ObjectProperty(None)
    subjectLabel = ObjectProperty(None)
    #Used to store the value of the subject that the user has chosen
    subjectChosenName = ""

    def __init__(self, **kwargs):
        super(SubjectScreen, self).__init__(**kwargs)
        self.getSubjects()

    #Used to get the subjects to fill the list of labels on the subject scren
    def getSubjects(self):
        self.subjects = [{'text': str(x)} for x in range(20)]
        #self.data.append({'text': str("Hello it works")})

    #Called when button 'Add Subject' is clicked
    def addSubjectBtn(self):
        print(self.subject.text.upper())

        #Used to check if the subject being added already exists in the subject list
        #And if it doesnt then its added to the topic list
        if self.subject.text in self.subjects:
            print("Already exists")
        else:
            self.subjects.append(self.subject.text)

    #Gets called when the user selects a subject from the list on the subject screen
    def subjectSelected(subjectName):
        print("Subject was passed to SubjectScreen")
        print("Subject passed = " + subjectName)
        SubjectScreen.subjectChosenName = subjectName


    #Used to open a pop up window that will allow the user to update and delete subjects
    def openSubPopup(self):
        pops = SubPopup()
        pops.open()


class TopicScreen(Screen):
    topics = ListProperty([])
    topic = ObjectProperty(None)
    #Used to store the value of the topic that the user has chosen
    topicChosenName = ""

    def __init__(self, **kwargs):
        super(TopicScreen, self).__init__(**kwargs)
        self.getTopics()

    #Gets called when the add topic button is clicked on the topic screen
    def addTopicBtn(self):
        print("Add topic btn works")
        #Used to check if the topic being added already exists in the topics list
        #And if it doesnt then its added to the topic list
        if self.topic.text in self.topics:
            print("Already exists")
        else:
            self.topics.append(self.topic.text)

    #Used to get the topics to fill the list of labels on the topic scren
    def getTopics(self):
        print("In getTopics")
        self.topics = [{'text': str(x)} for x in range(20)]

    #Gets called when the user selects a topic from the list on the topic screen
    def topicSelected(topicName):
        print("Topic was passed to TopicScreen")
        print("Topic passed = " + topicName)
        #Sets the variable as the topic the user selected
        TopicScreen.topicChosenName = topicName

    #Used to test if the two variables subjectChosenName and topicChosenName change accordingly
    def testTopic(self):
        print("hello i am the testTopic")
        print("Subject chosen = " + SubjectScreen.subjectChosenName)
        print("Topic chosen = " + TopicScreen.topicChosenName)

    #def getSubjectSelected(self, subjectName):
        #print("Subject selected was ")
        #print(self.manager.ids.SubjectScreen.ids.subjectLabel.text)


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class wlApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    wlApp().run()