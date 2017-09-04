# -*- coding: utf-8 -*-
import os
import time
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()

def extract_id(filepath):
    data = {}
    try:
        for l in open(filepath, encoding="utf8"):
            if l.startswith('ID'):
                data['ID'] = l.split(' ', 1)[1]
            if l.startswith('Type'):
                data['Type'] = l.split(' ', 1)[1]
    except UnicodeDecodeError:
        data['Type'] = '<span style="color: red;">Encoding Error.</span>'
        data['ID'] = '<span style="color: red;">Encoding Error.</span>'

    if not data.get('ID'):
        data['ID'] = '<span style="color: red;">No ID found.</span>'

    if not data.get('Type'):
        data['Type'] = '<span style="color: red;">No Type found.</span>'

    return data
            

def extract_name(filepath):
    data = {}
    try:
        for l in open(filepath, encoding="utf8"):
            if l.startswith('Name'):
                data['Name'] = l.split(' ', 1)[1]
            if l.startswith('Description'):
                data['Description'] = l.split(' ', 1)[1]
    except UnicodeDecodeError:
        data['Name'] = '<span style="color: red;">Encoding Error.</span>'
        data['Description'] = '<span style="color: red;">Encoding Error./span>'
        
    if not data.get('Description'):
        data['Description'] = '<span style="color: red;">No description found.</span>'

    if not data.get('Name'):
        data['Name'] = '<span style="color: red;">No name found.</span>'
        
    return data

filepath = ''
while not (filepath.endswith('304930') or filepath.endswith('Content') or filepath.endswith('Bundles')):
    print('Please navigate to your Unturned "Bundles" or "Workshop" directory. (Directory named "Bundles" in Unturned folder, or "304930" in the Workshop folder.)')
    filepath = filedialog.askdirectory()
    print(filepath)
    if (filepath.endswith('304930') or filepath.endswith('Content')):
        print('This is probably an item bundles directory. Or at least I hope it is.\n')
    else:
        print('This is not a bundles directory.')

ids = open('items.html', "w+", encoding='utf-8')
ids.write('<!DOCTYPE html><html><head><title>Unturned Items IDs</title></head><body><h1>Unturned Item IDs</h1><br />')
ids.close()
ids = open('items.html', 'a+', encoding='utf-8')
print('Working... \n')
timestart = time.time()

for directory, subdirs, files in os.walk(filepath):
    folder = directory.replace('\\', '/')
    for name in files:
        if 'English.dat' == name:
            data = extract_name(folder + '/' + name)
            ids.write('<ul><li>Name: {}</li><li>Description: {}</li>'.format(data['Name'], data['Description']))
            try:
                item = os.path.basename(os.path.normpath(folder))
                data = extract_id(folder + '/' + item + '.dat')
                ids.write('<li>ID: {}</li><li>Type: {}</li></ul><hr>'.format(data['ID'], data['Type']))
            except:
                ids.write('<li>ID: <span style="color: red;">{}</span></li><li>Type:  <span style="color: red;">{}</span></li></ul><hr>'.format('Missing', 'Missing'))

print('Done! All items processed in ' + str(time.time() - timestart) + ' seconds.')
print('You can find the item list in \'items.html\' that this script is located in.')

ids.write('</body></html>')
ids.close()
        
