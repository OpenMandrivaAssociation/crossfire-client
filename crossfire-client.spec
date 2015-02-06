%define	version	1.70.0
%define release 2

Name:		crossfire-client
Version:	%{version}
Release:	%{release}
Summary:	Client for connecting to crossfire game servers
Group:		Games/Adventure
License:	GPLv2+
URL:		http://crossfire.real-time.com/
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source3:	%{name}-icon-small.png
Source4:	%{name}-icon-medium.png
Source5:	%{name}-icon-large.png
BuildRequires:	gtk2-devel
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(glu)
BuildRequires:	alsa-oss-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(lua)
Requires:	%{name}-data >= 1.50.0

%description
Crossfire is a highly graphical role-playing adventure game with
characteristics reminiscent of rogue, nethack, omega, and gauntlet. 
It has multiplayer capability and presently runs under X11.

This package contains client for playing the new client/server based version
of Crossfire. It allows you to connect to crossfire servers around the world.
You do not need to install the crossfire server in order to play crossfire.

%prep
%setup -q

sed -ri -e '/^.TH/s:$: 6:' $(find . -name "*man")

bzip2 -c ChangeLog > ChangeLog.bz2

%build
# If data file path is changed, crossfire-client-data spec file
# needs to be adjusted as well.
%configure2_5x \
	--with-sound-dir=%{_gamesdatadir}/%{name}/sounds \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir}

%make LIBS="-lX11 -lpng -lcurl"

%install
%makeinstall_std

# icons
mkdir -p %{buildroot}{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
install -m 0644 %{SOURCE3} %{buildroot}%{_miconsdir}/%{name}.png
install -m 0644 %{SOURCE4} %{buildroot}%{_iconsdir}/%{name}.png
install -m 0644 %{SOURCE5} %{buildroot}%{_liconsdir}/%{name}.png

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Crossfire Client
Comment=%{summary}
Exec=crossfire-client-gtk2 -cache -download_all_faces -fasttcpsend -nosplash -fog -opengl -showicon
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Game;AdventureGame;
EOF

%files
%doc ChangeLog.bz2 NOTES README TODO
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
