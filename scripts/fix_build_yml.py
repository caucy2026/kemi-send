#!/usr/bin/env python3
"""Fix build.yml: remove secrets from step-level if, replace actions-rs/toolchain."""
import re

path = "/Volumes/ORICO/kemi/kemi-send/.github/workflows/build.yml"
src = open(path, encoding="utf-8").read()

# 1. key.properties decode step - remove `if:` with secrets, use tolerant shell
pat1 = re.compile(
    r"- name: Decode key\.properties\n"
    r"(\s*)if: \${{ secrets\.ANDROID_KEY_PROPERTIES != '' }}\n"
    r"(\s*)env:\n"
    r"(\s*)ENCODED_STRING: \${{ secrets\.ANDROID_KEY_PROPERTIES }}\n"
    r"(\s*)run: echo \$ENCODED_STRING \| base64 -di > app/android/key\.properties",
    re.M,
)
rep1 = (
    "- name: Decode key.properties\n"
    r"\1env:\n"
    r"\3ENCODED_STRING: ${{ secrets.ANDROID_KEY_PROPERTIES }}\n"
    r"\4run: |\n"
    r"\4  if [ -n \"$ENCODED_STRING\" ]; then\n"
    r"\4    echo \"$ENCODED_STRING\" | base64 -di > app/android/key.properties\n"
    r"\4  fi"
)
src, n1 = pat1.subn(rep1, src)

# 2. keystore decode step
pat2 = re.compile(
    r"- name: Decode keystore\n"
    r"(\s*)if: \${{ secrets\.ANDROID_KEY_STORE != '' }}\n"
    r"(\s*)env:\n"
    r"(\s*)ENCODED_STRING: \${{ secrets\.ANDROID_KEY_STORE }}\n"
    r"(\s*)run: mkdir -p android-keystore && echo \$ENCODED_STRING \| base64 -di > android-keystore/kemi-send\.keystore",
    re.M,
)
rep2 = (
    "- name: Decode keystore\n"
    r"\1env:\n"
    r"\3ENCODED_STRING: ${{ secrets.ANDROID_KEY_STORE }}\n"
    r"\4run: |\n"
    r"\4  if [ -n \"$ENCODED_STRING\" ]; then\n"
    r"\4    mkdir -p android-keystore\n"
    r"\4    echo \"$ENCODED_STRING\" | base64 -di > android-keystore/kemi-send.keystore\n"
    r"\4  fi"
)
src, n2 = pat2.subn(rep2, src)

# 3. actions-rs/toolchain -> dtolnay/rust-toolchain@stable (global, 3x)
pat3 = re.compile(
    r"uses: actions-rs/toolchain@v1\n(\s*)with:\n(\s*)toolchain: \${{ env\.RUST_VERSION }}\n(\s*)override: true",
    re.M,
)
src, n3 = pat3.subn("uses: dtolnay/rust-toolchain@stable", src)

open(path, "w", encoding="utf-8").write(src)
print(f"key.properties 修复: {n1} 处")
print(f"keystore 修复: {n2} 处")
print(f"actions-rs 替换: {n3} 处")
