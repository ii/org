exec 2>&1

mkdir -p /tmp/amd
cd /tmp/amd
wget https://github.com/M-Bab/linux-kernel-amdgpu-binaries/raw/53819982954987ddde463c9354608655cf1ba211/firmware-radeon-ucode_2.40_all.deb
wget https://github.com/M-Bab/linux-kernel-amdgpu-binaries/raw/53819982954987ddde463c9354608655cf1ba211/linux-headers-4.19.6_18.12.04.amdgpu.ubuntu_amd64.deb
wget https://github.com/M-Bab/linux-kernel-amdgpu-binaries/raw/53819982954987ddde463c9354608655cf1ba211/linux-image-4.19.6_18.12.04.amdgpu.ubuntu_amd64.deb
dpkg -i *deb
cd -
rm -rf /tmp/amd
:
