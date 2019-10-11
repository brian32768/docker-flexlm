# docker-flexlm

Do you wonder who is using your ArcGIS licenses?

Is the available monitoring software too expensive? (you can just buy more ArcGIS seats
for less $!)

Do you want to run the ArcGIS license manager inside a Docker?

My ultimate goal in this project is just to get a monitor running
(just a Web page) with the license manager running in it At this stage
all I have is a Docker that will extract the executable for 'lmutil'
for use in the monitor docker to create a Web front end.

To get there, the project at this stage just builds a Docker image
(called "flexlm") containing complete copy of the ESRI version of
Flexera flexlm.

Because Flexera FlexLM is licensed software, if you want to do this
build you will need to download the Linux version of the license
manager from ESRI and put it here before doing the build.

## Stage 1, lmutil extraction

### Notes on the Dockerfile

The Dockerfile is currently built on this version:

    ArcGIS_License_Manager_Linux_2019_0_169356.tar.gz

If the version number changes you will have to change the Dockerfile.

The requirements doc at ESRI call for RHEL 6 or 7; the Dockerfile uses Centos 7.

I took their list of required packages and dropped them into the Dockerfile.

You'll see I broke up the package installation into multiple RUN commands. That's because
when I tried doing them in one pass, it failed. I did not try to fine tune it or confirm
which ones were really needed.

Installation is done in "silent" mode so there is no requirement for
any X Window server or any interactions from you.

### Build, stage 1

First go to my.esri.com and download the latest Linux license manager. It will be a file
ending in 'tar.gz'. The newest one right now is:
ArcGIS_License_Manager_Linux_2019_0_169356.tar.gz

Then run the build command to create an image named 'flexlm'.

    docker build -t flexlm .

After building, you will have an image file called flexlm with a complete copy of the
license software installed in /home/flexlm/arcgis but no working configuration or
license keys.

### Confirm it built

You can look around in the new container by launching into a shell.
if you don't want to, skip to the Extraction section below.

    docker run -it --rm --name=lm flexlm bash

Now you're in a bash shell in the home directory of the 'flexlm' user.
You can examine install log files and things like that. You should be able
to execute the lmutil program which is in the LicenseManager/bin folder.

The "--rm" will remove the container name "lm" when you exit from the shell.
If it does not then you can remove it yourself with

    docker rm lm

### Extaction lmutil

Mount a volume and extract the utility.

    docker run -it --rm -v bin:/mnt --rm --name=lm flexlm 'bash cp lmutil /mnt'

The command will mount the bin folder as a volume and then copy lmutil into it.

All this work up to this point was just to extract the lmutil program to the local filesystem!

Did it work? From the host command prompt, if you run

    bin/lmutil

and you get some reasonable output, you can move on. It might not be able
to run on the host you are running Docker on but that's okay, the next
step is to install it into another Docker container to actually use it.

## Other applications for this Docker

Of course you can use this as the starting point for a
Dockerised license manager. It is completely capable of running
as a service if you add the service file and the command to
start lmgrd running. That's 2 lines of code.

Drop me a line if you want to try it and need help.

It's much easier to set up Docker than to set up a complete, separate
RHEL 7 server to support just the one license manager application.

But that's not what I am up to here. Not yet anyway. I have not set up
the repo for the monitor yet. I will start on that as soon as this one
is done and add more comments here.

I started a Windows-based monitor and quit when I found
out how hard it was (FOR ME) to work with Docker On Windows.

That repo is still out there; I might take another crack at it someday. See
http://github.com/brian32768/node-service

