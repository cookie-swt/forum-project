#!c:\users\acer\desktop\课程文件\web高级程序设计\大作业\myforum\myforum\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'autobahn==22.4.2','console_scripts','wamp'
__requires__ = 'autobahn==22.4.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('autobahn==22.4.2', 'console_scripts', 'wamp')()
    )
