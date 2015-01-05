"""
This class starts the AddDefinitions add-on

This add-on will provide support to add definitions to a card
when the card/cards have been selected in the deck view.
Will support German and Japanese specifically

reference: I used the japanse support add-on as a reference for
setting up the menus and editing the card fields

author: Kelsey Jones
date: 12/12/14
"""

#import main window object(mw) from ankiqt
from aqt import mw

#import tools
from aqt.utils import showInfo

#import all QT GUI library
from aqt.qt import * #Change this later to classes you actually use

#imports the addhook, some kind of sortcut
from anki.hooks import addHook


def show_add_on():
    """
    This method determines if the user is within the deck view and
    has selected at least 1 card.
    """
    #Not yet implemented
    return True

def add_def():
    """
    Calls the 
    """
    # Not yet implemented

def createDefinitions(noteIds):
    """
    This method is passed the selected note cards from the deck browser
    """
    pass
    #Not yet implemented

class setupFieldsDialog(QDialog):
    """
    This class is the dialog that asks the user in a popup window
    to selected the word field to look up, the field to add definitions to,
    and a field to add the dictionary form if selected.
    """
    def __init__(self):
        super(setupFieldsDialog, self).__init__()

        languages = ["German", "Japanese"]
        self.decks = sorted(mw.col.decks.allNames(dyn=False))
        
        self.setWindowTitle("Select Deck Fields")
        layout = QVBoxLayout(self)

        self.label = QLabel("Select language: ")

        layout.addWidget(self.label)

        self.langSelection = QComboBox()
        for lang in languages:
            self.langSelection.addItem(lang)
            
        layout.addWidget(self.langSelection)

        #Testing signal
        #self.connect()
        """ Need to figure out how to change fields based on deck
        combo box being triggered """
        

        self.label = QLabel("Select Deck: ")

        layout.addWidget(self.label)

        self.deckSelection = QComboBox()
        for deck in self.decks:
            self.deckSelection.addItem(deck)

        self.deckSelection.setCurrentIndex(0)
            
        layout.addWidget(self.deckSelection)

        #word
        self.label = QLabel("Select word field: ")

        layout.addWidget(self.label)

        self.wordSelection = QComboBox()
        self.wordSelection.addItem("-")
        layout.addWidget(self.wordSelection)
        
        #definition

        self.label = QLabel("Select field to add definition to: ")

        layout.addWidget(self.label)

        self.defSelection = QComboBox()
        self.defSelection.addItem("-")
        layout.addWidget(self.defSelection)

        #dictionary form visible if japanese isn't selected

        self.label = QLabel("Select Dictionary form field: ")

        layout.addWidget(self.label)

        self.dicSelection = QComboBox()
        self.dicSelection.addItem("-")
        layout.addWidget(self.dicSelection)

        #calls private method to add deck fields into each checkBox
        self.deckSelection.currentIndexChanged.connect(self.addFields)

        #ok and cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        buttons = QDialogButtonBox(QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def addFields(self):
        """ This method is called when the deck selection combo box has
            changed to something other than 0. This method adds
            the fields of the current deck selected into the 3 other combo
            boxes
            word
            def
            dic

            might want to fix this later
            because decks can have different cards therefore different fields
            this just selects the fields from the first note in the deck.
        """
        deckName = self.decks[self.deckSelection.currentIndex()]

        #debugging
        sys.stderr.write("deckName: " + str(deckName))
        
        deckId = mw.col.decks.id(deckName)

        #DBG = Debugging
        sys.stderr.write("deckName: " + str(deckId))

        deck = mw.col.decks.get(deckId, default=False)

        #I'm sure there's an easier way to select the note in order to get the
        #the fields however this was a solution I came up with
        mw.col.decks.select(deckId)
        noteId = mw.col.findNotes('')[0]
        note = mw.col.getNote(noteId)

        #DBG
        sys.stderr.write("Note: " + str(note))

        for field in note.values():
            sys.stderr.write("Note field name: %s \n"%str(field))
        

        #get the first or a random card in the deck
        #get a list of all fields in that deck
        #add all fields to the wordSelection combo box and
        #defSelection and dicSelection

        
    

def onRegenerate(browser):
    #calls the setup fields dialog to start the dialog and ask for fields
    setupFields = setupFieldsDialog()
    #calls the QDialog method that runs the dialog
    setupFields.exec_()

    #add return statement to accept selected fields and use with create
    #definitions
    
    createDefinitions(browser.selectedNotes())

def setup_browser_menu(browser):
    a = QAction("Add definitions", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onRegenerate(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)


def start():
    menu = QMenu()
    menu.setTitle("Add Definitions")
    mw.form.menuTools.addAction(menu.menuAction())

    mw.form.menu_add = menu

    if show_add_on():
        #creates the menu item add
        add = QAction(mw)
        add.setText("Add definitions to cards")
        menu.addAction(add)
        mw.connect(add, SIGNAL("triggered()"), add_def)

        #this adds the menu item in the deck browser view
        addHook("browser.setupMenus", setup_browser_menu)
        

start()
