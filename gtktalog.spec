%define name gtktalog
%define version 1.0.4
%define release %mkrel 9
%define theirversion %version

Name: %{name}
Summary: The Gnome disk catalog
Version: %{version}
Release: %{release}
License: GPLv2+
Group: Archiving/Other
Source0: http://savannah.nongnu.org/download/gtktalog/gtktalog.pkg/%theirversion/%{name}-%{theirversion}.tar.bz2
Source10: gtktalog48.png.bz2
Patch0: gtktalog-1.0.3-dont-scan-mime-types-by-default.patch
Patch1: gtktalog-1.0.4-fix-docs-build.patch
#gw fix bug #26517
Patch2: gtktalog-1.0.4-report-as-text.patch
#gw fix missing header and format strings
Patch3: gtktalog-1.0.4-fix-build.patch
URL: http://www.freesoftware.fsf.org/gtktalog/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: flex gnome-libs-devel mpgtx ncurses-devel
BuildRequires: docbook-utils
#gw if patched:
BuildRequires: automake1.7
BuildRequires: gettext-devel
Requires: file mpgtx

%description
GTKtalog is a disk catalog, it means you can use it to create a really small
database with images of files and folders of your CD-rom. So you can browse all
your CD's very quickly, see contents of certain files (tar.gz, rpm files ...).
You can give to each folder and file a category and a description. You can
search for files in your database with filename, category, description or file
information parameter, and find in which CD the file you are looking for is.

%prep
%setup -q -n %{name}-%{theirversion}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
libtoolize --install --force
aclocal-1.7 -I m4
autoconf
autoheader
automake-1.7
perl -pi -e "s/book1.html/index.html/" Docs/*/topic.dat

%build
%configure2_5x --disable-mp3info --enable-catalog3 --enable-fixcd --enable-mpgtx
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall mkinstalldirs=`pwd`/mkinstalldirs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GTKtalog
Comment=The Gnome disk catalog
Exec=%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Archiving-Other;Archiving;
EOF


mkdir -p $RPM_BUILD_ROOT/%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_liconsdir}
install gtktalog16.png $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install gtktalog32.png $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
bzcat %{SOURCE10} > $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

%find_lang %{name} --with-gnome

#(peroyvind) remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png
rm -f $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Applications/gtktalog.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO BUGS
%{_bindir}/*
%{_datadir}/gtktalog
%_datadir/applications/mandriva*
%{_libdir}/%{name}
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_mandir}/*/*

