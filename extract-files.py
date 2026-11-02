#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/dada-miuicamera',
]


def lib_fixup_system_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'system' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    'vendor.xiaomi.hardware.campostproc@1.0': lib_fixup_system_suffix,
    'libcameraopt': lib_fixup_system_suffix,
    'vendor.xiaomi.hardware.misys@1.0': lib_fixup_system_suffix,
    'vendor.xiaomi.hardware.misys@3.0': lib_fixup_system_suffix,
    'vendor.xiaomi.hardware.bgservice@1.0': lib_fixup_system_suffix,
    'vendor.xiaomi.hardware.aidlbgservice-V1-ndk': lib_fixup_system_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'system/lib64/libcamera_algoup_jni.xiaomi.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system/lib64/libcamera_mianode_jni.xiaomi.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system/lib64/libmicar_algoengine_jni.xiaomi.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system/lib64/libvirtualcamera_surfaceutils_jni.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system/lib64/libmigui.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system/lib64/libmicampostproc_client.so': blob_fixup()
        .remove_needed('libhidltransport.so'),
    'system/lib64/libmisys_jni.xiaomi.so': blob_fixup()
        .remove_needed('libhidltransport.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'dada-miuicamera',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
