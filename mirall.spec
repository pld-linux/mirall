# TODO:
# * Fix ocsync packaging for and fix plugin dependencies here
# * Fix and package lang stuff
# * Package ruby gem based cli
Summary:	Desktop file sync client for directory sharing and syncronization
Name:		mirall
Version:	1.6.2
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	52518b622e9b2c151e64a4b56bcf2414
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

%package -n owncloud-client
Summary:	Desktop file sync client for owncloud, a Dropbox-like directory sharing and syncronization tool
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	ocsync-owncloud >= 0.90.2

%description -n owncloud-client
Meta package to install the front end client for owncloud, a Dropbox
like directory sharing and syncronization tool.

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
%{_iconsdir}/hicolor/*/apps/owncloud.png
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

