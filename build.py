import os
import subprocess
import shutil
import sys


def build_exe():
    print("开始打包骰子概率计算器...")

    # 打包命令
    cmd = [
        "pyinstaller",
        "--name=骰子概率计算器",
        "--windowed",
        "--onefile",
        "--icon=dice_icon.ico" if os.path.exists("dice_icon.ico") else "",
        "--add-data=README.md;.",
        "dice_calculator_gui.py",
    ]

    # 移除空参数
    cmd = [item for item in cmd if item]

    # 执行打包命令
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("打包过程中出现错误:")
        print(result.stderr)
        return False

    # 打印成功信息
    print("打包成功！可执行文件保存在 dist 目录中。")

    # 打包其他文件夹
    try:
        if os.path.exists("dist"):
            # 复制说明文档
            if os.path.exists("README.md"):
                shutil.copy("README.md", "dist/")

            print("所有文件复制完成。")
    except Exception as e:
        print(f"复制文件时出错: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    # 创建图标文件（简单的默认图标）
    if not os.path.exists("dice_icon.ico"):
        try:
            # 尝试创建一个简单的图标
            from PIL import Image, ImageDraw

            # 创建一个32x32的图像
            img = Image.new("RGBA", (256, 256), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # 绘制一个简单的骰子图标
            draw.rectangle(
                [(40, 40), (216, 216)],
                fill=(30, 144, 255),
                outline=(255, 255, 255),
                width=8,
            )

            # 绘制骰子点
            dot_positions = [
                (128, 128),  # 中心点
                (80, 80),
                (176, 176),  # 对角线上的点
                (80, 176),
                (176, 80),  # 对角线上的点
                (80, 128),
                (176, 128),  # 中间的点
            ]

            for pos in dot_positions:
                draw.ellipse(
                    [(pos[0] - 20, pos[1] - 20), (pos[0] + 20, pos[1] + 20)],
                    fill=(255, 255, 255),
                )

            # 保存为ico文件
            img.save("dice_icon.ico")
            print("已创建默认图标文件")
        except ImportError:
            print("无法创建图标文件: 缺少PIL库")
            print("继续使用默认图标...")
        except Exception as e:
            print(f"创建图标时出错: {str(e)}")
            print("继续使用默认图标...")

    # 创建README文件
    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("""# 骰子概率计算器

## 简介
骰子概率计算器是一款帮助用户计算各种骰子表达式概率分布的工具。无论是角色扮演游戏、桌游还是概率教学，这个工具都能帮助您理解骰子组合的概率分布。

## 使用方法
1. 在输入框中输入骰子表达式，例如 "2D6"、"D20+5" 或 "3D6+D4+2"
2. 点击"计算"按钮查看概率分布和统计信息
3. 可以添加多个表达式进行对比分析
4. 使用快速示例按钮尝试常见的骰子表达式

## 表达式格式
- xDy: 投掷x个y面骰子（例如：2D6表示投掷2个6面骰子）
- 可以使用加号组合多个骰子表达式（例如：2D6+D4）
- 可以添加固定修正值（例如：D20+5）

## 统计信息说明
- 期望值：结果的平均值
- 标准差：反映结果的离散程度
- 中位数：50%的情况下会得到的结果
- 最大值和最小值：可能的结果范围

## 图表说明
- 条形图显示每个可能结果的概率
- 绿色线表示累积概率
- 红色虚线表示期望值
- 绿色虚线表示中位数

希望这个工具能帮助您更好地理解骰子的概率分布！
""")

    success = build_exe()
    if success:
        # 在Windows系统上自动打开文件夹
        if sys.platform == "win32":
            os.startfile("dist")
        print("打包完成！可执行文件在dist文件夹中。")
