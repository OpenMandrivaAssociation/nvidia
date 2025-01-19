# nvidia
This repository contains the NVIDIA Proprietary and Open drivers.

The following packages are built in ABF from this repository:

* `nvidia` - the main driver meta package
* `nvidia-32bit` - support for 32 bit applications (games, etc..)
* `nvidia-kmod-<kernel_flavor>` - precompiled kernel modules (i.e. `desktop`, `server`, etc...)
* `nvidia-dkms-kmod` - dynamically built kernel module (advanced use, kernel tweaking, etc...)
* `nvidia-dkms-kmod-open` - open source dynamically built kernel module (highly experimental)
* `nvidia-kmod-open-source` - open kernel module source code
* `nvidia-kmod-headers` - precompiled headers
* `nvidia-kmod-common` - common files needed by the kernel modules
* `nvidia-kmod-persistenced` - service for headless systems to keep the kernel module from being unloaded
* `nvidia-modprobe` - required binary to load the kernel modules correctly
* `nvidia-settings` - GUI and CLI based binary to modify graphics settings
