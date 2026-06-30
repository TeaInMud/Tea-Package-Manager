# 🍵 Tea Package Manager (TPM)

A fast, lightweight, and cross-platform custom package manager designed specifically for minimal environments like **Termux (Android)** and **iSH Shell (iOS / Alpine Linux)**. TPM allows you to effortlessly host your own global command-line utilities via GitHub and install them natively on any mobile device.

---

## ✨ Features

* **Dual-Platform Engine:** Intelligently detects whether you are running on Termux or iSH Shell and switches paths (`/data/data/com.termux/...` vs `/usr/local/bin`) automatically.
* **Global Cloud Registry:** Packages are dynamically synced over the network from a single, cloud-hosted Python registry configuration.
* **Native Integration:** Installed tools automatically receive `chmod +x` executable permissions and are placed in your system `\$PATH`, allowing you to run them from anywhere.
* **Smart Telemetry:** Quietly logs system and download errors locally to `~/.tea/errors.log` for seamless debugging without breaking user workflow.

---

## 🚀 One-Line Installation

Open your terminal environment and run the matching command to automatically download dependencies and bootstrap TPM globally:

### For iSH Shell (Alpine iOS)
```bash
apk update && apk add curl python3 && curl -fsSL https://raw.githubusercontent.com/TeaInMud/Tea-Package-Manager/refs/heads/master/tpm/install/iOS/iOS.py | python3
```

### For Termux (Android)
```bash
pkg update && pkg install curl python && curl -fsSL https://raw.githubusercontent.com/TeaInMud/Tea-Package-Manager/refs/heads/master/tpm/install/Android/android.py | python
```

---

## 🛠️ Usage & Commands

```bash
# Install a custom package from the global cloud registry
tea add -c <package-name>

# Update a specific custom package to its latest version
tea update <package-name>

# Update all locally installed custom packages at once
tea update all

# Search the global registry for available tools
tea search <query>

# List all available custom packages globally
tea list

# Fallback pass-through to native package managers (apk / pkg)
tea add <native-package>
```

---

## 📂 The Ecosystem Repository Stack

The ecosystem is split into multiple modules for cleaner management:

1. **`tea` (Core Manager):** The script managed right here in this repository. Handles searching, downloading, updating, and syncing packages.
2. **[tpm.reg.py](https://github.com/TeaInMud/Tea-Package-Manager/blob/master/tpm/registry/tpm.reg.py):** Holds the centralized global registry file `tea-registry.py`.
3. **`better-git`:** A custom tool packaged via TPM that builds a streamlined, user-friendly wrapper around Git commands for faster mobile commits (`better-git save`, `better-git sync`).

---

## ➕ Contributing & Registering Packages

To add a new script or utility to the global `tea` ecosystem:
1. Upload your shell (`.sh`) or Python (`.py`) file to a public GitHub repository.
2. Open a Pull Request or Issue on the **[TPM-Registry](https://github.com)** repository.
3. Append your new application identifier and its raw GitHub link into the `PACKAGES` dictionary block:

```python
PACKAGES = {
    "package name": "raw github url"
}
```
