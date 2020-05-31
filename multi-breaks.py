#!/usr/bin/env python3

import datetime as dt
import logging
import os.path
from collections import OrderedDict

import rumps
from AppKit import NSAttributedString
from Cocoa import (NSFont, NSFontAttributeName, NSColor, NSForegroundColorAttributeName, NSBackgroundColorAttributeName)
from PyObjCTools.Conversion import propertyListFromPythonCollection

CONFIG_FILE = "multi-breaks.ini"
LOG_FILE = "multi-breaks.log"

INTERVAL_MENU = OrderedDict(
    [
        ("20/20/20 eyesight / 20 minutes", (20, "20/20/20")),
        ("Breathe / 45 minutes", (45, "Mindful Breathing")),
        ("Stand-up / 1 hour", (60, "Stand-up and Walk")),
        ("Water / 2 hour", (120, "Drink Water")),
    ]
)


class MultiBreaksApp(rumps.App):
    def __init__(self, *args, **kwargs):
        menu_spec = [
            self._build_interval_submenu(),
            None,
            "Silent",
            None,
            "Quit",
        ]
        super(MultiBreaksApp, self).__init__(
            *args, menu=menu_spec, quit_button=None, **kwargs
        )
        self.timers = {}
        self.silent = False
        self.setup_initial_timers()
        logging.info("start (program init)")

    @rumps.clicked("Quit")
    def quit(self, _):
        logging.info("stop (program end)")
        rumps.quit_application()

    @rumps.clicked("Silent")
    def silent_mode(self, sender):
        sender.state = not sender.state
        self.silent = sender.state

    @rumps.timer(60)
    def refresh(self, _=None):
        time_now = dt.datetime.now()
        if self.silent:
            logging.info("Silent model. returning")
            return
        for timer_key, timer_val in self.timers.items():
            timer_start, timer_interval, timer_message = timer_val
            timer_interval_in_seconds = timer_interval * 60
            delta_seconds_from_start = (time_now - timer_start).total_seconds()
            if delta_seconds_from_start >= timer_interval_in_seconds:
                self.timers[timer_key] = (
                    dt.datetime.now(),
                    timer_interval,
                    timer_message,
                )
                self.set_title(timer_message)
            else:
                self.title = ""

    def set_title(self, title):
        self.title = title

        if title is not None:
            # This is hacky, but works
            # https://github.com/jaredks/rumps/issues/30
            fg_color = NSColor.systemOrangeColor()
            bg_color = NSColor.darkGrayColor()

            font = NSFont.menuBarFontOfSize_(0)
            attributes = propertyListFromPythonCollection(
                {
                    NSForegroundColorAttributeName: fg_color,
                    NSBackgroundColorAttributeName: bg_color,
                    NSFontAttributeName: font
                },
                conversionHelper=lambda x: x
            )
            string = NSAttributedString.alloc().initWithString_attributes_(' ' + title, attributes)
            self._nsapp.nsstatusitem.setAttributedTitle_(string)

    def calibrated_color(self, red, green, blue, alpha=1):
        return NSColor.colorWithCalibratedRed_green_blue_alpha_(red / 255, green / 255, blue / 255, alpha)

    def setup_initial_timers(self):
        for title, value in INTERVAL_MENU.items():
            minutes, message = value
            self.timers[title] = (dt.datetime.now(), minutes, message)

    def _build_interval_submenu(self):
        menu = rumps.MenuItem("Breaks")
        for title, value in INTERVAL_MENU.items():

            def cb(sender):
                minutes, message = sender.value
                sender.state = not sender.state
                if sender.state:
                    timer_start = dt.datetime.now()
                    self.timers[sender.title] = (timer_start, minutes, message)
                else:
                    del self.timers[sender.title]

            mi = rumps.MenuItem(title, callback=cb)
            mi.state = True
            mi.value = value
            menu[title] = mi

        return menu


def main():
    app_name = "Multi Breaks"
    log_path = os.path.join(rumps.application_support(app_name), LOG_FILE)
    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format="%(asctime)s  %(levelname)s %(message)s",
    )
    MultiBreaksApp(app_name, icon="data/timer.pdf", template=True).run()


if __name__ == "__main__":
    main()
