%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           luma
Version:        3.0.3-sprint3
Release:        1%{?dist}
Summary:        LDAP browser and administration utility

Group:          Applications/Communications
License:        GPLv2
URL:            http://luma.sf.net
Source0:        http://downloads.sourceforge.net/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  PyQt4
BuildRequires:  desktop-file-utils

Requires:       python
Requires:       PyQt4
Requires:       python-ldap
Requires:       python-obexftp

%description
Luma is a cross-platform LDAP browser and administration utility.
It provides a plugin system to enchance LDAP administration.
From the core distribution it ships with plugins for:

- browsing LDAP object entries
- ...

%prep


%build


%install


%post


%postun


%clean


%files


%changelog

