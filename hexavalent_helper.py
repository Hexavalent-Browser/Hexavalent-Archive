#!/usr/bin/env python3

"""
hexavalent-helper.py

Helper script for patching, branding, and generating build
configuration for Hexavalent.

Run like hexavalent-helper.py --help for more info.
"""

import argparse
import pathlib
import platform
import re
import shutil
import subprocess
import sys

# Hash tables are cool!
config = {
    # All targets for which hexavalent can currently build.
    "targets": {
        # Path to OS specific patches and GN args -- relative to
        # Hexavalent source directory.
        # "Common" is not a real OS target. It is only for specifying
        # patches that will be applied for all target OS. No GN args
        # for "common" either as it doesn't make sense.
        "common": {
            "patches": "patches",
            "gn_args": None,
        },
        "linux": {
            "patches": "patches/linux",
            "gn_args": "linux_args.gn",
        },
        # "mac": {
        #     "patches": "patches/mac",
        #     "gn_args": "mac_args.gn",
        # },
        "windows": {
            "patches": "patches/windows",
            "gn_args": "windows_args.gn",
        },
    },
    "branding": {
        # Directory containing icons -- relative to Hexavalent source
        # directory. Its contents will be copied directly to chromium
        # source directory.
        "icons": "icons",
        "replacement": {
            # Replace the given pattern in the following files:
            # It is a list of dicts (hash tables) with the following convention:
            # file_path (relative to chromium source): pattern.
            "files": [
                # UI Strings
                {
                    "chrome/app/theme/chromium/BRANDING": "(C|c)hromium",
                    "chrome/app/chromium_strings.grd": "Chromium",
                    "chrome/app/settings_chromium_strings.grdp": "Chromium",
                    "components/components_chromium_strings.grd": "(?<!</ph>)Chromium",
                },
                # Profile Path
                {
                    # Windows: Profile path is CHROME_INSTALL_DIR/User Data
                    "chrome/install_static/chromium_install_modes.cc": '(C|c)hromium(?=";)',
                },
                # Chromium binaries
                {
                    # chrome.exe
                    # * Icon
                    "chrome/app/chrome_exe.rc": "chromium(?=\.ico)",
                    # * In GN config
                    "chrome/BUILD.gn": "chrome(?=\.exe)|(?<=initialexe/)chrome",
                    "chrome/installer/mini_installer/BUILD.gn": "chrome(?=\.exe)",
                    # * In source code
                    "chrome/common/chrome_constants.cc": "chrome(?=\.exe)",
                    "chrome/tools/build/win/FILES.cfg": "chrome(?=\.exe)",
                    "chrome/installer/mini_installer/chrome.release": "chrome(?=\.exe)",
                    "chrome/tools/build/win/release.rules": "chrome(?=\.exe)",
                    "chrome/installer/util/util_constants.cc": "chrome(?=\.exe)",
                    "tools/clang/scripts/goma_link.py": "chrome(?=\.exe)",
                    "infra/scripts/sizes.py": "chrome(?=\.exe)",
                    "infra/archive_config/win-tagged.json": "chrome(?=\.exe)",
                    "tools/binary_size/sizes.py": "chrome(?=\.exe)",
                    "tools/bisect_repackage/bisect_repackage.py": "chrome(?=\.exe)",
                    "chrome/browser/safe_browsing/incident_reporting/binary_integrity_analyzer_win.cc": "chrome(?=\.exe)",
                    "build/win/reorder-imports.py": "chrome(?=\.exe)",
                    "chrome/app/chrome_exe.ver": "chrome(?=\.exe)",
                    "chrome/app/chrome_exe.vsprops": "chrome(?=\.exe)",
                    "chrome/chrome_cleaner/components/system_report_component.cc": "chrome(?=\.exe)",
                    "chrome/installer/launcher_support/chrome_launcher_support.cc": "chrome(?=\.exe)",
                    "chrome/chrome_cleaner/components/reset_shortcuts_component.cc": "chrome(?=\.exe)",
                    "tools/win/ChromeDebug/ChromeDebug/AttachDialog.cs": "chrome(?=\.exe)",
                    "chrome/browser/browser_switcher/bho/browser_switcher_core.cc": "chrome(?=\.exe)",
                    "chrome/browser/browser_switcher/bho/mini_bho.cc": "chrome(?=\.exe)",
                    "chrome/browser/browser_switcher/alternative_browser_driver_win.cc": "chrome(?=\.exe)",
                    "chrome/notification_helper/notification_activator.cc": "Chrome(?=\.exe)",
                    "chrome/browser/profile_resetter/resettable_settings_snapshot.cc": "chrome(?=\.exe)",
                    "components/crash/content/app/hard_error_handler_win.cc": "chrome(?=\.exe)",
                    "tools/bisect-builds.py": "chrome(?=\.exe)",
                    "tools/win/copy-installer.bat": "chrome(?=\.exe)",
                    "tools/variations/bisect_variations.py": "chrome(?=\.exe)",
                    "tools/win/IdleWakeups/idle_wakeups.cpp": "chrome(?=\.exe)",
                    # * In tests
                    "chrome/test/BUILD.gn": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_dev_installed.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_user_installed.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_beta_installed.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_system_installed.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_canary_installed.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/previous_chrome_user_installed.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/previous_chrome_canary_installed.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/previous_chrome_system_installed.prop": "chrome(?=\.exe)",
                    "chrome/browser/safe_browsing/incident_reporting/binary_integrity_analyzer_win_unittest.cc": "chrome(?=\.exe)",
                    "chrome/browser/chrome_browser_main_win_unittest.cc": "chrome(?=\.exe)",
                    "chrome/test/chromedriver/test/run_py_tests.py": "chrome(?=\.exe)",
                    "chrome/chrome_cleaner/components/system_report_component_unittest.cc": "chrome(?=\.exe)",
                    "chrome/browser/browser_switcher/browser_switcher_service_browsertest.cc": "chrome(?=\.exe)",
                    "chrome/browser/browser_switcher/alternative_browser_driver_unittest.cc": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_user_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_system_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_canary_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_dev_not_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_user_not_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_beta_not_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_canary_not_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/mini_installer/config/chrome_system_not_inuse.prop": "chrome(?=\.exe)",
                    "chrome/test/enterprise/e2e/policy/webprotect_bulk_text_entry/webprotect_bulk_text_entry_webdriver.py": "chrome(?=\.exe)",
                    "tools/accessibility/nvda/nvda_chrome_tests.py": "chrome(?=\.exe)",
                    "chrome/install_static/product_install_details_unittest.cc": "chrome(?=\.exe)",
                    "chrome/credential_provider/test/gcp_gls_output_unittest.cc": "chrome(?=\.exe)",
                    "native_client_sdk/src/build_tools/find_chrome.py": "chrome(?=\.exe)",
                    "chrome/browser/win/uninstallation_via_os_settings_unittest.cc": "chrome(?=\.exe)",
                    "chrome/credential_provider/gaiacp/gaia_credential_unittests.cc": "chrome(?=\.exe)",
                    "chrome/credential_provider/gaiacp/reauth_credential_unittests.cc": "chrome(?=\.exe)",
                    "chrome/credential_provider/gaiacp/gaia_credential_other_user_unittests.cc": "chrome(?=\.exe)",
                    "chrome/test/enterprise/e2e/policy/user_data_dir/user_data_dir_webdriver.py": "chrome(?=\.exe)",
                    "chrome/test/enterprise/e2e/policy/translate_enabled/translate_enabled_webdriver_test.py": "chrome(?=\.exe)",
                    "ppapi/native_client/tools/browser_tester/browsertester/browserlauncher.py": "chrome(?=\.exe)",
                    "components/metrics/call_stack_profile_builder_unittest.cc": "chrome(?=\.exe)",
                    "content/test/gpu/measure_power_intel.py": "chrome(?=\.exe)",
                    "tools/ipc_fuzzer/scripts/play_testcase.py": "chrome(?=\.exe)",
                    "testing/scripts/run_variations_smoke_tests.py": "chrome(?=\.exe)",
                },
                {
                    # chrome_proxy.exe
                    # * In GN config
                    "chrome/chrome_proxy/BUILD.gn": 'executable\("chrome_proxy"\) \{(?!\n  output_name)',
                    # * In source code
                    "chrome/chrome_proxy/chrome_proxy_main_win.cc": "chrome(?=_proxy\.exe)",
                    "chrome/installer/mini_installer/chrome.release": "chrome(?=_proxy\.exe)",
                    "chrome/tools/build/win/FILES.cfg": "chrome(?=_proxy\.exe)",
                    "chrome/installer/util/util_constants.cc": "chrome(?=_proxy\.exe)",
                    "infra/archive_config/win-tagged.json": "chrome(?=_proxy\.exe)",
                    "tools/binary_size/sizes.py": "chrome(?=_proxy\.exe)",
                    "tools/checkbins/checkbins.py": "chrome(?=_proxy\.exe)",
                    "chrome/browser/web_applications/web_app_shortcut_win.cc": "chrome(?=_proxy\.exe)",
                    "chrome/chrome_proxy/chrome_proxy.ver": "chrome(?=_proxy\.exe)",
                    # * In tests
                    "chrome/test/mini_installer/config/chrome_dev_installed.prop": "chrome(?=_proxy\.exe)",
                    "chrome/test/mini_installer/config/chrome_user_installed.prop": "chrome(?=_proxy\.exe)",
                    "chrome/test/mini_installer/config/chrome_beta_installed.prop": "chrome(?=_proxy\.exe)",
                    "chrome/test/mini_installer/config/chrome_system_installed.prop": "chrome(?=_proxy\.exe)",
                    "chrome/test/mini_installer/config/chrome_canary_installed.prop": "chrome(?=_proxy\.exe)",
                    "chrome/test/mini_installer/config/previous_chrome_user_installed.prop": "chrome(?=_proxy\.exe)",
                    "chrome/test/mini_installer/config/previous_chrome_canary_installed.prop": "chrome(?=_proxy\.exe)",
                    "chrome/test/mini_installer/config/previous_chrome_system_installed.prop": "chrome(?=_proxy\.exe)",
                },
                {
                    # chrome.dll
                    # * Icon
                    "chrome/app/chrome_dll.rc": "chromium(?=\.ico)",
                    # * In GN config
                    "chrome/BUILD.gn": '(?<=output_name = ")chrome|chrome(?=\.dll)',
                    "chrome/installer/mini_installer/BUILD.gn": "chrome(?=\.dll)",
                    # * In source code
                    "chrome/common/chrome_constants.cc": "chrome(?=\.dll)",
                    "chrome/installer/mini_installer/chrome.release": "chrome(?=\.dll)",
                    "chrome/installer/util/util_constants.cc": "chrome(?=\.dll)",
                    "chrome/tools/build/win/FILES.cfg": "chrome(?=\.dll)",
                    "chrome/tools/build/win/release.rules": "chrome(?=\.dll)",
                    "infra/archive_config/win-tagged.json": "chrome(?=\.dll)",
                    "tools/clang/scripts/goma_link.py": "chrome(?=\.dll)",
                    "infra/scripts/sizes.py": "chrome(?=\.dll)",
                    "tools/binary_size/sizes.py": "chrome(?=\.dll)",
                    "tools/bisect_repackage/bisect_repackage.py": "chrome(?=\.dll)",
                    "chrome/browser/safe_browsing/incident_reporting/environment_data_collection_win.cc": "chrome(?=\.dll)",
                    "chrome/browser/safe_browsing/incident_reporting/binary_integrity_analyzer_win.cc": "chrome(?=\.dll)",
                    "chrome/app/chrome_dll.ver": "chrome(?=\.dll)",
                    "chrome/tools/build/win/create_installer_archive.py": "chrome(?=\.dll)",
                    "ui/base/resource/resource_bundle.cc": "chrome(?=\.dll)",
                    "components/browser_watcher/extended_crash_reporting.cc": "chrome(?=\.dll)",
                    "tools/win/pe_summarize.py": "chrome(?=\.dll)",
                    "tools/win/sizeviewer/sizeviewer.py": "chrome(?=\.dll)",
                    # * In tests
                    "chrome/test/mini_installer/config/chrome_dev_installed.prop": "chrome(?=\.dll)",
                    "chrome/test/mini_installer/config/chrome_user_installed.prop": "chrome(?=\.dll)",
                    "chrome/test/mini_installer/config/chrome_beta_installed.prop": "chrome(?=\.dll)",
                    "chrome/test/mini_installer/config/chrome_system_installed.prop": "chrome(?=\.dll)",
                    "chrome/test/mini_installer/config/chrome_canary_installed.prop": "chrome(?=\.dll)",
                    "chrome/test/mini_installer/config/previous_chrome_user_installed.prop": "chrome(?=\.dll)",
                    "chrome/test/mini_installer/config/previous_chrome_canary_installed.prop": "chrome(?=\.dll)",
                    "chrome/test/mini_installer/config/previous_chrome_system_installed.prop": "chrome(?=\.dll)",
                    "chrome/browser/safe_browsing/incident_reporting/binary_integrity_analyzer_win_unittest.cc": "chrome(?=\.dll)",
                    "chrome/test/delayload/delayloads_unittest.cc": "chrome(?=\.dll)",
                    "chrome/chrome_elf/third_party_dlls/packed_list_file_unittest.cc": "chrome(?=\.dll)",
                    "chrome/installer/util/delete_old_versions_unittest.cc": "chrome(?=\.dll)",
                },
                {
                    # chrome_elf.dll
                    # * In GN config
                    "chrome/chrome_elf/BUILD.gn": 'shared_library\("chrome_elf"\) \{(?!\n  output_name)',
                    # * In source code
                    "chrome/common/chrome_constants.cc": "chrome(?=_elf\.dll)",
                    "chrome/installer/mini_installer/chrome.release": "chrome(?=_elf\.dll)",
                    "chrome/browser/safe_browsing/incident_reporting/environment_data_collection_win.cc": "chrome(?=_elf\.dll)",
                    "chrome/tools/build/win/FILES.cfg": "chrome(?=_elf\.dll)",
                    "chrome/browser/safe_browsing/incident_reporting/binary_integrity_analyzer_win.cc": "chrome(?=_elf\.dll)",
                    "infra/archive_config/win-tagged.json": "chrome(?=_elf\.dll)",
                    "infra/scripts/sizes.py": "chrome(?=_elf\.dll)",
                    "build/win/reorder-imports.py": "chrome(?=_elf\.dll)",
                    "tools/bisect_repackage/bisect_repackage.py": "chrome(?=_elf\.dll)",
                    "chrome/chrome_elf/chrome_elf.ver": "chrome(?=_elf\.dll)",
                    "chrome/chrome_elf/chrome_elf_x64.def": "chrome(?=_elf\.dll)",
                    "chrome/chrome_elf/chrome_elf_x86.def": "chrome(?=_elf\.dll)",
                    "chrome/chrome_elf/chrome_elf_arm64.def": "chrome(?=_elf\.dll)",
                    "chrome/app/version_assembly/version_assembly_manifest.template": "chrome(?=_elf\.dll)",
                    # * In tests
                    "chrome/browser/safe_browsing/incident_reporting/binary_integrity_analyzer_win_unittest.cc": "chrome(?=_elf\.dll)",
                    "chrome/chrome_elf/pe_image_safe/pe_image_safe_unittest.cc": "chrome(?=_elf\.dll)",
                    "chrome/test/delayload/delayloads_unittest.cc": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/chrome_beta_installed.prop": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/chrome_canary_installed.prop": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/chrome_dev_installed.prop": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/chrome_system_installed.prop": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/chrome_user_installed.prop": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/previous_chrome_canary_installed.prop": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/previous_chrome_system_installed.prop": "chrome(?=_elf\.dll)",
                    "chrome/test/mini_installer/config/previous_chrome_user_installed.prop": "chrome(?=_elf\.dll)",
                },
                {
                    # chrome_pwa_launcher.exe
                    # * Icon
                    "chrome/browser/web_applications/chrome_pwa_launcher/chrome_pwa_launcher_exe.rc": '(?<=ICON ")chrome',
                    # * In GN config
                    "chrome/browser/web_applications/chrome_pwa_launcher/BUILD.gn": 'executable\("chrome_pwa_launcher"\) \{(?!\n  output_name)',
                    # * In source code
                    "chrome/browser/web_applications/chrome_pwa_launcher/chrome_pwa_launcher.ver": "chrome(?=_pwa_launcher\.exe)",
                    "chrome/browser/web_applications/chrome_pwa_launcher/chrome_pwa_launcher_util.cc": "chrome(?=_pwa_launcher\.exe)",
                    "chrome/installer/mini_installer/chrome.release": "chrome(?=_pwa_launcher\.exe)",
                    "chrome/tools/build/win/FILES.cfg": "chrome(?=_pwa_launcher\.exe)",
                    "infra/archive_config/win-tagged.json": "chrome(?=_pwa_launcher\.exe)",
                    "tools/checkbins/checkbins.py": "chrome(?=_pwa_launcher\.exe)",
                    # * In tests
                    "chrome/browser/web_applications/chrome_pwa_launcher/launcher_update_unittest.cc": "chrome(?=_pwa_launcher\.exe)",
                },
                {
                    # TODO
                    # Change the target name from chrome to hexavalent, so we can build like:
                    # ninja hexavalent
                    "chrome/BUILD.gn": '(?<=group\(")chrome(?="\))|(?<=:)chrome(?=")',
                    "chrome/test/BUILD.gn": '"//chrome"',
                    "chrome/installer/mini_installer/BUILD.gn": '"//chrome"',
                    "chrome/test/chromedriver/BUILD.gn": '(?<="//chrome:)chrome(?=")',
                    "chromeos/lacros/BUILD.gn": '(?<="//chrome:)chrome(?=")',
                    "BUILD.gn": '(?<="//chrome:)chrome(?=")|"//chrome"',
                    "testing/buildbot/gn_isolate_map.pyl": '(?<="//chrome:)chrome(?=")',
                    "build/config/chromeos/rules.gni": '"//chrome"',
                    "tools/perf/chrome_telemetry_build/BUILD.gn": '"//chrome"',
                    "chrome/installer/linux/BUILD.gn": '"//chrome"',
                    "media/BUILD.gn": '"//chrome"',
                    "media/midi/BUILD.gn": '"//chrome"',
                    "gpu/BUILD.gn": '"//chrome"',
                    "components/viz/BUILD.gn": '"//chrome"',
                },
                # Chromium ProgID prefix, install modes and details.
                {
                    "chrome/install_static/chromium_install_modes.cc": '(?<=")(C|c)hromium',
                    "chrome/install_static/product_install_details_unittest.cc": "(?<=\\\\)Chromium",
                    "chrome/install_static/install_util_unittest.cc": '(C|c)hromium(?=")',
                    "chrome/install_static/user_data_dir_win_unittest.cc": "(?<=\\\\)Chromium",
                    "chrome/installer/launcher_support/chrome_launcher_support.cc": "(?<=\\\\)Chromium",
                    "chrome/installer/mini_installer/mini_installer_constants.cc": "(?<=\\\\)Chromium",
                    "chrome/installer/setup/install_worker_unittest.cc": "(?<=\\\\)Chromium",
                    "chrome/installer/setup/installer_crash_reporter_client.cc": "(?<=\\\\)Chromium",
                    "chrome/installer/util/logging_installer.cc": "chromium",
                },
                # {
                #     # TODO Merge these with the rest. It is basically duck's branding patch.
                #     "base/files/file_util_posix.cc": "(?<=\.)(C|c)hromium",
                #     "base/mac/foundation_util.mm": "(?<=\.)(C|c)hromium",
                #     "chrome/app/theme/chromium/win/README": "chromium(?=\.ico)",
                #     "chrome/common/channel_info_posix.cc": "chromium",
                #     "chrome/common/chrome_content_client_constants.cc": "Chromium(?= PDF)",
                #     "chrome/common/chrome_constants.cc": '(?<=")Chromium(?=")',
                #     "chrome/common/chrome_paths.cc": "(?<=/)(C|c)hromium(?=/)",
                #     "chrome/common/chrome_paths_linux.cc": '(?<=data_dir_basename = ")chromium',
                #     "chrome/common/chrome_paths_mac.mm": '(?<=product_dir_name = ")Chromium',
                #     "chrome/common/service_process_util_linux.cc": '(?<=")(C|c)hromium',
                #     "chrome/common/service_process_util_posix.cc": "(?<=\.)(C|c)hromium",
                #     "chrome/install_static/chromium_install_modes.cc": '(?<=")(C|c)hromium',
                #     "chrome/installer/mini_installer/mini_installer_constants.cc": "(?<=\\\\)Chromium",
                #     "chrome/installer/util/logging_installer.cc": "chromium",
                #     "chrome/updater/branding.gni": '(?<=("|\.))(C|c)hromium',
                #     "components/os_crypt/key_storage_linux.cc": '(?<=")(C|c)hromium',
                #     "components/os_crypt/keychain_password_mac.mm": '(?<=")(C|c)hromium',
                #     "components/sync/engine/net/url_translator.cc": '(?<=")(C|c)hromium',
                #     "remoting/branding_Chromium": "(C|c)hromium",
                #     "tools/mac/power/utils.py": '(?<=("|\.))(C|c)hromium',
                # },
            ],
            # Replace the following strings with the alternative if found in above files.
            # string_to_replace: alternative_string
            "strings": {
                "Chromium": "Hexavalent",
                "chromium": "hexavalent",
                "chrome": "hexavalent",
                'executable("chrome_proxy") {': 'executable("chrome_proxy") {\n  output_name = "hexavalent_proxy"\n',
                'shared_library("chrome_elf") {': 'shared_library("chrome_elf") {\n  output_name = "hexavalent_elf"\n',
                'executable("chrome_pwa_launcher") {': 'executable("chrome_pwa_launcher") {\n  output_name = "hexavalent_pwa_launcher"\n',
                '"//chrome"': '"//chrome:hexavalent"',
            },
        },
    },
}


class NoPatchFiles(Exception):
    """Indicate that no patch files found to apply."""

    pass


class InvalidTargetOS(Exception):
    pass


# Custom actions for argument parser.
class StrLower(argparse.Action):
    """Convert string to lowercase."""

    def __call__(self, parser, namespace, values, option_string) -> None:
        setattr(namespace, self.dest, values.lower())


def replace(pattern, repl, file_path):
    """
    Replace the strings matching the given pattern in the given file
    with repl, which can be either a string or a function (refer to
    python documentaion of re.sub).
    """
    # Read the file and replace the strings matching the pattern
    # with repl.
    with open(file_path, "r", newline="") as file:
        content = file.read()
        content = re.sub(pattern, repl, content)

    # Overwrite the modified content to the file. There is no
    # need of backing up the file as it is handeled by git.
    with open(file_path, "w", newline="") as file:
        file.write(content)


def apply_branding(chromium_src, hexavalent_src, branding_config):
    """
    Apply Hexavalent branding to chromium source.
    """
    # Copy Hexavalent icons to chromium source directory.
    shutil.copytree(
        pathlib.Path(hexavalent_src, branding_config["icons"]),
        chromium_src,
        dirs_exist_ok=True,
    )

    # Replace chromium strings with hexavalent in relevant files.
    # TODO Implement concurrency.
    for files in branding_config["replacement"]["files"]:
        for file_path, pattern in files.items():
            replace(
                pattern,
                lambda matchobj: branding_config["replacement"]["strings"].get(
                    matchobj.group()
                ),
                pathlib.Path.joinpath(chromium_src, file_path),
            )


def get_files(dir, pattern="*"):
    """
    Get list of all files in a directory whose name matches a given glob pattern.
    """
    # Get all contents of dir matching the given pattern, and filter the files.
    contents_dir = pathlib.Path(dir).glob(pattern)
    return [stuff for stuff in contents_dir if stuff.is_file()]


def apply_patches(chromium_src, patches):
    """
    Apply all patches from patches directory to chromium source.
    """
    # Get list of all patch files to apply. Raise exception if no patch files found.
    patch_files = get_files(patches, pattern="*.patch")
    if len(patch_files) == 0:
        raise NoPatchFiles

    # Apply all the patch files using git am.
    subprocess.run(["git", "-C", chromium_src, "am"] + patch_files)


def get_current_os():
    """
    Return the current operating system as a string of characters.
    """
    os_name = platform.system().lower()
    if os_name == "darwin":
        return "mac"
    else:
        return os_name


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # Command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chromium_src",
        metavar="CHROMIUM_SRC_DIR",
        type=pathlib.Path,
        help="Path to chromium source directory.",
    )
    parser.add_argument(
        "-x",
        "--hexavalent-src",
        metavar="PATH",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help="Path to Hexavalent source directory. Default: current directory.",
    )
    parser.add_argument(
        "-t",
        "--target",
        metavar="OS",
        action=StrLower,
        default=get_current_os(),
        help="Apply patches and GN args for this target OS. Default: current OS.",
    )
    parser.add_argument(
        "-g",
        "--gn-build-dir",
        metavar="PATH",
        default=None,
        help="Path to GN build directory, relative to chromium source.",
    )
    parser.add_argument(
        "-b",
        "--branding",
        action="store_true",
        help="Apply Hexavalent branding changes. Warning: Branding is WIP.",
    )
    parser.add_argument(
        "--no-patch", action="store_true", help="Do not apply patch files."
    )
    args = parser.parse_args()

    # Check if target is valid.
    if not args.target in config["targets"] or args.target == "common":
        raise InvalidTargetOS

    # Apply common and OS specific patches.
    if not args.no_patch:
        apply_patches(
            args.chromium_src,
            pathlib.Path(args.hexavalent_src, config["targets"]["common"]["patches"]),
        )
        try:
            apply_patches(
                args.chromium_src,
                pathlib.Path(
                    args.hexavalent_src, config["targets"][args.target]["patches"]
                ),
            )
        except NoPatchFiles:
            print("Warning: OS specific patch files not found.")

    # Copy GN configuration file from Hexavlent directory to GN build directory.
    if args.gn_build_dir:
        shutil.copyfile(
            pathlib.Path(
                args.hexavalent_src, config["targets"][args.target]["gn_args"]
            ),
            pathlib.Path(args.chromium_src, args.gn_build_dir, "args.gn"),
        )

    # Apply Hexavalent branding.
    if args.branding:
        apply_branding(args.chromium_src, args.hexavalent_src, config["branding"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
