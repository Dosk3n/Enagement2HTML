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

def Json2Dict(filename):
    jsonfile = open(filename, "r")
    jsondata = jsonfile.read()
    jsonfile.close()
    hostdata = json.loads(jsondata)
    return hostdata

######## Methods for writing HTML ###########

def WriteBootstrapHead(savefilename, hostdata):
    code = """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <title>""" + hostdata["ip"] + """</title>
  </head>
  <body>

  <div class="container">
    """
    htmlfile = open(savefilename, "a")
    htmlfile.write(code)
    htmlfile.close()

def WriteBootstrapFoot(savefilename):
    code = """    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
  </body>
</html>"""
    htmlfile = open(savefilename, "a")
    htmlfile.write(code)
    htmlfile.close()

def JumbotronHTML(savefilename, hostdata):
    title = ""
    if("label" in hostdata):
        title = hostdata["label"]
    elif("ip" in hostdata):
        title = hostdata["ip"]
    code = """
        <div class="jumbotron">
        <div class="container">
            <h1 class="display-4">""" + title + """</h1>
            <p class="lead">An HTML report generated from the JSON results of https://pentest.ws.</p>
        </div>
        </div>
    """
    htmlfile = open(savefilename, "a")
    htmlfile.write(code)
    htmlfile.close()

def MainNotesHTML(savefilename, hostdata):
    if("notes" in hostdata):
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
    if("credentials" in hostdata):
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
    MainNotesHTML(savefilename, hostdata)
    CredentialsHTML(savefilename, hostdata)
    WriteBootstrapFoot(savefilename)


filename = ArgParse()
FileExists(filename)
hostdata = Json2Dict(filename)
savefilename = hostdata["ip"] + ".html"

os.remove(savefilename)
BuildHTML(savefilename, hostdata)