from flask import Flask, render_template, send_from_directory, request
from flask_restful import Api, Resource, reqparse, abort
import re

class Error:
    def __init__(self,code,message):
        self.code = code
        self.message = message

    def abort(self):
        if(code != abort):
            abort(code,message = 'message')

class PackageMetadata:
    def __init__(self,Name,Version):
        self.Name = PackageName(Name)
        self.Version = SemverRange(Version)
        self.ID = ID
    
    @staticmethod
    def validate_name(Name):
        #enter keyboard format
        return Name

class PackageID:
    def __init__(self, ID):
        id_format = (r'\d+')
        if re.match(id_format, ID):
            self.ID = ID
        else:
            raise ValueError("Must have a valid ID number")
class PackageQuery:
    def __init(self,Name,Version=None):
        self.Name = PackageName(Name)
        self.Version = SemverRange(Version)
        
class SemverRange:
    def __init__(self,Version):
        version_format = (r'\((\^|\~)?(\d+\.\d+\.\d+)(\-\d+\.\d+\.\d+)?\)')
        if Version == None:
            self.Version = None
        elif re.match(version_format, Version):
            self.Version = Version
        else:
            self.Version = None 
            print('Incorrect version format')
            ## log incorrect version format

class PackageName:
    def __init__(self,Name):
        name_format = (r'[ -~]+')
        search = re.search(r'\*', Name)
        if Name == None:
            raise ValueError("Name cannot be null")
        elif (search != None and len(Name) != 1):
            raise ValueError("Name cannot use the * character, as this is reserved")
        elif re.match(name_format, Name):
            self.Name = Name
        else:
            raise ValueError("Name must only contain keyboard characters")




