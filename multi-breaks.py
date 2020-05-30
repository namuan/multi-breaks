#!/usr/bin/env python3

import datetime as dt
import logging
import os.path
from collections import OrderedDict

import rumps

CONFIG_FILE = "multi-breaks.ini"
LOG_FILE = "multi-breaks.log"

INTERVAL_MENU = OrderedDict(
    [
        ("Breath / 5 minutes", (5, "Mindful Breathing")),
        ("20/20/20 eyesight / 20 minutes", (20, "20/20/20")),
        ("Stand-up / 1 hour", (60, "Stand-up and Walk")),
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
                self.title = timer_message
                logging.info(
                    f"Notifying {timer_message} every {timer_interval} starting at {timer_start}"
                )
                self.timers[timer_key] = (
                    dt.datetime.now(),
                    timer_interval,
                    timer_message,
                )
            else:
                self.title = ""

    def _build_interval_submenu(self):
        menu = rumps.MenuItem("Breaks")
        for title, value in INTERVAL_MENU.items():

            def cb(sender):
                minutes, message = sender.value
                sender.state = not sender.state
                if sender.state:
                    logging.info(
                        f"[{sender.title}] - Start Timer for {minutes} minutes"
                    )
                    timer_start = dt.datetime.now()
                    self.timers[sender.title] = (timer_start, minutes, message)
                else:
                    logging.info(f"[{sender.title}] - Stop Timer for {minutes} minutes")
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