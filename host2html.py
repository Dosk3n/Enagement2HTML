#!/usr/bin/python3
#
# Host2HTML - Script to take host json data from pentest.ws and
# create an individual HTML report for that host.
#

import sys
import json
from os import listdir
from os.path import isfile, join
import os

def ArgParse():
    if(len(sys.argv) < 2):
        sys.exit("Exiting... You must supply a file name")
    return sys.argv[1]

def FileExists(filename):
    if(os.path.isfile(filename)):
        return True
    else:
        sys.exit("Exiting... " + filename + " does not exist")

def DeleteFileIfExists(filename):
    if(os.path.isfile(filename)):
        os.remove(filename)

def Json2Dict(filename):
    jsonfile = open(filename, "r")
    jsondata = jsonfile.read()
    jsonfile.close()
    hostdata = json.loads(jsondata)
    return hostdata

######## Methods for writing HTML ###########

def WriteBootstrapHead(savefilename, hostdata):
    ipaddr = ""
    if("ip" in hostdata):
        if hostdata["ip"] is not None:
            ipaddr = hostdata["ip"]

    code = """<!doctype html>
<html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

        <title>""" + ipaddr + """</title>
    </head>
    <body>
    """
    htmlfile = open(savefilename, "a")
    htmlfile.write(code)
    htmlfile.close()

def WriteBootstrapFoot(savefilename):
    code = """
            <br>
        <br>
        <br>
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
    </body>
</html>
    """
    htmlfile = open(savefilename, "a")
    htmlfile.write(code)
    htmlfile.close()

def GetHostFlagsHTML(hostdata):
    flags = ""
    if hostdata["flags"] is not None:
        f = hostdata["flags"]
        flagdata = f[0]
        if(flagdata["root"]):
            flags = flags + '<span class="badge badge-danger">root</span>\n'
        if(flagdata["shell"]):
            flags = flags + '<span class="badge badge-warning">shell</span>\n'
        if(flagdata["out_of_scope"]):
            flags = flags + '<span class="badge badge-info">out_of_scope</span>\n'
        if(flagdata["not_interested"]):
            flags = flags + '<span class="badge badge-light">not_interested</span>\n'
        if(flagdata["interested"]):
            flags = flags + '<span class="badge badge-success">interested</span>\n'
        if(flagdata["reviewed"]):
            flags = flags + '<span class="badge badge-secondary">reviewed</span>\n'
        if(flagdata["flagged"]):
            flags = flags + '<span class="badge badge-primary">flagged</span>\n'
    return flags

def JumbotronHTML(savefilename, hostdata):
    title = "No Title Found"
    subtext = "An HTML report generated from the JSON results of https://pentest.ws."

    if hostdata["label"] is not None:
        if(hostdata["label"] != ""):
            title = hostdata["label"]

    flagbadges = GetHostFlagsHTML(hostdata)

    code = """
        <div class="container">
            <div class="jumbotron">
                <h1 class="display-4">""" + title + """</h1>
                <p class="lead">""" + subtext + """</p>
                """ + flagbadges + """
            </div>
        </div>
    """
    htmlfile = open(savefilename, "a")
    htmlfile.write(code)
    htmlfile.close()

def GetPortInfoHTML(hostdata):
    portinfohtml = ""
    if hostdata["ports"] is not None:
        portdata = hostdata["ports"]
        for port in portdata:
            portnum  = ""
            service  = ""
            protocol = ""
            version  = ""
            status   = ""
            if port["port"] is not None:
                portnum = port["port"]

            code = """
                                    <tr>
                                    <th scope="row">""" + str(portnum) + """</th>
                                    <td>""" + str(service) + """</td>
                                    <td>""" + str(protocol) + """</td>
                                    <td>""" + str(version) + """</td>
                                    <td>""" + str(status) + """<span class="badge badge-danger">Owned</span></td>
                                    </tr>
            """
            portinfohtml = portinfohtml + code

    return portinfohtml

def HostAndPortHTML(savefilename, hostdata):
    ipaddr  = ""
    label   = ""
    opsys   = ""
    systype = ""
    ostype  = ""
    if hostdata["ip"] is not None:
        ipaddr = hostdata["ip"]
    if hostdata["label"] is not None:
        label = hostdata["label"]
    if hostdata["os"] is not None:
        opsys = hostdata["os"]
    if hostdata["type"] is not None:
        systype = hostdata["type"]
        if(systype == "question"):
            systype = ""
    if hostdata["os_type"] is not None:
        ostype = hostdata["os_type"]
        if(ostype == "question"):
            ostype = ""

    portinfohtml = GetPortInfoHTML(hostdata)

    code = """
        <div class="container">
            <div class="row">
                <!-- HOST INFORMATION -->
                <div class="col-sm-4">
                    <div class="card">
                        <h5 class="card-header">Host Information</h5>
                        <div class="card-body">
                            <p class="card-text"><strong>IP Address: </strong> """ + ipaddr + """</p>
                            <p class="card-text"><strong>Label: </strong> """ + label + """</p>
                            <p class="card-text"><strong>Operating System: </strong> """ + opsys + """</p>
                            <p class="card-text"><strong>Type: </strong> """ + systype + """</p>
                            <p class="card-text"><strong>OS Type: </strong> """ + ostype + """</p>
                        </div>
                    </div>
                </div>

                <!-- PORT INFORMATION -->
                <div class="col-sm-8">
                    <div class="card">
                        <h5 class="card-header">Port Information</h5>
                        <div class="card-body">
                            <table class="table">
                                <thead>
                                    <tr>
                                    <th scope="col">Port</th>
                                    <th scope="col">Service</th>
                                    <th scope="col">Protocol</th>
                                    <th scope="col">Version</th>
                                    <th scope="col">Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    """ + portinfohtml + """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <br>
    """
    htmlfile = open(savefilename, "a")
    htmlfile.write(code)
    htmlfile.close()

def MainNotesHTML(savefilename, hostdata):
    if hostdata["notes"] is not None:
        code = """
            <div class="card">
            <h5 class="card-header">Notes</h5>
            <div class="card-body">
                <p class="card-text">""" + hostdata["notes"] + """</p>
            </div>
            </div>
        """
        htmlfile = open(savefilename, "a")
        htmlfile.write(code)
        htmlfile.close()

def CredentialsHTML(savefilename, hostdata):
    if hostdata["credentials"] is not None:
        htmlfile = open(savefilename, "a")
        maincardstart = """
        <br>
        <div class="card">
            <h5 class="card-header">Credentials</h5>
            <div class="card-body">
            <div class="row">
        """
        maincardend = """
        </div>
        </div>
            </div>
        """

        htmlfile.write(maincardstart)


        credentials = hostdata["credentials"]
        for cred in credentials:
            code = """
            <div class="col-sm-6">
                <div class="card">
                <div class="card-body">
                    <h5 class="card-title">""" + cred["service"] + """</h5>
                    <table class="table">
                        <tbody>
                            <tr>
                            <th scope="row">Username</th>
                            <td>""" + cred["username"] + """</td>
                            </tr>
                            <tr>
                            <th scope="row">Password</th>
                            <td>""" + cred["password"] + """</td>
                            </tr>
                            <tr>
                            <th scope="row">Fullname</th>
                            <td>""" + cred["fullname"] + """</td>
                            </tr>
                            <tr>
                            <th scope="row">Hash</th>
                            <td>""" + cred["hash"] + """</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                </div>
            </div>
            """
            htmlfile.write(code)
        

        htmlfile.write(maincardend)
        htmlfile.close()



def BuildHTML(savefilename, hostdata):
    #todo: Check if file exists and delete but ask first
    WriteBootstrapHead(savefilename, hostdata)
    JumbotronHTML(savefilename, hostdata)
    HostAndPortHTML(savefilename, hostdata)
    WriteBootstrapFoot(savefilename)


filename = ArgParse()
FileExists(filename)
hostdata = Json2Dict(filename)
savefilename = hostdata["ip"] + ".html"
DeleteFileIfExists(savefilename)
BuildHTML(savefilename, hostdata)