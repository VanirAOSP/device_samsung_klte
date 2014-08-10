# Copyright (C) 2012 The Android Open Source Project
# Copyright (C) 2014 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Custom OTA commands for klte devices"""

gsm_bootloaders=["G900A", "G900T", "G900D", "G9005", "G900F", "G900W", "G900I", "G900M"]    # LIST OF ALL GSM BOOTLOADERS
cdma_bootloaders=["G900V", "G900P", "G900R4", "G900R6", "G900R7"]                           # LIST OF ALL CDMA BOOTLOADERS

def determineVariants(info, bootloader): # determines the specific sets of blobs to dump on top of /system/ recursively for this bootloader
  variants=["gsm","nfc"]
  if bootloader in cdma_bootloaders:
    variants=["cdma"]
    if bootloader == "G900P":   # special case for sprint NFC
      variants.append("nfcspr")
    elif bootloader == "G900V": #verizon uses sprint NFC and special sauce
      variants.append("nfcspr")
      variants.append("vzw")
    else:
      variants.append("nfc")    # else - use gsm nfc
  return variants

def writeVariantExtras(info, bootloader): # appendExtra the specficic directories to extract on top of /system/ for each one of all bootloaders
  for var in determineVariants(info,bootloader):
    extra = 'ifelse(is_substring("%s", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/%s/* /system/"));' % (bootloader, var)
    info.script.AppendExtra(extra)
    print extra

def FullOTA_InstallEnd(info):
  for bootloader in gsm_bootloaders+cdma_bootloaders:
    writeVariantExtras(info,bootloader)

  info.script.AppendExtra('delete_recursive("/system/blobs/");')
