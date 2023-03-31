from flask import Flask, render_template, send_from_directory, request
from flask_restful import Api, Resource, reqparse, abort
import re



class Error:
    def __init__(self,code,message):
        self.code = code
        self.message = message

    def abort_check(self):
        if(self.code == 200):
            return
        if(self.code == 400):
            abort(self.code,'There is missing field(s) in the PackageID/AuthenticationToken\
            \ or it is formed improperly, or the AuthenticationToken is invalid.')
        if(self.code == 413):
            abort(self.code,'Too many packages returned.')   
        if(self.code == 401):
            abort(self.code,'You do not have permission to reset the registry.')    
        else:
            abort(self.code,self.message)
        

class PackageMetadata:
    def __init__(self,Name,Version):
        self.Name = PackageName(Name)
        self.Version = SemverRange(Version)
        self.ID = ID
    
    def jsonify(self):
        resource_fields = {
            'Version': self.Version,
            'Name': self.Name
        }
        return resource_fields

class PackageID:
    def __init__(self, ID):
        id_format = (r'\d+')
        if re.match(id_format, ID):
            self.ID = ID
        else:
            raise ValueError("Must have a valid ID number")
class PackageQuery:
    def __init__(self,Name,Version=None):
        self.Name = PackageName(Name)
        self.Version = SemverRange(Version)
        
class SemverRange:
    def __init__(self,Version):
        version_format = (r'(\^|\~)?(\d+\.\d+\.\d+)(\-\d+\.\d+\.\d+)?')
        if Version == None:
            self.Version = None
        elif re.match(version_format, Version):
            self.Version = Version
        else:
            self.Version = None 
            raise ValueError('Incorrect version format')
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

class EnumerateOffset:
    def __init__(self,request):
        self.offset = str(request.args.get('offset',default = 0, type = int))

