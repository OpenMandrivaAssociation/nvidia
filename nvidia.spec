%global debug_package %{nil}
%global _dracut_conf_d  %{_prefix}/lib/dracut/dracut.conf.d
%global _modprobe_d     %{_prefix}/lib/modprobe.d/
%global kernel_source_dir %{_builddir}/%{name}-%{version}/linux-%{kversion}
%global nvidia_driver_dir %{_builddir}/%{name}-%{version}/NVIDIA-Linux-%{_arch}-%{version}
%global open_dkms_name nvidia-open
%global open_kmod_source %{_builddir}/%{name}-%{version}/NVIDIA-kernel-module-source
%global dkms_name nvidia

%global kmod_o_dir		%{_libdir}/nvidia/%{_arch}/%{version}/

%global kernels desktop server rc-desktop rc-server desktop-gcc server-gcc rc-desktop-gcc rc-server-gcc

Summary:	Binary-only driver for nvidia graphics chips
Name:		nvidia
Version:	545.29.06
Release:	1
ExclusiveArch:	%{x86_64} %{aarch64}
Url:		http://www.nvidia.com/object/unix.html
Source0:	http://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source1:	http://download.nvidia.com/XFree86/Linux-aarch64/%{version}/NVIDIA-Linux-aarch64-%{version}.run
Source2:	modpackage.template
Source3:	https://gitweb.frugalware.org/frugalware-current/raw/master/source/x11-extra/nvidia/xorg-nvidia.conf
Source4:	https://gitweb.frugalware.org/frugalware-current/raw/master/source/x11-extra/nvidia/modprobe-nvidia.conf

Patch0:		nvidia-545-kernel-6.7.patch

Group:		Hardware
License:	distributable

# Just to be on the safe side, it may not be wise
# to load clang-built modules into a gcc-built kernel
BuildRequires:	gcc
%(for i in %{kernels}; do echo BuildRequires: kernel-$i-devel; done)

Requires:	%{name}-kmod = %{version}

# Not really, the %%{name}-kmod = %%{EVRD} requirement is enough.
# But we need to make sure dnf prefers the option most people
# will want over something like dkms
Requires:	%{name}-kmod-desktop = %{version}

Requires:	libglvnd-egl
Requires:	vulkan-loader
Requires:	egl-wayland

Conflicts:	nvidia-production
Conflicts:	nvidia-beta

%description
This is a binary-only driver for nvidia graphics chips.

It is NOT supported.
It may WIPE YOUR HARDDISK, SEND ALL YOUR DATA TO YOUR COMPETITORS,
and worse.
It is developed by a very Anti-Linux company, and source code is not
released so nobody but them can tell what it actually does.

The preferred way to solve the problem is to BOYCOTT NVIDIA!
Alternatively, use the Nouveau driver that comes with the default
installation.

This package should only be used as a last resort.

%ifarch %{x86_64}
%package 32bit
Summary:	Binary-only 32-bit driver for nvidia graphics chips

Requires:	%{name} = %{version}

Provides:   libGLdispatch0
Provides:   libGL1
Provides:   libEGL1
Provides:   libGLESv2_2
Provides:   libOpenGL0

%description 32bit
This is a 32-bit binary-only driver for nvidia graphics chips.

It is NOT supported.
It may WIPE YOUR HARDDISK, SEND ALL YOUR DATA TO YOUR COMPETITORS,
and worse.
It is developed by a very Anti-Linux company, and source code is not
released so nobody but them can tell what it actually does.

The preferred way to solve the problem is to BOYCOTT NVIDIA!
Alternatively, use the Nouveau driver that comes with the default
installation.

This package should only be used as a last resort.
%endif

%package kmod
%define kversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-desktop-devel |sort -V |tail -n1)
%define kdir %(rpm -q --qf '%%{VERSION}-desktop-%%{RELEASE}%%{DISTTAG}\\n' kernel-desktop-devel |sort -V |tail -n1)
Summary:	Kernel modules needed by the binary-only nvidia driver
Provides:	%{name}-kmod = %{EVRD}
Requires:	%{name}-kmod-common = %{version}
Requires:	%{name}-modprobe = %{version}
Requires:	%{name}-persistenced = %{version}
Requires:	kernel = %{kversion}

Conflicts:	kernel > %{kversion}

Group:		Hardware
Provides:	should-restart = system
Requires(post,postun):	sed dracut grub2 kmod
BuildRequires:	kernel-desktop-devel

Obsoletes:	nvidia-current <= %{version}
Obsoletes:	nvidia-kernel-modules-desktop <= %{version}
Obsoletes:	nvidia-kernel-modules-server <= %{version}
Obsoletes:	nvidia-kernel-modules-desktop-clang <= %{version}
Obsoletes:	nvidia-kernel-modules-server-clang <= %{version}
Obsoletes:	nvidia-kernel-modules-desktop-rc <= %{version}
Obsoletes:	nvidia-kernel-modules-server-rc <= %{version}
Obsoletes:	nvidia-kernel-modules-desktop-gcc <= %{version}
Obsoletes:	nvidia-kernel-modules-server-gcc <= %{version}

%description kmod
Kernel modules needed by the binary-only nvidia driver

# =======================================================================================#
# dkms-nvidia - modified from https://github.com/NVIDIA/yum-packaging-dkms-nvidia
# =======================================================================================#

%package dkms-kmod
License:        NVIDIA License
Summary:        NVIDIA display driver kernel module. **This is an unsupported proprietary driver. Use with caution!
URL:            http://www.nvidia.com/object/unix.html

# Package is not noarch as it contains pre-compiled binary code
ExclusiveArch:  %{x86_64} ppc64le %{aarch64}
Source5:   dkms-%{dkms_name}.conf

BuildRequires:  sed

Provides:       %{name}-kmod = %{version}
Requires:       %{name}-kmod-common = %{version}
Requires:       %{name}-kmod-headers = %{version}
Requires:		%{name}-modprobe = %{version}
Requires:		%{name}-persistenced = %{version}
Requires:       dkms

Obsoletes:	nvidia-kernel-modules-desktop <= %{version}
Obsoletes:	nvidia-kernel-modules-server <= %{version}
Obsoletes:	nvidia-kernel-modules-desktop-clang <= %{version}
Obsoletes:	nvidia-kernel-modules-server-clang <= %{version}
Obsoletes:	nvidia-kernel-modules-desktop-rc <= %{version}
Obsoletes:	nvidia-kernel-modules-server-rc <= %{version}
Obsoletes:	nvidia-kernel-modules-desktop-gcc <= %{version}
Obsoletes:	nvidia-kernel-modules-server-gcc <= %{version}

%description dkms-kmod
This package provides the proprietary Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

# =======================================================================================#
# dkms-open-nvidia - modified from https://github.com/NVIDIA/yum-packaging-dkms-nvidia
# =======================================================================================#
ttp://www.nvidia.com/object/unix.html
%package kmod-%{open_dkms_name}-dkms

Summary:        NVIDIA driver open kernel module flavor
License: 			NVIDIA and GPL-2
BuildRequires:  sed

Conflicts:      kmod-nvidia-latest-dkms
Provides:       %{name}-kmod = %{version}
Requires:       %{name}-kmod-common = %{version}
Requires:		%{name}-modprobe = %{version}
Requires:		%{name}-persistenced = %{version}
Requires:       dkms

%description kmod-%{open_dkms_name}-dkms
This package provides the open-source Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

%package -n nvidia-kmod-source
Summary:        NVIDIA open kernel module source files
AutoReq:        0
Conflicts:      kmod-nvidia-latest-dkms

%description -n nvidia-kmod-source
NVIDIA kernel module source files for compiling open flavor of nvidia.o and nvidia-modeset.o kernel modules.

%package kmod-headers
Summary:        NVIDIA header files for precompiled streams
AutoReq:        0
Conflicts:      kmod-nvidia-latest-dkms

%description kmod-headers
NVIDIA header files for precompiled streams

# =======================================================================================#
# nvidia-kmod-common - modified from https://github.com/NVIDIA/yum-packaging-nvidia-kmod-common
# =======================================================================================#

%package kmod-common
Summary:        Common file for NVIDIA's proprietary driver kernel modules
License:        NVIDIA Licensefile:///home/nreist/Development/Source/Repos/nvidia-legacy/nvidia-legacy.spec
URL:            http://www.nvidia.com/object/unix.html

BuildArch:      noarch
Source6:	60-nvidia.rules
Source7:	99-nvidia.conf

BuildRequires:  systemd-rpm-macros

Requires:       %{name}-kmod = %{version}
Provides:       %{name}-kmod-common = %{version}
Requires:       %{name} = %{version}
Obsoletes:      cuda-nvidia-kmod-common <= %{version}

%description kmod-common
This package provides the common files required by all NVIDIA kernel module
package variants.

# =======================================================================================#
# nvidia-persistenced - modified from https://github.com/NVIDIA/yum-packaging-nvidia-persistenced
# =======================================================================================#

%package persistenced
Summary:        A daemon to maintain persistent software state in the NVIDIA driver
License:        GPLv2+
URL:            https://github.com/NVIDIA/nvidia-persistenced
ExclusiveArch:  %{ix86} x86_64 ppc64le aarch64
Source8:		https://github.com/NVIDIA/nvidia-persistenced/archive/refs/tags/%{version}.tar.gz
Source9:		nvidia-persistenced.service
Source10:		nvidia-persistenced.conf

BuildRequires:	llvm
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	m4
BuildRequires:	systemd

# Requires cuda, but the kmod-common "builds" that
Requires:		%{name}-kmod-common = %{version}

%description persistenced
The nvidia-persistenced utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.

# =======================================================================================#
# nvidia-modprobe - modified from https://github.com/NVIDIA/yum-packaging-nvidia-modprobe
# =======================================================================================#

%package modprobe
Summary:        NVIDIA kernel module loader
License:        GPLv2+
URL:			https://github.com/NVIDIA/nvidia-modprobe
ExclusiveArch:  %{ix86} x86_64 ppc64le aarch64
Source11:		https://github.com/NVIDIA/nvidia-modprobe/archive/refs/tags/%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	m4
Requires:		%{name}-kmod == %{version}

%description modprobe
This utility is used by user-space NVIDIA driver components to make sure the
NVIDIA kernel modules are loaded and that the NVIDIA character device files are
present.

%prep
%setup -T -c

%ifarch %{x86_64}
sh %{S:0} --extract-only
%else
%ifarch %{aarch64}
sh %{S:1} --extract-only
%endif
%endif
cd %{nvidia_driver_dir}
%autopatch -p1

# nvidia-settings
# Install desktop file
sed -i 's:__PIXMAP_PATH__:%{_datadir}/pixmaps:g' %{nvidia_driver_dir}/nvidia-settings.desktop
sed -i 's:__UTILS_PATH__:%{_bindir}:g' %{nvidia_driver_dir}/nvidia-settings.desktop
mkdir -p %{buildroot}%{_datadir}/{applications,pixmaps}
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ %{nvidia_driver_dir}/nvidia-settings.desktop
cp %{nvidia_driver_dir}/nvidia-settings.png %{buildroot}%{_datadir}/pixmaps/

# dkms kmod - closed and open
cp -f %{S:5} %{nvidia_driver_dir}/kernel/dkms.conf
cp -f %{S:5} %{nvidia_driver_dir}/kernel-open/dkms.conf
sed -i -e 's/__VERSION_STRING/%{version}/g' %{nvidia_driver_dir}/kernel/dkms.conf
sed -i -e 's/__VERSION_STRING/%{version}/g' %{nvidia_driver_dir}/kernel-open/dkms.conf
cp -r %{nvidia_driver_dir}/kernel-open %{open_kmod_source}

# persistenced
tar -xf %{S:8} -C %{_builddir}/%{name}-%{version}
cd %{_builddir}/%{name}-%{version}/nvidia-persistenced-%{version}
# Remove additional CFLAGS added when enabling DEBUG
sed -i -e '/+= -O0 -g/d' utils.mk

# modprobe
tar -xf %{S:11} -C %{_builddir}/%{name}-%{version}
# Remove additional CFLAGS added when enabling DEBUG
sed -i '/+= -O0 -g/d' utils.mk

%build

# The IGNORE_CC_MISMATCH flags below are needed because for some
# reason, the kernel appends the LLD version to clang kernels while
# nvidia does not.

# kmod
for i in %{kernels}; do
	K=$(echo $i |sed -e 's,-,_,g')
	KD=$(rpm -q --qf "%%{VERSION}-$i-%%{RELEASE}%%{DISTTAG}\n" kernel-${i}-devel |tail -n1)
	if echo $i |grep -q rc; then
		KD=$(echo $KD |sed -e 's,-rc,,')
	fi
	# The IGNORE_CC_MISMATCH flags below are needed because for some
	# reason, the kernel appends the LLD version to clang kernels while
	# nvidia does not.

	# kmod
	cd %{nvidia_driver_dir}/kernel

	cp -r /usr/src/linux-$KD %{kernel_source_dir}-$i
	# A proper kernel module build uses /lib/modules/KVER/{source,build} respectively,
	# but that creates a dependency on the 'kernel' package since those directories are
	# not provided by kernel-devel. Both /source and /build in the mentioned directory
	# just link to the sources directory in /usr/src however, which ddiskit defines
	# as kmod_kernel_source.
	KERNEL_SOURCES=%{kernel_source_dir}-$i
	KERNEL_OUTPUT=%{kernel_source_dir}-$i

	# These could affect the linking so we unset them both there and in %%post
	unset LD_RUN_PATH
	unset LD_LIBRARY_PATH

	#
	# Compile kernel modules
	#
	if echo $i |grep -q gcc; then
		%{make_build} SYSSRC=${KERNEL_SOURCES} SYSOUT=${KERNEL_OUTPUT} CC=gcc CXX=g++
	else
		%{make_build} SYSSRC=${KERNEL_SOURCES} SYSOUT=${KERNEL_OUTPUT} IGNORE_CC_MISMATCH=1
	fi

	mkdir -p %{_builddir}/%{name}-%{version}/modules-$i
	mv *.ko %{_builddir}/%{name}-%{version}/modules-$i

	cd %{nvidia_driver_dir}/kernel-open
	cp -r /usr/src/linux-$KD %{kernel_source_dir}-$i
	# A proper kernel module build uses /lib/modules/KVER/{source,build} respectively,
	# but that creates a dependency on the 'kernel' package since those directories are
	# not provided by kernel-devel. Both /source and /build in the mentioned directory
	# just link to the sources directory in /usr/src however, which ddiskit defines
	# as kmod_kernel_source.
	KERNEL_SOURCES=%{kernel_source_dir}-$i
	KERNEL_OUTPUT=%{kernel_source_dir}-$i

	# These could affect the linking so we unset them both there and in %%post
	unset LD_RUN_PATH
	unset LD_LIBRARY_PATH

	#
	# Compile kernel modules
	#
	if echo $i |grep -q gcc; then
		%{make_build} SYSSRC=${KERNEL_SOURCES} SYSOUT=${KERNEL_OUTPUT} CC=gcc CXX=g++
	else
		%{make_build} SYSSRC=${KERNEL_SOURCES} SYSOUT=${KERNEL_OUTPUT} IGNORE_CC_MISMATCH=1
	fi

	mkdir -p %{_builddir}/%{name}-%{version}/modules-open-$i
	mv *.ko %{_builddir}/%{name}-%{version}/modules-open-$i
done

# persistenced
cd %{_builddir}/%{name}-%{version}/nvidia-persistenced-%{version}
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
export LDFLAGS="%{?__global_ldflags} -ltirpc"
%make DEBUG=1 \
		LIBS="-ldl -ltirpc" \
		NV_VERBOSE=1 \
		PREFIX=%{_prefix} \
		STRIP_CMD=true

# modprobe
cd %{_builddir}/%{name}-%{version}/nvidia-modprobe-%{version}
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
export LDFLAGS="%{?__global_ldflags} -ltirpc"
%make DEBUG=1 \
		LIBS="-ldl -ltirpc" \
		NV_VERBOSE=1 \
		PREFIX=%{_prefix} \
		STRIP_CMD=true

%install
# dkms kmod open
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{open_dkms_name}-%{version}/src
rm -rf \
	%{nvidia_driver_dir}/kernel-open/conftest \
	%{nvidia_driver_dir}/kernel-open/conftest*.c \
	%{nvidia_driver_dir}/kernel-open/modules.order \
	%{nvidia_driver_dir}/kernel-open/nv_compiler.h \
	%{nvidia_driver_dir}/kernel-open/Module.symvers
cp -fr %{nvidia_driver_dir}/kernel-open/* %{buildroot}%{_usrsrc}/%{open_dkms_name}-%{version}/

# Add symlink
cd %{buildroot}%{_usrsrc}/%{open_dkms_name}-%{version}/src/ &&
ln -sf ../../%{open_dkms_name}-%{version}/ kernel-open &&
cd - >/dev/null
cd %{nvidia_driver_dir}
# end dkms kmod open

inst() {
	install -m 644 -D $(basename $1) %{buildroot}"$1"
	if [ -e "32/$(basename $1)" ]; then
		install -m 644 -D "32/$(basename $1)" %{buildroot}$(echo $1 |sed -e 's,%_lib,lib,')
	fi
}
instx() {
	install -m 755 -D $(basename $1) %{buildroot}"$1"
	if [ -e "32/$(basename $1)" ]; then
		install -m 755 -D "32/$(basename $1)" %{buildroot}$(echo $1 |sed -e 's,%_lib,lib,')
	fi
}
sl() {
	if [ -n "$2" ]; then ln -s lib$1.so.%{version} %{buildroot}%{_libdir}/lib$1.so.$2; fi
	if [ -z "$3" ]; then ln -s lib$1.so.%{version} %{buildroot}%{_libdir}/lib$1.so; fi
%ifarch %{x86_64}
	if [ -e %{buildroot}%{_prefix}/lib/lib$1.so.%{version} ]; then
		if [ -n "$2" ]; then ln -s lib$1.so.%{version} %{buildroot}%{_prefix}/lib/lib$1.so.$2; fi
		if [ -z "$3" ]; then ln -s lib$1.so.%{version} %{buildroot}%{_prefix}/lib/lib$1.so; fi
	fi
%endif
}

# X driver
instx %{_libdir}/xorg/modules/drivers/nvidia_drv.so
inst %{_datadir}/vulkan/icd.d/nvidia_icd.json

# OpenGL core library
instx %{_libdir}/libnvidia-glcore.so.%{version}
sl nvidia-glcore
inst %{_datadir}/glvnd/egl_vendor.d/10_nvidia.json

# GLX extension module for X
instx %{_libdir}/xorg/modules/nvidia/extensions/libglxserver_nvidia.so.%{version}
ln -s libglxserver_nvidia.so.%{version} %{buildroot}%{_libdir}/xorg/modules/nvidia/extensions/libglxserver_nvidia.so
instx %{_libdir}/libGLX_nvidia.so.%{version}
sl GLX_nvidia 0 n
# libglvnd indirect entry point
ln -sf libGLX_nvidia.so.%{version} %{buildroot}%{_libdir}/libGLX_indirect.so.0

# EGL
instx %{_libdir}/libEGL_nvidia.so.%{version}
sl EGL_nvidia 0
instx %{_libdir}/libnvidia-eglcore.so.%{version}
sl nvidia-eglcore

# OpenGL ES
instx %{_libdir}/libGLESv1_CM_nvidia.so.%{version}
sl GLESv1_CM_nvidia 1
instx %{_libdir}/libGLESv2_nvidia.so.%{version}
sl GLESv2_nvidia.so 2

# GLSI
instx %{_libdir}/libnvidia-glsi.so.%{version}
sl nvidia-glsi

# CUDA
instx %{_libdir}/libcuda.so.%{version}
sl cuda 1
instx %{_libdir}/libcudadebugger.so.%{version}
instx %{_libdir}/libnvcuvid.so.%{version}
sl nvcuvid 1
instx %{_libdir}/libnvidia-ml.so.%{version}
sl nvidia-ml 1
# CUDA?
instx %{_libdir}/libnvidia-ptxjitcompiler.so.%{version}
sl nvidia-ptxjitcompiler 1
instx %{_libdir}/libnvidia-gpucomp.so.%{version}

# nvidia-tls library
instx %{_libdir}/libnvidia-tls.so.%{version}
sl nvidia-tls

# OpenCL
inst %{_sysconfdir}/OpenCL/vendors/nvidia.icd
instx %{_libdir}/libnvidia-cfg.so.%{version}
sl nvidia-cfg 1
instx %{_libdir}/libnvidia-opencl.so.%{version}

# Encode (what is this?)
instx %{_libdir}/libnvidia-encode.so.%{version}
sl nvidia-encode 1

# Fbc (Framebuffer console?)
instx %{_libdir}/libnvidia-fbc.so.%{version}
sl nvidia-fbc 1

# Assorted libraries
instx %{_libdir}/libnvidia-allocator.so.%{version}
instx %{_libdir}/libnvidia-api.so.1
instx %{_libdir}/libnvidia-ngx.so.%{version}
instx %{_libdir}/libnvidia-nvvm.so.%{version}
sl nvidia-nvvm 4
instx %{_libdir}/libnvidia-opticalflow.so.%{version}
instx %{_libdir}/libnvidia-pkcs11.so.%{version}
instx %{_libdir}/libnvidia-pkcs11-openssl3.so.%{version}
instx %{_libdir}/libnvidia-rtcore.so.%{version}
instx %{_libdir}/libnvidia-wayland-client.so.%{version}
instx %{_libdir}/libnvoptix.so.%{version}

# Firmware
mkdir -p %{buildroot}%{_prefix}/lib
cp -a firmware %{buildroot}%{_prefix}/lib

# Yuck...
instx %{_libdir}/libnvidia-gtk2.so.%{version}

%ifarch %{x86_64}
instx %{_libdir}/libnvidia-gtk3.so.%{version}
%endif

# VDPAU
instx %{_libdir}/vdpau/libvdpau_nvidia.so.%{version}
ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau/libvdpau_nvidia.so.1.0
ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau/libvdpau_nvidia.so.1
ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau/libvdpau_nvidia.so

# Tools
for i in *.1.gz; do
	gunzip $i
done
instx %{_bindir}/nvidia-bug-report.sh
instx %{_bindir}/nvidia-smi
inst %{_mandir}/man1/nvidia-smi.1
instx %{_bindir}/nvidia-settings
inst %{_mandir}/man1/nvidia-settings.1
inst %{_datadir}/applications/nvidia-settings.desktop
inst %{_datadir}/pixmaps/nvidia-settings.png

# glvk
instx %{_libdir}/libnvidia-glvkspirv.so.%{version}

# Assorted stuff
inst %{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc
inst %{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation

# Configs
mkdir -p %{buildroot}%{_datadir}/X11/xorg.conf.d/
sed -e 's,@LIBDIR@,%{_libdir},g' %{S:3} >%{buildroot}%{_datadir}/X11/xorg.conf.d/20-nvidia.conf

# license and doc files
mkdir -p %{buildroot}%{_docdir}/%{name}
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}
cp %{nvidia_driver_dir}/LICENSE %{buildroot}%{_datadir}/licenses/%{name}
cp %{nvidia_driver_dir}/NVIDIA_Changelog %{buildroot}%{_docdir}/%{name}
cp %{nvidia_driver_dir}/README.txt %{buildroot}%{_docdir}/%{name}
cp -r %{nvidia_driver_dir}/html %{buildroot}%{_docdir}/%{name}

# Kernel modules
for i in %{kernels}; do
	KD=$(rpm -q --qf "%%{VERSION}-$i-%%{RELEASE}%%{DISTTAG}\n" kernel-${i}-devel |sort -V |tail -n1)
	if echo $i |grep -q rc; then
		KD=$(echo $KD |sed -e 's,rc-,,g')
	fi
	mkdir -p %{buildroot}/lib/modules/$KD/kernel/drivers/video/nvidia %{buildroot}/lib/modules/$KD/kernel/drivers/video/nvidia-open
	mv ../modules-$i/*.ko %{buildroot}/lib/modules/$KD/kernel/drivers/video/nvidia/
	mv ../modules-open-$i/*.ko %{buildroot}/lib/modules/$KD/kernel/drivers/video/nvidia-open/

	# And create the package...
	K=$(echo $i |sed -e 's,-,_,g')
	KV=$(rpm -q --qf "%%{VERSION}-%%{RELEASE}\n" kernel-${i}-devel |sort -V |tail -n1 |sed -e 's,-rc,,')

	sed -e "s,@TYPE@,$i,g;s,@KV@,$KV,g;s,@KD@,$KD,g;s,@REL@,%{release}_$(echo $KV |sed -e 's,-,_,g'),g" %{S:2} >%{specpartsdir}/$i.specpart
done

# dkms-kmod
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr %{nvidia_driver_dir}/kernel/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_modprobe_d}/
mkdir -p %{buildroot}%{_dracut_conf_d}/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_presetdir}

# Blacklist nouveau and load nvidia-uvm:
install -p -m 0644 %{S:4} %{buildroot}%{_modprobe_d}/

# Avoid Nvidia modules getting in the initrd:
install -p -m 0644 %{S:7} %{buildroot}%{_dracut_conf_d}/

# UDev rules:
# https://github.com/NVIDIA/nvidia-modprobe/blob/master/modprobe-utils/nvidia-modprobe-utils.h#L33-L46
# https://github.com/negativo17/nvidia-driver/issues/27
install -p -m 644 %{S:6} %{buildroot}%{_udevrulesdir}

# persistenced
cd %{_builddir}/%{name}-%{version}/nvidia-persistenced-%{version}
%make_install \
	NV_VERBOSE=1 \
	PREFIX=%{_prefix} \
	STRIP_CMD=true
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}-persistenced/
cp COPYING %{buildroot}%{_datadir}/licenses/%{name}-persistenced/COPYING

mkdir -p %{buildroot}%{_sharedstatedir}/nvidia-persistenced
# Systemd unit files
install -p -m 644 -D %{SOURCE8} %{buildroot}%{_unitdir}/nvidia-persistenced.service
install -p -m 644 -D %{SOURCE10} %{buildroot}%{_prefix}/lib/sysusers.d/nvidia-persistenced.conf

# modprobe
cd %{_builddir}/%{name}-%{version}/nvidia-modprobe-%{version}
%make_install \
	NV_VERBOSE=1 \
	PREFIX=%{_prefix} \
	STRIP_CMD=true

mkdir -p %{buildroot}%{_datadir}/licenses/%{name}-modprobe
cp COPYING %{buildroot}%{_datadir}/licenses/%{name}-modprobe/COPYING

%post kmod-common
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="nouveau.modeset=0 nvidia-drm.modeset=1 nvidia-drm.fbdev=1 /' %{_sysconfdir}/default/grub
/sbin/depmod -a
/usr/bin/dracut -f
%{_sbindir}/update-grub2

%postun kmod-common
sed -i 's/nouveau.modeset=0 nvidia-drm.modeset=1 nvidia-drm.fbdev=1 //g' %{_sysconfdir}/default/grub
/sbin/depmod -a
/usr/bin/dracut -f
%{_sbindir}/update-grub2

%files kmod-common
%{_sysconfdir}/dracut.conf.d/99-nvidia.conf
%{_udevrulesdir}/60-nvidia.rules
%{_prefix}/lib/firmware/*

%post dkms-kmod
dkms add -m %{dkms_name}-v %{version} || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} || :
dkms install -m %{dkms_name} -v %{version} --force || :

%preun dkms-kmod
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} --all || :

%post kmod-%{open_dkms_name}-dkms
dkms add -m %{open_dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{open_dkms_name} -v %{version} -q || :
dkms install -m %{open_dkms_name} -v %{version} -q --force || :

%preun kmod-%{open_dkms_name}-dkms
# Remove all versions from DKMS registry
dkms remove -m %{open_dkms_name} -v %{version} -q --all || :

%files
%{_datadir}/licenses/%{name}/LICENSE
%{_docdir}/%{name}/NVIDIA_Changelog
%{_docdir}/%{name}/README.txt
%{_docdir}/%{name}/html
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_datadir}/vulkan/icd.d/nvidia_icd.json
%{_libdir}/libnvidia-glcore.so*
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%{_libdir}/xorg/modules/nvidia/extensions/libglxserver_nvidia.so*
%{_libdir}/libGLX_nvidia.so*
%{_libdir}/libEGL_nvidia.so*
%{_libdir}/libnvidia-eglcore.so*
%{_libdir}/libGLESv1_CM_nvidia.so*
%{_libdir}/libGLESv2_nvidia.so*
%{_libdir}/libnvidia-glsi.so*
%{_libdir}/libGLX_indirect.so.0
%{_libdir}/libnvidia-allocator.so*
%{_libdir}/libnvidia-api.so*
%{_libdir}/libnvidia-ngx.so*
%{_libdir}/libnvidia-nvvm.so*
%{_libdir}/libnvidia-opticalflow.so*
%{_libdir}/libnvidia-pkcs11-openssl3.so*
%{_libdir}/libnvidia-pkcs11.so*
%{_libdir}/libnvidia-rtcore.so*
%{_libdir}/libnvidia-wayland-client.so*
%{_libdir}/libnvoptix.so*
%{_libdir}/libcuda.so*
%{_libdir}/libcudadebugger.so*
%{_libdir}/libnvcuvid.so*
%{_libdir}/libnvidia-ml.so*
%{_libdir}/libnvidia-ptxjitcompiler.so*
%{_libdir}/libnvidia-tls.so*
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%{_libdir}/libnvidia-cfg.so*
%{_libdir}/libnvidia-opencl.so*
%{_libdir}/libnvidia-encode.so*
%{_libdir}/libnvidia-gpucomp.so*
%{_libdir}/libnvidia-fbc.so*
%{_libdir}/libnvidia-gtk2.so*
%ifarch %{x86_64}
%{_libdir}/libnvidia-gtk3.so*
%endif
%{_libdir}/vdpau/libvdpau_nvidia.so*
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-smi
%{_mandir}/man1/nvidia-smi.1*
%{_bindir}/nvidia-settings
%{_mandir}/man1/nvidia-settings.1*
%{_datadir}/applications/nvidia-settings.desktop
%{_datadir}/pixmaps/nvidia-settings.png
%{_libdir}/libnvidia-glvkspirv.so*
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation
%{_datadir}/X11/xorg.conf.d/20-nvidia.conf

%ifarch %{x86_64}
%files 32bit
%{_prefix}/lib/libnvidia-glcore.so*
%{_prefix}/lib/libGLX_nvidia.so*
%{_prefix}/lib/libEGL_nvidia.so*
%{_prefix}/lib/libnvidia-eglcore.so*
%{_prefix}/lib/libGLESv1_CM_nvidia.so*
%{_prefix}/lib/libGLESv2_nvidia.so*
%{_prefix}/lib/libnvidia-glsi.so*
%{_prefix}/lib/libcuda.so*
%{_prefix}/lib/libnvcuvid.so*
%{_prefix}/lib/libnvidia-ml.so*
%{_prefix}/lib/libnvidia-ptxjitcompiler.so*
%{_prefix}/lib/libnvidia-tls.so*
%{_prefix}/lib/libnvidia-gpucomp.so*
%{_prefix}/lib/libnvidia-opencl.so*
%{_prefix}/lib/libnvidia-encode.so*
%{_prefix}/lib/libnvidia-fbc.so*
%{_prefix}/lib/vdpau/libvdpau_nvidia.so*
%{_prefix}/lib/libnvidia-glvkspirv.so*
%{_prefix}/lib/libnvidia-allocator.so*
%{_prefix}/lib/libnvidia-nvvm.so*
%{_prefix}/lib/libnvidia-opticalflow.so*
%endif

%files dkms-kmod
%{_usrsrc}/%{dkms_name}-%{version}

%files kmod-%{open_dkms_name}-dkms
%{_usrsrc}/%{open_dkms_name}-%{version}/common
%{_usrsrc}/%{open_dkms_name}-%{version}/nvidia*
%{_usrsrc}/%{open_dkms_name}-%{version}/Kbuild
%{_usrsrc}/%{open_dkms_name}-%{version}/Makefile
%{_usrsrc}/%{open_dkms_name}-%{version}/conftest.sh
%{_usrsrc}/%{open_dkms_name}-%{version}/dkms.conf
%{_usrsrc}/%{open_dkms_name}-%{version}/*.mk

%files -n nvidia-kmod-source
%{_usrsrc}/%{open_dkms_name}-%{version}/src

%files kmod-headers
%{_usrsrc}/%{dkms_name}-%{version}

%files persistenced
%license COPYING
%{_mandir}/man1/nvidia-persistenced.1.*
%{_bindir}/nvidia-persistenced
%{_unitdir}/nvidia-persistenced.service
%attr(750,nvidia-persistenced,nvidia-persistenced) %{_sharedstatedir}/nvidia-persistenced
%{_prefix}/lib/sysusers.d/nvidia-persistenced.conf

%files modprobe
%license COPYING
%attr(4755, root, root) %{_bindir}/nvidia-modprobe
%{_mandir}/man1/nvidia-modprobe.1.*
