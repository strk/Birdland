#!/usr/bin/python
# ------------------------------------------------------------------------------------
#   WRW 19 Mar 2022 - Make a birdland.desktop file and 
#   customized to the type of packaging and installation location.
#   Install in ~/.local/share/applications where the menu software will find it.
# ------------------------------------------------------------------------------------

import os
import sys
from pathlib import Path
import datetime
import site

# ------------------------------------------------------------------------------------

desktop_proto = """
# -----------------------------------------------------------------
#   birdland.desktop
#   Birdland Musician's Assistant             
#   This is generated by fb_make_desktop.py for a package type.
#   Generated: <Date>
#   Package type: <Type>
# -----------------------------------------------------------------
[Desktop Entry]
Categories=Audio;Player;AudioVideo;Midi;Viewer;
Comment[en_US]=
Comment=
Exec=<Exec>
Icon=<Icon>
Path=<Path>
GenericName[en_US]=Birdland Musician's Assistant
GenericName=Birdland Musician's Assistant
MimeType=
Name[en_US]=Birdland
Name=Birdland
StartupNotify=true
Terminal=false
Type=Application
Version=1.0
X-DBUS-ServiceName=
X-DBUS-StartupType=
X-Desktop-File-Install-Version=0.15
X-KDE-SubstituteUID=false
X-KDE-Username=
"""

# ------------------------------------------------------------------------------------

def make_desktop( package_type, verbose ):

    # -------------------------------------------------------
    #   Collect some common values.

    date = datetime.datetime.today().strftime( '%a, %d-%b-%Y, %H:%M:%S')
    home = os.getenv( 'HOME' )              # or os.environ[ 'HOME' ]

    # -------------------------------------------------------
    #   Get values specific to package_type

    #   Tar mimics Setuptools installation.

    if package_type == 'Tar' or package_type == 'Setuptools' or package_type == 'GitHub':
        program = Path( sys.argv[0] ).resolve().as_posix()          # Where birdland executed
        program_dir = Path( __file__ ).parent.resolve().as_posix()  # Where modules live
        Exec = f"/bin/sh -c {program}"
        Icon = f"{program_dir}/Icons/Bluebird-64.png"
        PPath = program_dir

    # elif package_type  ==  'PyInstaller':
    #     executable = Path( sys.executable ).resolve().as_posix()
    #     executable_parent = Path( sys.executable ).parent.resolve().as_posix()
    #     Exec = f"/bin/sh -c {executable}"
    #     Icon = f"{executable_parent}/src/Icons/Bluebird-64.png"
    #     PPath = executable_parent

    # elif package_type  ==  'Nuitka':
    #     executable = Path( sys.executable ).resolve().as_posix()
    #     executable_parent = Path( sys.executable ).parent.resolve().as_posix()
    #     Exec = f"/bin/sh -c {executable_parent}/birdland"
    #     Icon = f"{executable_parent}/Icons/Bluebird-64.png"
    #     PPath = executable_parent

    #   This should be last as always present in install directory in addition to one of the above.

    elif package_type == 'Development':
        program = Path( sys.argv[0] ).resolve().as_posix()          # Where birdland executed
        program_dir = Path( __file__ ).parent.resolve().as_posix()  # Where modules live
        Exec = f"/bin/sh -c {program}"
        Icon = f"{program_dir}/Icons/Bluebird-64.png"
        PPath = program_dir

    # -------------------------------------------------------
    #   Do tilda expansion

    Exec = Exec.replace( '~', home )
    Icon = Icon.replace( '~', home )
    PPath = PPath.replace( '~', home )

    #   Substitute values in prototype

    d = desktop_proto
    d = d.replace( '<Exec>', Exec )
    d = d.replace( '<Icon>', Icon )
    d = d.replace( '<Path>', PPath )
    d = d.replace( '<Type>', package_type )
    d = d.replace( '<Date>', date )
    # d = d.replace( '<Python>', python )

    # -------------------------------------------------------
    #   Show off our work. No, only for debugging

    # if verbose:
    #     print( d )

    # -------------------------------------------------------
    #   Install the file for now on every launch. Important
    #   for testing because I will forget to remove it.

    ofile = 'birdland.desktop'
    opath = Path( '~/.local/share/applications', ofile ).expanduser()

    # if opath.is_file():
    #     print( f"NOTE: {opath} exists, overwriting", file=sys.stderr )

    opath.write_text( d )

# ------------------------------------------------------------------------------------

if __name__ == '__main__':
    make_desktop( 'Development', True ) 
    make_desktop( 'Tar', True )
    make_desktop( 'Setuptools', True ) 
    make_desktop( 'PyInstaller', True ) 
    make_desktop( 'Nuitka', True ) 

# ------------------------------------------------------------------------------------
