import os
import xml.dom.minidom


class APKPlugin:

    @staticmethod
    def unzip_apk_file(apk_file_name, output_dir=None):
        """
        解压ak文件到指定目录
        :param apk_file_name:
        :param output_dir:
        :return:
        """
        if output_dir is None:
            output_dir = apk_file_name.replace(".apk", "")
        if not os.path.exists(output_dir):
            print("开始反编译原apk...")
            cmd = f'java -jar lib\\apk_tool.jar d {apk_file_name} -o {output_dir}'
            if os.system(cmd) == 0:
                print("成功反编译原apk")
            else:
                raise Exception("反编译原apk失败")

    @staticmethod
    def zip_apk_file(apk_file_dir, apk_file=None):
        """
        把apk_file_dir文件夹打包成apk
        :param signer_file:
        :param apk_file_dir:
        :param apk_file:
        :return:
        """
        if apk_file is None:
            apk_file = apk_file_dir + ".apk"
        print("开始打包新的apk...")
        cmd_zip = f'java -jar lib\\apk_tool.jar b {apk_file_dir} -o {apk_file}'
        if os.system(cmd_zip) == 0:
            print("成功打包新的apk")
        else:
            raise Exception("打包新的apk失败")

    @staticmethod
    def signer_apk_file(signer_file, apk_file, signer_apk_file=None):
        """
        为apk签名
        :param signer_apk_file:
        :param signer_file:
        :param apk_file:
        :return:
        """
        if signer_apk_file is None:
            signer_apk_file = apk_file.replace(".apk", "_signer.apk")
        print("开始为新的apk签名...")
        cmd_signer = f'java -jar lib\\apk_signer.jar sign  --ks {signer_file} --ks-key-alias yeyan --ks-pass pass:yeyan123 --key-pass  pass:yeyan123 --out {signer_apk_file} {apk_file}'
        if os.system(cmd_signer) == 0:
            print("成功为新的apk签名")
        else:
            raise Exception("为新的apk签名失败")
        os.remove(signer_apk_file + ".idsig")

    @staticmethod
    def change_dex_to_jar(dex_file, jar_file=None):
        """
        把dex转化成jar
        :param dex_file:
        :param jar_file:
        :return:
        """
        if dex_file is None:
            jar_file = dex_file.replace(".dex", ".jar")
        cmd = f'dex2jar-2.0/d2j-dex2jar.bat  --output {dex_file} {jar_file}'
        if os.system(cmd) == 0:
            print("成功把dex文件转化为jar文件")
        else:
            raise Exception("dex文件转化失败")

    @staticmethod
    def change_jar_to_dex(jar_file, dex_file=None):
        """
        把jar转化成dex
        :param jar_file:
        :param dex_file:
        :return:
        """
        if dex_file is None:
            dex_file = jar_file.replace(".jar", ".dex")
        cmd = f'dx --dex --output {dex_file} {jar_file}'
        if os.system(cmd) == 0:
            print("成功把jar文件转化为dex文件")
        else:
            raise Exception("jar文件转化为dex文件失败")

    @staticmethod
    def decode_amxl(axml_file, par_file=None):
        """
        解析 android_manifest_file
        :param axml_file:
        :param par_file:
        :return:
        """
        if par_file is None:
            par_file = axml_file.replace(".xml", "_new.xml")
        cmd = f'java -jar lib\\apk_axml_tool.jar d {axml_file} {par_file}'
        if os.system(cmd) == 0:
            print("成功解析axml文件")
        else:
            raise Exception("axml文件解析失败") @ staticmethod

    @staticmethod
    def decode_apk_by_axml_print(axml_file, par_file=None):
        """
        解析 android_manifest_file
        :param axml_file:
        :param par_file:
        :return:
        """
        if par_file is None:
            par_file = axml_file.replace(".xml", "_new.xml")
        cmd = f'java -jar lib\\apk_axml_print.jar {axml_file} {par_file}'
        if os.system(cmd) == 0:
            print("成功解析axml文件")
        else:
            raise Exception("axml文件解析失败")

    @staticmethod
    def encode_amxl(axml_file, par_file=None):
        """
        加密 android_manifest_file
        :param axml_file:
        :param par_file:
        :return:
        """
        if par_file is None:
            par_file = axml_file.replace(".xml", "_new.xml")
        cmd = f'java -jar lib\\apk_axml_tool.jar e {axml_file} {par_file}'
        if os.system(cmd) == 0:
            print("成功加密axml文件")
        else:
            raise Exception("axml文件加密失败")

    @staticmethod
    def get_apk_info(android_manifest_file):
        """
        获取原始apk的信息
        :param android_manifest_file:
        :return:
        """
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(android_manifest_file)
        document_element = DOMTree.documentElement
        apk_package = document_element.getAttribute("package")
        app_version_name = document_element.getAttribute("android:versionName")
        ele_application = document_element.getElementsByTagName("application")[0]
        app_name = ele_application.getAttribute("android:name")
        return app_name, apk_package, app_version_name

    #
    # @staticmethod
    # def encrypt_apk_dex_by_java(apk_file_name, proxy_app_aar, new_apk_file_name=None):
    #     """
    #     加密dex文件为xed文件
    #     :param proxy_app_aar:
    #     :param apk_file_name:
    #     :param new_apk_file_name:
    #     :return:
    #     """
    #     if new_apk_file_name is None:
    #         new_apk_file_name = apk_file_name.replace(".apk", "_01.apk")
    #     app_name, apk_package, app_version_name = APKPlugin.get_apk_info(apk_file_name)
    #     package_middle = apk_package.split(".")[1]
    #     cmd_aes_dex = f'java -jar lib\\apk_proxy_tools.jar {apk_file_name} {proxy_app_aar} {signer}{package_middle} {new_apk_file_name}'
    #     if os.system(cmd_aes_dex) == 0:
    #         print("dex文件加密成功")
    #     else:
    #         print("dex文件加密失败")
