%define	version	1.50.0
%define	release %mkrel 1

Name:		crossfire-client
Version:	%{version}
Release:	%{release}
Summary:	Client for connecting to crossfire game servers
Group:		Games/Adventure
License:	GPLv2+
URL:		http://crossfire.real-time.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source3:	%{name}-icon-small.png
Source4:	%{name}-icon-medium.png
Source5:	%{name}-icon-large.png
Patch0:		%{name}-1.50.0-fix-str-fmt.patch
BuildRequires:	gtk2-devel
BuildRequires:	libglade2-devel
BuildRequires:	SDL_image-devel
BuildRequires:	libmesaglut-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	curl-devel
BuildRequires:	lua-devel
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
%patch0 -p0

bzip2 -c ChangeLog > ChangeLog.bz2

%build
# If data file path is changed, crossfire-client-data spec file
# needs to be adjusted as well.
%configure2_5x \
	--with-sound-dir=%{_gamesdatadir}/%{name}/sounds \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir}

%make

%install
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog.bz2 NOTES README TODO
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
