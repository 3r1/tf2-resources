#!/usr/bin/env python
# python3, tested with 3.10.6

# Info:
# demo processing credit to demopan (https://github.com/vixus0/demopan)
# this script is a vast simplification of demopan because ds_record saves demo
#   files with datetime as name
# this removes the requirement of having demopan running alongside tf2
#   consequently, this script can be run at any time to pull demos from tf2 at
#   your leisure
# this also allows us to have scoreboard screenshots and ds_mark markers
# you will have to link the event file in tf/demos/ created by ds_record 
#   manually as I feel it's silly to copy/overrite or diffcheck+append

# What it do tho?
# For use with ds_record and ds_mark. Moves and renames .dem, .json, and .tga
#   appending mapname, playername

from __future__ import print_function

import os, struct, string, shutil

from argparse import ArgumentParser

def clean_str(str):
    return ''.join(filter(lambda x: x in string.printable, str))

def process_dem(dem):
    HEADER_FMT = '8sii260s260s260s260sfiii'

    siz = struct.calcsize(HEADER_FMT)
    with open(dem, 'rb') as f:
        b = f.read(siz)
    d = struct.unpack(HEADER_FMT, b)
    client = d[4].split(b'\0',1)[0].decode('utf8').replace(' ', '_')
    map = d[5].split(b'\0',1)[0].decode('utf8').replace(' ', '_')
    duration = d[7]
    return clean_str(client), clean_str(map), duration

def save_dem(dem, out_dir, in_dir):
    # need to store name in order to combine it with mapname
    name = dem

    dem = os.path.join(in_dir, dem)
    # dem is now full path to input file

    client, map, duration = process_dem(dem)

    # remove .dem so the first part of name format doesn't contain a duplicate .dem
    name = name[:-4]
    name ='{}-{}-{}.dem'.format(name, map, client)

    out = os.path.join(out_dir, name)
    # out is now fullpath to output file

    shutil.move(dem, out)
    print('dem saved to: '+out)
    # print('name',name,'\n')
    # print('out_dir',out_dir,'\n')
    # print('out',out,'\n')

    # .json
    demojson = dem[:-3]
    demojson += "json"

    if os.path.isfile(demojson):
        jsonout = out[:-3]
        jsonout += "json"
        shutil.move(demojson, jsonout)
        print('json saved to: '+jsonout)

    # .tga
    screenshot = dem[:-3]
    screenshot += "tga"
    if os.path.isfile(screenshot):
        ssout = out[:-3]
        ssout += "tga"
        shutil.move(screenshot, ssout)
        print('tga saved to: '+ssout)

def main():
    # args
    ap = ArgumentParser(description='For use with ds_record. Moves and renames demos, appending mapname, playername')
    ap.add_argument('-i', help='input directory to look for recorded demos', action='store', dest="input_dir")
    ap.add_argument('-o', help='output directory to save renamed demos', action='store', dest="output_dir")

    args = ap.parse_args()

    if not os.path.exists(args.output_dir):
        print('Creating demo save directory: '+args.output_dir+'\n')
        os.makedirs(args.output_dir)
    else:
        print('Saving demo to: '+args.output_dir+'\n')

    # loop through dir to find .dem files
    for file in os.listdir(args.input_dir):
        if file.endswith(".dem"):
            print('found file',file)
            save_dem(file,args.output_dir,args.input_dir)
            print('\n')

if __name__ == "__main__":
    main()
