# TODO
# - probably can use a lot of system libs
Summary:	Group chat and IM - built for teams
Name:		hipchat
Version:	1.99.894
Release:	0.1
License:	Unknown
Group:		Applications/Communications
Source0:	http://downloads.hipchat.com/linux/arch/%{name}-i686.tar.xz
# NoSource0-md5:	99d3caf93f18b6f26f4b2082a8080d57
NoSource:	0
Source1:	http://downloads.hipchat.com/linux/arch/%{name}-x86_64.tar.xz
# NoSource1-md5:	0728c72e93e55b7e0a22081e7db4c2d8
NoSource:	1
URL:		https://www.hipchat.com/linux
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_libdir}/%{name}
%define		_enable_debug_packages	0

# we don't want these to be provided as system libraries
# to update, 'rpm -q --provides' should be empty
%define		stdc_libs	'libstdc\\+\\+.so.6'
%define		qt_libs		libQt5Core.so.5 libQt5DBus.so.5 libQt5Declarative.so.5 libQt5Gui.so.5 libQt5Multimedia.so.5 libQt5MultimediaWidgets.so.5 libQt5Network.so.5 libQt5OpenGL.so.5 libQt5PrintSupport.so.5 libQt5Qml.so.5 libQt5Quick.so.5 libQt5Script.so.5 libQt5Sensors.so.5 libQt5Sql.so.5 libQt5WebKit.so.5 libQt5WebKitWidgets.so.5 libQt5Widgets.so.5 libQt5X11Extras.so.5 libQt5Xml.so.5 libQt5XmlPatterns.so.5
%define		icu_libs	libicudata.so.44 libicui18n.so.44 libicuuc.so.44
%define		canberra_libs	libcanberra-alsa.so libcanberra-multi.so libcanberra-null.so libcanberra-oss.so libcanberra-pulse.so libcanberra.so.0
%define		k_libs		libKIdleTime.so.5 libKNotifications.so libKWindowSystem.so.5
%define		misc_libs	libcanberraSoundNotification.so libdbusmenu-qt5.so.2 libhipchatdbusscripting.so libqxmpp.so.0 libsonnetcore.so libsonnetui.so libvorbis.so.0 libvorbisfile.so.3 libcomposeplatforminputcontextplugin.so libibusplatforminputcontextplugin.so libappmenu-qt.so
%define		kspell_libs	libkspell_aspell.so libkspell_enchant.so libkspell_hunspell.so
%define		misc_libs2	libogg.so.0 libqconnmanbearer.so libqgenericbearer.so libqgif.so libqico.so libqjpeg.so libqnmbearer.so libqxcb.so

%define		_noautoprov		%{stdc_libs} %{k_libs} %{qt_libs} %{icu_libs} %{misc_libs} %{canberra_libs} %{kspell_libs} %{misc_libs2}

# and as we don't provide them, don't require either
%define		_noautoreq		%{_noautoprov}

%description
Persistent group chat using XMPP.

%prep
%ifarch %{ix86}
%setup -qcT -b 0
%endif
%ifarch %{x8664}
%setup -qcT -b 1
%endif

# simplify for install
mv opt/HipChat/{bin,lib,share/fonts/truetype} .
%{__sed} -i -e '/^Exec=.*/ s,^Exec=.*,Exec=%{_bindir}/%{name},' usr/share/applications/%{name}.desktop

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_pixmapsdir},%{_desktopdir}}
cp -a bin lib $RPM_BUILD_ROOT%{_appdir}
ln -s %{_appdir}/bin/hipchat $RPM_BUILD_ROOT%{_bindir}
cp -a usr/share/* $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hipchat
%{_desktopdir}/hipchat.desktop
%{_iconsdir}/hicolor/*/apps/hipchat-attention.png
%{_iconsdir}/hicolor/*/apps/hipchat.png
%dir %{_appdir}
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/HipChatNowPlaying.rb
%attr(755,root,root) %{_appdir}/bin/hipchat
%attr(755,root,root) %{_appdir}/bin/linuxbrowserlaunch
%dir %{_appdir}/lib
%attr(755,root,root) %{_appdir}/lib/hipchat.bin
%attr(755,root,root) %{_appdir}/lib/kurasshu
%attr(755,root,root) %{_appdir}/lib/lib*.so*

%dir %{_appdir}/lib/plugins
%dir %{_appdir}/lib/plugins/bearer
%attr(755,root,root) %{_appdir}/lib/plugins/bearer/lib*.so

%dir %{_appdir}/lib/plugins/imageformats
%attr(755,root,root) %{_appdir}/lib/plugins/imageformats/lib*.so

%dir %{_appdir}/lib/plugins/menubar
%attr(755,root,root) %{_appdir}/lib/plugins/menubar/lib*.so

%dir %{_appdir}/lib/plugins/platforminputcontexts
%attr(755,root,root) %{_appdir}/lib/plugins/platforminputcontexts/lib*.so

%dir %{_appdir}/lib/plugins/platforms
%attr(755,root,root) %{_appdir}/lib/plugins/platforms/lib*.so

%dir %{_appdir}/lib/plugins/sonnet_clients
%attr(755,root,root) %{_appdir}/lib/plugins/sonnet_clients/lib*.so

%dir %{_appdir}/lib/libcanberra-*
%attr(755,root,root) %{_appdir}/lib/libcanberra-*/libcanberra-*.so
