%global _commit 48dbe04196ab8bf416d62626d66818507db1f40c

Name: kernel
ExclusiveArch: aarch64
Version: 6.15.11
Release: 1.Strawberry.ThinLTO
Summary: AIO package for linux kernel, modules and headers for Xiaomi Pad 6 (pipa).
URL: https://github.com/rmux-random-stuff-which-doesnt-work/linux
Source1: %{url}/archive/%{_commit}/linux-%{_commit}.tar.gz
Source2: https://raw.githubusercontent.com/pocketblue/packages/main/sm8250/kernel/pipa.config
License: GPL

Provides: kernel = %{version}-%{release}
Provides: kernel-core = %{version}-%{release}
Provides: kernel-modules = %{version}-%{release}

BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: zstd
BuildRequires: clang, lld, llvm
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: glibc-static
BuildRequires: rsync
BuildRequires: openssl-devel
BuildRequires: bison, flex

Requires: dracut >= 027
Requires: bash
Requires: coreutils
Requires: systemd

%description
Mainline kernel for Xiaomi Pad 6 (pipa) — Clang + ThinLTO + BORE.

%prep
tar -xzf %{SOURCE1}
cd linux-%{_commit}
cp %{SOURCE2} .config
make ARCH=arm64 LLVM=1 LLVM_IAS=1 olddefconfig
# enable ThinLTO
scripts/config --disable LTO_NONE
scripts/config --enable LTO_CLANG_THIN
scripts/config --disable GCC_PLUGINS
make ARCH=arm64 LLVM=1 LLVM_IAS=1 olddefconfig

%build
cd linux-%{_commit}
make ARCH=arm64 LLVM=1 LLVM_IAS=1 \
    EXTRAVERSION="-%{release}" \
    -j`nproc`

%install
cd linux-%{_commit}
kernel_version=$(make ARCH=arm64 LLVM=1 LLVM_IAS=1 EXTRAVERSION="-%{release}" kernelrelease)

mkdir -p %{buildroot}/boot/
cp arch/arm64/boot/Image.gz %{buildroot}/boot/vmlinuz-$kernel_version
cp System.map %{buildroot}/boot/System.map-$kernel_version
cp .config %{buildroot}/boot/config-$kernel_version

make ARCH=arm64 LLVM=1 LLVM_IAS=1 \
    EXTRAVERSION="-%{release}" \
    modules_install INSTALL_MOD_PATH=%{buildroot}/usr

cp arch/arm64/boot/dts/qcom/sm8250-xiaomi-pipa.dtb %{buildroot}/usr/lib/modules/$kernel_version/devicetree
ln -s ./devicetree %{buildroot}/usr/lib/modules/$kernel_version/dtb
cp arch/arm64/boot/Image.gz %{buildroot}/usr/lib/modules/$kernel_version/vmlinuz

make ARCH=arm64 LLVM=1 LLVM_IAS=1 \
    EXTRAVERSION="-%{release}" \
    headers_install INSTALL_HDR_PATH=%{buildroot}/usr

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


%package core
License: GPL
Summary: AIO package for linux kernel, modules and headers for Xiaomi Pad 6 (pipa).
Requires: kernel
%description core
Mainline kernel for Xiaomi Pad 6 (pipa).
%files core

%package modules
License: GPL
Summary: AIO package for linux kernel, modules and headers for Xiaomi Pad 6 (pipa).
Requires: kernel
%description modules
Mainline kernel for Xiaomi Pad 6 (pipa).
%files modules

%package devel
License: GPL
Summary: AIO package for linux kernel, modules and headers for Xiaomi Pad 6 (pipa).
Requires: kernel-headers
%description devel
Mainline kernel header for Xiaomi Pad 6 (pipa).
%files devel

%package headers
License: GPL
Summary: AIO package for linux kernel, modules and headers for Xiaomi Pad 6 (pipa).
Provides: kernel-devel = %{version}-%{release}
%description headers
Mainline kernel headers for Xiaomi Pad 6 (pipa).
%files headers
/usr/include

%package devel-matched
License: GPL
Summary: AIO package for linux kernel, modules and headers for Xiaomi Pad 6 (pipa).
Requires: kernel-devel
Requires: kernel-core
%description devel-matched
Mainline kernel headers for Xiaomi Pad 6 (pipa).
%files devel-matched
