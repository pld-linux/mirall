# TODO:
# * Fix ocsync packaging for and fix plugin dependencies here
# * Fix and package lang stuff
# * Package ruby gem based cli
Summary:	Desktop file sync client for directory sharing and syncronization
Name:		mirall
Version:	1.7.0
Release:	0.2
License:	GPL v2
Group:		Libraries
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	f662f4510ef26b5484f754304f8d9295
URL:		http://www.owncloud.org
BuildRequires:	QtGui-devel
BuildRequires:	QtTest-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	QtKeychain-devel
BuildRequires:	check
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	kde4-icons-oxygen
BuildRequires:	libstdc++-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
Requires:	iproute2
Requires:	kde4-icons-oxygen
Requires:	net-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mirall is the the QT baesd frontend desktop client for owncloud using
ocsync as a backend.

%package nautilus
Summary:	A nautilus extension for %{name}
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus-python

%description nautilus
A mirall extension to nautilus file browser.

%package devel
Summary:	Header files for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name}

%prep
%setup -q

%build
if test ! -e "build"; then
	%{__mkdir} build
fi

cd build

%cmake \
	-DCSYNC_INCLUDE_PATH=%{_includedir}/ocsync \
	-DCMAKE_C_FLAGS:STRING="%{optflags}" \
	-DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
	-DCMAKE_SKIP_RPATH=ON \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DPREFIX=%{_prefix} \
	-DSYSCONFDIR=%{_sysconfdir} \
	$RPM_BUILD_ROOT/%{name}-%{version} \
	..

%{__make}
%{__make} doc

cd ..

%install
rm -rf $RPM_BUILD_ROOT

cd build

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv ${RPM_BUILD_ROOT}/%{_libdir}/owncloud/* ${RPM_BUILD_ROOT}/%{_libdir}/
rmdir ${RPM_BUILD_ROOT}/%{_libdir}/owncloud

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md COPYING ChangeLog
%attr(755,root,root) %{_bindir}/owncloud
%attr(755,root,root) %{_bindir}/owncloudcmd
%dir %{_sysconfdir}/ownCloud
%{_sysconfdir}/ownCloud/sync-exclude.lst
%attr(755,root,root) %{_libdir}/libowncloudsync.so.*.*.*
%ghost %{_libdir}/libowncloudsync.so.0
%attr(755,root,root) %{_libdir}/libocsync.so.*
%{_desktopdir}/owncloud.desktop
%{_iconsdir}/hicolor/*/apps/own*.png
%dir %{_datadir}/owncloud
%dir %{_datadir}/owncloud/i18n
%{_datadir}/owncloud/i18n/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libowncloudsync.so
%attr(755,root,root) %{_libdir}/libocsync.so
%{_libdir}/libhttpbf.a
%{_includedir}/httpbf.h
%dir %{_includedir}/owncloudsync
%dir %{_includedir}/owncloudsync/mirall
%dir %{_includedir}/owncloudsync/creds
%{_includedir}/owncloudsync/mirall/*
%{_includedir}/owncloudsync/creds/*

%files nautilus
%defattr(644,root,root,755)
%{_datadir}/nautilus-python/extensions/*.py

