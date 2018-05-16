import sys
import argparse
import configparser
from subprocess import call
from os import path, remove
from re import sub
from tempfile import gettempdir
import uuid


def xml_regex(tag):
    return '<' + tag + '>(.*?)</' + tag + '>'


def include_match(m):
    f = None
    for p in str(args.include).split(';'):
        if path.exists(p + '/' + m.group(1)):
            f = p + '/' + m.group(1)
    if f is None:
        return "<p><b>FILE NOT FOUND</b><br /><small>Coudn't find file to include.</small><br></p>"
    if not f.endswith('.haml'):
        f = open(f, 'r')
        txt = f.read()
        f.close()
        return txt
    else:
        tmp = gettempdir() + '/' + uuid.uuid4().hex + '.tmp'
        comp(f, tmp, args.config)
        f = open(tmp, 'r')
        txt = f.read()
        f.close()
        remove(tmp)
        return txt


def comp(inp, out, cfgf):
    if inp == out:
        print("Input and output file mustn't be the same.")
        return

    if not path.exists(inp):
        print("inp doesn't exist!")
        return

    call(['haml', inp, out])

    f = open(out, 'r')
    html = f.read()
    f.close()

    if path.exists(cfgf):
        cfg = configparser.ConfigParser()
        cfg._interpolation = configparser.ExtendedInterpolation()
        cfg.read(cfgf)
        for k in cfg['aliases']:
            if str(cfg['aliases'][k]).startswith('py::'):
                html = sub(xml_regex(k), eval(cfg['aliases'][k][4:]), html)
            else:
                html = sub(xml_regex(k), cfg['aliases'][k], html)

    html = sub(xml_regex('include'), include_match, html)
    html = str(html).replace('\r', '')

    f = open(out, 'w')
    f.write(html)
    f.close()


# py haml.py -i .;haml haml\index.haml haml\index.html
par = argparse.ArgumentParser(description='Compiling and post-processing HAML.')
par.add_argument('input', metavar='inp', help='.haml file to be processed', action='store')
par.add_argument('output', metavar='out', help='the .html output file', action='store', nargs='?')

par.add_argument('-c', '--config', metavar='cfg', help='a config file for the compilation. (default: post_haml.ini)',
                 action='store', default='post_haml.ini')
par.add_argument('-i', '--include', metavar='paths', help='paths to be included while searching for %include file',
                 default='.')

args = par.parse_args()

if args.output is None:
    args.output = args.input[:args.input.rfind('.')] + '.html'

comp(args.input, args.output, args.config)
