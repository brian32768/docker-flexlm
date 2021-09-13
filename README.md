# docker-flexlm

DEPRECATED PROJECT -- see https://github.com/Wildsong/arctic-monitor

Do you wonder who is using your ArcGIS concurrent licenses?

Is the available monitoring software too expensive? (you can just buy
more ArcGIS seats for less money!)

Do you want to run the ArcGIS license manager inside a Docker? 
If you have this idea, it might be possible but 
[first read this note from someone who tried!](https://github.com/brian32768/docker-flexlm/issues/2#issuecomment-808343899)

The current version has some support for running the
license manager but I am not currently in a position to test it.

The monitor is a small app written in Python running as a service.
The Python script needs to query the license manager and it does that
using the "lmutil" command line utility that is included in the 
Esri download for the license manager.

I originally wrote the python services to run only in a Docker container but
now I have it working outside Docker as long as the host machine
has a copy of "lmutil" on it.

If you want to deploy to a machine that does not have the ArcGIS license
manager running on it, you can build the Docker version.

Because the license manager "Flexera FlexLM" is licensed software, if
you want to use this monitor in the Docker, you will need to download
the Linux version of the license manager package from ESRI and put it
here in the project folder before doing the Docker build.

## The obligatory screenshot

![Screenshot of monitor for ArcGIS Flexlm](screenshot.png?raw=true "What the web page looks like")

## License manager CAVEAT

2021-Feb-26 Today I added code to run the license manager and the monitor together
in docker-compose.yml

2021-Mar-26 As mentioned above, this is probably [a bad idea](https://github.com/brian32768/docker-flexlm/issues/2#issuecomment-808343899).
I don't use this set up so I cannot configure and test it completely. If you figure out more drop me a line or add comments in the issue.

My personal experience with Esri and Docker reminds me of the Ever Given and the Suez Canal.

brian@wildsong.biz

## Docker comment

The license monitor illustrates why Docker is such a great concept. I don't
want to manage a separate virtual machine just to check license
usage. I don't want to pollute a shared machine with the 400+ packages
that get installed to support the pre-requisites in RHEL 7 for
Flexera. Using a Docker container keeps everything contained and
isolated.

## Test the app

You can test the app without having any special ESRI software
installed, using the lmstat.txt file included in this repo.  Set up a
conda environment and run it. Like this,

```bash
conda create --name flexlm
conda activate flexlm
conda install -c conda-forge --file requirements.txt
FLASK_APP=start_app flask run
```

#### Prerequisites

The Dockerfiles are based on this version of the license manager:

   ArcGIS_License_Manager_Linux_2021.0_177950.tar.gz

When the version number changes you will have to change the Dockerfile.
To get the file, go to my.esri.com and download the latest Linux
license manager.  It will be a file ending in 'tar.gz'. Put the file
in this folder. (The one containing the Dockerfiles.)

#### Notes on the Dockerfile

The requirements doc at ESRI call for RHEL 6 or 7; this Dockerfile uses Centos 7.

I took the list of required RPM packages from the ESRI documentation and
dropped them into the Dockerfile as "stage 1".

I broke up the package installation into multiple RUN commands. That's
because when I tried doing them in one pass, it failed. I did not try
to fine tune it or confirm which ones were really needed or what order
to install them in once I got it working.

The license manager installation step is done in "silent" mode so
there is no requirement for any X Window server or any interactions
from you.

### Docker build

Make sure you've downloaded the tar.gz file, see Prerequisites.

Then run the build command to create images for the license manager and the monitor.

    docker-compose build

If the build fails with a message about not being able to ADD then you
did not put the tar.gz file here or you need to update its name in
"Dockerfile.flexlm" around line 51. 

After the license manager is installed Docker will emit a long series
of Copy File and Install File messages from the flexlm installer. It
will stop at this point if the install fails.

For the monitor, only file we need from the ESRI installation is lmutil.
When the monitor image is built, the file will be copied from the flexlm image.

Once the builds complete you will have an image called "flexlm" with a
complete copy of the license software installed in /home/flexlm/arcgis
and one with just the lmutil tool called flexlm_monitor.

### Confirm the build (optional step!)

You can look around in the new containers by launching into a bash shell.
If you don't want to, skip to the next section.

```bash
docker run -it --rm flexlm bash
docker run -it --rm flexlm_monitor bash
```

When you are in a shell in either of the containers you can examine
install log files and things like that. In the flexlm container you
can run lmgrd. in the monitor container you should be able to execute
the lmutil program.

You can run lmutil with this command

```bash
lmutil
```

When the license tarball from ESRI is updated you have to build a new
image, but that only happens once or twice a year.

## Deployment

The python code and its environment were already set up in the Docker
file.


If you are only running the monitor container then you need a current
copy of the "service.txt" file from your license manager.  You need to
edit the service.txt file so that it has the actual license server
host name instead of "This_Host".  Copy the service.txt file into the
config/ directory, and edit it.

When using both containers the name of the lmgrd host and the name in the service.txt
file have to match. When running the lmgrd somewhere else it has to be
the name of that other machine.

Now you just have to run the containers.

```bash
docker-compose up -d
```

If you only want to run the monitor, you should be able to type

```bash
    docker-compose up monitor
```

The monitor will show up at http://localhost:5000/ (or use your server
name in place of localhost if you are not running it locally).

The output of my running license manager looked like this when I started it.

```bash
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) ===============================================
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) === Vendor Daemon ===
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Vendor daemon: ARCGIS
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Start-Date: Fri Feb 26 2021 14:23:57 PST
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) PID: 8
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) VD Version: v11.16.5.1 build 257031 x64_lsb ( build 257031 (ipv6))
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@)
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) === Startup/Restart Info ===
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Options file used: None
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Is vendor daemon a CVD: No
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Is FlexNet Licensing Service installed and compatible: No
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) FlexNet Licensing Service Version: -NA-
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Is TS accessed: No
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) TS access time: -NA-
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Number of VD restarts since LS startup: 0
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@)
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) === Network Info ===
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Listening port: 27001
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Daemon select timeout (in seconds): 1
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@)
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) === Host Info ===
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Host used in license file: cc-testmaps
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) HostID node-locked in license file: NA
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) HostID of the License Server: 0242ac150003
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) Running on Hypervisor: Unknown Hypervisor
lmgrd_1    | 14:23:57 (ARCGIS) (@ARCGIS-SLOG@) ===============================================
lmgrd_1    | 14:24:33 (ARCGIS) TCP_NODELAY NOT enabled
```

## Misc

I previously started working on a Windows-based monitor and quit when
I found out how hard it was (FOR ME) to work with Docker On Windows.

That incomplete repo is still out there. See
http://github.com/brian32768/node-service


## Resources

### Bootstrap 3

I'm using conda, and they have the flask-bootstrap version 3 package. Bootstrap moved to version 4 ages ago. Docs for 3 are here.

http://bootstrapdocs.com/v3.0.3/docs/getting-started/

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

## Optimization

### What it really uses

That Esri list of required packages is absurdly long and only needed by the installer.
The lmutil program is 32-bit so you have to install compat packages for that,
otherwise things could get tiny. I could not convince it to run on Alpine or Debian (yet).

Lmutil ends up installed in /home/flexlm/arcgis/licensemanager/bin
Here is what it really needs.


```bash
    ldd lmutil
        linux-gate.so.1 =>  (0xf7f59000)
        libpthread.so.0 => /lib/libpthread.so.0 (0xf7f2f000)        glibc
        libm.so.6 => /lib/libm.so.6 (0xf7eed000)                    glibc
        libgcc_s.so.1 => /lib/libgcc_s.so.1 (0xf7ed2000)            libgcc
        libc.so.6 => /lib/libc.so.6 (0xf7d07000)                    glibc
        libdl.so.2 => /lib/libdl.so.2 (0xf7d01000)                  glibc
        librt.so.1 => /lib/librt.so.1 (0xf7cf8000)
        /lib/ld-lsb.so.3 => /lib/ld-linux.so.2 (0xf7f5b000)
```

So in stage two I build an image with only those libraries in it. That shrinks
the image size from about 2+ GB to 1 GB once the fancy flask packages my app
uses are installed with miniconda.

## TO-DO

* Run in waitress instead of using "flask run".
* Actually test and finish lmgrd support

### Version 2 ideas

The advantage of doing this is that I can see the log file and respond as soon as anything happens instead of polling. The disadvantage is that if the server is down, the monitoring web site will be down too. Further it precludes multiple redundant license servers.

I think if I put a tiny REST service on the license manager, and let it run both lmstat
and monitor the logs, and then make a dumber flask app that does not need to have
lmstat installed, I will be several steps ahead. So I will be doing that on the "dev"
branch of this project starting right this minute.

Further I am abandoning the idea that this project can actually be a license server.
It is ONLY for monitoring from now on.


