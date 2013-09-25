# TODO:
# * Fix ocsync packaging for and fix plugin dependencies here
# * Fix and package lang stuff
# * Package ruby gem based cli
Summary:	Desktop file sync client for directory sharing and syncronization
Name:		mirall
Version:	1.4.0
Release:	0.2
License:	GPL v2
Group:		Libraries
Source0:	http://download.owncloud.com/download/%{name}-%{version}.tar.bz2
# Source0-md5:	05a69082b4e940b4282c2b05344c143a
URL:		http://www.owncloud.org
BuildRequires:	QtGui-devel
BuildRequires:	QtTest-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	check
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	kde4-icons-oxygen
BuildRequires:	libstdc++-devel
BuildRequires:	ocsync-devel
Requires:	PackageKit-gtk-module
Requires:	iproute2
Requires:	kde4-icons-oxygen
Requires:	net-tools
Requires:	net-tools
Requires:	ocsync
#Requires:	ocsync-plugin-sftp
#Requires:	ocsync-plugin-smb
#Requires:	ruby-owncloud-admin
Requires:	sitecopy
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mirall is the the QT baesd frontend desktop client for owncloud using
ocsync as a backend.

%package -n owncloud-client
Summary:	Desktop file sync client for owncloud, a Dropbox-like directory sharing and syncronization tool
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	ocsync-owncloud

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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md COPYING
%attr(755,root,root) %{_bindir}/owncloud
%dir %{_sysconfdir}/ownCloud
%{_sysconfdir}/ownCloud/sync-exclude.lst
%attr(755,root,root) %{_libdir}/libowncloudsync.so.*.*.*
%ghost %{_libdir}/libowncloudsync.so.0
%{_desktopdir}/owncloud.desktop
%{_iconsdir}/hicolor/48x48/apps/owncloud.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libowncloudsync.so

%files -n owncloud-client
%defattr(644,root,root,755)
