#!/usr/bin/env python3

from pyparsing import (Suppress,removeQuotes,Word,alphas,alphanums,printables,Group,Dict,ZeroOrMore,OneOrMore,
CaselessLiteral,Literal,Optional,SkipTo,restOfLine,LineStart,LineEnd,White,ParserElement)
import subprocess, os, time
import pprint
import sys


settings = {}


def rsync(source, destination):
    # TODO: determine if rsync exists first
    # ensure source and destination are valid paths
    output = subprocess.run(['rsync', '-aP', '--info=NAME,SYMSAFE,BACKUP,STATS', source, destination], stdout=subprocess.PIPE, env={"DISPLAY":":0.0"})
    print(output.stdout.decode('utf-8'))

def norm_path(path):
    return os.path.normcase(os.path.expandvars(os.path.expanduser(path)))

def add_trail(path):
    return os.path.join(path, '')

def as_file(path):
    return norm_path(path).rstrip(os.sep)

def as_dir(path):
    return norm_path(path)


# to specify literal directories so that the contents are copied to the same basename folder in the destination
# or to sync the folder itself
def process_directories(directories):
    for dir in directories:
        src = as_dir(dir['source'])
        dest = add_trail(as_dir(os.path.join(settings['backupdir'], dir['destination'])))

        print("\nrsync %s -> %s" % (src, dest))

        rsync(src, dest)

# to specify only files to be synced
def process_files(files):
    for file in files:
        src = as_file(file['source'])
        dest = add_trail(as_dir(os.path.join(settings['backupdir'], file['destination'])))

        print("\nrsync %s -> %s" % (src, dest))

        rsync(src, dest)

settings_actions = {
    "backupdir": as_dir
}
def process_settings(_settings):
    global settings

    if not "backupdir" in _settings:
        print("Backup directory not set, stopping...")
        sys.exit(1)
    else:
        for key in _settings:
            settings[key] = _settings[key]

            if key in settings_actions:
                settings[key] = settings_actions[key](settings[key])



backup_proc = {
    "directories": process_directories,
    "files": process_files,
    "settings": process_settings
}


# Grammar Parsing
# ParserElement.setDefaultWhitespaceChars(' \t')

WS = Optional(White(' \t')).suppress()

EQ = WS + Suppress('=') + WS
FRT = WS + Suppress('->') + WS
HSTART = Suppress('[')
HEND = Suppress(']') + WS

comment = Literal('#') + restOfLine

sec_directories = HSTART + CaselessLiteral("directories")   + HEND
sec_files       = HSTART + CaselessLiteral("files")         + HEND
sec_settings    = HSTART + CaselessLiteral("settings")      + HEND
section         = HSTART + Word(printables + " ")           + HEND

keyvalue = ~HSTART + Dict(Group(Word(alphanums) + EQ + Word(printables)))
fromto = Group(
    ~HSTART
    + SkipTo(FRT).setResultsName("source").setParseAction(lambda x: x[0]) # whyyy
    + FRT
    + restOfLine.setResultsName("destination")
)

part_directories    = Dict(Group(sec_directories + Group(ZeroOrMore(fromto)))).setName("part_directories")
part_files          = Dict(Group(sec_files       + Group(ZeroOrMore(fromto)))).setName("part_files")
part_settings       = Dict(Group(sec_settings    + OneOrMore(keyvalue))).setName("part_settings")

g = Optional(part_directories) & Optional(part_files) & part_settings
g.ignore(comment)

# End Grammar Parsing


instr = open(os.path.expanduser("~/.backup-settings"), "r").read()

parsed = g.parseString(instr).asDict()
# TODO: error/exception checking and recovery
#
# pp = pprint.PrettyPrinter(2)
# pp.pprint(parsed)


print("Beginning sync operation: %s\n" % time.strftime("%d-%m-%Y %H:%M:%S"))

if "settings" in parsed:
    process_settings(parsed["settings"])
else:
    print("Settings not defined: no backup directory set, stopping...")
    sys.exit(1)

if "directories" in parsed:
    process_directories(parsed["directories"])

if "files" in parsed:
    process_files(parsed["files"]);

print("\nFinished sync operation: %s\n" % time.strftime("%d-%m-%Y %H:%M:%S"))
subprocess.run(["notify-send", "Dropbox Synch", "Finished sync", "--icon=sync-synchronizing"])
