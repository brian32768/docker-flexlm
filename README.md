# docker-flexlm

Do you wonder who is using your ArcGIS licenses?

Is the available monitoring software too expensive? (you can just buy more ArcGIS seats
for less $!)

Do you want to run the ArcGIS license manager inside a Docker?

My ultimate goal in this project is just to get a monitor running
(just a Web page). 

To get there, the project at this stage just builds a Docker image
(called "flexlm") containing complete copy of the ESRI version of
Flexera flexlm.

Because Flexera FlexLM is licensed software, if you want to do this
build you will need to download the Linux version of the license
manager from ESRI and put it here before doing the build.

There could be additional steps to build another separate Docker image
that has just what's needed to run the lmutil executable and the web
service but I don't do that yet. It's not as efficient as it could be,
in other words.

## Stage 1, build license manager server

### Notes on the Dockerfile

The Dockerfile is currently built on this version:

    ArcGIS_License_Manager_Linux_2019_0_169356.tar.gz

You also need a copy of the service.txt file from your license manager. 
You need to edit the service.txt file so that it has the actual license server host name instead of "This_Host".

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

If the build fails with a message about not being able to COPY then you did not put
the tar.gz file here. The nice part about Docker is that it will pick up where it left
off after you get the file and do the "docker build" command again.

A successful build ends up with a long series of Copy File and Install File messages from
the flexlm installer that runs inside the container and finally with

    Successfully tagged flexlm:latest

At this point, you will have an image file called "flexlm" with a complete copy of the
license software installed in /home/flexlm/arcgis but no working configuration or
license keys.

### Confirm the build (optional step!)

You can look around in the new container by launching into a shell.
if you don't want to, skip to the Extraction section below.

    docker run -it --rm --name=lm flexlm bash

Now you're in a bash shell in the home directory of the 'flexlm' user.
You can examine install log files and things like that. You should be able
to execute the lmutil program which is in the LicenseManager/bin folder.

You can now run lmutil with this command

    ~/arcgis/licensemanager/bin/lmutil

The output should be all the subcommands and options for lmutil. After confirming
it works, type 'exit' to leave the Docker container.

The "--rm" will remove the container name "lm" when you exit from the shell.
If it does not then you can remove it yourself with

    docker rm lm

## Stage 2, the monitor.

This is currently folded into this project. I intend on breaking it out someday.

The python code and its environment were already set up in the Docker file. Now you just have to run it.

    docker run -it --rm -p 5000:5000 --name=lm flexlm

And visit the URL http://localhost:5000/ (or use your server name in place of localhost).

Presumably you want it to run forever and survive reboots so this is the command to move to deployment.

    docker run -d --restart always -p 5000:5000 --name=lm flexlm

See it run

    docker ps
    
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

