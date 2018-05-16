import argparse
import configparser
import os
from subprocess import call as call_
from os import path


def call(l):
    if args.dry:
        print(l)
    else:
        call_(l)


def comp_scss(inp, out):
    call([r'scss', inp, out])


def comp_coffee(inp, out):
    call([r'coffee', '-o', out, inp])


def comp_haml(inp, out):
    call([r'python', 'haml.py', '-i', args.src_haml + ';' + args.out_haml, inp, out])


def get_name(p):
    p = path.abspath(p)
    absname, ext = path.splitext(p)
    dir, name = path.split(absname)
    return name


def _(d, lmb, ext, out, ext_prev):
    if d == "":
        return
    for root, subdirs, files in os.walk(d):
        for f in files:
            s = path.abspath(d + '/' + f)
            if s.endswith(ext_prev):
                lmb(s, out + '/' + get_name(s) + ext)


par = argparse.ArgumentParser(description='Building sites.')
par.add_argument('--file', '-f', help='single file', action='store', default=None)
par.add_argument('-C', '--cfg', '--config', help='the config file')
par.add_argument('-d', '--dry', action='store_true', help='dry run (only prints commands)')

group = par.add_argument_group(title='', description='What to build.')
group.add_argument('-a', '--all', action='store_true', help='build everything (default)')
group.add_argument('-H', '--haml', action='store_true', help='only build .haml')
group.add_argument('-s', '--scss', action='store_true', help='only build .scss')
group.add_argument('-c', '--coffee', action='store_true', help='only build .coffee')

group = par.add_argument_group(title='Source directories', description='')
group.add_argument('--src-all', action='store', default='', help='source directory for all files')
group.add_argument('--src-haml', action='store', default='', help='source directory for all .haml files')
group.add_argument('--src-scss', action='store', default='', help='source directory for all .scss files')
group.add_argument('--src-coffee', action='store', default='', help='source directory for all .coffee files')

group = par.add_argument_group(title='Output directories', description='')
group.add_argument('--out-all', action='store', default='', help='output directory for all files')
group.add_argument('--out-haml', action='store', default='', help='output directory for all .haml files')
group.add_argument('--out-scss', action='store', default='', help='output directory for all .scss files')
group.add_argument('--out-coffee', action='store', default='', help='output directory for all .coffee files')

args = par.parse_args()

if args.all:
    args.haml = True
    args.scss = True
    args.coffee = True

if args.src_all != '':
    args.src_haml += ';' + args.src_all
    args.src_scss += ';' + args.src_all
    args.src_coffee += ';' + args.src_all

if args.out_haml == '':
    args.out_haml = args.out_all

if args.out_scss == '':
    args.out_scss = args.out_all

if args.out_coffee == '':
    args.out_coffee = args.out_all

cfg = configparser.ConfigParser()
if path.exists(str(args.cfg)):
    cfg._interpolation = configparser.ExtendedInterpolation()
    cfg.read(args.cfg)

if args.file is not None:
    for f in str(args.file).split(';'):
        if f == '':
            continue
        if f.endswith('.haml'):
            if get_name(f).startswith('_'):
                args.haml = True
            comp_haml(f, args.out_haml +  '/' + get_name(f) + '.html')
        if str(f).endswith('.scss'):
            comp_scss(f, args.out_scss + '/' + get_name(f) + '.css')
        if str(f).endswith('.coffee'):
            comp_coffee(f, args.out_coffee + '/' + get_name(f) + '.js')

if args.scss:
    for d in str(args.src_scss).split(';'):
        _(d, comp_scss, '.css', args.out_scss, '.scss')

if args.coffee:
    for d in str(args.src_coffee).split(';'):
        _(d, comp_coffee, '.js', args.out_coffee, '.coffee')

if args.haml:
    for d in str(args.src_haml).split(';'):
        _(d, comp_haml, '.html', args.out_haml, '.haml')
