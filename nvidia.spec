%define kversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-desktop-devel |sort -V |tail -n1)
%define kdir %(rpm -q --qf '%%{VERSION}-desktop-%%{RELEASE}%%{DISTTAG}\\n' kernel-desktop-devel |sort -V |tail -n1)
%global debug_package %{nil}
%global	_dracut_conf_d	%{_prefix}/lib/dracut/dracut.conf.d
%global	_modprobe_d		%{_prefix}/lib/modprobe.d/
%global	open_dkms_name	nvidia-open
%global	dkms_name	nvidia

%global	kernels desktop server rc-desktop rc-server desktop-gcc server-gcc rc-desktop-gcc rc-server-gcc
# Sometimes RC kernels restrict previously exported symbols to EXPORT_SYMBOL_GPL
# When that happens, the closed kernel modules frequently won't compile anymore,
# but we can still build the open versions
%global rc_openonly 0

Name:		nvidia
Version:	555.58
# Sometimes helpers (persistenced, modprobe) don't change and aren't
# retagged. When possible, helpers_version should be set to %{version}.
%define helpers_version %{version}
# Sometimes they release aarch64 late -- usually should be %{version}
%define aarch64version %{version}
%ifarch %{aarch64}
%define ver %{aarch64version}
%else
%define ver %{version}
%endif
Release:	2
ExclusiveArch:	%{x86_64} %{aarch64}
Summary:	Binary-only driver for NVIDIA graphics chips
Url:		http://www.nvidia.com/object/unix.html
Source0:	http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source1:	https://us.download.nvidia.com/XFree86/aarch64/%{ver}/NVIDIA-Linux-aarch64-%{ver}.run
Source2:	modpackage.template
Source3:	https://gitweb.frugalware.org/frugalware-current/raw/master/source/x11-extra/%{name}/xorg-nvidia.conf

%global	kernel_source_dir	%{_builddir}/%{buildsubdir}-build/%{name}-%{version}/linux-%{kversion}
%global	nvidia_driver_dir	%{_builddir}/%{buildsubdir}-build/%{name}-%{version}/NVIDIA-Linux-%{_arch}-%{ver}
%global	open_kmod_source 	%{_builddir}/%{buildsubdir}-build/%{name}-%{version}/NVIDIA-kernel-module-source
%global	kmod_o_dir		%{_libdir}/nvidia/%{_arch}/%{ver}/

# nvidia

# nvidia-settings
Patch1:		%{name}-settings-desktop.patch

# not currently building a so
#Patch2:		%%{name}-settings-so.patch
#Patch3:		%%{name}-settings-libXNVCtrl.patch

Patch4:		%{name}-settings-lib-permissions.patch
#Patch10:	nvidia-kernel-6.10.patch

Group:		Hardware
License:	distributable

Provides:	%{name} = %{version}

BuildRequires:	sed
BuildRequires:	appstream-util
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(vdpau) >= 1.0
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	m4
BuildRequires:	systemd
BuildRequires:	systemd-rpm-macros
BuildRequires:	desktop-file-utils
BuildRequires:	appstream-util
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(dri)
BuildRequires:	egl-devel
BuildRequires:	pkgconfig(gtk+-2.0) > 2.4
BuildRequires:	pkgconfig(gtk+-3.0)
# Even if we aren't building for the desktop kernel,
# this package is needed to determine %%{kversion}
BuildRequires:	kernel-desktop-devel

Requires:	%{name}-kmod-common = %{version}
Requires:	%{name}-modprobe = %{EVRD}
Suggests:	%{name}-settings = %{EVRD}
%(for i in %{kernels}; do
	echo "Requires:	(%{name}-kmod-$i if kernel-$i)"
done)

%ifarch %{x86_64}
Requires:	%{name}-32bit = %{version}
%endif

Requires:	libglvnd-egl
Requires:	egl-wayland
Requires:	vulkan-loader

%(for i in %{kernels};
	do
		echo BuildRequires: kernel-$i-devel

		# Because this service is primarily for non-X11/Wayland use cases
		# so the kernel doesn't unload the module when not in use
		# the persistenced service is only needed in the server kernels
		if [[ $i == *"server"* ]]; then
			echo Requires: %{name}-persistenced = %{version}
		fi

		# Just to be on the safe side, it may not be wise
		# to load clang-built modules into a gcc-built kernel
		if [[ $i == *"gcc" ]]; then
			echo BuildRequires: gcc
		fi
done)

Obsoletes:	%{name}-current <= %{version}

%description
This is a binary-only driver for NVIDIA graphics chips.

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

Provides:	libGLdispatch0 >= 1.4.0-1
Provides:	libGL1 >= 1.4.0-1
Provides:	libEGL1 >= 1.4.0-1
Provides:	libGLESv2_2 >= 1.4.0-1
Provides:	libOpenGL0 >= 1.4.0-1

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

# =======================================================================================#
# dkms-nvidia - modified from https://github.com/NVIDIA/yum-packaging-dkms-nvidia
# =======================================================================================#

%package dkms-kmod
License:	NVIDIA License
Summary:	NVIDIA display driver kernel module. **This is an unsupported proprietary driver. Use with caution!
URL:		http://www.nvidia.com/object/unix.html

Source4:	dkms-%{dkms_name}.conf

Provides:	%{name}-kmod = %{version}
Provides:	should-restart = system

Requires:	%{name}-kmod-headers = %{version}
Requires:	%{name}-kmod-common = %{version}
Requires:	dkms

Conflicts:	kmod-nvidia-latest-dkms

%description dkms-kmod
This package provides the proprietary Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

# =======================================================================================#
# dkms-open-nvidia - modified from https://github.com/NVIDIA/yum-packaging-dkms-nvidia
# =======================================================================================#
%package dkms-kmod-open

Summary:	NVIDIA driver open kernel module flavor
License:	NVIDIA and GPL-2

Provides:	%{name}-kmod = %{version}
Provides:	should-restart = system

Requires:	%{name}-kmod-common = %{version}
Requires:	dkms
Requires:	nvidia-firmware

Conflicts:	kmod-nvidia-latest-dkms

%description dkms-kmod-open
This package provides the open-source Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

%package kmod-open-source
Summary:	NVIDIA open kernel module source files
BuildArch:	noarch
AutoReq:	0

Conflicts:	kmod-nvidia-latest-dkms

Obsoletes:	kmod-%{open_dkms_name}-dkms-nvidia-kmod-source <= %{version}

%description kmod-open-source
NVIDIA kernel module source files for compiling open flavor of nvidia.o and nvidia-modeset.o kernel modules.

%package kmod-headers
Summary:	NVIDIA header files for precompiled streams
AutoReq:	0

Conflicts:	kmod-nvidia-latest-dkms

%description kmod-headers
NVIDIA header files for precompiled streams

# =======================================================================================#
# nvidia-kmod-common - modified from https://github.com/NVIDIA/yum-packaging-nvidia-kmod-common
# =======================================================================================#

%package kmod-common
Summary:	Common file for NVIDIA's proprietary driver kernel modules
License:	NVIDIA License
URL:		http://www.nvidia.com/object/unix.html

BuildArch:	noarch
Source5:	60-nvidia.rules
Source6:	99-nvidia.conf

Provides:	%{name}-kmod-common = %{version}

Requires:	%{name}-kmod = %{version}
Requires:	%{name} = %{version}

Obsoletes:	cuda-nvidia-kmod-common <= %{version}

%description kmod-common
This package provides the common files required by all NVIDIA kernel module
package variants.

# =======================================================================================#
# nvidia-persistenced - modified from https://github.com/NVIDIA/yum-packaging-nvidia-persistenced
# =======================================================================================#

%package persistenced

Summary:	A daemon to maintain persistent software state in the NVIDIA driver
License:	GPLv2+
URL:		https://github.com/NVIDIA/nvidia-persistenced
Source7:	https://github.com/NVIDIA/nvidia-persistenced/archive/refs/tags/%{helpers_version}.tar.gz#/%{name}-persistenced-%{helpers_version}.tar.gz
Source8:	nvidia-persistenced.service
Source9:	nvidia-persistenced.conf

# Requires cuda, but the kmod-common "builds" that
Requires:	%{name} = %{version}

%description persistenced
The nvidia-persistenced utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.

# =======================================================================================#
# nvidia-modprobe - modified from https://github.com/NVIDIA/yum-packaging-nvidia-modprobe
# =======================================================================================#

%package modprobe
Summary:	NVIDIA kernel module loader
License:	GPLv2+
URL:		https://github.com/NVIDIA/nvidia-modprobe
Source10:	https://github.com/NVIDIA/nvidia-modprobe/archive/refs/tags/%{helpers_version}.tar.gz#/%{name}-modprobe-%{helpers_version}.tar.gz

Requires:	%{name} = %{version}

%description modprobe
This utility is used by user-space NVIDIA driver components to make sure the
NVIDIA kernel modules are loaded and that the NVIDIA character device files are
present.

# =======================================================================================#
# nvidia-settings - modified from https://github.com/NVIDIA/yum-packaging-nvidia-settings
# =======================================================================================#

%package settings
Summary:	Configure the NVIDIA graphics driver
License:	GPLv2+
Source11:	https://github.com/NVIDIA/nvidia-settings/archive/refs/tags/%{helpers_version}.tar.gz#/%{name}-settings-%{helpers_version}.tar.gz
Source12:	%{name}-settings-load.desktop
Source13:	%{name}-settings.appdata.xml

#Requires:	%%{name}-libXNVCtrl = %%{version}
Requires:	%{name} = %{version}
Requires:	%{_lib}vdpau1 >= 0.0

%description settings
The %{name}-settings utility is a tool for configuring the NVIDIA graphics
driver. It operates by communicating with the NVIDIA X driver, querying and
updating state as appropriate.

This communication is done with the NV-CONTROL X extension.

# The current version of nvidia-settings does not have the ability to be built into an so
# it gets linked statically. Explore enabling this if it gets fixed upstream

# %%package libXNVCtrl
# Summary:	Library providing the NV-CONTROL API
# Provides:	libXNVCtrl = %%{EVRD}
#
# Requires(post):	/sbin/ldconfig
#
# %%description libXNVCtrl
# This library provides the NV-CONTROL API for communicating with the proprietary
# NVidia xorg driver. It is required for proper operation of the %%{name}-settings utility.
#
# %%package libXNVCtrl-devel
# Summary:	Development files for libXNVCtrl
# Requires:	nvidia-libXNVCtrl = %%{EVRD}
# Requires:	pkgconfig(libX11)
#
# %%description libXNVCtrl-devel
# This devel package contains libraries and header files for
# developing applications that use the NV-CONTROL API.

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
%autopatch -m 5 -p1

# dkms kmod - closed and open
cp -f %{S:4} %{nvidia_driver_dir}/kernel/dkms.conf
cp -f %{S:4} %{nvidia_driver_dir}/kernel-open/dkms.conf
sed -i -e 's/__VERSION_STRING/%{version}/g' %{nvidia_driver_dir}/kernel/dkms.conf
sed -i -e 's/__VERSION_STRING/%{version}/g' %{nvidia_driver_dir}/kernel-open/dkms.conf
cp -r %{nvidia_driver_dir}/kernel-open %{open_kmod_source}

# persistenced
tar -xf %{S:7} -C %{_builddir}/%{name}-%{version}
# Remove additional CFLAGS added when enabling DEBUG
sed -i -e '/+= -O0 -g/d' %{_builddir}/%{name}-%{version}/nvidia-persistenced-%{helpers_version}/utils.mk

# modprobe
tar -xf %{S:10} -C %{_builddir}/%{name}-%{version}
# Remove additional CFLAGS added when enabling DEBUG
sed -i '/+= -O0 -g/d' %{_builddir}/%{name}-%{version}/nvidia-modprobe-%{helpers_version}/utils.mk

# settings
tar -xf %{S:11} -C %{_builddir}/%{name}-%{version}
cd %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}
%autopatch -m 1 -M 4 -p1
# Remove bundled jansson
rm -fr %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}/src/jansson
# Remove additional CFLAGS added when enabling DEBUG
sed -i '/+= -O0 -g/d' %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}/utils.mk %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}/src/libXNVCtrl/utils.mk
# Change all occurrences of destinations in each utils.mk.
sed -i -e 's|$(PREFIX)/lib|$(PREFIX)/%{_lib}|g' %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}/utils.mk %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}/src/libXNVCtrl/utils.mk

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
%if %{rc_openonly}
	if ! echo $i |grep -q ^rc; then
%endif
		if echo $i |grep -q gcc; then
			%{make_build} SYSSRC=${KERNEL_SOURCES} SYSOUT=${KERNEL_OUTPUT} CC=gcc CXX=g++
		else
			%{make_build} SYSSRC=${KERNEL_SOURCES} SYSOUT=${KERNEL_OUTPUT} IGNORE_CC_MISMATCH=1
		fi

		mkdir -p %{_builddir}/%{name}-%{version}/modules-$i
		mv *.ko %{_builddir}/%{name}-%{version}/modules-$i
%if %{rc_openonly}
	fi
%endif

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
cd %{_builddir}/%{name}-%{version}/nvidia-persistenced-%{helpers_version}
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
export LDFLAGS="%{?__global_ldflags} -ltirpc"
%make DEBUG=1 \
		LIBS="-ldl -ltirpc" \
		NV_VERBOSE=1 \
		PREFIX=%{_prefix} \
		STRIP_CMD=true

# modprobe
cd %{_builddir}/%{name}-%{version}/nvidia-modprobe-%{helpers_version}
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
export LDFLAGS="%{?__global_ldflags} -ltirpc"
%make DEBUG=1 \
		LIBS="-ldl -ltirpc" \
		NV_VERBOSE=1 \
		PREFIX=%{_prefix} \
		STRIP_CMD=true

# settings
cd %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}
export CFLAGS="%{optflags} -fPIC"
export LDFLAGS="%{?__global_ldflags}"
%make DEBUG=1 \
	NV_USE_BUNDLED_LIBJANSSON=0 \
	NV_VERBOSE=1 \
	PREFIX=%{_prefix} \
	XNVCTRL_LDFLAGS="-L%{_libdir}"

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
%ifarch %{x86_64}
instx %{_libdir}/libnvidia-pkcs11.so.%{version}
instx %{_libdir}/libnvidia-pkcs11-openssl3.so.%{version}
%endif

instx %{_libdir}/libnvidia-rtcore.so.%{version}
instx %{_libdir}/libnvoptix.so.%{version}

# Firmware
mkdir -p %{buildroot}%{_prefix}/lib
cp -a firmware %{buildroot}%{_prefix}/lib

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
%if %{rc_openonly}
	if ! echo $i |grep -q ^rc; then
%endif
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
%if %{rc_openonly}
	fi
%endif
done

# dkms-kmod
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr %{nvidia_driver_dir}/kernel/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_presetdir}

# Avoid Nvidia modules getting in the initrd:
install -p -m 0644 %{S:6} %{buildroot}%{_sysconfdir}/dracut.conf.d/

# UDev rules:
# https://github.com/NVIDIA/nvidia-modprobe/blob/master/modprobe-utils/nvidia-modprobe-utils.h#L33-L46
# https://github.com/negativo17/nvidia-driver/issues/27
install -p -m 644 %{S:5} %{buildroot}%{_udevrulesdir}

# persistenced
cd %{_builddir}/%{name}-%{version}/nvidia-persistenced-%{helpers_version}
%make_install \
	NV_VERBOSE=1 \
	PREFIX=%{_prefix} \
	STRIP_CMD=true
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}-persistenced/
cp COPYING %{buildroot}%{_datadir}/licenses/%{name}-persistenced/COPYING

mkdir -p %{buildroot}%{_sharedstatedir}/nvidia-persistenced
# Systemd unit files
install -p -m 644 -D %{S:8} %{buildroot}%{_unitdir}/nvidia-persistenced.service
install -p -m 644 -D %{S:9} %{buildroot}%{_prefix}/lib/sysusers.d/nvidia-persistenced.conf

# modprobe
cd %{_builddir}/%{name}-%{version}/nvidia-modprobe-%{helpers_version}
%make_install \
	NV_VERBOSE=1 \
	PREFIX=%{_prefix} \
	STRIP_CMD=true

mkdir -p %{buildroot}%{_datadir}/licenses/%{name}-modprobe
cp COPYING %{buildroot}%{_datadir}/licenses/%{name}-modprobe/COPYING

# settings
cd %{_builddir}/%{name}-%{version}/nvidia-settings-%{helpers_version}

# devel package not currently building into a so

# # Install libXNVCtrl headers
# mkdir -p %%{buildroot}%%{_includedir}/NVCtrl
# cp -af src/libXNVCtrl/*.h %%{buildroot}%%{_includedir}/NVCtrl/

%make_install \
	DEBUG=1 \
	NV_USE_BUNDLED_LIBJANSSON=0 \
	NV_VERBOSE=1 \
	PREFIX=%{_prefix}

mkdir -p %{buildroot}%{_datadir}/licenses/%{name}-settings/
cp COPYING %{buildroot}%{_datadir}/licenses/%{name}-settings/COPYING

# Install desktop file
mkdir -p %{buildroot}%{_datadir}/{applications,pixmaps}
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ doc/%{name}-settings.desktop
cp doc/%{name}-settings.png %{buildroot}%{_datadir}/pixmaps/

# Install autostart file to load settings at login
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/
install -p -m 644 %{S:12} %{buildroot}%{_sysconfdir}/xdg/autostart/

# install AppData and add modalias provides
mkdir -p %{buildroot}%{_metainfodir}/
install -p -m 0644 %{S:13} %{buildroot}%{_metainfodir}/

# Remove bundled wayland client
rm -vf %{buildroot}/%{_libdir}/libnvidia-wayland-client.so*

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-settings.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-settings-load.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}-settings.appdata.xml

%post kmod-common
if ! grep -q nvidia-drm.modeset %{_sysconfdir}/default/grub; then
	sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=['\''"]/&nouveau.modeset=0 nvidia-drm.modeset=1 nvidia-drm.fbdev=1 /' %{_sysconfdir}/default/grub
fi
/sbin/depmod -a
/usr/bin/dracut -f
%{_sbindir}/update-grub2

%postun kmod-common
if [ "$1" = "0" ]; then
	sed -i 's/nouveau.modeset=0 nvidia-drm.modeset=1 nvidia-drm.fbdev=1 //g' %{_sysconfdir}/default/grub
fi
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

%post dkms-kmod-open
dkms add -m %{open_dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{open_dkms_name} -v %{version} -q || :
dkms install -m %{open_dkms_name} -v %{version} -q --force || :

%preun dkms-kmod-open
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
%ifarch %{x86_64}
%{_libdir}/libnvidia-pkcs11-openssl3.so*
%{_libdir}/libnvidia-pkcs11.so*
%endif
%{_libdir}/libnvidia-rtcore.so*
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
%{_libdir}/vdpau/libvdpau_nvidia.so*
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-smi
%{_mandir}/man1/nvidia-smi.1*
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

%files dkms-kmod-open
%{_usrsrc}/%{open_dkms_name}-%{version}/common
%{_usrsrc}/%{open_dkms_name}-%{version}/nvidia*
%{_usrsrc}/%{open_dkms_name}-%{version}/Kbuild
%{_usrsrc}/%{open_dkms_name}-%{version}/Makefile
%{_usrsrc}/%{open_dkms_name}-%{version}/conftest.sh
%{_usrsrc}/%{open_dkms_name}-%{version}/dkms.conf
%{_usrsrc}/%{open_dkms_name}-%{version}/*.mk

%files kmod-open-source
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

%files settings
%license COPYING
%{_bindir}/%{name}-settings
%{_metainfodir}/%{name}-settings.appdata.xml
%{_datadir}/applications/%{name}-settings.desktop
%{_datadir}/pixmaps/%{name}-settings.png
%{_libdir}/libnvidia-gtk3.so.%{helpers_version}
%exclude %{_libdir}/libnvidia-gtk2.so.%{helpers_version}
%{_libdir}/libnvidia-gtk2.so.%{helpers_version}
%{_mandir}/man1/%{name}-settings.*
%{_sysconfdir}/xdg/autostart/%{name}-settings-load.desktop

# upstream not building a so

# %%files libXNVCtrl
# %%license COPYING
# %%{_libdir}/%%{_lib}XNVCtrl.so.*
#
# %%files libXNVCtrl-devel
# %%doc doc/NV-CONTROL-API.txt doc/FRAMELOCK.txt
# %%{_includedir}/NVCtrl
# %%{_libdir}/%%{_lib}XNVCtrl.so
