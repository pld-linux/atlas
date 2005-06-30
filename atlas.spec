# TODO:
# - missing BR/R?
# - disable altivec/3dnow autodetection - force values from spec
# - fix for other arches
# - deal with -fPIC to get shared libs
Summary:	The atlas libraries for numerical linear algebra
Summary(pl):	Biblioteki numeryczne atlas do algebry liniowej
Name:		atlas
Version:	3.7.10
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
# Source0-md5:	c24aa9f676122fe6331fa63dd88c4113
URL:		http://math-atlas.sourceforge.net/
BuildRequires:	expect
BuildRequires:	gcc-g77
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

%description -l pl
Projekt ATLAS (Automatically Tuned Linear Algebra Software -
automatycznie dostrajane oprogramowanie do algebry liniowej) to próby
badawcze skupiaj±ce siê na stosowaniu technik empirycznych w celu
zapewnienia przeno¶nej wydajno¶ci. Aktualnie dostarczane s± interfejsy
w C i Fortranie 77 do przeno¶nej, wydajnej implementacji BLAS, a tak¿e
kilku procedur LAPACK.

%package devel
Summary:	atlas header files
Summary(pl):	Pliki nag³ówkowe atlas
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
atlas header files.

%description devel -l pl
Pliki nag³ówkowe atlas.

%package static
Summary:	Static atlas libraries
Summary(pl):	Biblioteki statyczne atlas
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static atlas libraries.

%description static -l pl
Biblioteki statyczne atlas.

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
%ifarch %{x8664} sparc64
    -nocase {Enter bit number \[2\]:}	{send "2\n"}
%endif
    -nocase {Enter number at top left of screen}  {send "25\n"}
    -nocase {Have you scoped the errata file\?}   {send "y\n"}
    -nocase {Are you ready to continue\?}         {send "y\n"}
    -nocase {Enter machine number \[2\]: }        {send "1\n"}
    -nocase {Are you using a cross-compiler\?}    {send "n\n"}
    -nocase {enable Posix threads support\?}      {send "y\n"}
    -nocase {use express setup\?}                 {send "y\n"}
    -nocase -indices -re {Enter Architecture name \(ARCH\) \[(.*)\]}
     {global arch; set arch \$expect_out(1,string); send "\$arch\n"}
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
%{__make} xconfig
expect -f config.expect
rm -f config.expect

mksolib() {
	#set -x
	lib=$1
	mode=$2
	v=$3
	so=$4
	rm -f lib$lib.a
	ar ruv lib$lib.a *.o
	if [ -r *.lo ]; then
	  ar ruv lib$lib.a *.lo
	fi
	%{__cc} -shared -Wl,-soname,lib${lib}.so.${so} -Wl,--whole-archive -L. -l${lib} -Wl,--no-whole-archive -o lib${lib}.so.${v}
	ln -s lib${lib}.so.${v} lib${lib}.so.${so}
	ln -s lib${lib}.so.${v} lib${lib}.so
	rm -f *.o *.lo
}

%ifarch %{x8664} sparc64
OBJECT_MODE=64
%else
OBJECT_MODE=32
%endif
export OBJECT_MODE

arch=$(ls -1 Make.Linux* | sed -e 's#^Make\.##g')

%{__make} install \
	CC="%{__cc}" \
	arch=${arch}

install -d lib/${arch}/shared
cd lib/${arch}/shared
libs="atlas cblas f77blas lapack tstatlas"

for lib in `echo ${libs} | xargs`; do
	case "$lib" in
		"lapack")
			lib=atllapack
			;;
		"cblas")
			lib=atlcblas
			;;
	esac
	echo $lib
	ar x ../lib${lib}.a
	mksolib ${lib} ${OBJECT_MODE} 1.1 1
	mv *.so* ..
	mv *.a ..
done
cd ../../..
rm -rf lib/${arch}/shared

%install
rm -rf $RPM_BUILD_ROOT

arch=$(ls -1 Make.Linux* | sed -e 's#^Make\.##g')

install -d $RPM_BUILD_ROOT{%{_includedir}/%{name},%{_libdir}}

libs="atlas cblas f77blas lapack tstatlas"

cd lib/${arch}
for lib in `echo ${libs} | xargs`; do
	install lib${lib}.a $RPM_BUILD_ROOT%{_libdir}
	install lib${lib}.so.1.1 $RPM_BUILD_ROOT%{_libdir}
	ln -s lib${lib}.so.1.1 $RPM_BUILD_ROOT%{_libdir}/lib${lib}.so
done
cd ../..

cp -a include/* $RPM_BUILD_ROOT%{_includedir}/%{name}


%clean
rm -fr $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
