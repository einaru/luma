%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global srcname distribute

Name:		luma
Version:	3.0.6b
Release:	1%{?dist}
Summary:	LDAP Browser and administration utility
Group:		Applications/System
License:	GNU General Public License (GPL) version 2
URL:		http://luma.sf.net/
Source0:	http://folk.ntnu.no/einaru/luma/dist/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	python2-devel

Requires:	python >= 2.6
Requires:	python-ldap >= 2.3
Requires:	PyQt4
Requires:	python-smbpasswd
Requires:	hicolor-icon-theme

%description
Luma is an cross-platform and open soruce graphical utility for accessing and
managing data stored on LDAP enabled servers. It is written in Python, using 
PyQt4 and python-ldap. Luma supports plugins through its own plugin system. A
selection of plugins, providing useful LDAP-functionality, is includeed in the
base application.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
python setup.py install -O1 --root=${buildroot} --record=INSTALLED_FILES
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Fri May 6 2011 Einar Uvsløkk <einar.uvslokk@linux.com> 3.0.6b-1
- Initial rpm build for the new Luma (version 3.*) - Beta 1 Release
