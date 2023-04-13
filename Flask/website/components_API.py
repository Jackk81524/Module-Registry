from flask import Flask, render_template, send_from_directory, request
from flask_restful import Api, Resource, reqparse, abort
import re
from enum import Enum

# Update for package data
def MetaData_reqparse():
    args = reqparse.RequestParser()
    args.add_argument("Name",type = str,help = "Name of package is required",required = True)
    args.add_argument("Version",type = str,help = "Version is required",required = True)
    return args

class Error:
    def __init__(self,code,message):
        self.code = code
        self.message = message

    def abort_check(self):
        if(self.code == 200 or self.code == 201):
            return
        if(self.code == 400):
            abort(self.code,'There is missing field(s) in the PackageID/AuthenticationToken\
            \ or it is formed improperly, or the AuthenticationToken is invalid.')
        if(self.code == 413):
            abort(self.code,'Too many packages returned.')   
        if(self.code == 401):
            abort(self.code,'You do not have permission to reset the registry.')
        if(self.code == 404):
            abort(self.code,'Package does not exist.')
        if(self.code == 424):
            abort(self.code,'Package is not uploaded due to the disqualified rating.') 
        if(self.code == 500):
            abort(self.code,'The package rating system choked on at least one of the metrics.')
        else:
            abort(self.code,self.message)
        

class PackageMetadata:
    def __init__(self,Name,Version,ID):
        self.Name = PackageName(Name)
        self.Version = SemverRange(Version)
        self.ID = ID
    
    def to_dict(self,ID = False):
        resource_fields = {
            'Version': self.Version.Version,
            'Name': self.Name.Name
        }
        if ID == True:
            resource_fields["ID"] = self.ID
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
        self.offset = str(request.args.get('offset',default = 1, type = int))


class Package:
    def __init__(self,Name,Version,Data):
        self.MetaData = MetaData(Name,Version)
        self.PackageData = Data

class PackageData:
    def __init__(self,request_type,JSProgram, content = None,URL = None):
        if request_type == 'get':
            self.content = content
            self.URL = URL
            self.JSProgram = JSProgram

class PackageRating:
    def __init__(self,RampUp,Correctness,BusFactor,ResponsiveMaintainer,LicenseScore,GoodPinningPractice,PullRequest,NetScore):
        self.RampUp = RampUp
        self.Correctness = Correctness
        self.BusFactor = BusFactor
        self.ResponsiveMaintainer = ResponsiveMaintainer
        self.LicenseScore = LicenseScore
        self.GoodPinningPractice = GoodPinningPractice
        self.PullRequest = PullRequest
        self.NetScore = NetScore

class PackageHistoryEntry:
    def __init__(self,User,Date,PackageMetadata,Action):
        self.User = User
        self.Date = Date
        self.PackageMetadata = PackageMetadata
        self.Action = Action

class User:
    def __init__(self,Name,isAdmin):
        self.Name = Name
        self.isAdmin = isAdmin

class Action(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DOWNLOAD = 'DOWNLOAD'
    RATE = 'RATE'