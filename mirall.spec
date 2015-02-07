#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	nautilus		# build Nautilus extension

%define	qtver	4.7.0
Summary:	Desktop file sync client for directory sharing and syncronization
Name:		mirall
Version:	1.7.0
Release:	0.4
License:	GPL v2
Group:		Libraries
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	f662f4510ef26b5484f754304f8d9295
URL:		https://owncloud.org/install/#desktop
BuildRequires:	check
BuildRequires:	cmake >= 2.8
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	neon-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sphinx-pdg
%if %{with qt4}
BuildRequires:	QtGui-devel >= %{qtver}
BuildRequires:	QtKeychain-devel
BuildRequires:	QtSql-devel >= %{qtver}
BuildRequires:	QtTest-devel >= %{qtver}
BuildRequires:	QtWebKit-devel >= %{qtver}
BuildRequires:	QtXmlPatterns-devel >= %{qtver}
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	iproute2
Requires:	net-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mirall is the the QT based frontend desktop client for owncloud using
ocsync as a backend.

%package nautilus
Summary:	A nautilus extension for %{name}
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus-python

%description nautilus
A mirall extension to nautilus file browser.

%package libs
Summary:	owncloudsync and ocsync libraries
Group:		Libraries

%description libs
owncloudsync and ocsync libraries.

%package devel
Summary:	Header files for %{name}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name}

%prep
%setup -q

%if %{without nautilus}
%{__sed} -i -e "s/add_subdirectory(nautilus)//" shell_integration/CMakeLists.txt
%endif

%build
install -d build
cd build

%cmake \
	-DCSYNC_INCLUDE_PATH=%{_includedir}/ocsync \
	-DWITH_ICONV=ON \
	-DDOC=ON \
	-DUNIT_TESTING=ON \
	-DCMAKE_DISABLE_FIND_PACKAGE_Libsmbclient=OFF \
	-DCMAKE_DISABLE_FIND_PACKAGE_LibSSH=OFF \
	%{!?with_qt4:-DBUILD_LIBRARIES_ONLY=ON} \
	%{?with_qt4:-DBUILD_WITH_QT4=ON} \
	..

%{__make}
%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/{html,latex}

mv $RPM_BUILD_ROOT%{_libdir}/owncloud/* $RPM_BUILD_ROOT%{_libdir}
rmdir $RPM_BUILD_ROOT%{_libdir}/owncloud

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc README.md COPYING ChangeLog
%attr(755,root,root) %{_bindir}/owncloud
%attr(755,root,root) %{_bindir}/owncloudcmd
%{_mandir}/man1/owncloud.1*
%{_mandir}/man1/owncloudcmd.1*
%dir %{_sysconfdir}/ownCloud
%{_sysconfdir}/ownCloud/sync-exclude.lst
%{_desktopdir}/owncloud.desktop
%{_iconsdir}/hicolor/*/apps/own*.png
%dir %{_datadir}/owncloud
%dir %{_datadir}/owncloud/i18n
%{_datadir}/owncloud/i18n/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libocsync.so.*.*.*
%ghost %{_libdir}/libocsync.so.0
%attr(755,root,root) %{_libdir}/libowncloudsync.so.*.*.*
%ghost %{_libdir}/libowncloudsync.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libowncloudsync.so
%attr(755,root,root) %{_libdir}/libocsync.so
%{_libdir}/libhttpbf.a
%{_includedir}/httpbf.h
%{_includedir}/owncloudsync

%if %{with nautilus}
%files nautilus
%defattr(644,root,root,755)
%{_datadir}/nautilus-python/extensions/*.py
%endif
