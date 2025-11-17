%global _commit 38a617d78ba5178ebc8c986109abeebd0b8f8da5

Name: kernel
ExclusiveArch: aarch64
Version: 6.15.8
Release: rmux
Summary: AIO package for linux kernel, modules and headers for Xiaomi Pad 6 (pipa).
URL: https://github.com/PipaDB/linux
Source1: %{url}/archive/%{_commit}.tar.gz
Source2: pipa.config
License: GPL

Provides: kernel = %{version}-%{release}
Provides: kernel-core = %{version}-%{release}
Provides: kernel-modules = %{version}-%{release}

BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: zstd
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: rust, rust-src, bindgen, rustfmt, clippy
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: glibc-static
BuildRequires: rsync
BuildRequires: opencsd-devel >= 1.0.0
BuildRequires: openssl-devel

Requires: dracut >= 027
Requires: bash
Requires: coreutils
Requires: systemd

%description
Mainline kernel for Xiaomi Pad 6 (pipa).

%prep
tar -xzf %{SOURCE1}
cd linux-%{_commit}
cp %{SOURCE2} .config
# patch -p1 < %{SOURCE3}  <-- removed

%build
cd linux-%{_commit}
make EXTRAVERSION="-%{release}" -j`nproc`

%install
cd linux-%{_commit}
kernel_version=$(make EXTRAVERSION="-%{release}" kernelrelease)

mkdir -p %{buildroot}/boot/
cp arch/arm64/boot/Image.gz %{buildroot}/boot/vmlinuz-$kernel_version
cp System.map %{buildroot}/boot/System.map-$kernel_version
cp .config %{buildroot}/boot/config-$kernel_version

make EXTRAVERSION="-%{release}" modules_install INSTALL_MOD_PATH=%{buildroot}/usr
cp arch/arm64/boot/dts/qcom/sm8250-xiaomi-pipa.dtb %{buildroot}/usr/lib/modules/$kernel_version/devicetree
ln -s ./devicetree %{buildroot}/usr/lib/modules/$kernel_version/dtb
cp arch/arm64/boot/Image.gz %{buildroot}/usr/lib/modules/$kernel_version/vmlinuz
make EXTRAVERSION="-%{release}" headers_install INSTALL_HDR_PATH=%{buildroot}/usr
rm %{buildroot}/usr/lib/modules/%{version}*/build

%files
/boot/System.map-%{version}*
/boot/config-%{version}*
/boot/vmlinuz-%{version}*
/usr/lib/modules/%{version}*

%posttrans
dracut -f --kver %{version}-%{release} /usr/lib/modules/%{version}-%{release}/initramfs.img
kernel-install add %{version}-%{release} /usr/lib/modules/%{version}-%{release}/vmlinuz /usr/lib/modules/%{version}-%{release}/initramfs.img

%postun
kernel-install remove %{version}-%{release} /usr/lib/modules/%{version}-%{release}/vmlinuz
