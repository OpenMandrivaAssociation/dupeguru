%bcond_without tests
%define gitsnapshot 20201027
%global debug_package %{nil}

Name:           dupeguru
Version:        %{gitsnapshot}
Release:        1
Summary:     Duplicate File Finder with fuzzy picture and music file support
License:        GPLv3
URL:            https://dupeguru.voltaicideas.net/
Source0:        https://github.com/arsenetar/dupeguru/archive/%{version}/%{name}-src-%{version}.tar.xz
BuildRequires:  imagemagick
BuildRequires:  fdupes
BuildRequires:  hicolor-icon-theme
# BuildRequires:  python-qt5-utils
BuildRequires:  python-Send2Trash >= 1.3.0
BuildRequires:  python-sphinx
BuildRequires:  python-hsaudiotag3k
BuildRequires:  python-polib
BuildRequires:  python-qt5-devel
BuildRequires:  python-pytest
BuildRequires:  python-pytest-monkeyplus
BuildRequires:  python-flake8
BuildRequires:  python-devel
BuildRequires:  python-sip-qt5

Requires:       python-Send2Trash >= 1.3.0
Requires:       python-hsaudiotag3k
Requires:       python-jobprogress
Requires:       python-polib
Requires:       python-qt5
Requires:       python-libxml2
Requires:       python-sip-qt5

%description
dupeGuru is a tool to find duplicate files on your computer. It can scan
either filenames or contents. The filename scan features a fuzzy matching
algorithms that can find duplicate filenames even when they are not exactly
identical. dupeGuru is good with music and pictures. It has a special music 
and picture  modes that can scan tags and show music-specific information 
whilst the picture mode can scan pictures fuzzily, which allows you to find 
pictures that are similar but not identical. 


%prep
%setup -q -c -n %{name}-src-%{version}
 

%build
export NO_VENV=true
%make_build

%install

cat > %{name}.desktop << EOF
[Desktop Entry]
Name=dupeGuru
GenericName=Duplicate Files Finder
GenericName[ru]=Поиск одинаковых файлов
Comment=Find duplicate files
Comment[ru]=Поиск одинаковых файлов
Type=Application
Exec=dupeguru
Icon=dupeguru
Categories=System;Utility;Filesystem;
Terminal=false
StartupNotify=true
EOF

# There is no make install target
install -dm 0755 %{buildroot}{%{_bindir}/,%{python3_sitearch}/%{name}/}
cp -R {core,hscommon,locale,qt,qtlib}  %{buildroot}%{python3_sitearch}/%{name}/
install -m0755 run.py %{buildroot}%{python3_sitearch}/%{name}/

# Link executable to bindir.
ln -s %{python3_sitearch}/%{name}/run.py %{buildroot}%{_bindir}/%{name}



# Clean out unecessary files
rm -rf %{buildroot}%{python3_sitearch}/%{name}/qtlib/.tx/
rm -rf %{buildroot}%{python3_sitearch}/%{name}/qtlib/locale/
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name ".gitignore" -delete
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.c" -delete
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.h" -delete
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.po" -delete
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.pot" -delete
find %{buildroot}%{python3_sitearch}/%{name}/

# locales.
%find_lang columns
%find_lang core
%find_lang ui

# Install icons
install -Dm 644 images/dgse_logo_128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
for size in 96x96 64x64 48x48 32x32 22x22 16x16 ; do
install -dm 0755 \
    %{buildroot}%{_datadir}/icons/hicolor/${size}/apps
convert -strip -resize ${size} images/dgse_logo_128.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/%{name}.png
done

install -Dm 644 %{name}.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
    
%files -f columns.lang -f core.lang -f ui.lang
#%%files 
%license LICENSE
%doc CREDITS README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.*


%{python3_sitearch}/%{name}/core/__pycache__/
%{python3_sitearch}/%{name}/core/gui/
%{python3_sitearch}/%{name}/core/me/
%{python3_sitearch}/%{name}/core/pe/
%{python3_sitearch}/%{name}/core/se/
%{python3_sitearch}/%{name}/core/tests/
%{python3_sitearch}/%{name}/core/*.py
%{python3_sitearch}/%{name}/hscommon/
%{python3_sitearch}/%{name}/qt/
%{python3_sitearch}/%{name}/qtlib/
%{python3_sitearch}/%{name}/run.py
%{python3_sitearch}/%{name}/__pycache__/
