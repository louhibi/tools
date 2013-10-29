#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import yaml
import os
import traceback
import logging

class Error(Exception):
    def __init__(self, value, trace, **args):
        self.value = value
        self.trace = trace
        self.initHook(**args)

    def initHook(self):
        pass

    def __str__(self):
        return repr(self.value)


class Error_File_Yaml(Error):
    def initHook(self):
        self.value = "YAML Error: Fail to open the Yaml file %s" % self.value

class Error_import_app(Error):
    def initHook(self):
        self.value = "Module Loader Error: Fails to load %s" % self.value

def LoadYaml(pathFile):
    """
    Loads the Yaml file and returns it as Yaml object
    """
    # checking if the file exists else raise error file does not exists
    if os.path.exists(pathFile):
        with open(pathFile) as f:
            dataToReturn = yaml.safe_load(f)
        return Yaml_object(**dataToReturn)

    else:
        raise Error_File_Yaml(pathFile, traceback.format_exc())

def ipv4_check(ip):
    """
    @returns True if valid ip v4 else return False
    """
    ipParts = ip.split(".")
    if len(ipParts) != 4:
        return False
    for part in ipParts:
        if not 0 <= int(part) <= 255:
            return False
    return True

def cleanFormatNumber(number):
    """
    Cleans Format a Number
    cleanFormatNumber(514-546-1234) returns 5145461234
    or cleanFormatNumber(514 546 1234) returns 5145461234
    """
    return "".join(number.replace(" ", "").split('-'))

def cleanFormatListNumber(Listnumber):
    """
    Cleans Format a list of Numbers
    cleanFormatNumber(["5145461234", "514-546-1234", "514 546-1234"]) returns ["5145461234", "5145461234", "5145461234"]
    """
    return [cleanFormatNumber(i) for i in Listnumber]

def import_module(app):
    """
    @returns the the imported module or it raises an error
    """
    try:
        return __import__('apps.%s' % app, globals(), locals(), [app], -1)
    except ImportError:
        raise Error_import_app(app, traceback.format_exc())

def initialise_log(self, pathToFile=None, nameFile=None, level=None, uid=False, console=False):
    """
    returns a logging instance with the right Handler and Formatting
    """
    logger = logging.getLogger('simple_example')
    if pathToFile is not None:
        pathToLogFile = '%s/%s.log' % (pathToFile, nameFile)
    else:
        if nameFile:
            pathToLogFile = '/tmp/%s.log' %nameFile
        else:
            console= True

    if console:
        logHandler = logging.StreamHandler()
    else:
        logHandler= logging.FileHandler(pathToLogFile)

    logger.setLevel(level)
    if not uid:
        logHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
    else:
        logHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(uid)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(logHandler)        
    return logger

def is_number(number):
    """
    returns True if number is digit else False
    """
    try:
        int(number)
        return True
    except ValueError:
        return False


class Yaml_object:
    """
    object Yaml file.
    y = YamlFile
    print y.property
    print y.property.property1
    """
    def __init__(self, **entries):
        self.dictionary = entries
        for k, v in entries.items():
            if not isinstance(v, dict):
                setattr(self, k, v)
            else:
                setattr(self, k, Yaml_object(**v))
    def __str__(self):
        return "<Yaml_object: %s>" % repr(self.dictionary)


if __name__ == '__main__':
    assert ipv4_check("12.14.213.13") == True
    assert ipv4_check("12.14.213.256") == False
    assert ipv4_check("12.14.213.5.13") == False
    assert ipv4_check("12.14.213") == False
    assert cleanFormatNumber("514-546-1234") == "5145461234"
    assert cleanFormatNumber("514 546 1234") == "5145461234"
    assert cleanFormatNumber("514 546-1234") == "5145461234"
    assert cleanFormatNumber("5145461234") == "5145461234"
    assert cleanFormatListNumber(["5145461234", "514-546-1234", "514 546-1234"]) == ["5145461234", "5145461234", "5145461234"]
    assert is_number("25") == True
    assert is_number("25del") == False
    assert is_number("del") == False
    assert is_number("??") == False
