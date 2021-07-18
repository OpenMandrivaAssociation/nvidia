%define debug_package %{nil}
%bcond_with kernel_rc

Summary:	Binary-only driver for nvidia graphics chips
Name:		nvidia
Version:	465.27
Release:	1
ExclusiveArch:	%{x86_64}
Url:		http://www.nvidia.com/object/unix.html
Source0:	http://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source1:	https://gitweb.frugalware.org/frugalware-current/raw/master/source/x11-extra/nvidia/xorg-nvidia.conf	
Source2:	https://gitweb.frugalware.org/frugalware-current/raw/master/source/x11-extra/nvidia/modprobe-nvidia.conf
Patch0:         nvidia-fix-linux-5.10.patch	
Group:		Hardware
License:	distributable
# Just to be on the safe side, it may not be wise
# to load clang-built modules into a gcc-built kernel
BuildRequires:	gcc
Requires:	%{name}-kernel-modules = %{EVRD}
#FIXME#
# /usr/lib64/libnvidia-egl-wayland.so.1 conflicts between attempted installs of nvidia-460.67-1.x86_64 and lib64nvidia-egl-wayland1-1.1.6-1.x86_64
# So disable it for now, until someone knowledgeable about NVIDIA has time to fix this problem.
#Requires:	egl-wayland

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

%package kernel-modules-desktop
%define kversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-release-desktop-devel |tail -n1)
%define kdir %(rpm -q --qf '%%{VERSION}-desktop-%%{RELEASE}%%{DISTTAG}\\n' kernel-release-desktop-devel |tail -n1)
Summary:	Kernel modules needed by the binary-only nvidia driver
Provides:	%{name}-kernel-modules = %{EVRD}
Requires:	kernel-release-desktop = %{kversion}
#Conflicts:	kernel-release-desktop < %%{kversion}
Conflicts:	kernel-release-desktop > %{kversion}
#Conflicts:	%%{name}-kernel-modules < %%{kversion}
Group:		Hardware
Provides:	should-restart = system
Requires(post,postun):	sed dracut grub2 kmod
BuildRequires:	kernel-release-desktop-devel

%description kernel-modules-desktop
Kernel modules needed by the binary-only nvidia driver

%package kernel-modules-desktop-clang
%define ckversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-release-desktop-clang-devel |tail -n1)
%define ckdir %(rpm -q --qf '%%{VERSION}-desktop-clang-%%{RELEASE}%%{DISTTAG}\\n' kernel-release-desktop-clang-devel |tail -n1)
Summary:	Kernel modules needed by the binary-only nvidia driver
Provides:	%{name}-kernel-modules = %{EVRD}
Requires:	kernel-release-desktop-clang = %{kversion}
#Conflicts:	kernel-release-desktop < %%{kversion}
Conflicts:	kernel-release-desktop-clang > %{kversion}
#Conflicts:	%%{name}-kernel-modules < %%{kversion}
Group:		Hardware
Provides:	should-restart = system
Requires(post,postun):	sed dracut grub2 kmod
BuildRequires:	kernel-release-desktop-clang-devel

%description kernel-modules-desktop-clang
Kernel modules needed by the binary-only nvidia driver

%package kernel-modules-server
%define skversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-release-server-devel |tail -n1)
%define skdir %(rpm -q --qf '%%{VERSION}-desktop-%%{RELEASE}%%{DISTTAG}\\n' kernel-release-server-devel |tail -n1)
Summary:	Kernel modules needed by the binary-only nvidia driver
Provides:	%{name}-kernel-modules = %{EVRD}
Requires:	kernel-release-server = %{skversion}
Conflicts:	kernel-release-server < %{skversion}
#Conflicts:	kernel-release-server > %%{skversion}
Conflicts:	%{name}-kernel-modules < %{skversion}
Group:		Hardware
Provides:	should-restart = system
Requires(post,postun):	sed dracut grub2 kmod
BuildRequires:	kernel-release-server-devel

%description kernel-modules-server
Kernel modules needed by the binary-only nvidia driver

%package kernel-modules-server-clang
%define cskversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-release-server-clang-devel |tail -n1)
%define cskdir %(rpm -q --qf '%%{VERSION}-desktop-clang-%%{RELEASE}%%{DISTTAG}\\n' kernel-release-server-clang-devel |tail -n1)
Summary:	Kernel modules needed by the binary-only nvidia driver
Provides:	%{name}-kernel-modules = %{EVRD}
Requires:	kernel-release-server-clang = %{kversion}
#Conflicts:	kernel-release-desktop < %%{kversion}
Conflicts:	kernel-release-server-clang > %{kversion}
#Conflicts:	%%{name}-kernel-modules < %%{kversion}
Group:		Hardware
Provides:	should-restart = system
Requires(post,postun):	sed dracut grub2 kmod
BuildRequires:	kernel-release-server-clang-devel

%description kernel-modules-server-clang
Kernel modules needed by the binary-only nvidia driver

%if %{with kernel_rc}
%package kernel-modules-rc-desktop
%define rkversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-rc-desktop-devel |tail -n1)
%define rkdir %(rpm -q --qf '%%{VERSION}-desktop-%%{RELEASE}%%{DISTTAG}\\n' kernel-rc-desktop-devel |tail -n1)
Summary:	Kernel modules needed by the binary-only nvidia driver
Provides:	%{name}-kernel-modules = %{EVRD}
Requires:	kernel-rc-desktop = %{rkversion}
Conflicts:	kernel-rc-desktop < %{rkversion}
Conflicts:	kernel-rc-desktop > %{rkversion}
Group:		Hardware
Provides:	should-restart = system
Requires(post,postun):	sed dracut grub2 kmod
BuildRequires:	kernel-rc-desktop-devel

%description kernel-modules-rc-desktop
Kernel modules needed by the binary-only nvidia driver

%package kernel-modules-rc-server
%define rskversion %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel-rc-server-devel |tail -n1)
%define rskdir %(rpm -q --qf '%%{VERSION}-server-%%{RELEASE}%%{DISTTAG}\\n' kernel-rc-server-devel |tail -n1)
Summary:	Kernel modules needed by the binary-only nvidia driver
Provides:	%{name}-kernel-modules = %{EVRD}
Requires:	kernel-rc-server = %{rskversion}
Conflicts:	kernel-rc-server < %{rskversion}
Conflicts:	kernel-rc-server > %{rskversion}
Group:		Hardware
Provides:	should-restart = system
Requires(post,postun):	sed dracut grub2 kmod
BuildRequires:	kernel-rc-server-devel

%description kernel-modules-rc-server
Kernel modules needed by the binary-only nvidia driver
%endif

%prep
%setup -T -c %{name}-%{version}
sh %{S:0} --extract-only
#%%patch0 -p1

%build
cd NVIDIA-Linux-x86_64-%{version}

cp -a kernel kernel-server
cp -a kernel kernel-clang
cp -a kernel kernel-server-clang

%if %{with kernel_rc}
cp -a kernel kernel-rc
cp -a kernel kernel-rc-server
%endif

cd kernel
make SYSSRC=%{_prefix}/src/linux-%{kdir} CC=%{_bindir}/gcc

cd ../kernel-clang
make SYSSRC=%{_prefix}/src/linux-%{ckdir} CC=%{_bindir}/clang IGNORE_CC_MISMATCH=1

cd ../kernel-server
make SYSSRC=%{_prefix}/src/linux-%{skdir} CC=%{_bindir}/gcc

cd ../kernel-server-clang
make SYSSRC=%{_prefix}/src/linux-%{cskdir} CC=%{_bindir}/clang IGNORE_CC_MISMATCH=1

%if %{with kernel_rc}
cd ../kernel-rc
make SYSSRC=%{_prefix}/src/linux-%{rkdir} CC=%{_bindir}/gcc IGNORE_CC_MISMATCH=1

cd ../kernel-rc-server
make SYSSRC=%{_prefix}/src/linux-%{rskdir} CC=%{_bindir}/gcc IGNORE_CC_MISMATCH=1
%endif

%install
cd NVIDIA-Linux-x86_64-%{version}

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
instx %{_libdir}/libnvcuvid.so.%{version}
sl nvcuvid 1
instx %{_libdir}/libnvidia-ml.so.%{version}
sl nvidia-ml 1
# CUDA?
instx %{_libdir}/libnvidia-ptxjitcompiler.so.%{version}
sl nvidia-ptxjitcompiler 1

#instx %%{_libdir}/libnvidia-fatbinaryloader.so.%%{version}

# nvidia-tls library
instx %{_libdir}/libnvidia-tls.so.%{version}
sl nvidia-tls

# OpenCL
inst %{_sysconfdir}/OpenCL/vendors/nvidia.icd
instx %{_libdir}/libnvidia-cfg.so.%{version}
sl nvidia-cfg 1

instx %{_libdir}/libnvidia-compiler.so.%{version}
instx %{_libdir}/libnvidia-opencl.so.%{version}

# Encode (what is this?)
instx %{_libdir}/libnvidia-encode.so.%{version}
sl nvidia-encode 1

# Fbc (Framebuffer console?)
instx %{_libdir}/libnvidia-fbc.so.%{version}
sl nvidia-fbc 1

# Yuck...
instx %{_libdir}/libnvidia-gtk2.so.%{version}
instx %{_libdir}/libnvidia-gtk3.so.%{version}

# IFR
instx %{_libdir}/libnvidia-ifr.so.%{version}
sl nvidia-ifr 1

# VDPAU
instx %{_libdir}/vdpau/libvdpau_nvidia.so.%{version}
ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau/libvdpau_nvidia.so.1.0
ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau/libvdpau_nvidia.so.1
ln -s libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau/libvdpau_nvidia.so

# Wayland
# FIXME can this be replaced by https://github.com/NVIDIA/egl-wayland ?
wlibso=$(ls libnvidia-egl-wayland.so* | sed 's/.*so.\(.*\)/\1/')
instx %{_libdir}/libnvidia-egl-wayland.so.$wlibso
ln -s libnvidia-egl-wayland.so.$wlibso %{buildroot}%{_libdir}/libnvidia-egl-wayland.so.1
ln -s libnvidia-egl-wayland.so.$wlibso %{buildroot}%{_libdir}/libnvidia-egl-wayland.so
inst %{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json

# Tools
for i in *.1.gz; do
	gunzip $i
done
instx %{_bindir}/nvidia-bug-report.sh
instx %{_bindir}/nvidia-smi
inst %{_mandir}/man1/nvidia-smi.1
instx %{_bindir}/nvidia-settings       
inst %{_mandir}/man1/nvidia-settings.1

# glvk
instx %{_libdir}/libnvidia-glvkspirv.so.%{version}

# Assorted stuff
inst %{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc
inst %{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation

# Configs
install -D -m 644 %{S:1} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/15-nvidia.conf
install -D -m 644 %{S:2} %{buildroot}%{_sysconfdir}/modprobe.d/nvidia.conf

# Kernel modules
cd kernel
inst /lib/modules/%{kdir}/kernel/drivers/video/nvidia.ko
inst /lib/modules/%{kdir}/kernel/drivers/video/nvidia-drm.ko
inst /lib/modules/%{kdir}/kernel/drivers/video/nvidia-modeset.ko
inst /lib/modules/%{kdir}/kernel/drivers/video/nvidia-uvm.ko

cd ../kernel-clang
inst /lib/modules/%{ckdir}/kernel/drivers/video/nvidia.ko
inst /lib/modules/%{ckdir}/kernel/drivers/video/nvidia-drm.ko
inst /lib/modules/%{ckdir}/kernel/drivers/video/nvidia-modeset.ko
inst /lib/modules/%{ckdir}/kernel/drivers/video/nvidia-uvm.ko

cd ../kernel-server
inst /lib/modules/%{skdir}/kernel/drivers/video/nvidia.ko
inst /lib/modules/%{skdir}/kernel/drivers/video/nvidia-drm.ko
inst /lib/modules/%{skdir}/kernel/drivers/video/nvidia-modeset.ko
inst /lib/modules/%{skdir}/kernel/drivers/video/nvidia-uvm.ko

cd ../kernel-server-clang
inst /lib/modules/%{cskdir}/kernel/drivers/video/nvidia.ko
inst /lib/modules/%{cskdir}/kernel/drivers/video/nvidia-drm.ko
inst /lib/modules/%{cskdir}/kernel/drivers/video/nvidia-modeset.ko
inst /lib/modules/%{cskdir}/kernel/drivers/video/nvidia-uvm.ko

%files
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
%{_libdir}/libcuda.so*
%{_libdir}/libnvcuvid.so*
%{_libdir}/libnvidia-ml.so*
%{_libdir}/libnvidia-ptxjitcompiler.so*
#%%{_libdir}/libnvidia-fatbinaryloader.so*
%{_libdir}/libnvidia-tls.so*
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%{_libdir}/libnvidia-cfg.so*
%{_libdir}/libnvidia-compiler.so*
%{_libdir}/libnvidia-opencl.so*
%{_libdir}/libnvidia-encode.so*
%{_libdir}/libnvidia-fbc.so*
%{_libdir}/libnvidia-gtk2.so*
%{_libdir}/libnvidia-gtk3.so*
%{_libdir}/libnvidia-ifr.so*
%{_libdir}/vdpau/libvdpau_nvidia.so*
%{_libdir}/libnvidia-egl-wayland.so*
%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-smi
%{_mandir}/man1/nvidia-smi.1*
%{_bindir}/nvidia-settings
%{_mandir}/man1/nvidia-settings.1*
%{_libdir}/libnvidia-glvkspirv.so*
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation
%{_sysconfdir}/X11/xorg.conf.d/15-nvidia.conf
%{_sysconfdir}/modprobe.d/nvidia.conf

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
#%%{_prefix}/lib/libnvidia-fatbinaryloader.so*
%{_prefix}/lib/libnvidia-tls.so*
%{_prefix}/lib/libnvidia-compiler.so*
%{_prefix}/lib/libnvidia-opencl.so*
%{_prefix}/lib/libnvidia-encode.so*
%{_prefix}/lib/libnvidia-fbc.so*
%{_prefix}/lib/libnvidia-ifr.so*
%{_prefix}/lib/vdpau/libvdpau_nvidia.so*
%{_prefix}/lib/libnvidia-glvkspirv.so*
%endif

%files kernel-modules-desktop
/lib/modules/%{kdir}/kernel/drivers/video/*

%post kernel-modules-desktop
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="rd.driver.blacklist=nouveau /' %{_sysconfdir}/default/grub
/sbin/depmod -a %{kdir}
/usr/bin/dracut -f --kver %{kdir}
%{_sbindir}/update-grub2

%postun kernel-modules-desktop
sed -i 's/rd.driver.blacklist=nouveau //g' %{_sysconfdir}/default/grub
/sbin/depmod -a %{kdir}
/usr/bin/dracut -f --kver %{kdir}
%{_sbindir}/update-grub2

%files kernel-modules-desktop-clang
/lib/modules/%{ckdir}/kernel/drivers/video/*

%post kernel-modules-desktop-clang
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="rd.driver.blacklist=nouveau /' %{_sysconfdir}/default/grub
/sbin/depmod -a %{ckdir}
/usr/bin/dracut -f --kver %{ckdir}
%{_sbindir}/update-grub2

%postun kernel-modules-desktop-clang
sed -i 's/rd.driver.blacklist=nouveau //g' %{_sysconfdir}/default/grub
/sbin/depmod -a %{ckdir}
/usr/bin/dracut -f --kver %{ckdir}
%{_sbindir}/update-grub2

%files kernel-modules-server
/lib/modules/%{skdir}/kernel/drivers/video/*

%post kernel-modules-server
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="rd.driver.blacklist=nouveau /' %{_sysconfdir}/default/grub
/sbin/depmod -a %{skdir}
/usr/bin/dracut -f --kver %{skdir}
%{_sbindir}/update-grub2

%postun kernel-modules-server
sed -i 's/rd.driver.blacklist=nouveau //g' %{_sysconfdir}/default/grub
/sbin/depmod -a %{skdir}
/usr/bin/dracut -f --kver %{skdir}
%{_sbindir}/update-grub2

%files kernel-modules-server-clang
/lib/modules/%{cskdir}/kernel/drivers/video/*

%post kernel-modules-server-clang
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="rd.driver.blacklist=nouveau /' %{_sysconfdir}/default/grub
/sbin/depmod -a %{cskdir}
/usr/bin/dracut -f --kver %{cskdir}
%{_sbindir}/update-grub2

%postun kernel-modules-server-clang
sed -i 's/rd.driver.blacklist=nouveau //g' %{_sysconfdir}/default/grub
/sbin/depmod -a %{cskdir}
/usr/bin/dracut -f --kver %{cskdir}
%{_sbindir}/update-grub2

%if %{with kernel_rc}
%files kernel-modules-rc-desktop
/lib/modules/%{rkdir}/kernel/drivers/video/*

%post kernel-modules-rc-desktop
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="rd.driver.blacklist=nouveau /' %{_sysconfdir}/default/grub
/sbin/depmod -a %{rkdir}
/usr/bin/dracut -f --kver %{rkdir}
%{_sbindir}/update-grub2

%postun kernel-modules-rc-desktop
sed -i 's/rd.driver.blacklist=nouveau //g' %{_sysconfdir}/default/grub
/sbin/depmod -a %{rkdir}
/usr/bin/dracut -f --kver %{rkdir}
%{_sbindir}/update-grub2

%files kernel-modules-rc-server
/lib/modules/%{rskdir}/kernel/drivers/video/*

%post kernel-modules-rc-server
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="rd.driver.blacklist=nouveau /' %{_sysconfdir}/default/grub
/sbin/depmod -a %{rkdir}
/usr/bin/dracut -f --kver %{rskdir}
%{_sbindir}/update-grub2

%postun kernel-modules-rc-server
sed -i 's/rd.driver.blacklist=nouveau //g' %{_sysconfdir}/default/grub
/sbin/depmod -a %{rskdir}
/usr/bin/dracut -f --kver %{rskdir}
%{_sbindir}/update-grub2
%endif
