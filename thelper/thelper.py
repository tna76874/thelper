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
        The central config file from the HOME directory will be loaded if exist.
        Otherwise a config file will be created.

        Returns
        -------
        None

        """
        self.args['conffile'] = os.path.join(self.args['confdir'],'config.ini')
            
        if os.path.isfile(self.args['conffile']):
            self.config = configparser.ConfigParser()
            self.config.read(self.args['conffile'])
            self.config['SETTINGS']['defaulttemplate']=self.args['d']
            self.rendervars.update(dict(self.config['VARIABLES']))
        else:
            self.config = configparser.ConfigParser()
            self.config['SETTINGS'] =       {
                                            'templatebasedir'           : "templates",
                                            'defaulttemplate'           : self.args['d'],
                                            }
            self.config['TEMPLATES'] =      {
                                            'main_template'             : "document.tex.j2",
                                            'style_template'            : "thelper.sty.j2",
                                            'meta_template'             : "meta.tex.j2",
                                            'python_template'           : "main.py.j2",
                                            'content_template'          : "content.tex.j2",
                                            }
            self.config['VARIABLES'] =      self.rendervars

            with open(self.args['conffile'], 'w') as savefile:
                self.config.write(savefile)
                
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
        """
        The config file from the current working directory will be loaded if exist.
        Otherwise a config file will be created.

        Returns
        -------
        None.

        """
        subconffile = os.path.join(os.getcwd(),'config.ini')
            
        if os.path.isfile(subconffile):
            config = configparser.ConfigParser()
            config.read(subconffile)
            self.rendervars.update(dict(config['VARIABLES']))
        else:
            config = configparser.ConfigParser()
            config['VARIABLES'] = self.rendervars

            with open(subconffile, 'w') as savefile:
                config.write(savefile)

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
        
            
    def render_latex_template(self,tkey: str, tempdir: str ) -> None:
        """
        Render a single template file.

        Parameters
        ----------
        tkey : str
            The key of the config section 'TEMPLATES'.
        tempdir : str
            The foldername of the template category.

        Returns
        -------
        None

        """
        env = Environment(loader=FileSystemLoader(tempdir))
        template_vars = self.get_render_variables()
        
        template = env.get_template(self.config['TEMPLATES'][tkey])        
        template_out = template.render(template_vars)
        
        if template_out=='':
            return
        
        renderfile = os.path.join(os.getcwd(), self.get_render_filename(tkey))
        if not os.path.exists(renderfile):
            with open(renderfile, "w",encoding="utf8") as myfile:
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
        

def main(headless=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("--confdir", help="path to config dir", default=os.path.join(os.environ['HOME'],'.config','thelper'),type=str)
    parser.add_argument("-t", help="template category e.g. default", default='default' ,type=str)
    parser.add_argument("-d", help="default template category e.g. default", default='default' ,type=str)
    parser.add_argument("-r", help="render latex templates", action="store_true")


    args = parser.parse_args()
  
    # init object
    if headless: _ = thelper(**vars(args))
    else: return thelper(**vars(args))

if __name__ == "__main__":   
    self = main(headless=False)