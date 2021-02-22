import daemon

from instaScraper import *

with daemon.DaemonContext():
    do_main_program()
