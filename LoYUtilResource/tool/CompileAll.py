import glob
import os
import os.path
import sys

import CommandCompiler
import DataTableBuilder
import DngmapConv


cleared_dirs = []


def clear_odir(path):
    if path in cleared_dirs:
        return
    for x in glob.glob(os.path.join(path, "*")):
        os.remove(x)
    cleared_dirs.append(path)


def get_odir(path):
    odir = os.path.join(os.path.dirname(path), "compiled")
    if not os.path.exists(odir):
        os.mkdir(odir)
    clear_odir(odir)
    return odir


def compile_scripts(path=""):
    #odir = os.path.join(path, "compiled")
    pat = os.path.join(path, "**", "*.Script.txt")
    for txt in glob.glob(pat, recursive=True):
        odir = get_odir(txt)
        print("compile %s into %s" % (txt, odir))
        CommandCompiler.compiler(txt, odir, ex_flag_path="exflags.efl")


def encode_maps(path=""):
    #odir = os.path.join(path, "compiled")
    pat = os.path.join(path, "**", "*.xlsx")
    for xlsx in glob.glob(pat, recursive=True):
        if not DngmapConv.is_dngmapxlsx(xlsx):
            continue
        odir = get_odir(xlsx)
        dngmap = os.path.join(odir, os.path.splitext(os.path.basename(xlsx))[0] + ".dngmap.json")
        print("encode %s into %s" % (xlsx, dngmap))
        DngmapConv.xls2json(xlsx, dngmap, force=True)


def convert_datatables(path=""):
    #odir = os.path.join(path, "compiled")
    pat = os.path.join(path, "**", "*.xlsx")
    for xlsx in glob.glob(pat, recursive=True):
        if not DataTableBuilder.is_datatablexlsx(xlsx):
            continue
        odir = get_odir(xlsx)
        print("convert %s into %s" % (xlsx, odir))
        DataTableBuilder.build_table(xlsx, odir)


if __name__ == "__main__":
    path = ""
    if len(sys.argv) != 1:
        if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
            path = sys.argv[1]
    compile_scripts(path=path)
    encode_maps(path=path)
    convert_datatables(path=path)
