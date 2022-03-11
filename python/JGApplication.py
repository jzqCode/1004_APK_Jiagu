import os
from threading import Thread

from androguard.core.bytecodes.apk import APK
from lxml import etree

from python.plugin.AESPlugin import AESPlugin
from python.plugin.FilePlugin import FilePlugin
from python.plugin.ZipPlugin import ZipPlugin


class JGApplication(Thread):

    def __init__(self, apk_name, signer_file=None, apk_dir=None):
        self.apk_name = apk_name
        self.signer_file = signer_file
        if apk_dir is None:
            self.apk_dir = apk_name.replace(".apk", "")

    # 修改manifest文件
    @staticmethod
    def change_apk_manifest(apk_file_name, proxy_application_name=None):
        apk = APK(apk_file_name)
        android_manifest_axml = apk.get_android_manifest_axml()
        axml = android_manifest_axml.get_xml_obj()
        # 获取原始app的数据，修改xml内容
        ele_application = axml.find('application')
        application_name = ele_application.attrib.get("{http://schemas.android.com/apk/res/android}name")
        apk_package = apk.get_package()
        app_version_name = apk.get_androidversion_name()
        if proxy_application_name is None:
            proxy_application_name = "com.proxymder.core.ProxyApplication"
        element_key_name = '{http://schemas.android.com/apk/res/android}name'
        element_key_value = '{http://schemas.android.com/apk/res/android}value'
        ele_application.set(element_key_name, f'{proxy_application_name}')
        etree.SubElement(ele_application, _tag='meta-data',
                         attrib={element_key_name: 'app_name', element_key_value: application_name})
        etree.SubElement(ele_application, _tag='meta-data',
                         attrib={element_key_name: 'app_version', element_key_value: app_version_name})
        etree.SubElement(ele_application, _tag='meta-data',
                         attrib={element_key_name: 'app_package', element_key_value: apk_package})
        axml_byte_buffer = etree.tostring(axml, pretty_print=True, encoding="utf-8")
        FilePlugin.wirte_byte_to_file(axml_byte_buffer, "AndroidManifest.xml")

    # 修改dex文件
    @staticmethod
    def change_apk_dex(apk_file_name):
        output_dir = apk_file_name.replace(".apk", "")
        ZipPlugin.un_zip_file(apk_file_name, output_dir)
        aesPlugin = AESPlugin("179D278870E26DBF", "FBD62E078872D971")
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)  # 原来的文件路径
                if file_path.find(".dex") != -1:
                    bytes = FilePlugin.read_byte_from_file(file_path)
                    decrypt_content = aesPlugin.encrypt_byte(bytes)
                    os.remove(file_path)
                    FilePlugin.wirte_byte_to_file(decrypt_content, file_path.replace(".dex", ".xed"))
        ZipPlugin.make_zip(output_dir, apk_file_name.replace(".apk", "._apk"))
