FROM conda/miniconda3-centos7

# =================================================================
# STAGE 1 -- Configure a build host and install the license manager
# This list of packages is from the ESRI requirements description.

RUN yum install -y \
 compat-libstdc++-33.i686 \
 compat-libf2c-34.i686 \
 compat-openldap.i686 \
 cairo.i686 \
 freeglut.i686 \
 fuse-libs.i686 \
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
 libstdc++.i686 \
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
    mkdir -p /usr/local/share/macrovision/storage && \
    chmod 777 /usr/local/share/macrovision/storage

USER flexlm
WORKDIR /home/flexlm

COPY ArcGIS_License_Manager_Linux_2019_2_173095.tar.gz LicenseManager.tar.gz
RUN tar xzvf LicenseManager.tar.gz && \
    cd LicenseManager_Linux && \
    ./Setup -l Yes -m silent

# Dump messages out so that errors will be visible on the console when building 
RUN cat arcgis/licensemanager/.Setup/LicenseManager_InstallLog.log

# ===========================================
# STAGE 2 -- install and run the microservice

# Someday I will separate out the files needed to run lmutil out and put them here.
# I'd need to look at the dynamic libraries and install them in another container. ldd lmutil
# For now I just install everything right here
#VOLUME /mnt

USER root

# Might not need this section, just following boilerplate on Python 3 for redhat
#RUN yum install -y centos-release-scl
#RUN yum install -y @development
#RUN yum install -y rh-python36

# This will upgrade conda, so the fact that the base image is old does not matter
# flask-bootstrap needs hugo
RUN conda update -n base -c defaults conda
RUN conda config --add channels conda-forge && \
    conda config --add channels hugo && \
    conda config --add channels Esri

COPY requirements.txt ./
RUN conda install --file requirements.txt

# Add python to the path for flexlm user
USER flexlm
WORKDIR /home/flexlm
ENV LMUTIL /home/flexlm/arcgis/licensemanager/bin/lmutil

# Add the commands to flexlm user's PATH
RUN echo "export PATH=\$PATH:$HOME/arcgis/licensemanager/bin/" >> .bashrc

# Install the microservice
COPY service.txt .
COPY license_monitor.py .

EXPOSE 5000

# Run the microservice
CMD "./license_monitor.py" "./service.txt"
