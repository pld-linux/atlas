Summary:	The atlas libraries for numerical linear algebra
Summary(pl):	Biblioteki numeryczne atlas do algebry liniowej
Name:		atlas
Version:	3.7.10
Release:	1
License:	freely distributable
Group:		Development/Libraries
Source0:	http://dl.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
# Source0-md5:	c24aa9f676122fe6331fa63dd88c4113
URL:		http://math-atlas.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	gcc-g77
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

%package devel
Summary:	atlas header files
Summary(pl):	Pliki nag³ówkowe atlas
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	blas-devel = %{version}
Obsoletes:	lapack-man

%description devel
atlas header files.

%description devel -l pl
Pliki nag³ówkowe atlas.

%package static
Summary:	Static atlas libraries
Summary(pl):	Biblioteki statyczne atlas
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static atlas libraries.

%description static -l pl
Biblioteki statyczne atlas.

%package -n blas
Summary:	The BLAS (Basic Linear Algebra Subprograms) library for Linux
Summary(pl):	Biblioteka BLAS (Basic Linear Algebra Subprograms) dla Linuksa
Group:		Development/Libraries
Obsoletes:	lapack-blas

%description -n blas
BLAS (Basic Linear Algebra Subprograms) is a standard library for
numerical algebra. BLAS provides a number of basic algorithms for
linear algebra. BLAS is fast and well-tested, was written in FORTRAN
77.

Warning: this is a reference implementation from Netlib. If possible,
use version optimized for your architecture instead.

%description -n blas -l pl
BLAS (Basic Linear Algebra Subprograms) jest standardow± bibliotek±
numeryczn± algebry. Dostarcza wiele podstawowych algorytmów dla
algebry liniowej. Jest szybka i dobrze przetestowana, zosta³a napisana
w Fortranie 77.

Ostrze¿enie: to jest implementacja przyk³adowa z repozytorium Netlib.
Je¿eli to mo¿liwe, nale¿y u¿ywaæ zamiast niej wersji zoptymalizowanej
pod dan± architekturê.

%package -n blas-devel
Summary:	BLAS header files
Summary(pl):	Pliki nag³ówkowe BLAS
Group:		Development/Libraries
Requires:	blas = %{version}
Obsoletes:	blas-man

%description -n blas-devel
BLAS header files.

%description -n blas-devel -l pl
Pliki nag³ówkowe BLAS.

%package -n blas-static
Summary:	Static BLAS libraries
Summary(pl):	Biblioteki statyczne BLAS
Group:		Development/Libraries
Requires:	blas-devel = %{version}

%description -n blas-static
Static BLAS libraries.

%description -n blas-static -l pl
Biblioteki statyczne BLAS.

%prep
%setup -q -n ATLAS

%build
# make config CC=xlc_r
cat > config.expect <<EOF
log_file "config.expect.log"
set finished 0
set arch foo
spawn ./xconfig
while {\$finished == 0} {
  set timeout 120
  expect {
    -nocase {Enter number at top left of screen}  {send "99\n"}
    -nocase {Have you scoped the errata file\?}   {send "y\n"}
    -nocase {Are you ready to continue\?}         {send "y\n"}
    -nocase {Enter machine number \[2\]: }        {send "1\n"}
    -nocase {Are you using a cross-compiler\?}    {send "n\n"}
    -nocase {enable Posix threads support\?}      {send "y\n"}
    -nocase {use express setup\?}                 {send "y\n"}
    -nocase -indices -re {Enter Architecture name \(ARCH\) \[(.*)\]}
     {global arch; set arch Linux_PPCGP; send "Linux_PPCGP\n"}
    -nocase {overwrite it\?}                      {send "y\n"}
    -nocase {Enter File creation delay in seconds}
                                                  {send "0\n"}
    -nocase {Enter Top level ATLAS directory}     {send "\n"}
    -nocase {Enter Directory to build libraries in}     {send "\n"}
    -nocase {Enter f77 compiler}                  {send "\n"}
    -nocase {Enter F77 Flags}                     {send "\n"}
    -nocase {Enter F77 linker}                    {send "\n"}
    -nocase {Enter F77 Link Flags}                {send "\n"}
    -nocase {Enter ANSI C compiler}               {send "\n"}
    -nocase {Enter C Flags \(CCFLAGS\)}           {send "\n"}
    -nocase {Enter C compiler for generated code} {send "\n"}
    -nocase {Enter C FLAGS \(MMFLAGS\)}           {send "\n"}
    -nocase {Enter C Linker}                      {send "\n"}
    -nocase {Enter C Link Flags}                  {send "\n"}
    -nocase {Enter Archiver \[}                   {send "\n"}
    -nocase {Enter Archiver flags}                {send "\n"}
    -nocase {Enter Ranlib}                        {send "\n"}
    -nocase {Enter BLAS library}                  {send "\n"}
    -nocase {Enter General and system libs}       {send "\n"}
    -nocase {kill old subdirectories\?}           {send "y\n"}
    -nocase {Tune the Level 1 BLAS\?}             {send "\n"}
    -nocase {use supplied default values for install\?}
                                                  {send "y\n"}
    -nocase {Configuration completed successfully} {set finished 1}
    timeout                                       {puts timeout; exit 1}
  }
}
close
#file copy -force CONFIG/ATLrun.\$arch CONFIG/ATLrun.Linux
#file copy -force Make.\$arch Make.Linux
exit
EOF
  make xconfig
  expect -f config.expect
  rm -f config.expect

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

# present both in blas and lapack
rm -f man/manl/{lsame,xerbla}.l

install -d $RPM_BUILD_ROOT%{_mandir}/man3
for d in man/manl/*.l blas/man/manl/*.l ; do
	install $d $RPM_BUILD_ROOT%{_mandir}/man3/`basename $d .l`.3
done

echo "%defattr(644, root, root, 755)" > blasmans.list
find blas/man/manl -name "*.l" -printf "%{_mandir}/man3/%%f\n" | sed 's/\.l/.3*/' >> blasmans.list
echo "%defattr(644, root, root, 755)" > mans.list
find man/manl -name "*.l" -printf "%{_mandir}/man3/%%f\n" | sed 's/\.l/.3*/' >> mans.list

%clean
rm -fr $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post   -n blas -p /sbin/ldconfig
%postun -n blas -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/liblapack.so.*.*.*

%files devel -f mans.list
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblapack.so
%{_libdir}/liblapack.la

%files static
%defattr(644,root,root,755)
%{_libdir}/liblapack.a

%files -n blas
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblas.so.*.*.*

%files -n blas-devel -f blasmans.list
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblas.so
%{_libdir}/libblas.la

%files -n blas-static
%defattr(644,root,root,755)
%{_libdir}/libblas.a
