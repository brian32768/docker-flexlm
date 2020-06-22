# docker-flexlm

Do you wonder who is using your ArcGIS concurrent licenses?

Is the available monitoring software too expensive? (you can just buy more ArcGIS seats
for less money!)

Do you want to run the ArcGIS license manager inside a Docker?

My goal in this project has been to get a monitor running (just a Web page so far).

It does this using a small app written in Python running as a service.
The Python script needs to query the license manager and it does that
using the "lmutil" command line utility.

To get a copy of lmutil, the Docker contains a complete copy of
the ESRI version of Flexera flexlm.

Because Flexera FlexLM is licensed software, if you want to use this
monitor, you will need to download the Linux version of the license
manager from ESRI and put it here before doing the build.

## Docker comment

This project illustrates why Docker is such a great concept. I don't
want to manage a separate virtual machine just to check license
usage. I don't want to pollute a shared machine with the 400+ packages
that get installed to support the pre-requisites in RHEL 7 for
Flexera. Using a Docker container keeps everything contained and
isolated.

## Future directions

Use MQTT and then integrate with "arctic".
It could publish each time license usage changes.

TIMEZONE -- I should do the trick to mount the timezone files or at
least read an environment variable instead of hardcoding Los_Angeles
into the Python script.

## Stage 0, test the app

You can test the app without having any special ESRI software installed,
using the lmstat.txt file included in this repo. 
Set up a conda environment and run it. Like this,

```bash
conda create --name flexlm
conda activate flexlm
conda install -c conda-forge --file requirements.txt
python3 start_app.py
```   

## Stage 1, build the license manager

### Prerequisites

The Dockerfile is currently built using this version of the license manager:

   ArcGIS_License_Manager_Linux_2019_2_173095.tar.gz

If the version number changes you will have to change the Dockerfile.
To get the file go to my.esri.com and download the latest Linux
license manager.  It will be a file ending in 'tar.gz'. Put the file
in this folder. (The one containing the Dockerfile.)

You also need a copy of the "service.txt" file from your license
manager.  You need to edit the service.txt file so that it has the
actual license server host name instead of "This_Host".

Copy the edited file into this folder, too.

### Notes on the Dockerfile

The requirements doc at ESRI call for RHEL 6 or 7; this Dockerfile uses Centos 7.

I took the list of required RPM packages from the ESRI documentation and
dropped them into the Dockerfile.

You'll see I broke up the package installation into multiple RUN
commands. That's because when I tried doing them in one pass, it
failed. I did not try to fine tune it or confirm which ones were
really needed or what order to install them in once I got it working.

The license manager installation step is done in "silent" mode so
there is no requirement for any X Window server or any interactions
from you.

The previous version of this project used "pip" to install Python
packages.  The current version uses "conda" instead, so I moved from
basing the Docker on a plain Centos7 image to
"conda/miniconda3-centos7" so that I don't have to separately install
Conda.

### Docker build, stage 1

Make sure you've downloaded the tar.gz file, see Prerequisites.

Then run the build command to create an image named 'flexlm'.

    docker build -t flexlm .

If the build fails with a message about not being able to COPY then
you did not put the tar.gz and/or service.txt files here. Add them and
run the build command again.  Docker will pick up where it left off
after you get the file(s) into place (Docker won't have to download
and install all the requirement files again.)

After the license manager is installed Docker will emit a long series
of Copy File and Install File messages from the flexlm installer. It
will stop at this point if the install fails.

If it succeeds it will proceed to install the Python modules needed to
run the web microservice. Finally it will say:

    Successfully tagged flexlm:latest

At this point, you will have an image file called "flexlm" with a
complete copy of the license software installed in /home/flexlm/arcgis.

### Confirm the build (optional step!)

You can look around in the new container by launching into a bash shell.
If you don't want to, skip to the next section.

    docker run -it --rm flexlm bash

Now you're in a bash shell in the home directory of the 'flexlm' user.
You can examine install log files and things like that. You should be able
to execute the lmutil program which is in the LicenseManager/bin folder.

You can run lmutil with this command

    lmutil

## Stage 2, the web monitor.

The python code and its environment were already set up in the Docker
file. Now you just have to run it. To try it out, do this:

    docker run -it --rm -p 5000:5000 --name=lm flexlm

Then visit the URL http://localhost:5000/ (or use your server name in place of localhost).

Now that you see it's working, presumably you want it to run forever
on a server and to survive reboots so this is the command to move to
deployment.

    docker run -d --restart always -p 5000:5000 --name=lm flexlm

You can confirm it's running, 

    docker ps
    
## Other applications for this Docker

You can use this as the starting point for a Dockerised license
manager. It is already completely capable of running as a service if
you add the command to start lmgrd running. That's 2 lines of code.

Drop me a line if you want to try it and need help.

I previously started working on a Windows-based monitor and quit when
I found out how hard it was (FOR ME) to work with Docker On Windows.

That incomplete repo is still out there. See
http://github.com/brian32768/node-service


## Resources

### Another similar project

Uses lmutil and stores output in SQL Server:
https://github.com/jmitz/ArcGISLicenseMonitor/blob/master/LicenseMonitor.py

### WATCHING THE LOG FILE

#### REPORT LOGGING - can be enabled in OPTIONS file but produces an encrypted file that is of no use without Flexera software.

See https://openlm.com/blog/are-flexnet-flexlm-manager-report-logs-essential-for-license-consumption-monitoring/

#### Watch for DENIED messages

14:46:39 (telelogic) DENIED: DOORS indkach@indkach  [telelogic] 
(Licensed number of users already reached. (-4,342:10054 )) 
14:46:39 (telelogic) DENIED: DOORS indkach@indkach  [telelogic] 
(Licensed number of users already reached. (-4,342:10054 )) 
14:46:39 (telelogic) OUT: TLSTOK-token indkach@indkach  [DOORS] 
(3 licenses)
