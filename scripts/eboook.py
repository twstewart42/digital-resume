#!/usr/bin/python3
# Convert epub/lit to text with meta data
import ebooklib
from ebooklib import epub
import html2text
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
import subprocess

def _write_to_file(filename, title, author, tags, textd):
    save = filename.replace("epub", "txt")
    tfile = open(os.path.join("txt_proc", save), "a+")
    tfile.write('\n=================================')
    tfile.write("\nTitle: " + title[0][0])
    tfile.write("\nAuthor: " + author[0][0])
    for t in tags:
        print (t[0])
        tfile.write("\nTags: " + str(t[0]))
    tfile.write("\nContent: ")
    tfile.write(textd)

def _get_data(filename):
    book = epub.read_epub(filename)
    title = book.get_metadata('DC', 'title')
    author = book.get_metadata('DC', 'creator')
    tags = book.get_metadata('DC', 'subject')
    print(title, author, tags)
    #for t in tags:
    #    print (t[0])

    #items = book.get_items()
    #print(items)
    for item in book.get_items():
       if item.get_type() == ebooklib.ITEM_DOCUMENT:
       #print('==================================')
            #rint('NAME : ', item.get_name())
            section_name = item.get_name()
            #if '002' in section_name or '003' in section_name or '004' in section_name:
            print('NAME : ', section_name)
            data = item.get_content()
            soup = BeautifulSoup(data, 'html.parser')
            textd = soup.get_text()
            #print('CONTENT : ', textd)
            basename = os.path.basename(filename)
            _write_to_file(basename, title, author, tags, textd)
            #exit

def _convert_to_ebook(filename):
    litfile = filename.replace("lit", "epub")
    print (litfile)
    command = "ebook-convert \"%s\" \"%s\"" %(filename, litfile)
    try:
        subprocess.run(command, shell=True)
    except:
        print ("skip - " + command)
        pass
    else:
        os.remove(filename)
    return litfile


for subdir, dirs, files in os.walk('.'):
    for f in files:
        #print(f)
        filename = subdir + os.sep + f
        if filename.endswith(".lit"):
            print(filename)
            try:
                newfile = _convert_to_ebook(filename)
                _get_data(newfile)
            except:
                print("skip - " + filename)
                pass
        elif filename.endswith(".epub"):
            print(filename)
            #try:
            _get_data(filename)

