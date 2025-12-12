%bcond_without tests
%global _disable_ld_no_undefined 1
#global _empty_manifest_terminate_build 0

Summary:	Duplicate File Finder with fuzzy picture and music file support
Name:		dupeguru
Version:	4.3.1
Release:	3 
License:	GPLv3
URL:		https://dupeguru.voltaicideas.net/
Source0:	https://github.com/arsenetar/dupeguru/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	desktop-file-utils
BuildRequires:	fdupes
BuildRequires:	gettext
BuildRequires:	imagemagick
# setup
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(polib)
BuildRequires:	python%{pyver}dist(sphinx)
#install
BuildRequires:	mutagen
BuildRequires:	python%{pyver}dist(distro)
BuildRequires:	python%{pyver}dist(pyqt5)
BuildRequires:	python%{pyver}dist(send2trash)
BuildRequires:	python%{pyver}dist(semantic-version)
BuildRequires:	python%{pyver}dist(xxhash)
#BuildRequires:	python%{pyver}dist(pyqt5-sip)
# extra
BuildRequires:	python%{pyver}dist(flake8)
BuildRequires:	python%{pyver}dist(black)
#BuildRequires:	python-hsaudiotag3k
# test
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-monkeyplus)

%description
dupeGuru is a tool to find duplicate files on your computer. It can scan
either filenames or contents. The filename scan features a fuzzy matching
algorithms that can find duplicate filenames even when they are not exactly
identical. dupeGuru is good with music and pictures. It has a special music 
and picture  modes that can scan tags and show music-specific information 
whilst the picture mode can scan pictures fuzzily, which allows you to find 
pictures that are similar but not identical. 

%files -f columns.lang -f core.lang -f ui.lang
%license LICENSE
%doc CREDITS README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{py_platsitedir}/%{name}/core
%{py_platsitedir}/%{name}/hscommon
%{py_platsitedir}/%{name}/qt
%{py_platsitedir}/%{name}/run.py

#-----------------------------------------------------------------------

%prep
%autosetup -p1

%build
export NO_VENV=true

#configure
%set_build_flags
%make_build

%install
export NO_VENV=true
%make_install PREFIX=%{_prefix}

# fix build path
install -dm 0755 %{buildroot}%{python3_sitearch}/%{name}/
mv %{buildroot}%{_datadir}/%{name}/{core,hscommon,locale,qt,run.py}  %{buildroot}%{python3_sitearch}/%{name}/

# fix executable to bindir
ln -sf %{python3_sitearch}/%{name}/run.py %{buildroot}%{_bindir}/%{name}

# icons
for d in 16 22 32 48 64 72 96 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -strip -background none -size "${d}x${d}" images/dgse_logo_128.png \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
#install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
#convert -size 32x32 sources/pics/vector-logo/%{sname}-logo.svg \
#	%{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# .desktop
desktop-file-install \
	--dir=%{buildroot}%{_datadir}/applications \
	--set-generic-name='Duplicate Files Finder' \
	--add-category='System' \
	--add-category='Filesystem' \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# locales
%find_lang columns
%find_lang core
%find_lang ui

# clean out unecessary files
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.c" -delete
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.h" -delete
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.po" -delete
find %{buildroot}%{python3_sitearch}/%{name}/ -type f -name "*.pot" -delete

