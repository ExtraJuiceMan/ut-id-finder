# -*- coding: utf-8 -*-
import os
import time
import tkinter
from tkinter import filedialog
from jinja2 import Environment, FileSystemLoader

class Item():
    """Item class"""
    
    def __init__(self, name, description, itemid, itemtype):
        self.name = name
        self.description = description
        self.id = itemid
        self.type = itemtype

    def clean_info(self, s):
        """Strips text formatting that
        those damnned modders put in their mods"""
        
        c = s.replace('\n', '').replace('\t', '')
        return c

    def get(self):
        """Returns a dict containing item info"""
        
        return ({
            'Name' : self.name,
            'Description' : self.description,
            'ID' : self.id,
            'Type' : self.type
            })

    def get_clean(self):
        """Returns a dict containing item info
        stripped of it's formatting"""
        
        return ({
            'Name' : self.clean_info(self.name),
            'Description' : self.clean_info(self.description),
            'ID' : self.clean_info(self.id),
            'Type' : self.clean_info(self.type)
            })

def extract_id(filepath):
    """Get IDs from an item.dat"""
    
    data = {}
    
    try:
        for l in open(filepath, encoding="utf8"):
            if l.startswith('ID'):
                data['ID'] = l.split(' ', 1)[1]
            if l.startswith('Type'):
                data['Type'] = l.split(' ', 1)[1]
    except UnicodeDecodeError:
        data['Type'] = '<span class="error">Encoding Error.</span>'
        data['ID'] = '<span class="error">Encoding Error.</span>'
    #WHAT TYPE OF ENCODING DO THESE MOD AUTHORS USE?!?!

    if not data.get('ID'):
        data['ID'] = 'No ID found.'

    if not data.get('Type'):
        data['Type'] = 'No Type found.'

    return data
            

def extract_name(filepath):
    """Get item name and desc. from English.dat"""
    
    data = {}
    
    try:
        for l in open(filepath, encoding="utf8"):
            if l.startswith('Name'):
                data['Name'] = l.split(' ', 1)[1]
            if l.startswith('Description'):
                data['Description'] = l.split(' ', 1)[1]
    except UnicodeDecodeError:
        data['Name'] = '<span class="error">Encoding Error.</span>'
        data['Description'] = '<span class="error">Encoding Error.</span>'
        
    if not data.get('Description'):
        data['Description'] = 'No description found.'

    if not data.get('Name'):
        data['Name'] = 'No name found.'
        
    return data

filepath = ''
root = tkinter.Tk()
root.withdraw()

#Bit of a mess, may improve later
while not (filepath.endswith('304930') or filepath.endswith('Content') or filepath.endswith('Bundles')):
    print('Please navigate to your Unturned "Bundles" or "Workshop" directory.\n'
          '(Directory named "Bundles" in Unturned folder, or "304930" in the Workshop folder.)')
    filepath = filedialog.askdirectory()
    print(filepath)
    if (filepath.endswith('304930') or filepath.endswith('Content') or filepath.endswith('Bundles')):
        print('This is probably an item bundles directory. Or at least I hope it is.\n')
    else:
        print('This is not a valid directory.')

print('Working... \n')
timestart = time.time()
items = []

for directory, subdirs, files in os.walk(filepath):
    folder = directory.replace('\\', '/')
    for name in files:
        if 'English.dat' == name:
            try:
                data = extract_name(folder + '/' + name)
                n = data['Name']
                d = data['Description']
            except:
                n = '<span class="error">Missing</span>'
                d = '<span class="error">Missing</span>'
            #Thanks to the mod creators who don't follow standard procedure
                
            try:
                item = os.path.basename(os.path.normpath(folder))
                data = extract_id(folder + '/' + item + '.dat')
                i = data['ID']
                t = data['Type']
            except:
                n = '<span class="error">Missing</span>'
                d = '<span class="error">Missing</span>'

            item = Item(n, d, i, t)
            items.append(item.get_clean())

items = sorted(items, key=lambda k: int(k['ID'])) 

#Render template so I dont have to type a bunch of html
#in Python. I'm not doing that again. Ever.
env = Environment(loader=FileSystemLoader('template'))
template = env.get_template('base.html')
items_html = template.render(items=items)

with open('results/items.html', 'w+', encoding='utf8') as f:
    f.write(items_html)

print('Done! All items processed in ' + str(time.time() - timestart) + ' seconds.')
print('You can find the item list in the "results" directory.')

