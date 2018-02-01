import os
import sys

desktop_file = [
    "[Desktop Entry]",
    "Version=1.0",
    "Type=Application",
    "Name=Pay with Lightning Network",
    "Exec=",
    "MimeType=x-scheme-handler/lightning;",
    "Terminal=",
    "Icon=",
    "Comment=",
    "Path=",
    "StartupNotify=false",
    ]

MIMETYPE = 'x-scheme-handler/lightning=ln-pay.desktop'
APP = (os.getcwd() + "/python3 ln-pay.py")
#LOCALPATH = os.path.expanduser('~/.local/share/applications/')
LOCALPATH = os.getcwd()
ICONPATH = os.path.expanduser('~/.local/share/icons/hicolor/128x128/apps')

if sys.platform.startswith('linux'):
    desktop_file[4] = "Exec={} %u".format(APP)
    choice = input("ln-pay can be integrated into the desktop in two ways: \
                    \n1. Launch a terminal running ln-pay asking for confirmation \
                    \n2. Send a notification through Linux Desktop Notification asking for confirmation\
                    \nChoose 1 or 2 ")
    if choice == '1':
        desktop_file[6] = "Terminal=true"
    elif choice == '2':
        desktop_file[6] = "Terminal=false"
    print("This will add these configuration into {}\n".format(os.path.join(LOCALPATH,'ln-pay.desktop')))
    for i in desktop_file:
        print(i)

    print("\nand will append\n\n{}\n\ninto {}".format(MIMETYPE,os.path.join(LOCALPATH,'mimetype.list')))
    choice2 = input("Continue (y/n):")
    if choice2 == 'y':
        with open(os.path.join(LOCALPATH,'ln-pay.desktop'),'w') as f:
            for params in desktop_file:
                f.write(params+'\n')
        with open(os.path.join(LOCALPATH,'mimetype.list'),'a') as f:
            f.write(MIMETYPE)
        print("Installation complete")
    else:
        print("Installation cancelled")
else:
    print("OSes other than Linux are currently not supported by this install script")
    sys.exit(1)
