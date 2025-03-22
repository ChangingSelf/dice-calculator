import customtkinter as ctk
from dice_calculator import DiceCalculator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

# 设置matplotlib中文字体
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]  # 设置微软雅黑字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
plt.rcParams["font.size"] = 12  # 增大默认字体大小

# 设置主题和颜色模式
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DiceCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("骰子概率计算器")
        self.calculator = DiceCalculator()

        # 用于存储对比的表达式
        self.expression_entries = []  # 存储所有表达式输入框
        self.expression_vars = []  # 存储所有表达式变量
        self.current_focus = None  # 当前焦点所在的输入框

        # 设置窗口大小和位置
        window_width = 1400
        window_height = 900
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建主框架
        self.create_main_frame()

    def create_main_frame(self):
        # 创建左侧面板
        left_frame = ctk.CTkFrame(self.root)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # 创建右侧面板
        right_frame = ctk.CTkFrame(self.root)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # 添加标题
        title_label = ctk.CTkLabel(
            left_frame, text="骰子概率计算器", font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)

        # 创建输入区域
        self.input_frame = ctk.CTkFrame(left_frame)
        self.input_frame.pack(fill="x", padx=20, pady=10)

        # 按钮区域
        buttons_frame = ctk.CTkFrame(self.input_frame)
        buttons_frame.pack(pady=10)

        calculate_button = ctk.CTkButton(
            buttons_frame,
            text="计算",
            command=self.calculate,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        calculate_button.pack(side="left", padx=5)

        clear_button = ctk.CTkButton(
            buttons_frame,
            text="清除所有",
            command=self.clear_all,
            width=100,
            height=40,
            font=("Helvetica", 14),
            fg_color="#555555",
            hover_color="#777777",
        )
        clear_button.pack(side="left", padx=5)

        # 添加第一个表达式输入框
        self.add_expression_input("2D20+80")

        # 添加新表达式按钮
        add_button = ctk.CTkButton(
            self.input_frame,
            text="+ 添加表达式",
            command=self.add_expression_input,
            width=200,
            height=30,
            font=("Helvetica", 12),
        )
        add_button.pack(pady=10)

        # 创建示例区域（可折叠）
        self.examples_visible = True
        self.examples_container = ctk.CTkFrame(left_frame)
        self.examples_container.pack(fill="x", padx=20, pady=10)

        examples_header = ctk.CTkFrame(self.examples_container)
        examples_header.pack(fill="x")

        examples_label = ctk.CTkLabel(
            examples_header, text="快速示例", font=("Helvetica", 16, "bold")
        )
        examples_label.pack(side="left", pady=5)

        self.toggle_button = ctk.CTkButton(
            examples_header,
            text="折叠 △",
            command=self.toggle_examples,
            width=80,
            height=25,
            font=("Helvetica", 12),
            fg_color="#555555",
            hover_color="#777777",
        )
        self.toggle_button.pack(side="right", padx=5)

        # 示例按钮内容
        self.examples_content = ctk.CTkFrame(self.examples_container)
        self.examples_content.pack(fill="x", pady=5)

        examples_buttons_frame = ctk.CTkFrame(self.examples_content)
        examples_buttons_frame.pack(pady=5)

        # 单骰子组
        single_dice_frame = ctk.CTkFrame(self.examples_content)
        single_dice_frame.pack(fill="x", pady=5)

        single_dice_label = ctk.CTkLabel(
            single_dice_frame, text="单骰子对比:", font=("Helvetica", 12, "bold")
        )
        single_dice_label.pack(anchor="w", padx=10, pady=2)

        single_dice_buttons = ctk.CTkFrame(single_dice_frame)
        single_dice_buttons.pack(fill="x", pady=2)

        example1_button = ctk.CTkButton(
            single_dice_buttons,
            text="D4",
            command=lambda: self.fill_focused_input("d4"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example1_button.grid(row=0, column=0, padx=5, pady=5)

        example2_button = ctk.CTkButton(
            single_dice_buttons,
            text="D6",
            command=lambda: self.fill_focused_input("d6"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example2_button.grid(row=0, column=1, padx=5, pady=5)

        example3_button = ctk.CTkButton(
            single_dice_buttons,
            text="D8",
            command=lambda: self.fill_focused_input("d8"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example3_button.grid(row=0, column=2, padx=5, pady=5)

        example4_button = ctk.CTkButton(
            single_dice_buttons,
            text="D10",
            command=lambda: self.fill_focused_input("d10"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example4_button.grid(row=0, column=3, padx=5, pady=5)

        example5_button = ctk.CTkButton(
            single_dice_buttons,
            text="D12",
            command=lambda: self.fill_focused_input("d12"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example5_button.grid(row=0, column=4, padx=5, pady=5)

        example6_button = ctk.CTkButton(
            single_dice_buttons,
            text="D20",
            command=lambda: self.fill_focused_input("d20"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example6_button.grid(row=0, column=5, padx=5, pady=5)

        example7_button = ctk.CTkButton(
            single_dice_buttons,
            text="D100",
            command=lambda: self.fill_focused_input("d100"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example7_button.grid(row=1, column=0, padx=5, pady=5)

        # 多骰子组
        multi_dice_frame = ctk.CTkFrame(self.examples_content)
        multi_dice_frame.pack(fill="x", pady=5)

        multi_dice_label = ctk.CTkLabel(
            multi_dice_frame, text="多骰子对比:", font=("Helvetica", 12, "bold")
        )
        multi_dice_label.pack(anchor="w", padx=10, pady=2)

        multi_dice_buttons = ctk.CTkFrame(multi_dice_frame)
        multi_dice_buttons.pack(fill="x", pady=2)

        # D6系列
        example8_button = ctk.CTkButton(
            multi_dice_buttons,
            text="2D6",
            command=lambda: self.fill_focused_input("2d6"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example8_button.grid(row=0, column=0, padx=5, pady=5)

        example9_button = ctk.CTkButton(
            multi_dice_buttons,
            text="3D6",
            command=lambda: self.fill_focused_input("3d6"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example9_button.grid(row=0, column=1, padx=5, pady=5)

        example10_button = ctk.CTkButton(
            multi_dice_buttons,
            text="4D6",
            command=lambda: self.fill_focused_input("4d6"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example10_button.grid(row=0, column=2, padx=5, pady=5)

        example11_button = ctk.CTkButton(
            multi_dice_buttons,
            text="10D6",
            command=lambda: self.fill_focused_input("10d6"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example11_button.grid(row=0, column=3, padx=5, pady=5)

        # D20系列
        example12_button = ctk.CTkButton(
            multi_dice_buttons,
            text="2D20",
            command=lambda: self.fill_focused_input("2d20"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example12_button.grid(row=1, column=0, padx=5, pady=5)

        example13_button = ctk.CTkButton(
            multi_dice_buttons,
            text="3D20",
            command=lambda: self.fill_focused_input("3d20"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example13_button.grid(row=1, column=1, padx=5, pady=5)

        example14_button = ctk.CTkButton(
            multi_dice_buttons,
            text="4D20",
            command=lambda: self.fill_focused_input("4d20"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example14_button.grid(row=1, column=2, padx=5, pady=5)

        example15_button = ctk.CTkButton(
            multi_dice_buttons,
            text="2D10",
            command=lambda: self.fill_focused_input("2d10"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example15_button.grid(row=1, column=3, padx=5, pady=5)

        # 常用表达式组
        common_expr_frame = ctk.CTkFrame(self.examples_content)
        common_expr_frame.pack(fill="x", pady=5)

        common_expr_label = ctk.CTkLabel(
            common_expr_frame, text="常用表达式:", font=("Helvetica", 12, "bold")
        )
        common_expr_label.pack(anchor="w", padx=10, pady=2)

        common_expr_buttons = ctk.CTkFrame(common_expr_frame)
        common_expr_buttons.pack(fill="x", pady=2)

        # 第一行
        example16_button = ctk.CTkButton(
            common_expr_buttons,
            text="3D6+3",
            command=lambda: self.fill_focused_input("3d6+3"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example16_button.grid(row=0, column=0, padx=5, pady=5)

        example17_button = ctk.CTkButton(
            common_expr_buttons,
            text="D20+5",
            command=lambda: self.fill_focused_input("d20+5"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example17_button.grid(row=0, column=1, padx=5, pady=5)

        example18_button = ctk.CTkButton(
            common_expr_buttons,
            text="2D10+D8",
            command=lambda: self.fill_focused_input("2d10+d8"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example18_button.grid(row=0, column=2, padx=5, pady=5)

        example19_button = ctk.CTkButton(
            common_expr_buttons,
            text="D20+D4",
            command=lambda: self.fill_focused_input("d20+d4"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example19_button.grid(row=0, column=3, padx=5, pady=5)

        # 第二行 - 更多常用表达式
        example20_button = ctk.CTkButton(
            common_expr_buttons,
            text="2D6+6",
            command=lambda: self.fill_focused_input("2d6+6"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example20_button.grid(row=1, column=0, padx=5, pady=5)

        example21_button = ctk.CTkButton(
            common_expr_buttons,
            text="4D6取3",
            command=lambda: self.fill_focused_input("4d6k3"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example21_button.grid(row=1, column=1, padx=5, pady=5)

        example22_button = ctk.CTkButton(
            common_expr_buttons,
            text="2D20取1",
            command=lambda: self.fill_focused_input("2d20k1"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example22_button.grid(row=1, column=2, padx=5, pady=5)

        example23_button = ctk.CTkButton(
            common_expr_buttons,
            text="D20+10",
            command=lambda: self.fill_focused_input("d20+10"),
            width=80,
            height=30,
            font=("Helvetica", 12),
        )
        example23_button.grid(row=1, column=3, padx=5, pady=5)

        # 统计信息区域
        stats_frame = ctk.CTkFrame(left_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)

        stats_label = ctk.CTkLabel(
            stats_frame, text="统计信息", font=("Helvetica", 16, "bold")
        )
        stats_label.pack(pady=5)

        self.stats_text = ctk.CTkTextbox(
            stats_frame, width=350, height=200, font=("Helvetica", 12)
        )
        self.stats_text.pack(pady=5)

        # 计算原理区域
        theory_frame = ctk.CTkFrame(left_frame)
        theory_frame.pack(fill="x", padx=20, pady=10)

        theory_label = ctk.CTkLabel(
            theory_frame, text="计算原理", font=("Helvetica", 16, "bold")
        )
        theory_label.pack(pady=5)

        self.theory_text = ctk.CTkTextbox(
            theory_frame, width=350, height=250, font=("Helvetica", 12)
        )
        self.theory_text.pack(pady=5)
        self.theory_text.insert("end", "骰子概率计算原理：\n\n")
        self.theory_text.insert("end", "1. 单个骰子的概率分布：\n")
        self.theory_text.insert("end", "   对于一个n面骰子，每个面的概率为1/n\n\n")
        self.theory_text.insert("end", "2. 多个骰子的概率分布：\n")
        self.theory_text.insert("end", "   使用卷积计算多个骰子的组合概率\n")
        self.theory_text.insert(
            "end", "   例如：对于2D6，使用1D6的概率分布进行卷积\n\n"
        )
        self.theory_text.insert("end", "3. 中心极限定理：\n")
        self.theory_text.insert("end", "   当骰子数量增加时，分布趋向于正态分布\n")
        self.theory_text.insert(
            "end", "   这是为什么多个骰子的分布看起来相似的原因\n\n"
        )
        self.theory_text.insert("end", "4. 数学期望：\n")
        self.theory_text.insert("end", "   骰子的平均值\n")
        self.theory_text.insert("end", "   例如：1D6的期望值为3.5\n")
        self.theory_text.insert("end", "   nDm的期望值为n*(m+1)/2\n\n")
        self.theory_text.insert("end", "5. 标准差：\n")
        self.theory_text.insert("end", "   反映结果的离散程度\n")
        self.theory_text.insert("end", "   标准差越大，结果越不确定\n")
        self.theory_text.configure(state="disabled")  # 设置为只读

        # 使用说明区域
        help_frame = ctk.CTkFrame(left_frame)
        help_frame.pack(fill="x", padx=20, pady=10)

        help_label = ctk.CTkLabel(
            help_frame, text="使用说明", font=("Helvetica", 16, "bold")
        )
        help_label.pack(pady=5)

        help_text = ctk.CTkTextbox(
            help_frame, width=350, height=150, font=("Helvetica", 12)
        )
        help_text.pack(pady=5)
        help_text.insert("end", "骰子表达式格式说明：\n\n")
        help_text.insert("end", "1. xDy 表示投掷 x 个 y 面骰子\n")
        help_text.insert("end", "   例如：2D20 表示投掷2个20面骰子\n\n")
        help_text.insert("end", "2. 可以添加修正值\n")
        help_text.insert("end", "   例如：2D20+80 表示投掷2个20面骰子后加80\n\n")
        help_text.insert("end", "3. 支持多个骰子组合\n")
        help_text.insert("end", "   例如：2D20+3D6+10\n\n")
        help_text.insert("end", "4. 快速示例：\n")
        help_text.insert("end", "   点击示例按钮将在当前焦点输入框填入表达式\n\n")
        help_text.insert("end", "5. 多表达式对比：\n")
        help_text.insert("end", "   可以点击'添加表达式'增加更多表达式进行对比")
        help_text.configure(state="disabled")  # 设置为只读

        # 概率分布图区域
        self.plot_frame = ctk.CTkFrame(right_frame)
        self.plot_frame.pack(fill="both", expand=True, padx=20, pady=20)

        plot_label = ctk.CTkLabel(
            self.plot_frame, text="概率分布图", font=("Helvetica", 18, "bold")
        )
        plot_label.pack(pady=5)

        # 初始化matplotlib图形
        self.init_matplotlib_figure()

    def init_matplotlib_figure(self):
        """初始化matplotlib图形"""
        plt.style.use("dark_background")
        # 清理之前的图形，避免内存泄漏
        if hasattr(self, "fig") and self.fig:
            plt.close(self.fig)
        if hasattr(self, "canvas") and self.canvas:
            self.canvas.get_tk_widget().destroy()

        # 创建新图形
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # 初始化显示
        self.fig.tight_layout()
        self.canvas.draw()
        print("初始化图形完成")

    def add_expression_input(self, default_value=""):
        """添加新的表达式输入框"""
        # 创建框架
        index = len(self.expression_vars)
        expression_frame = ctk.CTkFrame(self.input_frame)

        # 获取计算按钮所在的框架
        buttons_frame = None
        for child in self.input_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame) and any(
                isinstance(widget, ctk.CTkButton) and widget.cget("text") == "计算"
                for widget in child.winfo_children()
            ):
                buttons_frame = child
                break

        # 将新表达式框添加在计算按钮下面
        if buttons_frame:
            expression_frame.pack(fill="x", pady=5, after=buttons_frame)
        else:
            expression_frame.pack(fill="x", pady=5)

        # 创建标签
        label_text = f"骰子表达式 {index + 1}:"
        input_label = ctk.CTkLabel(
            expression_frame, text=label_text, font=("Helvetica", 14)
        )
        input_label.pack(side="left", padx=5)

        # 创建字符串变量和输入框
        var = ctk.StringVar(value=default_value)
        self.expression_vars.append(var)

        entry = ctk.CTkEntry(
            expression_frame,
            textvariable=var,
            width=200,
            height=40,
            font=("Helvetica", 14),
        )
        entry.pack(side="left", padx=5)
        self.expression_entries.append(entry)

        # 为输入框绑定焦点事件
        entry.bind("<FocusIn>", lambda e, idx=index: self.set_focus(idx))

        # 默认使第一个输入框获得焦点
        if index == 0:
            entry.focus_set()
            self.current_focus = 0

        # 如果不是第一个输入框，添加删除按钮
        if index > 0:
            # 使用tag记录当前的索引位置，而不是使用lambda捕获
            entry.delete_index = index
            delete_button = ctk.CTkButton(
                expression_frame,
                text="×",
                command=lambda e=entry: self.remove_expression(e.delete_index),
                width=30,
                height=30,
                font=("Helvetica", 14, "bold"),
                fg_color="#aa5555",
                hover_color="#cc6666",
            )
            delete_button.pack(side="left", padx=5)

        return entry

    def remove_expression(self, index):
        """移除表达式输入框"""
        if len(self.expression_vars) <= 1:
            return  # 至少保留一个输入框

        try:
            # 获取要删除的输入框和变量
            entry = self.expression_entries[index]
            var = self.expression_vars[index]

            # 获取包含输入框的框架
            frame = entry.master

            # 从列表中移除
            self.expression_entries.pop(index)
            self.expression_vars.pop(index)

            # 销毁框架（会同时销毁其中的所有部件）
            frame.destroy()

            # 更新剩余输入框的标签和删除索引
            for i, entry in enumerate(self.expression_entries):
                # 更新标签
                label = entry.master.winfo_children()[0]  # 获取标签
                label.configure(text=f"骰子表达式 {i + 1}:")

                # 更新删除按钮的索引引用
                if hasattr(entry, "delete_index"):
                    entry.delete_index = i

            # 更新焦点
            if self.current_focus == index:
                self.current_focus = 0
                if self.expression_entries:
                    self.expression_entries[0].focus_set()
            elif self.current_focus > index:
                self.current_focus -= 1

            # 重新计算结果
            self.calculate()
        except Exception as e:
            self.show_error(f"删除表达式时出错：{str(e)}")
            import traceback

            print(traceback.format_exc())  # 打印详细的堆栈跟踪
            # 确保界面保持一致状态
            self.clear_all()  # 如果删除过程出错，重置整个界面

    def set_focus(self, index):
        """设置当前焦点"""
        self.current_focus = index

    def fill_focused_input(self, example):
        """将示例填入当前焦点输入框"""
        if self.current_focus is not None and 0 <= self.current_focus < len(
            self.expression_vars
        ):
            self.expression_vars[self.current_focus].set(example)
            self.calculate()
        else:
            # 如果没有焦点，默认填入第一个输入框
            if self.expression_vars:
                self.expression_vars[0].set(example)
                self.calculate()

    def toggle_examples(self):
        """切换示例区域的显示/隐藏状态"""
        if self.examples_visible:
            self.examples_content.pack_forget()
            self.toggle_button.configure(text="展开 ▽")
        else:
            self.examples_content.pack(fill="x", pady=5)
            self.toggle_button.configure(text="折叠 △")
        self.examples_visible = not self.examples_visible

    def calculate(self):
        """计算并显示骰子表达式的概率分布"""
        try:
            print("开始计算...")  # 调试信息

            # 获取所有有效的表达式
            valid_expressions = []
            for var in self.expression_vars:
                expr = var.get().strip()
                if expr:
                    valid_expressions.append(expr)
                    print(f"有效表达式: {expr}")  # 调试信息

            if not valid_expressions:
                self.show_error("请输入至少一个骰子表达式")
                return

            # 计算所有表达式的统计信息
            all_stats = []
            all_data = []

            for expr in valid_expressions:
                try:
                    print(f"正在计算表达式: {expr}")  # 调试信息
                    stats = self.calculator.get_statistics(expr)
                    x, prob = self.calculator.calculate_probability(expr)
                    all_stats.append((expr, stats))
                    all_data.append((expr, x, prob))
                    print(f"表达式 {expr} 计算成功")  # 调试信息
                except Exception as e:
                    print(f"计算表达式 '{expr}' 时出错: {str(e)}")  # 调试信息
                    self.show_error(f"计算表达式 '{expr}' 时出错：{str(e)}")
                    return

            if not all_stats:  # 确保至少有一个有效的计算结果
                print("没有有效的计算结果")  # 调试信息
                return

            print("开始更新统计信息显示...")  # 调试信息
            # 更新统计信息显示
            self.stats_text.configure(state="normal")  # 临时启用编辑
            self.stats_text.delete("1.0", "end")

            # 显示每个表达式的统计信息
            for i, (expr, stats) in enumerate(all_stats):
                self.stats_text.insert("end", f"表达式{i + 1} ({expr}):\n")
                for key, value in stats.items():
                    self.stats_text.insert("end", f"{key}: {value:.2f}\n")
                self.stats_text.insert("end", "\n")

            # 如果有多个表达式，显示它们之间的比较
            if len(all_stats) > 1:
                self.stats_text.insert("end", "表达式比较:\n")
                base_expr, base_stats = all_stats[0]
                for i, (expr, stats) in enumerate(all_stats[1:], 1):
                    self.stats_text.insert("end", f"{base_expr} vs {expr}:\n")
                    for key in base_stats:
                        diff = base_stats[key] - stats[key]
                        self.stats_text.insert("end", f"{key}差异: {diff:.2f}\n")
                    self.stats_text.insert("end", "\n")

            self.stats_text.configure(state="disabled")  # 恢复只读
            print("统计信息更新完成")  # 调试信息

            # 绘制图表
            self.plot_data(all_data, all_stats)

        except Exception as e:
            print(f"计算出错: {str(e)}")  # 调试信息
            import traceback

            print(traceback.format_exc())  # 打印详细的堆栈跟踪
            self.show_error(f"计算出错：{str(e)}")

    def plot_data(self, all_data, all_stats):
        """绘制骰子表达式的概率分布图"""
        try:
            print("开始绘制图表...")  # 调试信息

            # 重新初始化matplotlib图形，确保清理之前的内容
            self.init_matplotlib_figure()

            # 设置颜色循环
            colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

            # 是否启用堆叠条形图模式
            stacked_mode = len(all_data) <= 3 and len(all_data) > 1

            if len(all_data) > 1:
                if stacked_mode:
                    # 堆叠条形图模式 - 适合2-3个表达式
                    self.plot_stacked_bars(all_data, all_stats, colors)
                else:
                    # 多图表模式 - 每个表达式一个图表
                    self.plot_multiple_figures(all_data, all_stats, colors)
            else:
                # 单表达式模式
                self.plot_single_figure(all_data[0], all_stats[0], colors[0])

            print("图表绘制完成")  # 调试信息

        except Exception as e:
            print(f"绘制图表时出错: {str(e)}")  # 调试信息
            import traceback

            print(traceback.format_exc())  # 打印详细的堆栈跟踪
            self.show_error(f"绘制图表时出错：{str(e)}")

    def plot_stacked_bars(self, all_data, all_stats, colors):
        """绘制分组条形图（而非堆叠条形图）"""
        print("使用分组条形图模式")  # 调试信息

        # 找出所有可能的x值
        all_x = set()
        for _, x, _ in all_data:
            all_x.update(x)
        all_x = sorted(list(all_x))

        # 计算分组条形图的参数
        n_groups = len(all_data)
        total_width = 0.8  # 每个x位置的总宽度
        bar_width = total_width / n_groups  # 每个条形的宽度

        # 绘制分组条形图
        for i, (expr, x, prob) in enumerate(all_data):
            # 转换数据到公共x轴
            y_values = np.zeros(len(all_x))
            for j, x_val in enumerate(x):
                if x_val in all_x:
                    idx = all_x.index(x_val)
                    y_values[idx] = prob[j]

            # 计算条形的位置偏移
            offset = (i - n_groups / 2 + 0.5) * bar_width
            x_positions = np.array(all_x) + offset

            # 绘制条形图（分组而非堆叠）
            self.ax.bar(
                x_positions,
                y_values,
                width=bar_width,
                color=colors[i % len(colors)],
                alpha=0.7,
                label=f"表达式{i + 1}: {expr}",
            )

        # 设置标题和标签
        self.ax.set_title(
            f"骰子表达式概率分布对比",
            fontsize=18,
            pad=20,
            fontproperties="Microsoft YaHei",
        )
        self.ax.set_xlabel(
            "可能的结果值", fontsize=16, fontproperties="Microsoft YaHei"
        )
        self.ax.set_ylabel("出现概率", fontsize=16, fontproperties="Microsoft YaHei")

        # 设置X轴的刻度位置为原始值
        self.ax.set_xticks(all_x)

        # 设置网格和图例
        self.ax.grid(True, alpha=0.3, linestyle="--")
        self.ax.legend(fontsize=14, loc="upper right")

        # 设置Y轴为百分比格式
        self.ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: "{:.1%}".format(y))
        )

        # 标记期望值
        for i, (expr, stats) in enumerate(all_stats):
            expected_value = stats["期望值"]
            color = colors[i % len(colors)]
            self.ax.axvline(x=expected_value, color=color, linestyle="--", alpha=0.7)
            self.ax.text(
                expected_value,
                self.ax.get_ylim()[1] * (0.95 - i * 0.05),  # 错开显示避免重叠
                f"期望值{i + 1}: {expected_value:.1f}",
                rotation=90,
                va="top",
                ha="right",
                color=color,
                fontsize=14,
                fontproperties="Microsoft YaHei",
            )

        # 设置刻度标签
        self.ax.tick_params(axis="both", which="major", labelsize=14)
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_fontproperties("Microsoft YaHei")

        # 刷新图表
        self.fig.tight_layout()
        self.canvas.draw()

    def plot_multiple_figures(self, all_data, all_stats, colors):
        """绘制多个子图"""
        print("使用子图模式")  # 调试信息

        # 清理之前的图形
        plt.close(self.fig)
        self.canvas.get_tk_widget().pack_forget()

        # 确定布局
        rows = min(2, len(all_data))
        cols = (len(all_data) + rows - 1) // rows

        # 创建新的子图
        self.fig, axs = plt.subplots(rows, cols, figsize=(12, 8), sharex=True)

        # 处理不同数量子图的情况
        if rows == 1 and cols == 1:
            axs = np.array([axs])
        elif rows == 1:
            axs = np.array([axs])
        else:
            axs = axs.flatten()

        # 绘制每个子图
        for i, ((expr, x, prob), ax) in enumerate(zip(all_data, axs)):
            color = colors[i % len(colors)]

            # 绘制条形图
            bars = ax.bar(x, prob, color=color, alpha=0.7, width=0.7)

            # 设置标题
            ax.set_title(
                f"表达式{i + 1}: {expr}",
                fontsize=14,
                fontproperties="Microsoft YaHei",
            )

            # 设置Y轴为百分比格式
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda y, _: "{:.1%}".format(y))
            )

            # 设置网格
            ax.grid(True, alpha=0.3, linestyle="--")

            # 标记期望值
            expected_value = all_stats[i][1]["期望值"]
            ax.axvline(x=expected_value, color="red", linestyle="--", alpha=0.7)
            ax.text(
                expected_value,
                ax.get_ylim()[1] * 0.95,
                f"期望值: {expected_value:.1f}",
                rotation=90,
                va="top",
                ha="right",
                color="red",
                fontsize=12,
                fontproperties="Microsoft YaHei",
            )

            # 设置刻度标签
            ax.tick_params(axis="both", which="major", labelsize=12)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontproperties("Microsoft YaHei")

        # 创建大标题
        self.fig.suptitle(
            "骰子表达式概率分布对比",
            fontsize=20,
            fontproperties="Microsoft YaHei",
            y=0.98,
        )

        # 添加共享标签
        self.fig.text(
            0.5,
            0.01,
            "可能的结果值",
            ha="center",
            fontsize=16,
            fontproperties="Microsoft YaHei",
        )
        self.fig.text(
            0.01,
            0.5,
            "出现概率",
            va="center",
            rotation="vertical",
            fontsize=16,
            fontproperties="Microsoft YaHei",
        )

        # 隐藏多余的子图
        for i in range(len(all_data), len(axs)):
            axs[i].axis("off")

        # 重新创建Canvas并显示
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # 刷新图表
        self.fig.tight_layout()
        self.canvas.draw()

    def plot_single_figure(self, data, stats, color):
        """绘制单个图表"""
        print("使用单图表模式")  # 调试信息
        expr, x, prob = data

        # 解包stats参数，确保正确访问期望值
        # 注意：传入的stats是(expr, stats_dict)格式
        _, stats_dict = stats  # 正确提取统计信息字典

        # 绘制条形图
        bars = self.ax.bar(x, prob, color=color, alpha=0.7, width=0.7)

        # 在每个柱子上方显示概率百分比
        for bar in bars:
            height = bar.get_height()
            if height > 0.05:  # 只显示大于5%的概率值，避免图表过于拥挤
                self.ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{height:.1%}",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontproperties="Microsoft YaHei",
                )

        # 设置标题和标签
        self.ax.set_title(
            f"骰子表达式 {expr} 的概率分布",
            fontsize=18,
            pad=20,
            fontproperties="Microsoft YaHei",
        )
        self.ax.set_xlabel(
            "可能的结果值", fontsize=16, fontproperties="Microsoft YaHei"
        )
        self.ax.set_ylabel("出现概率", fontsize=16, fontproperties="Microsoft YaHei")

        # 设置网格
        self.ax.grid(True, alpha=0.3, linestyle="--")

        # 设置Y轴为百分比格式
        self.ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: "{:.1%}".format(y))
        )

        # 添加期望值垂直线
        expected_value = stats_dict["期望值"]
        self.ax.axvline(x=expected_value, color="red", linestyle="--", alpha=0.7)
        self.ax.text(
            expected_value,
            self.ax.get_ylim()[1] * 0.95,
            f"期望值: {expected_value:.1f}",
            rotation=90,
            va="top",
            ha="right",
            color="red",
            fontsize=14,
            fontproperties="Microsoft YaHei",
        )

        # 添加最常见结果标记
        most_likely_idx = np.argmax(prob)
        most_likely_value = x[most_likely_idx]
        most_likely_prob = prob[most_likely_idx]

        self.ax.scatter(
            most_likely_value,
            most_likely_prob,
            s=100,
            color="yellow",
            zorder=10,
            edgecolor="black",
            alpha=0.8,
        )

        self.ax.text(
            most_likely_value,
            most_likely_prob,
            f"最高概率: {most_likely_value}\n({most_likely_prob:.1%})",
            ha="center",
            va="bottom",
            fontsize=12,
            fontproperties="Microsoft YaHei",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.7),
        )

        # 设置刻度标签
        self.ax.tick_params(axis="both", which="major", labelsize=14)
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_fontproperties("Microsoft YaHei")

        # 添加CDF曲线（累积分布函数）
        cumulative_prob = np.cumsum(prob)
        ax2 = self.ax.twinx()
        ax2.plot(x, cumulative_prob, "g-o", linewidth=2, alpha=0.6, markersize=4)

        # 设置CDF的Y轴标签
        ax2.set_ylabel(
            "累积概率", color="g", fontsize=16, fontproperties="Microsoft YaHei"
        )

        # 设置CDF的Y轴为百分比格式并设置刻度标签颜色
        ax2.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: "{:.0%}".format(y))
        )
        ax2.tick_params(axis="y", colors="green", labelsize=14)
        for label in ax2.get_yticklabels():
            label.set_fontproperties("Microsoft YaHei")

        # 标记50%的概率线
        median_idx = np.searchsorted(cumulative_prob, 0.5)
        if median_idx < len(x):
            median = x[median_idx]
            ax2.axhline(y=0.5, color="green", linestyle=":", alpha=0.7)
            ax2.axvline(x=median, color="green", linestyle=":", alpha=0.7)
            ax2.text(
                median,
                0.52,
                f"中位数: {median}",
                color="green",
                fontsize=12,
                ha="right",
                fontproperties="Microsoft YaHei",
            )

        # 刷新图表
        self.fig.tight_layout()
        self.canvas.draw()

    def clear_all(self):
        """清除所有表达式并重置"""
        try:
            # 清除所有表达式输入框
            for entry in self.expression_entries:
                frame = entry.master
                frame.destroy()

            # 重置列表
            self.expression_entries = []
            self.expression_vars = []
            self.current_focus = None

            # 重新初始化图形
            self.init_matplotlib_figure()

            # 清除统计信息
            self.stats_text.configure(state="normal")
            self.stats_text.delete("1.0", "end")
            self.stats_text.configure(state="disabled")

            # 添加一个新的空输入框
            self.add_expression_input()
        except Exception as e:
            self.show_error(f"清除所有表达式时出错：{str(e)}")
            import traceback

            print(traceback.format_exc())  # 打印详细的堆栈跟踪

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("错误")
        error_window.geometry("400x150")
        error_window.transient(self.root)  # 设置为主窗口的临时窗口
        error_window.grab_set()  # 模态窗口，阻止用户与其他窗口交互

        # 防止窗口被立即关闭
        error_window.protocol("WM_DELETE_WINDOW", lambda: None)

        # 居中显示
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        error_window.geometry(f"+{x}+{y}")

        error_label = ctk.CTkLabel(
            error_window, text=message, font=("Helvetica", 14), wraplength=350
        )
        error_label.pack(pady=20)

        ok_button = ctk.CTkButton(
            error_window,
            text="确定",
            command=lambda: self.close_error_window(error_window),
            width=100,
            height=30,
        )
        ok_button.pack(pady=10)

        # 确保窗口显示在最前面
        error_window.lift()
        error_window.focus_force()

    def close_error_window(self, window):
        """安全关闭错误窗口"""
        window.grab_release()  # 释放模态状态
        window.destroy()  # 销毁窗口


def main():
    root = ctk.CTk()
    app = DiceCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
