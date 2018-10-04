import os
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from user_input_modal_window import UserInfoModalWindow
from item_modal_window import ItemModalWindow
from sizing_window import SizingHelpModalWindow
from cart import Cart
from parser import Parser
from bot_help import BotHelpWindow


class SupremeApp(QWidget):
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        super(SupremeApp, self).__init__()
        horizbox = QHBoxLayout()
        vertbox = QVBoxLayout()

        #             buttons               #
        self.init_user_btn = QPushButton('Users Actions', self)
        self.connect(self.init_user_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_user_info_modal_window())

        self.cart_btn = QPushButton('Cart', self)
        self.connect(self.cart_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_cart_window())

        self.sizing_btn = QPushButton('Sizing', self)
        self.connect(self.sizing_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_sizing_help_window())

        self.bot_help_btn = QPushButton('Bot Help', self)
        self.connect(self.bot_help_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_bot_help_window())

        self.start_btn = QPushButton('Start Bot', self)

        horizbox.addWidget(self.init_user_btn)
        horizbox.addWidget(self.cart_btn)
        horizbox.addWidget(self.sizing_btn)
        horizbox.addWidget(self.bot_help_btn)
        horizbox.addWidget(self.start_btn)

        #            items field            #
        self.field_layout = QGridLayout()

        # self.create_table()

        area = QWidget()
        area.setLayout(self.field_layout)
        self.items_field = QScrollArea()
        self.items_field.setWidget(area)
        self.items_field.show()
        vertbox.addWidget(self.items_field)
        vertbox.addLayout(horizbox)

        #           main window           #
        self.setGeometry(2500, 100, 1186, 875)
        self.setLayout(vertbox)
        self.setFixedWidth(1186)
        self.setWindowTitle('Py3SuprBot')

        self.setWindowIcon(QIcon(self.scriptDir + os.path.sep + 'logo.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()


    def create_item_modal_window(self, args):
        #        initializing cart json      #
        if os.path.isfile(self.scriptDir + "/items_to_buy.json"):
            pass
        else:
            os.system("touch items_to_buy.json")
            with open("items_to_buy.json", mode='r', encoding='utf-8') as f:
                json.dump('[]', f)

        window_modal = ItemModalWindow(args)


    def create_user_info_modal_window(self):
        window_modal = UserInfoModalWindow()


    def create_sizing_help_window(self):
        window_modal = SizingHelpModalWindow()


    def create_cart_window(self):
        window_modal = Cart()


    def create_bot_help_window(self):
        window_modal = BotHelpWindow()


    def create_table(self):
        # initializing parser
        parser_ = Parser()

        # parse_main_window_content() method first checks if latest drop has been changed
        # to do that, method finds a link to the latest droplist and compares it with a link that is saved in 'latest.txt'
        # if links differ, it parses droplist from community and saves it to json dump
        # also it writes down last used link to 'latest.txt'
        parser_.parse_main_window_content()

        # reading content from dump
        with open('current_drop.json', mode='r') as fin:
            drop = json.load(fin)

        # path where to find images for main window mesh
        images_path = self.scriptDir + '/img'

        # building mesh

        item_index = 0
        for i in range(len(drop) % 5 + 1):
            for j in range(5):
                img_name = str(i) + str(j) + '.jpg'
                if img_name in os.listdir(images_path):

                    btn = QPushButton()
                    btn.setIcon(QIcon('img/' + img_name))
                    btn.setIconSize(QSize(200, 200))
                    self.field_layout.addWidget(btn, i, j)

                    argsz = [drop[item_index]['type'],
                             drop[item_index]['name'],
                             drop[item_index]['description'],
                             ['White', 'Black', 'Red'],
                             img_name
                    ]
                    item_index += 1

                    self.connect(btn,
                                 SIGNAL('clicked()'),
                                 lambda: self.create_item_modal_window(argsz))