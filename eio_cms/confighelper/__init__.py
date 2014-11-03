#!/usr/bin/env python2
import argparse, os, pkg_resources

def replace_file(src, dest, sub):
    with open(src) as f:
        content = f.read()
        for k in sub:
            content = content.replace('$' + k, sub[k])
        with open(dest, 'w') as fout:
            fout.write(content)

    
def main():
    parser = argparse.ArgumentParser(description='''EIO CMS setup configuration helper script.

Before invoking it make sure the current directory has the file named settings.py
present in it with the appropriately configured values.

Example of a settings.py file is available as a sample-setttings.py in the package directory.''')
    parser.add_argument('cms_config_file', metavar='<cms.conf>', help='full path to the cms.conf file to be written')
    args = parser.parse_args()
    if not os.path.exists("settings.py"):
        raise Exception("Please, invoke this script from the directory, that contains the file settings.py")

    opts = {}
    execfile('settings.py', {}, opts)
    replace_file(
        pkg_resources.resource_filename('eio_cms.confighelper', 'conf/cms.conf'),
        args.cms_config_file,
        opts)

