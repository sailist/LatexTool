import argparse
from argparse import RawDescriptionHelpFormatter

description = "convert xls table to tex code"
usage = None
epilog = ""

prog = "x2t"

parser = argparse.ArgumentParser(prog=prog,
                                 usage=usage,
                                 description=description,
                                 epilog=epilog,
                                 formatter_class=RawDescriptionHelpFormatter)

parser.add_argument("-c","--center",
                    dest="center",
                    action="store_false", #store,store_const,store_true/store_false,append,append_const,version
                    help="help")

parser.add_argument("-f","--fill",
                    dest="fill",
                    action="store_false", #store,store_const,store_true/store_false,append,append_const,version
                    help="help")

parser.add_argument('FILE',
                    metavar='FILE',
                    type=str,
                    nargs='+',
                    help='help')

parg = parser.parse_args()

fill = parg.fill
center = parg.center

fs = parg.FILE
from LatexTool.ast import tabel

for f in fs:
    tab = tabel.Tabel(f,center=center,fill=fill)
    print(tab.to_tex())
    print()

exit(0)