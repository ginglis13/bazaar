#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
from checkbutton import checkButton

class myAssistant(Gtk.Assistant):
    def __init__(self):
        Gtk.Assistant.__init__(self, title="The Bazaar")
        self.set_default_size(800,600)

        self.software = set()

        intro = self.init_intro()
        nd = self.init_nd()
        utils = self.init_utils()
        summary = self.init_summary()

        for p in [intro, nd, utils, summary]:
            self.append_page(p)

        self.set_page_title(intro, "The Bazaar")
        self.set_page_title(nd, "Notre Dame Specific Software")
        self.set_page_title(utils, "Utility Software")
        self.set_page_title(summary, "Finished")

        self.set_page_type(intro, Gtk.AssistantPageType.INTRO)
        self.set_page_type(nd, Gtk.AssistantPageType.CONTENT)
        self.set_page_type(utils, Gtk.AssistantPageType.CONTENT)
        self.set_page_type(summary, Gtk.AssistantPageType.SUMMARY)

        self.set_page_complete(intro, True)
        self.set_page_complete(nd, True)
        self.set_page_complete(utils, True)

        self.connect("cancel", self.close)
        self.connect("close", self.close)
        self.connect("destroy", self.close)

    def init_intro(self):
        label = Gtk.Label()
        label.set_markup('''
                <big>Welcome to <b>The Bazaar!</b></big>

                <b>The Bazaar</b> is a software setup tool created
                by the Notre Dame Linux Users Group. This tool will
                help a Notre Dame student who is new to Linux get
                started with their favorite apps. If you are not a
                member of LUG (yet), consider joining!

                Check out our <a href='http://ndlug.org'>website</a> and the <a href='https://www.github.com/NDLUG/bazaar'>source code</a> for this project!
                ''')

        label.set_line_wrap(True)
        intro = Gtk.Frame()
        intro.add(label)

        return intro

    def init_nd(self):
        label = Gtk.Label()
        label.set_markup('''
                <big>Select the <b><i>Notre Dame specific</i></b> software you would like to install:</big>
                ''')
        nd = Gtk.Box(spacing = 6)
        nd.set_orientation(Gtk.Orientation.VERTICAL)
        nd.add(label)

        print_driver = checkButton('ND Print Driver', 'ndprint', 'nd')
        eduroam_driver = checkButton('Eduroam Driver', 'eduroam','nd')

        self.add_to_widget(nd, [print_driver, eduroam_driver])

        return nd

    def init_utils(self):
        label = Gtk.Label()
        label.set_markup('''
                <big>Select the <b><i>Utility</i></b> software you would like to install:</big>
                ''')
        utils = Gtk.Box(spacing = 6)
        utils.set_orientation(Gtk.Orientation.VERTICAL)
        utils.add(label)

        # Coding
        coding   = Gtk.Label('Text Editors')
        vim      = checkButton('vim', 'vim', 'apt')
        vscodium = checkButton('VSCodium', 'vscodium', 'snap')
        vscode   = checkButton('Visual Studio Code', 'vscode --classic', 'snap')
        atom     = checkButton('Atom', 'atom --classic', 'snap')
        sublime  = checkButton('Sublime Text', 'sublime-text --classic', 'snap')

        self.add_to_widget(utils, [coding, vscodium, vscode, sublime])

        # Web Browsers
        browsers = Gtk.Label('Web Broswers')
        chromium = checkButton('Chromium', 'chromium', 'snap')
        chrome   = checkButton('Chrome', 'chrome', 'ppa')
        firefox  = checkButton('Firefox', 'firefox', 'snap')

        self.add_to_widget(utils, [browsers, chromium, chrome, firefox])

        # Gaming
        gaming  = Gtk.Label('Gaming')
        steam   = checkButton('Steam', 'steam', 'apt')
        lutris  = checkButton('Lutris', 'lutris', 'ppa')
        discord = checkButton('Discord', 'discord', 'snap')

        self.add_to_widget(utils,[gaming,steam,lutris,discord])

        # Chat
        chat     = Gtk.Label('Chat Applications')
        slack    = checkButton('Slack', 'slack --classic', 'snap')
        whatsapp = checkButton('WhatsApp', 'whatsapp')
        telegram = checkButton('Telegram', 'telegram-desktop', 'snap')
        signal   = checkButton('Signal', 'signal-desktop', 'snap')

        self.add_to_widget(utils,[chat, slack, whatsapp, telegram, signal])

        spotify  = checkButton('Spotify', 'spotify', 'snap')

        return utils

    def init_summary(self):
        label = Gtk.Label()
        label.set_markup('''
                <big>Summary</big>
                ''')
        summary = Gtk.Box(spacing = 6)
        summary.set_orientation(Gtk.Orientation.VERTICAL)
        summary.add(label)

        button = Gtk.Button(label="Install")
        button.connect("clicked", self.install)
        self.add_action_widget(button)

        return summary

    def add_to_widget(self, widget, widges):
        for w in widges:
            self.software.add(w)
            widget.add(w)

    def install(self, widget):
        p = self.get_nth_page(-1)
        for i in self.software:
            if isinstance(i, Gtk.CheckButton) and i.get_active():
                print('Installing {}...'.format(i.value))
                label = Gtk.Label('Installing {}...'.format(i.value))
                p.add(label)
                p.show_all()
                subprocess.Popen([i.pkgsource, 'install', i.value])

    def close(self, widget):
        Gtk.main_quit()

a = myAssistant()
a.show_all()
Gtk.main()
