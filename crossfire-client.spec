%define	version	1.9.1
%define	release %mkrel 3

Name:		crossfire-client
Version:	%{version}
Release:	%{release}
Summary:	Client for connecting to crossfire game servers
Group:		Games/Adventure
License:	GPL
URL:		http://crossfire.real-time.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source3:	%{name}-icon-small.png
Source4:	%{name}-icon-medium.png
Source5:	%{name}-icon-large.png
Patch0:		crossfire-client-1.8.0-glut-detect.patch

BuildRequires:	gtk2-devel
BuildRequires:	SDL_image1.2-devel
BuildRequires:	libmesaglut-devel
BuildRequires:	alsa-lib-devel
Requires:	%{name}-data >= 1.9.1

%description
Crossfire is a highly graphical role-playing adventure game with
characteristics reminiscent of rogue, nethack, omega, and gauntlet. 
It has multiplayer capability and presently runs under X11.

This package contains client for playing the new client/server based version
of Crossfire. It allows you to connect to crossfire servers around the world.
You do not need to install the crossfire server in order to play crossfire.


%prep
%setup -q
%patch0 -p1 -b .glut

autoconf

bzip2 -c ChangeLog > ChangeLog.bz2

%build
# If data file path is changed, crossfire-client-data spec file
# needs to be adjusted as well.
%configure2_5x \
	--disable-alsa \
	--disable-gtk \
	--with-sound-dir=%{_datadir}/%{name}/sounds \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir}

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# icons
mkdir -p $RPM_BUILD_ROOT{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{_gamesbindir}/gcfclient2 -cache -download_all_faces -fasttcpsend -nosplash -fog -opengl -showicon" \
icon="%{name}.png" \
longtitle="Client of Crossfire, a graphical adventure game" \
needs="x11" \
section="More Applications/Games/Adventure" \
title="Crossfire Client" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Crossfire Client
Comment=%{summary}
Exec=%{_gamesbindir}/gcfclient2 -cache -download_all_faces -fasttcpsend -nosplash -fog -opengl -showicon
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Game;AdventureGame;X-MandrivaLinux-MoreApplications-Games-Adventure;
Encoding=UTF-8
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog.bz2 NOTES README TODO
%{_gamesbindir}/*
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png


