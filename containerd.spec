%define gobuild(o:) \
CGO_CPPFLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-all" go build -compiler gc -buildmode pie -tags="rpm_crashtraceback libtrust_openssl ${BUILDTAGS:-}" -ldflags "-linkmode=external -compressdwarf=false ${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v -x %{?**};\

%global goipath github.com/containerd/containerd
Version: 1.6.28
%global goname containerd

%gometa

%global commit0 ae07eda36dd25f8a1b98dfbf587313b99c0190bb

Name: %{goname}
Release: 1%{?dist}
Summary: An open and reliable container runtime

License: Apache-2.0
URL: %{gourl}
Source0: %{gosource}
Source1: config.toml

Patch0: systemd-service-bin-path.patch

BuildRequires: systemd-rpm-macros
Requires: runc

%description
%{summary}

%prep
%goprep -k
%autopatch -p1

%build
export BUILDTAGS="no_btrfs"
export LDFLAGS="-X %{goipath}/version.Version=v%{version} \
-X %{goipath}/version.Revision=%{commit0} \
-X %{goipath}/version.Package=%{goipath} "

for cmd in cmd/{%{goname}{,-shim-runc-v2},ctr}; do
    %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
install -v -p -D -t %{buildroot}%{_bindir} %{gobuilddir}/bin/*
install -v -p -m 644 -D -t %{buildroot}%{_unitdir} %{goname}.service
install -v -m 750 -d %{buildroot}%{_sysconfdir}/%{goname}
install -v -m 640 -t %{buildroot}%{_sysconfdir}/%{goname} %{SOURCE1}

%post
%systemd_post %{goname}.service

%preun
%systemd_preun %{goname}.service

%postun
%systemd_postun_with_restart %{goname}.service

%files
%license LICENSE
%{_bindir}/*
%{_unitdir}/%{goname}.service
%dir %{_sysconfdir}/%{goname}
%config(noreplace) %{_sysconfdir}/%{goname}/config.toml

%changelog
* Mon Feb 05 2024 Karel Van Hecke <copr@karelvanhecke.com> - 1.6.28-1
- Bump containerd version to v1.6.28
* Tue Nov 07 2023 Karel Van Hecke <copr@karelvanhecke.com> - 1.6.24-1
- Bump containerd version to v1.6.24
* Tue Feb 21 2023 Karel Van Hecke <copr@karelvanhecke.com> - 1.6.18-1
- Initial build
