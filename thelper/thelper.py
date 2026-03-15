#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rendering templates from different sources
"""
import argparse
import os
import datetime
import shutil
from jinja2 import Environment, FileSystemLoader
import configparser
import yaml

class thelper(object):
    """
    Class managing the rendering process. Configurations are loaded from directory on $HOME/.config/thelper and are overwritten by local configs
    in current working directory
    """
    def __init__(self, **kwargs):
        """
        

        Parameters
        ----------
        **kwargs :
            Parameters from argparse.

        Returns
        -------
        None.

        """
        self.args = {
                    'd'     : 'default',
                    }
        self.args.update(kwargs)
        self.rendervars =       {
                                'author'        : "AUTHOR",
                                'shortauthor'   : "AUTHOR",
                                'title'         : "TITLE",
                                'subject'       : "SUBJECT",
                                'document'      : "document",
                                }

        # setting configdir as full path and ensuring directory exists
        for i in ['confdir']:
            self.args[i]  = os.path.abspath(self.args[i])
            self.ensure_dir(self.args[i])  
           
        # loading configs
        self.run_config_file()
        self.ensuring_template_dirs()
        self.run_sub_config_file()
        
        # execute rendering if set
        if self.args['r']:
            self.render_all_latex_templates()
            
 
    def ensure_dir(self, DIR: str) -> None:
        """
        Ensures recursively that a directory exists.

        Parameters
        ----------
        DIR : str
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.

        """
        dirlist = os.path.normpath(DIR).split(os.sep)
        for i in range(len(dirlist)):
            tmpdir = os.path.abspath(os.sep.join(dirlist[:i+1]))
            if not os.path.exists(tmpdir):
                os.mkdir(tmpdir)
                print('Create {:}'.format(tmpdir))
                
    def run_config_file(self) -> None:
        """
        Load or create YAML config file.
        """

        self.args['conffile'] = os.path.join(self.args['confdir'], 'config.yml')

        if os.path.isfile(self.args['conffile']):
            with open(self.args['conffile'], "r") as f:
                self.config = yaml.safe_load(f)

            self.config['SETTINGS']['defaulttemplate'] = self.args['d']
            self.rendervars.update(self.config['VARIABLES'])

        else:
            self.config = {
                "SETTINGS": {
                    "templatebasedir": "templates",
                    "defaulttemplate": self.args['d']
                },
                "TEMPLATES": {
                    "main_template": "document.tex.j2",
                    "style_template": "thelper.sty.j2",
                    "meta_template": "meta.tex.j2",
                    "python_template": "main.py.j2",
                    "content_template": "content.tex.j2"
                },
                "VARIABLES": self.rendervars
            }

            with open(self.args['conffile'], "w") as f:
                yaml.dump(self.config, f, sort_keys=False)
                
    def ensuring_template_dirs(self) -> None:
        """
        Ensuring template dirs exist and are set with full path

        Returns
        -------
        None

        """
        
        self.args['templatedir'] = os.path.join(self.args['confdir'],self.config['SETTINGS']['templatebasedir'],self.args['t'])
        self.args['defaulttemplatedir'] = os.path.join(self.args['confdir'],self.config['SETTINGS']['templatebasedir'],self.config['SETTINGS']['defaulttemplate'])
        for i in ['templatedir']:
            self.args[i]  = os.path.abspath(self.args[i])
            self.ensure_dir(self.args[i])
            
    def run_sub_config_file(self) -> None:

        subconffile = os.path.join(os.getcwd(), 'config.yml')

        if os.path.isfile(subconffile):

            with open(subconffile, "r") as f:
                config = yaml.safe_load(f)

            self.rendervars.update(config['VARIABLES'])

        else:

            config = {"VARIABLES": self.rendervars}

            with open(subconffile, "w") as f:
                yaml.dump(config, f, sort_keys=False)

    def get_render_variables(self) -> dict:
        """
        Getting all variables that are rendered on templates.

        Returns
        -------
        dict
            Dictionary holding render keys and render values for templates.

        """
        return self.rendervars.copy()
    
    def get_render_filename(self,tkey: str) -> str:
        """
        Get the filename of a rendered template.

        Parameters
        ----------
        tkey : str
            The key of the config section 'TEMPLATES'.

        Returns
        -------
        str
            Filename of rendered file.

        """
        if tkey!="main_template":
            return self.config['TEMPLATES'][tkey].replace('.j2','')
        else:
            return self.rendervars['document']+'.tex'
        
            
    def render_latex_template(self, tkey: str, tempdir: str) -> None:
            """
            Render a single template file or copy if it's a binary file.
            Skips copying if the binary file is empty (0 bytes).
            """
            # 1. Dateinamen aus der Config holen
            template_filename = self.config['TEMPLATES'][tkey]
            source_path = os.path.join(tempdir, template_filename)
            
            # Prüfen, ob die Quelldatei existiert
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Template {template_filename} not found in {tempdir}")
    
            # 2. Zielpfad bestimmen
            render_filename = self.get_render_filename(tkey)
            renderfile = os.path.join(os.getcwd(), render_filename)
    
            # Falls die Datei im Zielverzeichnis bereits existiert, überspringen
            if os.path.exists(renderfile):
                return
    
    
            # 3. Prüfung auf Binärdateien (Case-insensitive)
            binary_extensions = ('.jpg', '.jpeg', '.png', '.pdf', '.gif', '.zip', '.docx', '.otf', '.ttf')
            if template_filename.lower().endswith(binary_extensions):
                
                # --- NEU: Prüfung auf Dateigröße (0 Bytes) ---
                if os.path.getsize(source_path) == 0:
                    return
                
                # Kopieren der Binärdatei
                shutil.copy2(source_path, renderfile)
                return
    
            # 4. Normales Jinja2 Rendering für Textdateien
            env = Environment(loader=FileSystemLoader(tempdir))
            template_vars = self.get_render_variables()
            
            template = env.get_template(template_filename)        
            template_out = template.render(template_vars)
            
            # Auch hier: Falls das Render-Ergebnis leer ist, nicht schreiben
            if not template_out.strip():
                return
            
            with open(renderfile, "w", encoding="utf8") as myfile:
                myfile.write(template_out)

    def render_all_latex_templates(self) -> None:
        """
        Render all template files defined by initialisation of the class.
        First it will be tried to render from the selected template category.
        
        Example:
        ├── config.ini
        └── templates
            ├── blank
            │   ├── content.tex.j2
            │   └── meta.tex.j2
            └── default
                ├── content.tex.j2
                ├── document.tex.j2
                ├── main.py.j2
                ├── meta.tex.j2
                └── thelper.sty.j2
                
        If selected 'blank' as template category it will render 'content.tex.j2'
        and 'meta.tex.j2'. For the other templates it will fallback to the
        template category 'default'.


        Returns
        -------
        None

        """
        for tkey in self.config['TEMPLATES'].keys():
            try:
                self.render_latex_template(tkey,self.args['templatedir'])
            except:
                self.render_latex_template(tkey,self.args['defaulttemplatedir'])

    def convert_ini_to_yaml(self, ini_path: str, yaml_path: str = None) -> None:
        import configparser
        import yaml
        import os

        ini_path = os.path.abspath(ini_path)
        if not os.path.isfile(ini_path):
            raise FileNotFoundError(f"INI file not found: {ini_path}")

        if yaml_path is None:
            yaml_path = ini_path.replace(".ini", ".yml")

        config = configparser.ConfigParser()
        config.read(ini_path)

        data = {section: dict(config[section]) for section in config.sections()}

        # ⚠️ Sicherstellen, dass YAML nicht leer ist
        if not data:
            data = {"SETTINGS": {}, "TEMPLATES": {}, "VARIABLES": {}}

        with open(yaml_path, "w") as f:
            yaml.dump(data, f, sort_keys=False)

        print(f"Converted {ini_path} -> {yaml_path}")
        

def main(headless=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("--confdir", help="path to config dir", default=os.path.join(os.environ['HOME'],'.config','thelper'),type=str)
    parser.add_argument("-t", help="template category e.g. default", default='default' ,type=str)
    parser.add_argument("-d", help="default template category e.g. default", default='default' ,type=str)
    parser.add_argument("-r", help="render latex templates", action="store_true")
    parser.add_argument("--convert-ini", help="convert an existing config.ini to config.yml", type=str)


    args = parser.parse_args()

    if args.convert_ini:
        helper = thelper(**vars(args))
        helper.convert_ini_to_yaml(args.convert_ini)
        return
  
    # init object
    if headless: _ = thelper(**vars(args))
    else: return thelper(**vars(args))

if __name__ == "__main__":   
    self = main(headless=False)