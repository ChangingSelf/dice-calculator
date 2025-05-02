import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
import re


class DiceCalculator:
    def __init__(self):
        self.cache = {}

    def parse_expression(self, expression: str) -> Tuple[List[Tuple[int, int]], int]:
        """解析骰子表达式，返回骰子列表和修正值"""
        # 移除所有空格
        expression = expression.replace(" ", "")

        # 转换为小写以统一处理
        expression = expression.lower()

        if not expression:
            raise ValueError("表达式不能为空")

        try:
            # 处理纯数字情况
            if expression.isdigit():
                return [(1, int(expression))], 0

            # 提取骰子表达式和修正值（更健壮的方法）
            dice_list = []
            modifier = 0
            
            # 分割表达式为操作数（骰子或数字）和操作符（+ 或 -）
            operands = []
            operators = []
            current = ""
            
            # 解析表达式为操作数和操作符
            for i, char in enumerate(expression):
                if char in "+-" and i > 0:  # 不处理开头的符号
                    if current:
                        operands.append(current)
                        current = ""
                    operators.append(char)
                else:
                    current += char
            
            # 添加最后一个操作数
            if current:
                operands.append(current)
            
            # 处理所有操作数和操作符
            for i, operand in enumerate(operands):
                # 检查是否是骰子表达式（如 2d20）或纯数字
                if "d" in operand:
                    # 骰子表达式
                    if operand.startswith("d") and operand[1:].isdigit():
                        # 特殊情况：d20 表示 1d20
                        num_dice = 1
                        num_sides = int(operand[1:])
                    else:
                        # 标准格式：XdY
                        match = re.match(r"(\d+)d(\d+)", operand)
                        if match:
                            num_dice = int(match.group(1))
                            num_sides = int(match.group(2))
                        else:
                            raise ValueError(f"无效的骰子表达式: {operand}")
                    
                    # 验证骰子参数
                    if num_dice <= 0:
                        raise ValueError(f"骰子数量({num_dice})必须大于0")
                    if num_sides <= 0:
                        raise ValueError(f"骰子面数({num_sides})必须大于0")
                    
                    # 添加到骰子列表
                    dice_list.append((num_dice, num_sides))
                else:
                    # 纯数字，作为修正值
                    if operand.isdigit():
                        # 考虑操作符
                        op = "+" if i == 0 else operators[i-1]
                        value = int(operand)
                        if op == "+":
                            modifier += value
                        else:  # op == "-"
                            modifier -= value
                    else:
                        raise ValueError(f"无效的操作数: {operand}")
            
            if not dice_list:
                raise ValueError("表达式必须包含至少一个骰子")

            return dice_list, modifier

        except ValueError as e:
            # 保持原始错误
            raise
        except Exception as e:
            # 将其他错误转换为ValueError以提供更清晰的消息
            raise ValueError(f"解析骰子表达式时出错: {str(e)}")

    def calculate_probability(self, expression: str) -> Tuple[np.ndarray, np.ndarray]:
        """计算骰子表达式的概率分布"""
        if expression in self.cache:
            return self.cache[expression]

        dice_list, modifier = self.parse_expression(expression)

        # 计算单个骰子的概率分布
        distributions = []
        for num_dice, num_sides in dice_list:
            if num_dice == 1:
                dist = np.ones(num_sides) / num_sides
            else:
                # 使用卷积计算多个骰子的概率分布
                dist = np.ones(num_sides) / num_sides
                for _ in range(num_dice - 1):
                    dist = np.convolve(dist, np.ones(num_sides) / num_sides)
            distributions.append(dist)

        # 合并所有骰子的概率分布
        if len(distributions) == 1:
            final_dist = distributions[0]
        else:
            final_dist = distributions[0]
            for dist in distributions[1:]:
                final_dist = np.convolve(final_dist, dist)

        # 添加修正值
        min_value = sum(num_dice for num_dice, _ in dice_list) + modifier
        max_value = (
            sum(num_dice * num_sides for num_dice, num_sides in dice_list) + modifier
        )
        x = np.arange(min_value, max_value + 1)

        # 确保概率分布和x轴对齐
        if len(x) > len(final_dist):
            final_dist = np.pad(final_dist, (0, len(x) - len(final_dist)))
        elif len(x) < len(final_dist):
            final_dist = final_dist[: len(x)]

        self.cache[expression] = (x, final_dist)
        return x, final_dist

    def plot_probability(self, expression: str, save_path: str = None):
        """绘制概率分布图"""
        x, prob = self.calculate_probability(expression)

        plt.figure(figsize=(12, 6))
        plt.bar(x, prob)
        plt.title(f"骰子表达式 {expression} 的概率分布")
        plt.xlabel("结果")
        plt.ylabel("概率")
        plt.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path)
        plt.show()

    def get_statistics(self, expression: str) -> dict:
        """获取统计信息"""
        x, prob = self.calculate_probability(expression)

        # 计算期望值
        expected_value = np.sum(x * prob)

        # 计算方差
        variance = np.sum((x - expected_value) ** 2 * prob)
        std_dev = np.sqrt(variance)

        # 计算中位数
        cumulative_prob = np.cumsum(prob)
        median_idx = np.searchsorted(cumulative_prob, 0.5)
        median = x[median_idx]

        return {
            "期望值": expected_value,
            "标准差": std_dev,
            "中位数": median,
            "最小值": x[0],
            "最大值": x[-1],
        }


def main():
    calculator = DiceCalculator()

    # 示例使用
    expression = "2D20+80"
    print(f"\n计算表达式: {expression}")
    stats = calculator.get_statistics(expression)
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")

    calculator.plot_probability(expression)


if __name__ == "__main__":
    main()
