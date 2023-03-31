%define major 1

%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

%bcond_with crosscompile
%global optflags %{optflags} -Oz

Summary:	A utility for retrieving files using the HTTP or FTP protocols
Name:		wget2
Version:	2.0.1
Release:	2
Group:		Networking/WWW
License:	GPLv3
URL:		http://www.gnu.org/directory/GNU/wget.html
Source0:	https://ftp.gnu.org/pub/gnu/wget/%{name}-%{version}.tar.lz

BuildRequires:	autoconf-archive
BuildRequires:	lzip
BuildRequires:	gettext
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	texinfo
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(gpgme)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libunistring)
BuildRequires:	pkgconfig(libpsl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libpcre2-posix)
Requires:	openssl
Requires:	rootcerts
Requires:	%{libname} = %{version}-%{release}

%description
GNU Wget is a file retrieval utility which can use either the HTTP or FTP
protocols. Wget features include the ability to work in the background
while you're logged out, recursive retrieval of directories, file name
wildcard matching, remote file timestamp storage and comparison, use of
Rest with FTP servers and Range with HTTP servers to retrieve files over
slow or unstable connections, support for Proxy servers, and
configurability.

%package -n %{libname}
Summary:        Shared library for %{name}

%description -n %{libname}
Package providing library to for Wget2.
This package contains the shared library files.

%package -n %{devname}
Summary:        Development files for %{name}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Package providing development library to for Wget2.
This package contains development files for %{name}.

%prep
%autosetup -n wget2-%{version} -p1

aclocal -I m4
automake -a
autoconf

%build
# not compile with clang 15
export CC=gcc
export CXX=g++
%configure \
	--enable-ipv6 \
	--disable-rpath \
	--with-ssl=openssl \
	--with-linux-crypto \
	--with-openssl=no \
%if %{with crosscompile}
	--with-libssl-prefix=$SYSROOT
%endif

%make_build


%install
%make_install

%find_lang %{name} --all-name

%files -f %{name}.lang
%doc AUTHORS NEWS README
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libwget.so.%{major}*

%files -n %{devname}
%{_libdir}/libwget.so
%{_libdir}/pkgconfig/libwget.pc
%{_includedir}/wget.h
%{_includedir}/wgetver.h
