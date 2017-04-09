#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constants and discovered values, like path to current installation of pug-nlp."""
from __future__ import division, print_function, absolute_import, unicode_literals
from builtins import (  # noqa
    bytes, dict, int, list, object, range, str,
    ascii, chr, hex, input, next, oct, open,
    pow, round, super,
    filter, map, zip)

import re

removable = '''cl-pcl-msgs kpcli libcommons-httpclient-java libcommons-httpclient-java-doc libdap-dev libdapclient6v5 libgdal-dev libgdal1i
libhttpclient-java liblwgeom-2.2-5 libmail-imapclient-perl libnews-nntpclient-perl libopenscenegraph100v5 libpcl-apps1.7
libpcl-common1.7 libpcl-conversions-dev libpcl-dev libpcl-doc libpcl-features1.7 libpcl-filters1.7 libpcl-io1.7 libpcl-kdtree1.7
libpcl-keypoints1.7 libpcl-msgs-dev libpcl-octree1.7 libpcl-outofcore1.7 libpcl-people1.7 libpcl-recognition1.7
libpcl-registration1.7 libpcl-sample-consensus1.7 libpcl-search1.7 libpcl-segmentation1.7 libpcl-surface1.7 libpcl-tracking1.7
libpcl-visualization1.7 libpcl1 libpcl1-dev libpcl1.7 libpcl1.7-dbg libphp-pclzip libsfcgal1 libvtk6-dev libvtk6-java
libvtk6-qt-dev libvtk6.2 libvtk6.2-qt mcollective-plugins-centralrpclog pcl-tools php-pclzip postgresql-9.5-postgis-2.2
python-jsonrpclib python-pcl-msgs python-vtk6 ruby-httpclient sftpcloudfs tcl-vtk6 vtk6'''

removable = removable.split()

installed = '''libboost-exception1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libboost-python1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1
, automatic), libboost-wave-dev:amd64 (1.58.0.1ubuntu1, automatic), mcollective-common:amd64 (2.6.0+dfsg-2.1, automatic), libpcl-sam
ple-consensus1.7:amd64 (1.7.2-14build1), libltdl-dev:amd64 (2.4.6-0.1, automatic), libxdmf2:amd64 (2.1.dfsg.1-13, automatic), python
-oslo.utils:amd64 (3.8.0-2, automatic), libboost-math-dev:amd64 (1.58.0.1ubuntu1, automatic), libboost-test1.58-dev:amd64 (1.58.0+df
sg-5ubuntu3.1, automatic), qtbase5-dev-tools:amd64 (5.5.1+dfsg-16ubuntu7.2, automatic), libboost1.58-tools-dev:amd64 (1.58.0+dfsg-5u
buntu3.1, automatic), libxcb-present-dev:amd64 (1.11.1-1ubuntu1, automatic), python-jsonrpclib:amd64 (0.1.3-1build1), libboost-log1.
58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libhdf5-cpp-11:amd64 (1.8.16+docs-4ubuntu1, automatic), qtdeclarative5-dev:amd64 (
5.5.1-2ubuntu6, automatic), python-snappy:amd64 (0.5-1build1, automatic), libboost-locale1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, autom
atic), libboost-graph-parallel1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libparse-recdescent-perl:amd64 (1.967013+dfsg-1, aut
omatic), libboost-chrono-dev:amd64 (1.58.0.1ubuntu1, automatic), python-ftp-cloudfs:amd64 (0.25.2+20140217+git2a90c1a2eb-1, automati
c), libboost-iostreams-dev:amd64 (1.58.0.1ubuntu1, automatic), libterm-readline-gnu-perl:amd64 (1.28-2build1, automatic), ruby-domai
n-name:amd64 (0.5.20160216-2, automatic), python-sensor-msgs:amd64 (1.12.3-5, automatic), libx11-xcb-dev:amd64 (2:1.6.3-1ubuntu2, au
tomatic), libnetcdf-c++4:amd64 (4.2-4, automatic), libhwloc5:amd64 (1.11.2-3, automatic), libdata-password-perl:amd64 (1.12-1, autom
atic), python-sendfile:amd64 (2.0.1-1build1, automatic), libhwloc-plugins:amd64 (1.11.2-3, automatic), libjsoncpp-dev:amd64 (1.7.2-1
, automatic), ruby2.3:amd64 (2.3.1-2~16.04, automatic), rake:amd64 (10.5.0-2, automatic), libboost-graph-parallel1.58-dev:amd64 (1.5
8.0+dfsg-5ubuntu3.1, automatic), libegl1-mesa-dev:amd64 (12.0.6-0ubuntu0.16.04.1, automatic), libibverbs1:amd64 (1.1.8-1.1ubuntu2, a
utomatic), python-oslo.i18n:amd64 (3.5.0-2, automatic), libpcl-apps1.7:amd64 (1.7.2-14build1), libboost-timer1.58-dev:amd64 (1.58.0+
dfsg-5ubuntu3.1, automatic), php-common:amd64 (1:35ubuntu6, automatic), libboost-wave1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automat
ic), libvtk6-dev:amd64 (6.2.0+dfsg1-10build1, automatic), mcollective-plugins-centralrpclog:amd64 (0.0.0~git20120507.df2fa81-0ubuntu
1), libmysqlclient-dev:amd64 (5.7.17-0ubuntu0.16.04.2, automatic), libqt5opengl5-dev:amd64 (5.5.1+dfsg-16ubuntu7.2, automatic), ruby
-net-telnet:amd64 (0.1.1-2, automatic), libboost-coroutine1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), python-keystoneclient:am
d64 (1:2.3.1-2, automatic), unixodbc:amd64 (2.3.1-4.1, automatic), libnetcdf-cxx-legacy-dev:amd64 (4.2-4, automatic), ruby-httpclien
t:amd64 (2.7.1-1ubuntu1), python-requests:amd64 (2.9.1-3, automatic), libboost-math1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic),
 libpcl-segmentation1.7:amd64 (1.7.2-14build1), libgeos-dev:amd64 (3.5.0-1ubuntu2, automatic), libxcb-xfixes0-dev:amd64 (1.11.1-1ubu
ntu1, automatic), mesa-common-dev:amd64 (12.0.6-0ubuntu0.16.04.1, automatic), libboost-all-dev:amd64 (1.58.0.1ubuntu1, automatic), l
ibboost-context1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libcommons-logging-java:amd64 (1.2-1+build1, automatic), python-net
ifaces:amd64 (0.10.4-0.1build2, automatic), libboost-mpi-dev:amd64 (1.58.0.1ubuntu1, automatic), python-oslo.serialization:amd64 (2.
4.0-2, automatic), libxdmf-dev:amd64 (2.1.dfsg.1-13, automatic), libqt5webkit5-dev:amd64 (5.5.1+dfsg-2ubuntu1, automatic), libboost-
log-dev:amd64 (1.58.0.1ubuntu1, automatic), x11proto-gl-dev:amd64 (1.4.17-1, automatic), unixodbc-dev:amd64 (2.3.1-4.1, automatic), 
libpcl-recognition1.7:amd64 (1.7.2-14build1), libpcl-outofcore1.7:amd64 (1.7.2-14build1), python-monotonic:amd64 (0.6-2, automatic),
 libboost-locale1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libavformat-dev:amd64 (7:2.8.11-0ubuntu0.16.04.1, automatic), ru
by-json:amd64 (1.8.3-1build4, automatic), libmirclient-dev:amd64 (0.21.0+16.04.20160330-0ubuntu1, automatic), libpcl-octree1.7:amd64
 (1.7.2-14build1), sftpcloudfs:amd64 (0.12.2-2), libboost-python1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libhwloc-dev:amd64
 (1.11.2-3, automatic), libpcl-search1.7:amd64 (1.7.2-14build1), libpcl-features1.7:amd64 (1.7.2-14build1), libboost-random1.58.0:am
d64 (1.58.0+dfsg-5ubuntu3.1, automatic), qttools5-private-dev:amd64 (5.5.1-3build1, automatic), libboost-random-dev:amd64 (1.58.0.1u
buntu1, automatic), libmircommon-dev:amd64 (0.21.0+16.04.20160330-0ubuntu1, automatic), libqhull-dev:amd64 (2015.2-1, automatic), li
bxkbcommon-dev:amd64 (0.5.0-1ubuntu2, automatic), python-stevedore:amd64 (1.12.0-1, automatic), libboost-graph1.58.0:amd64 (1.58.0+d
fsg-5ubuntu3.1, automatic), libmircookie2:amd64 (0.21.0+16.04.20160330-0ubuntu1, automatic), libhdf5-dev:amd64 (1.8.16+docs-4ubuntu1
, automatic), openmpi-common:amd64 (1.10.2-8ubuntu1, automatic), cl-std-msgs:amd64 (0.5.9-2, automatic), libswresample-dev:amd64 (7:
2.8.11-0ubuntu0.16.04.1, automatic), libboost-graph-dev:amd64 (1.58.0.1ubuntu1, automatic), libterm-readkey-perl:amd64 (2.33-1build1
, automatic), ruby-unf-ext:amd64 (0.0.7.2-1build2, automatic), vtk6:amd64 (6.2.0+dfsg1-10build1, automatic), libpcl1.7:amd64 (1.7.2-
14build1), libboost-timer-dev:amd64 (1.58.0.1ubuntu1, automatic), libapache-pom-java:amd64 (10-2build1, automatic), libboost-seriali
zation-dev:amd64 (1.58.0.1ubuntu1, automatic), libpcl-surface1.7:amd64 (1.7.2-14build1), libpcl-tracking1.7:amd64 (1.7.2-14build1), 
python-vtk6:amd64 (6.2.0+dfsg1-10build1, automatic), ruby-minitest:amd64 (5.8.4-2, automatic), libopenni0:amd64 (1.5.4.0-14, automat
ic), libwebpdemux1:amd64 (0.4.4-1, automatic), libboost-mpi1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libavutil-dev:amd64 (7:
2.8.11-0ubuntu0.16.04.1, automatic), libtiff5-dev:amd64 (4.0.6-1ubuntu0.1, automatic), cl-sensor-msgs:amd64 (1.12.3-5, automatic), p
ython-prettytable:amd64 (0.7.2-3, automatic), openni-utils:amd64 (1.5.4.0-14, automatic), libvtk6.2:amd64 (6.2.0+dfsg1-10build1, aut
omatic), libqt5designercomponents5:amd64 (5.5.1-3build1, automatic), libgl2ps-dev:amd64 (1.3.8-1.2, automatic), libqt5concurrent5:am
d64 (5.5.1+dfsg-16ubuntu7.2, automatic), libavcodec-dev:amd64 (7:2.8.11-0ubuntu0.16.04.1, automatic), libvtk6.2-qt:amd64 (6.2.0+dfsg
1-10build1, automatic), python-keystoneauth1:amd64 (2.4.1-1ubuntu0.16.04.1, automatic), mpi-default-bin:amd64 (1.4, automatic), hdf5
-helpers:amd64 (1.8.16+docs-4ubuntu1, automatic), libglu1-mesa-dev:amd64 (9.0.0-2.1, automatic), python-pyftpdlib:amd64 (1.4.0-1, au
tomatic), libqt5quickwidgets5:amd64 (5.5.1-2ubuntu6, automatic), libxcb-randr0-dev:amd64 (1.11.1-1ubuntu1, automatic), libwayland-de
v:amd64 (1.9.0-1, automatic), libboost-program-options-dev:amd64 (1.58.0.1ubuntu1, automatic), python-debtcollector:amd64 (1.3.0-2, 
automatic), libcommons-parent-java:amd64 (39-3, automatic), libpcl-visualization1.7:amd64 (1.7.2-14build1), libxcb-dri3-dev:amd64 (1
.11.1-1ubuntu1, automatic), mpi-default-dev:amd64 (1.4, automatic), libboost-mpi-python-dev:amd64 (1.58.0.1ubuntu1, automatic), libr
uby2.3:amd64 (2.3.1-2~16.04, automatic), libboost-graph-parallel-dev:amd64 (1.58.0.1ubuntu1, automatic), mcollective-client:amd64 (2
.6.0+dfsg-2.1, automatic), pcl-tools:amd64 (1.7.2-14build1), python-paramiko:amd64 (1.16.0-1, automatic), libxcb-shape0-dev:amd64 (1
.11.1-1ubuntu1, automatic), ruby:amd64 (1:2.3.0+1, automatic), libjbig-dev:amd64 (2.1-3.1, automatic), qt5-qmake:amd64 (5.5.1+dfsg-1
6ubuntu7.2, automatic), x11proto-dri2-dev:amd64 (2.8-2, automatic), ruby-stomp:amd64 (1.3.5-1, automatic), libxshmfence-dev:amd64 (1
.2-1, automatic), libpcl-dev:amd64 (1.7.2-14build1), libcommons-httpclient-java-doc:amd64 (3.1-12), libopenmpi1.10:amd64 (1.10.2-8ub
untu1, automatic), libpcl-doc:amd64 (1.7.2-14build1), libboost-context1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), python-ecd
sa:amd64 (0.13-2, automatic), python-netaddr:amd64 (0.7.18-1, automatic), python-positional:amd64 (1.0.1-2, automatic), libboost-ios
treams1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), python-msgpack:amd64 (0.4.6-1build1, automatic), libspatialite-dev:amd64 (
4.3.0a-5, automatic), libgles2-mesa-dev:amd64 (12.0.6-0ubuntu0.16.04.1, automatic), libmail-imapclient-perl:amd64 (3.38-1), python-p
cl-msgs:amd64 (0.2.0-2), ruby-sqlite3:amd64 (1.3.11-2build1, automatic), python-oslo.config:amd64 (1:3.9.0-3, automatic), ieee-data:
amd64 (20150531.1, automatic), libhdf4-alt-dev:amd64 (4.2.10-3.2, automatic), libpcl1-dev:amd64 (1.6-1ubuntu1), libcommons-codec-jav
a:amd64 (1.10-1, automatic), libboost-wave1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libpcl1.7-dbg:amd64 (1.7.2-14build1), ru
by-unf:amd64 (0.1.4-1, automatic), libpcl-kdtree1.7:amd64 (1.7.2-14build1), libnews-nntpclient-perl:amd64 (0.37-8), libhttpclient-ja
va:amd64 (4.5.1-1), libboost-exception-dev:amd64 (1.58.0.1ubuntu1, automatic), python-trollius:amd64 (2.1~b1-3, automatic), libphp-p
clzip:amd64 (2.8.2-3ubuntu1), ruby-power-assert:amd64 (0.2.7-1, automatic), libpcl-registration1.7:amd64 (1.7.2-14build1), libboost-
locale-dev:amd64 (1.58.0.1ubuntu1, automatic), python-secretstorage:amd64 (2.1.3-1, automatic), uuid-dev:amd64 (2.27.1-6ubuntu3.2, a
utomatic), python-txaio:amd64 (1.0.0-3, automatic), libgl1-mesa-dev:amd64 (12.0.6-0ubuntu0.16.04.1, automatic), libtinyxml2.6.2v5:am
d64 (2.6.2-3, automatic), python-cloudfiles:amd64 (1.7.11-3, automatic), libboost-test1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automati
c), libboost-log1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), python-keyring:amd64 (7.3-1ubuntu1, automatic), libterm-shellui-pe
rl:amd64 (0.92-2, automatic), libogg-dev:amd64 (1.3.2-1, automatic), mcollective:amd64 (2.6.0+dfsg-2.1, automatic), libaec-dev:amd64
 (0.3.2-1, automatic), ruby-http-cookie:amd64 (1.0.2-1, automatic), rubygems-integration:amd64 (1.10, automatic), qtbase5-dev:amd64 
(5.5.1+dfsg-16ubuntu7.2, automatic), python-memcache:amd64 (1.57-1, automatic), libsort-naturally-perl:amd64 (1.03-1, automatic), li
bcrypt-rijndael-perl:amd64 (1.13-1build1, automatic), libqt5quickparticles5:amd64 (5.5.1-2ubuntu6, automatic), libpcl-common1.7:amd6
4 (1.7.2-14build1), libpcl-msgs-dev:amd64 (0.2.0-2), libwebp-dev:amd64 (0.4.4-1, automatic), libboost-graph1.58-dev:amd64 (1.58.0+df
sg-5ubuntu3.1, automatic), libboost-python-dev:amd64 (1.58.0.1ubuntu1, automatic), cl-pcl-msgs:amd64 (0.2.0-2), libdapserver7v5:amd6
4 (3.15.1-7, automatic), libcapture-tiny-perl:amd64 (0.32-1, automatic), libhttpcore-java:amd64 (4.4.4-1, automatic), libxerces-c-de
v:amd64 (3.1.3+debian-1, automatic), php-pclzip:amd64 (2.8.2-3ubuntu1), libboost-math1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automat
ic), ruby-systemu:amd64 (2.6.5-1, automatic), libboost-coroutine1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libboost-atomic-
dev:amd64 (1.58.0.1ubuntu1, automatic), libnetcdf-dev:amd64 (1:4.4.0-2, automatic), kpcli:amd64 (2.7-1), libvtk6-qt-dev:amd64 (6.2.0
+dfsg1-10build1, automatic), libopenni-dev:amd64 (1.5.4.0-14, automatic), libxxf86vm-dev:amd64 (1:1.1.4-1, automatic), libfile-keepa
ss-perl:amd64 (2.03-1, automatic), libgif-dev:amd64 (5.1.4-0.3~16.04, automatic), libopenni-sensor-pointclouds0:amd64 (5.1.0.41.5-1,
 automatic), python-swiftclient:amd64 (1:3.0.0-0ubuntu1, automatic), python-concurrent.futures:amd64 (3.0.5-1, automatic), libswscal
e-dev:amd64 (7:2.8.11-0ubuntu0.16.04.1, automatic), python-iso8601:amd64 (0.1.11-1, automatic), ocl-icd-libopencl1:amd64 (2.2.8-1, a
utomatic), libdap-dev:amd64 (3.15.1-7, automatic), ruby-test-unit:amd64 (3.1.7-2, automatic), libpcl1:amd64 (1.6-1ubuntu1), libflann
1.8:amd64 (1.8.4-4.1, automatic), libpcl-io1.7:amd64 (1.7.2-14build1), libxcb-sync-dev:amd64 (1.11.1-1ubuntu1, automatic), python-au
tobahn:amd64 (0.10.3+dfsg1-5, automatic), libpcl-people1.7:amd64 (1.7.2-14build1), libboost-mpi-python1.58-dev:amd64 (1.58.0+dfsg-5u
buntu3.1, automatic), x11proto-xf86vidmode-dev:amd64 (2.3.1-2, automatic), python-lz4:amd64 (0.7.0+dfsg-3build1, automatic), python-
twisted:amd64 (16.0.0-1, automatic), libmircookie-dev:amd64 (0.21.0+16.04.20160330-0ubuntu1, automatic), python-wrapt:amd64 (1.8.0-5
build2, automatic), libflann-dev:amd64 (1.8.4-4.1, automatic), openmpi-bin:amd64 (1.10.2-8ubuntu1, automatic), python-daemon:amd64 (
2.0.5-1, automatic), libxcb-dri2-0-dev:amd64 (1.11.1-1ubuntu1, automatic), libcommons-httpclient-java:amd64 (3.1-12), libtheora-dev:
amd64 (1.1.1+dfsg.1-8, automatic), libboost-mpi1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libxcb-glx0-dev:amd64 (1.11.1-1ub
untu1, automatic), libprotobuf-dev:amd64 (2.6.1-1.3, automatic), libdrm-dev:amd64 (2.4.70-1~ubuntu16.04.1, automatic), libpcl-conver
sions-dev:amd64 (0.2.1-1), libibverbs-dev:amd64 (1.1.8-1.1ubuntu2, automatic), libopenmpi-dev:amd64 (1.10.2-8ubuntu1, automatic), li
blzma-dev:amd64 (5.1.1alpha+20120614-2ubuntu2, automatic), libgdal-dev:amd64 (1.11.3+dfsg-3build2, automatic), libboost-tools-dev:am
d64 (1.58.0.1ubuntu1, automatic), libboost-mpi-python1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), python-mpi4py:amd64 (1.3.1+hg
20131106-2ubuntu5, automatic), libpcl-filters1.7:amd64 (1.7.2-14build1), libjasper-dev:amd64 (1.900.1-debian1-2.4ubuntu1, automatic)
, libboost-timer1.58.0:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libboost-coroutine-dev:amd64 (1.58.0.1ubuntu1, automatic), libvtk6
-java:amd64 (6.2.0+dfsg1-10build1, automatic), libboost-context-dev:amd64 (1.58.0.1ubuntu1, automatic), libtiffxx5:amd64 (4.0.6-1ubu
ntu0.1, automatic), libtool:amd64 (2.4.6-0.1, automatic), libboost-random1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic), libpcl-
keypoints1.7:amd64 (1.7.2-14build1), tcl-vtk6:amd64 (6.2.0+dfsg1-10build1, automatic), libboost-test-dev:amd64 (1.58.0.1ubuntu1, aut
omatic), qttools5-dev:amd64 (5.5.1-3build1, automatic), libnuma-dev:amd64 (2.0.11-1ubuntu1, automatic), cl-geometry-msgs:amd64 (1.12
.3-5, automatic), python-geometry-msgs:amd64 (1.12.3-5, automatic), ruby-did-you-mean:amd64 (1.0.0-2, automatic), libboost-program-o
ptions1.58-dev:amd64 (1.58.0+dfsg-5ubuntu3.1, automatic)'''

removed = []
removed += '''libruby2.3 mcollective mcollective-client mcollective-common mcollective-plugins-centralrpclog rake ruby ruby-did-you-mean
  ruby-domain-name ruby-http-cookie ruby-httpclient ruby-json ruby-sqlite3 ruby-stomp ruby-systemu ruby-unf ruby-unf-ext ruby2.3'''.split()
splitter = re.compile(r'\s*\([^)]*\)\s*[,]?\s*')
installed = sorted(splitter.split(installed))
installed = sorted([s.replace('\n', '') for s in installed if s])
installed = set([s[:-6] if s.endswith(':amd64') for s in installed])
set.remove(set(removed))
