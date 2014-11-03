#!/usr/bin/env python2
import argparse, ConfigParser, os, pkg_resources

def replace_file(src, dest, sub):
    with open(src) as f:
        content = f.read()
        for k in sub:
            content = content.replace('$' + k, sub[k])
        with open(dest, 'w') as fout:
            fout.write(content)

    
def main():
    parser = argparse.ArgumentParser(description='''EIO CMS setup configuration helper script.

Before invoking it make sure the current directory has the file named setup.cfg 
present in it with the appropriately configured [eio-cms] section.

Example of a setup.cfg file is available as a sample-setup.cfg in the package directory.''')
    parser.add_argument('cms_config_file', metavar='<cms.conf>', help='full path to the cms.conf file to be written')
    args = parser.parse_args()
    if not os.path.exists("setup.cfg"):
        raise Exception("Please, invoke this script from the directory, that contains the file setup.cfg")

    Config = ConfigParser.ConfigParser()
    Config.read("setup.cfg")
    if 'eio-cms' not in Config.sections():
        raise Exception("Please, make sure the section [eio-cms] exists in your setup.cfg")
    opts = {o: Config.get('eio-cms', o) for o in Config.options('eio-cms')}

    replace_file(
        pkg_resources.resource_filename('eio_cms.confighelper', 'conf/cms.conf'),
        args.cms_config_file,
        opts)

