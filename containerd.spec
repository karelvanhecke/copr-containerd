%global goipath github.com/containerd/containerd
Version: 1.6.18
%global goname containerd

%gometa

%global commit0 2456e983eb9e37e47538f59ea18f2043c9a73640

Name: %{goname}
Release: 1%{?dist}
Summary: An open and reliable container runtime

License: Apache-2.0
URL: %{gourl}
Source0: %{gosource}

Patch0: systemd-service-bin-path.patch

BuildRequires: systemd-rpm-macros
Requires: runc

%description
%{Summary}

%prep
%goprep -k
%autopatch -p1

%build
export BUILDTAGS="no_btrfs"
export LDFLAGS="-X %{goipath}/version.Version=%{version} \
-X %{goipath}/version.Revision=%{commit0} \
-X %{goipath}/version.Package=%{goipath} "

for cmd in cmd/{containerd*,ctr}; do
    %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
install -v -D -t %{buildroot}/%{_bindir} %{gobuilddir}/bin/*

%files
%license LICENSE
%{_bindir}/*

%changelog
* Tue Feb 21 2023 Karel Van Hecke <copr@karelvanhecke.com> - 1.6.18-1
- Initial build