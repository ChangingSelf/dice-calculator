import os
import subprocess
import sys


def create_installer():
    """创建简单的NSIS安装包"""
    print("开始创建安装包...")

    # 确保dist目录存在
    if not os.path.exists("dist"):
        print("错误：dist目录不存在，请先运行build.py进行打包")
        return False

    # 获取可执行文件路径
    exe_path = None
    for file in os.listdir("dist"):
        if file.endswith(".exe"):
            exe_path = os.path.join("dist", file)
            break

    if not exe_path:
        print("错误：在dist目录中找不到可执行文件")
        return False

    # 创建NSIS脚本
    with open("installer.nsi", "w", encoding="utf-8") as f:
        f.write("""
; 骰子概率计算器安装脚本
Unicode true

!include "MUI2.nsh"

; 基本信息
Name "骰子概率计算器"
OutFile "骰子概率计算器安装程序.exe"
InstallDir "$PROGRAMFILES\\骰子概率计算器"
InstallDirRegKey HKCU "Software\\骰子概率计算器" ""

; 界面设置
!define MUI_ABORTWARNING
!define MUI_ICON "dice_icon.ico"
!define MUI_UNICON "dice_icon.ico"

; 页面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; 语言
!insertmacro MUI_LANGUAGE "SimpChinese"

; 安装部分
Section "主程序" SecMain
  SetOutPath "$INSTDIR"
  
  ; 添加文件
  File "dist\\骰子概率计算器.exe"
  File "dist\\README.md"
  File "dice_icon.ico"
  
  ; 创建卸载程序
  WriteUninstaller "$INSTDIR\\卸载.exe"
  
  ; 创建开始菜单快捷方式
  CreateDirectory "$SMPROGRAMS\\骰子概率计算器"
  CreateShortcut "$SMPROGRAMS\\骰子概率计算器\\骰子概率计算器.lnk" "$INSTDIR\\骰子概率计算器.exe" "" "$INSTDIR\\dice_icon.ico"
  CreateShortcut "$SMPROGRAMS\\骰子概率计算器\\卸载.lnk" "$INSTDIR\\卸载.exe"
  
  ; 创建桌面快捷方式
  CreateShortcut "$DESKTOP\\骰子概率计算器.lnk" "$INSTDIR\\骰子概率计算器.exe" "" "$INSTDIR\\dice_icon.ico"
  
  ; 写入注册表
  WriteRegStr HKCU "Software\\骰子概率计算器" "" $INSTDIR
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\骰子概率计算器" "DisplayName" "骰子概率计算器"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\骰子概率计算器" "UninstallString" "$INSTDIR\\卸载.exe"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\骰子概率计算器" "DisplayIcon" "$INSTDIR\\dice_icon.ico"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\骰子概率计算器" "Publisher" "DiceCalculator"
SectionEnd

; 卸载部分
Section "Uninstall"
  ; 删除文件
  Delete "$INSTDIR\\骰子概率计算器.exe"
  Delete "$INSTDIR\\README.md"
  Delete "$INSTDIR\\dice_icon.ico"
  Delete "$INSTDIR\\卸载.exe"
  
  ; 删除快捷方式
  Delete "$SMPROGRAMS\\骰子概率计算器\\骰子概率计算器.lnk"
  Delete "$SMPROGRAMS\\骰子概率计算器\\卸载.lnk"
  Delete "$DESKTOP\\骰子概率计算器.lnk"
  
  ; 删除目录
  RMDir "$SMPROGRAMS\\骰子概率计算器"
  RMDir "$INSTDIR"
  
  ; 删除注册表项
  DeleteRegKey HKCU "Software\\骰子概率计算器"
  DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\骰子概率计算器"
SectionEnd
""")

    # 检查是否安装了NSIS
    nsis_found = False
    try:
        # 尝试查找安装的NSIS
        nsis_paths = [
            "C:\\Program Files\\NSIS\\makensis.exe",
            "C:\\Program Files (x86)\\NSIS\\makensis.exe",
        ]
        for path in nsis_paths:
            if os.path.exists(path):
                result = subprocess.run(
                    [path, "installer.nsi"], capture_output=True, text=True
                )
                nsis_found = True
                if result.returncode != 0:
                    print("编译安装脚本时出错:")
                    print(result.stderr)
                    return False
                break
    except Exception as e:
        print(f"运行NSIS时出错: {str(e)}")
        return False

    if not nsis_found:
        print("注意: 未找到NSIS编译器。已创建installer.nsi脚本文件。")
        print("要生成安装程序，请安装NSIS (https://nsis.sourceforge.io/)，")
        print("然后手动编译installer.nsi文件。")
        return False

    print("安装包创建成功：骰子概率计算器安装程序.exe")
    return True


if __name__ == "__main__":
    # 如果需要先运行build.py
    if not os.path.exists("dist"):
        print("先运行打包脚本...")
        os.system("python build.py")

    create_installer()
    print("\n完成！您可以分发以下文件：")
    print("1. dist/骰子概率计算器.exe - 单个可执行文件版本")
    if os.path.exists("骰子概率计算器安装程序.exe"):
        print("2. 骰子概率计算器安装程序.exe - 完整安装包（推荐给普通用户）")
