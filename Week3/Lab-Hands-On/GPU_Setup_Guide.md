# GPU Installation Guide: Windows, macOS & Linux

A practical guide to setting up your machine for GPU-accelerated Python (CuPy, PyTorch, TensorFlow). Covers NVIDIA driver + CUDA Toolkit installation, Python environment setup, and verification. 

> **Read this first:** CUDA only runs on **NVIDIA GPUs**. If your laptop doesn't have one (most MacBooks, many ultrabooks, integrated Intel/AMD graphics), skip to the [macOS / No-NVIDIA-GPU](#macos--no-nvidia-gpu) section. Installing CUDA there won't work no matter how carefully you follow steps.

---

## Quick Decision Guide

| Your machine | What you can do |
|---|---|
| Windows + NVIDIA GPU | Full CUDA Toolkit + CuPy/PyTorch with CUDA —> follow [Windows](#windows) |
| Linux + NVIDIA GPU | Full CUDA Toolkit + CuPy/PyTorch with CUDA —> follow [Linux](#linux-ubuntudebian) |
| Intel Mac or Apple Silicon Mac | **No CUDA support.** Use PyTorch's Metal (MPS) backend, or use Google Colab for CUDA/CuPy work, see [macOS](#macos--no-nvidia-gpu) |
| Windows/Linux, no NVIDIA GPU (e.g. AMD, Intel integrated) | Same as Mac —> no CUDA. Use Colab/cloud, or look into ROCm for AMD GPUs |

---

## Windows

### 1. Confirm you have a CUDA-capable NVIDIA GPU
- Press `Win + X` → **Device Manager** → expand **Display adapters**
- You need an **NVIDIA card** (GeForce, RTX, Quadro, Tesla). Integrated Intel/AMD graphics won't work.

### 2. Install the NVIDIA display driver
As of CUDA 13.1+, the driver is **no longer bundled** with the CUDA Toolkit installer, **you need to install it separately first**.
1. Go to [nvidia.com/drivers](https://www.nvidia.com/Download/index.aspx)
2. Select your exact GPU model and Windows version → **Search** → **Download**
3. Run the installer → choose **Express Installation**
4. Reboot

**Verify the driver:**
```bash
nvidia-smi
```
You should see your GPU name, driver version, and CUDA version it supports (this is the *maximum* CUDA version your driver supports —> install a Toolkit version at or below this).

### 3. Install the CUDA Toolkit
1. Go to [developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
2. Select **Windows → x86_64 → your Windows version → exe (local)**
3. Run the installer → **Express** install is fine for most users
4. Reboot if prompted

**Verify the Toolkit:**
```bash
nvcc --version
```

### 4. Set up a Python environment
Use either Miniconda or a plain `venv`. Miniconda is recommended since it makes switching CUDA-tagged packages easier.

```bash
# Miniconda route
conda create -n gpu-env python=3.11 -y
conda activate gpu-env
```

### 5. Install GPU-enabled Python libraries
Match the package suffix to the CUDA major version reported by `nvidia-smi` / `nvcc --version`.

```bash
# CuPy (NumPy/SciPy-compatible GPU arrays)
pip install cupy-cuda12x      # if your CUDA Toolkit is 12.x
pip install cupy-cuda13x      # if your CUDA Toolkit is 13.x

# PyTorch with CUDA (pick the matching command from pytorch.org/get-started)
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

> PyTorch's website (https://pytorch.org/get-started/locally/) generates the exact install command for your CUDA version — always check there, since wheel tags change between releases.

### 6. Verify from Python
```python
import cupy as cp
print(cp.cuda.runtime.getDeviceCount())   # number of GPUs visible
print(cp.array([1, 2, 3]) * 2)            # should run without error

import torch
print(torch.cuda.is_available())         # True if PyTorch sees your GPU
print(torch.cuda.get_device_name(0))
```

---

## Linux (Ubuntu/Debian)

The package manager route below is the most reliable; steps are similar for Fedora/RHEL with `dnf` instead of `apt`.

### 1. Confirm you have an NVIDIA GPU
```bash
lspci | grep -i nvidia
```

### 2. Install the NVIDIA driver
**Easiest method (Ubuntu):**
```bash
sudo ubuntu-drivers autoinstall
sudo reboot
```

**Manual method (any Debian-based distro):**
```bash
sudo apt update
sudo apt install nvidia-driver-<version>   # e.g. nvidia-driver-570
sudo reboot
```

**Verify:**
```bash
nvidia-smi
```

### 3. Install the CUDA Toolkit
Use NVIDIA's official `apt` repository rather than the Ubuntu repos, to get the latest version:
```bash
# Add NVIDIA's CUDA repo (example for Ubuntu 22.04, adjust the URL for your release)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit
```
Then add CUDA to your shell's `PATH` (append to `~/.bashrc`):
```bash
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
```bash
source ~/.bashrc
```

**Verify:**
```bash
nvcc --version
```

### 4. Set up a Python environment
```bash
conda create -n gpu-env python=3.11 -y
conda activate gpu-env
```

### 5. Install GPU-enabled Python libraries
```bash
pip install cupy-cuda12x      # or cupy-cuda13x, matching your Toolkit version
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

### 6. Verify from Python
```python
import cupy as cp
print(cp.cuda.runtime.getDeviceCount())
print(cp.array([1, 2, 3]) * 2)

import torch
print(torch.cuda.is_available())
```

### Using WSL2 (Windows users running Linux)
If you're doing this inside WSL2 on Windows: install only the **Windows** NVIDIA driver (from the Windows section above), do **not** install a separate Linux driver inside WSL. Then install the CUDA Toolkit inside WSL using NVIDIA's **WSL-specific** `apt` repo, listed on the CUDA downloads page under **Linux → WSL-Ubuntu**.

---

## macOS / No NVIDIA GPU

**CUDA does not run on macOS.** Apple dropped NVIDIA driver support entirely, and Apple Silicon (M-series) chips have no NVIDIA hardware at all, there is no version of this guide that ends with `nvidia-smi` working on a Mac. Be skeptical of any tutorial claiming otherwise; it's either outdated (pre-2018, Intel Mac + ancient eGPU) or wrong.

You have two real options:

### Option A: Use your Mac's own GPU via Metal (Apple Silicon only)
Apple Silicon Macs (M1/M2/M3/M4) have a capable on-chip GPU, accessible through **Metal Performance Shaders (MPS)**, not CUDA, but a genuine GPU backend with NumPy-like libraries.

```bash
conda create -n gpu-env python=3.11 -y
conda activate gpu-env
pip install torch torchvision torchvision torchaudio
```

```python
import torch
print(torch.backends.mps.is_available())   # True on Apple Silicon
device = torch.device("mps")
x = torch.rand(1000, 1000, device=device)
y = x @ x   # runs on the GPU
```

For TensorFlow, install the `tensorflow-metal` plugin:
```bash
pip install tensorflow tensorflow-metal
```

**Important:** CuPy specifically does **not** work this way, it's CUDA-only. If your coursework or notebook calls `import cupy`, this option won't run it locally.

### Option B: Use a cloud GPU (recommended for CUDA/CuPy coursework)
If you need actual CUDA (e.g. to run `cupy` code exactly as written), the practical path on a Mac is a remote NVIDIA GPU:
- **Google Colab** (free tier includes a T4 GPU): Runtime → Change runtime type → GPU
- **Kaggle Notebooks**: free GPU quota
- A cloud VM (AWS, GCP, Azure, Lambda, Paperspace) with an NVIDIA GPU attached

This is also simply the path of least friction if you don't want to manage local drivers at all, on any OS.

---

## Verification Checklist (any OS)

Run through these in order. If one fails, fix it before moving to the next:

1. `nvidia-smi` shows your GPU, driver version, and a CUDA version (Windows/Linux only)
2. `nvcc --version` shows a Toolkit version ≤ the driver's supported CUDA version
3. `python -c "import cupy as cp; print(cp.array([1,2,3])*2)"` runs without error
4. `python -c "import torch; print(torch.cuda.is_available())"` prints `True`

---

## Common Pitfalls

| Symptom | Likely Cause |
|---|---|
| `nvidia-smi` not found | Driver not installed, or not on `PATH` —> reboot after install, recheck |
| CuPy `CompileException` / can't find CUDA | `cupy-cudaXXx` suffix doesn't match installed Toolkit major version |
| `torch.cuda.is_available()` is `False` | Installed the CPU-only PyTorch wheel —> reinstall using the `--index-url` for your CUDA version |
| Driver supports CUDA 12.x but you installed Toolkit 13.x | Toolkit version must be ≤ what the driver supports —> update the driver, or install an older Toolkit |
| Works in one terminal, not another | `PATH`/`LD_LIBRARY_PATH` only exported in one shell session —> add the export lines to your shell profile (`~/.bashrc`, `~/.zshrc`) |
| WSL2: GPU not visible | Installed a Linux driver *inside* WSL —> remove it; only the Windows-side driver should be installed |

---

*This guide reflects CUDA Toolkit 13.x / CuPy 14.x as of mid-2026. Package suffixes (`cupy-cuda12x`, `cupy-cuda13x`) and PyTorch's install command change between releases! Always cross-check [pytorch.org/get-started](https://pytorch.org/get-started/locally/) and [docs.cupy.dev](https://docs.cupy.dev/en/stable/install.html) before installing.*
