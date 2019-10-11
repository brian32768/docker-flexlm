FROM centos:7

# =================================================================
# STAGE 1 -- Configure a build host and install the license manager

RUN yum install -y \
 compat-libstdc++-33.i686 \
 compat-libf2c-34.i686 \
 compat-openldap.i686 \
 cairo.i686 \
 freeglut.i686 \
 fuse-libs.i686

RUN yum install -y \
 gmp.i686 \
 gtk2.i686 \
 PackageKit-glib.i686 \
 PackageKit-gtk3-module.i686 \
 polkit.i686 \
 polkit.x86_64 \
 redhat-lsb.i686

RUN yum install -y \
 libcanberra.i686 \
 libgcc.i686 \
 libgfortran.i686 \
 libidn.i686 \
 libstdc++.i686

RUN yum install -y \
 libSM.i686 \
 libX11.i686 \
 libXau.i686 \
 libxcb.i686 \
 libXdamage.i686 \
 libXext.i686 \
 libXfixes.i686 \
 libXrender.i686 \
 libXp.i686 \
 libXScrnSaver.i686 \
 libXtst.i686

RUN yum install -y \
 mesa-libGL.i686 \
 mesa-libGLU.i686

RUN adduser flexlm && \
    mkdir -p /usr/local/share/macrovision/storage && chmod 777 /usr/local/share/macrovision/storage

USER flexlm
WORKDIR /home/flexlm

COPY ArcGIS_License_Manager_Linux_2019_0_169356.tar.gz LicenseManager.tar.gz
RUN tar xzvf LicenseManager.tar.gz && \
    cd LicenseManager_Linux && \
    ./Setup -l Yes -m silent

# Dump messages out so that errors will be visible on the console when building 
RUN cat arcgis/licensemanager/.Setup/LicenseManager_InstallLog.log

# ===========================================
# STAGE 2 -- install and run the microservice

# Someday I will pull the files needed to run lmutil out and put them here.
# I'd need to look at the dynamic libraries and install them in another container. ldd lmutil
# For now I just install everything right here
#VOLUME /mnt

USER root

# Might not need this section, just following boilerplate on Python 3 for redhat
RUN yum install -y centos-release-scl
RUN yum install -y @development
RUN yum install -y rh-python36

# Add python to the path for flexlm user
USER flexlm
ENV LMUTIL /home/flexlm/arcgis/licensemanager/bin/lmutil

# Add the commands to flexlm user's PATH
RUN echo "source /opt/rh/rh-python36/enable" > .bashrc
RUN echo "export PATH=\$PATH:$HOME/arcgis/licensemanager/bin/" >> .bashrc

RUN /opt/rh/rh-python36/root/bin/python -m venv license_monitor && \
  source license_monitor/bin/activate && \
  pip install flask

# Install the microservice and the config file
COPY service.txt .
COPY license_monitor.py .

EXPOSE 5000

# Run the microservice
CMD "./license_monitor/bin/python" "license_monitor.py" "./service.txt"
