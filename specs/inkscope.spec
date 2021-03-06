Summary: inkscope
Name: inkscope
%define inkscope_version 1.0.0
Version: %{inkscope_version} 
Release: 6
License: Apache License
Packager: Eric Mourgaya <eric.mourgaya@arkea.com>
Distribution: Redhat
Vendor: inkscopeTeams
AutoReqProv: no
Source0: inkscope.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Summary: install ceph probe and monitor clusters

%description
install  sysprobe scripts

%package common
Summary: common file beetwen all packages
Requires: python-bson
Requires: python-psutil
Requires: python-pymongo
%description common
install all conf files

%package sysprobe
Summary: monitor system
Requires: lshw
Requires: inkscope-common
%description sysprobe
install sysprobe scripts

%package cephprobe
Summary: monitoring  of ceph cluster
Requires: lshw
Requires: inkscope-common
%description cephprobe
install ceph prob only

%package cephrestapi
Summary: allow ceph rest api compute
Requires: lshw
Requires: ceph
%description cephrestapi
install a ceph-rest-api start script

%package admviz
summary:  install interface  of inkscope viz
Requires: inkscope-common
Requires: httpd >= 2.4.0
Requires: python-flask
Requires: mod_wsgi
Requires: python-requests
Requires: python-simplejson
Requires: python-ceph

%description admviz
install the admin interface

%prep

%build
mkdir -p tmp/
cd tmp/
tar xvzf %{SOURCE0}

%install
mkdir -p %{buildroot}/opt/inkscope/etc
mkdir -p %{buildroot}/opt/inkscope/bin
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/etc/logrotate.d/
mkdir -p %{buildroot}/var/www/inkscope/
mkdir -p %{buildroot}/etc/httpd/conf.d/


cd tmp/inkscope
install -m 600 inkscopeProbe/sysprobe.py %{buildroot}/opt/inkscope/bin/
install -m 600 inkscope.conf %{buildroot}/opt/inkscope/etc/
install -m 600 inkscopeProbe/cephprobe.py %{buildroot}/opt/inkscope/bin/
install -m 600 inkscopeProbe/daemon.py %{buildroot}/opt/inkscope/bin/
install -m 700 DISTRIBS/confs/init.d/sysprobe %{buildroot}/etc/init.d/
install -m 700 DISTRIBS/confs/init.d/cephprobe %{buildroot}/etc/init.d/
install -m 700 DISTRIBS/confs/init.d/ceph-rest-api %{buildroot}/etc/init.d/
install -m 644 DISTRIBS/confs/logrotate/inkscope  %{buildroot}/etc/logrotate.d/
install -m 644 DISTRIBS/confs/logrotate/cephrestapi  %{buildroot}/etc/logrotate.d/

install -m 644 DISTRIBS/confs/httpd/inkScope.conf  %{buildroot}/etc/httpd/conf.d/

install -m 644 index.html  %{buildroot}/var/www/inkscope/
for file in $(find inkscopeViz -type f); do
install -m 644 -D ${file}  %{buildroot}/var/www/inkscope/${file#source/}
done

for file in $(find inkscopeCtrl -type f); do
install -m 644 -D ${file}  %{buildroot}/var/www/inkscope/${file#source/}
done


%clean
rm -rf $RPM_BUILD_ROOT

%files admviz
%defattr(-,root,root)
/var/www/inkscope/index.html
/var/www/inkscope/inkscopeCtrl/*
/var/www/inkscope/inkscopeViz/*
%config(noreplace) /etc/httpd/conf.d/inkScope.conf

%files sysprobe
%defattr(-,root,root)
/opt/inkscope/bin/sysprobe.py
/etc/init.d/sysprobe

%files common
%defattr(-,root,root)
/opt/inkscope/bin/daemon.py
%config(noreplace)  /opt/inkscope/etc/inkscope.conf
/etc/logrotate.d/inkscope

%files cephprobe
%defattr(-,root,root)
/opt/inkscope/bin/cephprobe.py
/etc/init.d/cephprobe

%files cephrestapi
%defattr(-,root,root)
/etc/logrotate.d/cephrestapi
/etc/init.d/ceph-rest-api
