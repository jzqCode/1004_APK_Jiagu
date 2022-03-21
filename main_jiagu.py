from python.JGApplication import JGApplication
from python.plugin.APKPlugin import APKPlugin
from python.plugin.FilePlugin import FilePlugin
from python.plugin.HookModulePlugin import HookModulePlugin
from python.plugin.ZipPlugin import ZipPlugin
from python.utils.CacheUtil import CacheUtil

if __name__ == '__main__':
    cache_util = CacheUtil("jiagu_apk_info", "main_jiagu.ini")
    apk_file_name = cache_util.read_value_from_cache("apk_file_name")
    signature_file = cache_util.read_value_from_cache("signature_file")
    android_sdk_path = cache_util.read_value_from_cache("android_sdk_path", 'D\\:\\\\Android_SDK')
    gradle_path = cache_util.read_value_from_cache("gradle_path", "gradle")
    print("1.请确认配置了 jdk环境变量")
    print("2.请确认文件路径 没有中文")
    print(f"3.当前配置的apk文件为 {apk_file_name}")
    print(f"4.当前配置的签名文件为 {signature_file}")
    print(f"5.当前配置的gradle_path路径为 {gradle_path}")
    print(f"6.当前配置的android_sdk路径为 {android_sdk_path}")
    input("输入任意内容以便开始任务")
    apk_file_dir = apk_file_name.replace(".apk", "")
    FilePlugin.remove_path_file(apk_file_dir)
    ZipPlugin.un_zip_file(apk_file_name, apk_file_dir)
    axml_file = f"{apk_file_dir}\\AndroidManifest.xml"
    axml_decode_file = "AndroidManifest_decode.xml"
    # 解密axl
    APKPlugin.decode_amxl(axml_file, axml_decode_file)
    apk_name, apk_package, app_version_name = APKPlugin.get_apk_info(axml_decode_file)
    # 或许代理自定义代理app的相关参数
    package_middle = apk_package.split(".")[1]
    package_middle = "proxy" + package_middle
    proxy_aar_file = f"{package_middle}.aar"
    proxy_application_name = f"com.{package_middle}.core.ProxyApplication"
    # 替换axml
    JGApplication.change_apk_manifest_txt(axml_decode_file, proxy_application_name, apk_package, app_version_name)
    APKPlugin.encode_amxl(axml_decode_file, axml_file)
    FilePlugin.remove_path_file(axml_decode_file)
    # 加密dex文件
    apk_file_xed_name = apk_file_name.replace(".apk", "_xed.apk")
    JGApplication.encrypt_dex(apk_file_dir, "1234567890123456", "1234567890123456")
    # 修改AndroidSDK路径
    FilePlugin.wirte_str_to_file('sdk.dir=' + android_sdk_path, "HookApplication/local.properties")
    HookModulePlugin.change_core_app_package(HookModulePlugin.origin_name, package_middle)
    HookModulePlugin.make_proxy_core_app(gradle_path=gradle_path)
    HookModulePlugin.change_core_app_package(package_middle, HookModulePlugin.origin_name)
    FilePlugin.move_file("HookApplication/Proxy_Core/build/outputs/aar/Proxy_Core-release.aar", proxy_aar_file)
    ZipPlugin.un_zip_file(proxy_aar_file, "proxy_aar_temp")
    APKPlugin.change_jar_to_dex("proxy_aar_temp/classes.jar")
    FilePlugin.move_file("proxy_aar_temp/classes.dex", f"{apk_file_dir}/classes.dex")
    FilePlugin.remove_path_file("proxy_aar_temp")
    FilePlugin.remove_path_file(proxy_aar_file)
    ZipPlugin.make_zip_dir(apk_file_dir, apk_file_xed_name)
    FilePlugin.remove_path_file(apk_file_dir)
    # 重新签名
    APKPlugin.signer_apk_file(signature_file, apk_file_xed_name,
                              apk_file_xed_name.replace("_xed.apk", "_signer.apk"))
    FilePlugin.remove_path_file(apk_file_xed_name)
