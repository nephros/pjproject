# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.32
# 

Name:       pjproject

# >> macros
# << macros

Summary:    A multimedia communication library implementing standard based protocols such as SIP, SDP, RTP, STUN, TURN, and ICE
Version:    2.11.1
Release:    1
Group:      Development/Libraries
License:    GPLv2
URL:        https://github.com/savoirfairelinux/pjproject
Source0:    %{name}-%{version}.tar.gz
Source100:  pjproject.yaml
Patch0:     0009-add-config-site.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libresample)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  opus-devel

%description
%{summary}.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q -n %{name}-%{version}/upstream

# 0009-add-config-site.patch
%patch0 -p1
# >> setup
# << setup

%build
# >> build pre
#rm -f configure
#mv aconfigure.ac configure.ac
#autoreconf
# << build pre

%configure --disable-static \
    --enable-shared \
    --enable-pjsua2 \
    --enable-ssl \
    --enable-opus \
    --enable-libsamplerate \
    --disable-resample \
    --with-external-speex \
    --disable-libwebrtc \
    CFLAGS="$CFLAGS -DNDEBUG=1 -DPJ_HAS_IPV6=1"


# >> build post
make %{?_smp_mflags} dep
make %{?_smp_mflags} lib
# << build post

%install
rm -rf %{buildroot}
# >> install pre
find %{_builddir} -name "*.so.*"
# << install pre

# >> install post
printf "PJ_EXCLUDE_PJSUA2 is '%s'\n" $PJ_EXCLUDE_PJSUA2
%make_install
# somehow that doesn't get installed...
printf "manually installing pjsua2...\n"
%__install -D pjsip/lib/libpjsua2.so.2 %{buildroot}%{_libdir}/libpjsua2.so.2
find %{buildroot} -name "*.so.*"
# << install post

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# >> files
%{_libdir}/*.so.*
# << files

%files devel
%defattr(-,root,root,-)
# >> files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
# << files devel
