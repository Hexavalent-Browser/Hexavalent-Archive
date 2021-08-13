# Hexavalent

# A Chromium downstream project

# Why was this made?

- Linux distributions can be a mess. They don't package it properly.
- Existing packages are slow to update.
- To provide a reference for people who want to package Chromium.
- No "untouched" chromium with auto updates exists for Windows.

# Aims

- Use Clang/LLVM to compile Chromium as upstream intends.
- Use official builds only.
- Compile with modern security features that upstream provides.
- Be easy to maintain, clean, quick and efficent.
- Fast updates - no more than 4 days lag time ideally.
- Leverage the Windows hypervisor platform on Windows.

# Credits

 - The GrapheneOS project's Vanadium patchset.
   https://github.com/GrapheneOS/Vanadium
