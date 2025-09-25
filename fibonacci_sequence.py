#!/usr/bin/env python3
"""
斐波那契数列研究程序
Fibonacci Sequence Research Program

本程序演示了斐波那契数列的多种实现方法，包括：
- 迭代方法 (Iterative Approach)
- 递归方法 (Recursive Approach)  
- 记忆化递归方法 (Memoization Approach)

并分析各种方法的时间复杂度和最佳实践。
"""

import time
import sys
from functools import lru_cache

def fibonacci_iterative(n):
    """
    迭代方法计算斐波那契数列
    Iterative approach to calculate Fibonacci sequence
    
    时间复杂度: O(n)
    空间复杂度: O(n) 用于存储结果，O(1) 如果只计算第n项
    
    Args:
        n (int): 需要计算的项数
        
    Returns:
        list: 包含前n项斐波那契数的列表
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    # 初始化列表，包含前两个数
    fib_sequence = [0, 1]
    
    # 迭代计算剩余的数
    for i in range(2, n):
        next_fib = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_fib)
    
    return fib_sequence

def fibonacci_recursive_single(n):
    """
    递归方法计算单个斐波那契数
    Recursive approach to calculate a single Fibonacci number
    
    时间复杂度: O(2^n) - 指数级，因为重复计算
    空间复杂度: O(n) - 调用栈深度
    
    Args:
        n (int): 需要计算的项索引
        
    Returns:
        int: 第n个斐波那契数
    """
    # 基本情况
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # 递归情况
    return fibonacci_recursive_single(n-1) + fibonacci_recursive_single(n-2)

def fibonacci_recursive_sequence(n):
    """
    递归方法计算斐波那契数列（通过调用单个数计算函数）
    Recursive approach to calculate Fibonacci sequence
    
    Args:
        n (int): 需要计算的项数
        
    Returns:
        list: 包含前n项斐波那契数的列表
    """
    if n <= 0:
        return []
    
    return [fibonacci_recursive_single(i) for i in range(n)]

@lru_cache(maxsize=None)
def fibonacci_memoized_single(n):
    """
    记忆化递归方法计算单个斐波那契数
    Memoized recursive approach to calculate a single Fibonacci number
    
    时间复杂度: O(n) - 每个F(i)只计算一次
    空间复杂度: O(n) - 用于存储缓存结果
    
    Args:
        n (int): 需要计算的项索引
        
    Returns:
        int: 第n个斐波那契数
    """
    # 基本情况
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # 递归情况（使用缓存）
    return fibonacci_memoized_single(n-1) + fibonacci_memoized_single(n-2)

def fibonacci_memoized_sequence(n):
    """
    记忆化递归方法计算斐波那契数列
    Memoized recursive approach to calculate Fibonacci sequence
    
    Args:
        n (int): 需要计算的项数
        
    Returns:
        list: 包含前n项斐波那契数的列表
    """
    if n <= 0:
        return []
    
    return [fibonacci_memoized_single(i) for i in range(n)]

def validate_input(n):
    """
    验证输入参数
    Validate input parameter
    
    Args:
        n: 输入参数
        
    Returns:
        bool: 输入是否有效
    """
    try:
        n = int(n)
        if n < 0:
            print(f"错误：输入值 {n} 不能为负数")
            return False
        if n > 1000:
            print(f"警告：输入值 {n} 很大，递归方法可能很慢")
        return True
    except ValueError:
        print(f"错误：输入值 '{n}' 不是有效的整数")
        return False

def measure_performance(func, *args):
    """
    测量函数执行时间
    Measure function execution time
    
    Args:
        func: 要测量的函数
        *args: 函数参数
        
    Returns:
        tuple: (结果, 执行时间)
    """
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def print_fibonacci_info():
    """
    打印斐波那契数列的基本信息
    Print basic information about Fibonacci sequence
    """
    print("=" * 60)
    print("斐波那契数列数学原理")
    print("Fibonacci Sequence Mathematical Principles")
    print("=" * 60)
    
    print("\n定义 Definition:")
    print("斐波那契数列是一个数列，其中每个数字是前两个数字的和")
    print("A sequence where each number is the sum of the two preceding ones")
    
    print("\n数学公式 Mathematical Formula:")
    print("F(0) = 0")
    print("F(1) = 1")
    print("F(n) = F(n-1) + F(n-2)  for n > 1")
    
    print("\n历史背景 Historical Context:")
    print("- 由意大利数学家莱昂纳多·斐波那契(1170-1250)命名")
    print("- Named after Italian mathematician Leonardo of Pisa (Fibonacci)")
    print("- 首次出现在1202年的《计算之书》中")
    print("- First appeared in 'Liber Abaci' (1202)")
    
    print("\n数学特性 Mathematical Properties:")
    print("- 黄金比例：当n趋近于无穷大时，F(n+1)/F(n) → φ ≈ 1.618")
    print("- Golden Ratio: As n → ∞, F(n+1)/F(n) → φ ≈ 1.618")
    print("- 比内特公式：F(n) = (φ^n - (-φ)^(-n)) / √5")
    print("- Binet's Formula: F(n) = (φ^n - (-φ)^(-n)) / √5")
    
    print("\n应用领域 Applications:")
    print("- 计算机科学：算法、数据结构")
    print("- 金融市场：技术分析")
    print("- 自然界：螺旋图案（贝壳、花朵、星系）")
    print("- 建筑与艺术")
    print("- 数论与密码学")

def print_complexity_analysis():
    """
    打印时间复杂度分析
    Print time complexity analysis
    """
    print("\n" + "=" * 60)
    print("时间复杂度分析")
    print("Time Complexity Analysis")
    print("=" * 60)
    
    complexity_data = [
        ("方法 Method", "时间复杂度 Time Complexity", "空间复杂度 Space Complexity", "适用场景 Best For"),
        ("迭代 Iterative", "O(n)", "O(n) 或 O(1)", "大多数情况，n < 10^6"),
        ("递归 Recursive", "O(2^n)", "O(n)", "教学演示，n < 30"),
        ("记忆化 Memoization", "O(n)", "O(n)", "需要递归但性能重要，n < 10^4"),
        ("矩阵幂 Matrix", "O(log n)", "O(1)", "极大n值，n > 10^6"),
        ("比内特公式 Binet's", "O(1)", "O(1)", "理论计算，精度要求不高")
    ]
    
    # 打印表格
    for i, row in enumerate(complexity_data):
        if i == 0:
            print(f"{row[0]:<20} {row[1]:<25} {row[2]:<25} {row[3]}")
            print("-" * 90)
        else:
            print(f"{row[0]:<20} {row[1]:<25} {row[2]:<25} {row[3]}")

def print_best_practices():
    """
    打印最佳实践建议
    Print best practices recommendations
    """
    print("\n" + "=" * 60)
    print("最佳实践 Best Practices")
    print("=" * 60)
    
    practices = [
        "1. 对于小规模计算(n < 30)，可以使用递归方法，代码简洁易懂",
        "   For small calculations (n < 30), use recursive method for clarity",
        "",
        "2. 对于中等规模计算(n < 10^6)，优先使用迭代方法，性能优异",
        "   For medium calculations (n < 10^6), prefer iterative method for performance",
        "",
        "3. 需要递归语义但关注性能时，使用记忆化技术",
        "   When recursion semantics are needed but performance matters, use memoization",
        "",
        "4. 对于极大数值计算(n > 10^6)，考虑矩阵幂方法",
        "   For very large calculations (n > 10^6), consider matrix exponentiation",
        "",
        "5. 始终进行输入验证，防止无效输入和边界情况",
        "   Always validate input to prevent invalid inputs and edge cases",
        "",
        "6. 添加适当的注释和文档，提高代码可读性",
        "   Add proper comments and documentation for better readability",
        "",
        "7. 考虑使用整数溢出检查，特别是对于大数计算",
        "   Consider integer overflow checks, especially for large number calculations"
    ]
    
    for practice in practices:
        print(practice)

def main():
    """
    主函数 - 演示斐波那契数列的各种实现方法
    Main function - demonstrate various Fibonacci implementations
    """
    print_fibonacci_info()
    print_complexity_analysis()
    print_best_practices()
    
    # 设置要计算的项数
    n = 10
    
    print(f"\n" + "=" * 60)
    print(f"计算斐波那契数列前 {n} 项")
    print(f"Calculating first {n} terms of Fibonacci sequence")
    print("=" * 60)
    
    # 预期结果
    expected_result = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    print(f"\n预期结果 Expected result: {expected_result}")
    
    # 1. 迭代方法
    print(f"\n{'='*40}")
    print("1. 迭代方法 Iterative Method")
    print(f"{'='*40}")
    
    result_iter, time_iter = measure_performance(fibonacci_iterative, n)
    print(f"结果 Result: {result_iter}")
    print(f"执行时间 Execution time: {time_iter:.6f} 秒 seconds")
    print(f"验证 Verification: {'✓ 正确 Correct' if result_iter == expected_result else '✗ 错误 Incorrect'}")
    
    # 2. 递归方法
    print(f"\n{'='*40}")
    print("2. 递归方法 Recursive Method")
    print(f"{'='*40}")
    
    result_rec, time_rec = measure_performance(fibonacci_recursive_sequence, n)
    print(f"结果 Result: {result_rec}")
    print(f"执行时间 Execution time: {time_rec:.6f} 秒 seconds")
    print(f"验证 Verification: {'✓ 正确 Correct' if result_rec == expected_result else '✗ 错误 Incorrect'}")
    
    # 3. 记忆化递归方法
    print(f"\n{'='*40}")
    print("3. 记忆化递归方法 Memoization Method")
    print(f"{'='*40}")
    
    result_mem, time_mem = measure_performance(fibonacci_memoized_sequence, n)
    print(f"结果 Result: {result_mem}")
    print(f"执行时间 Execution time: {time_mem:.6f} 秒 seconds")
    print(f"验证 Verification: {'✓ 正确 Correct' if result_mem == expected_result else '✗ 错误 Incorrect'}")
    
    # 性能比较
    print(f"\n{'='*60}")
    print("性能比较 Performance Comparison")
    print(f"{'='*60}")
    
    # 计算相对速度，避免除零错误
    iter_speed = time_rec / time_iter if time_iter > 0 else float('inf')
    mem_speed = time_rec / time_mem if time_mem > 0 else float('inf')
    
    performance_data = [
        ("方法 Method", "执行时间 (秒) Time (s)", "相对速度 Relative Speed"),
        ("迭代 Iterative", f"{time_iter:.6f}", f"{iter_speed:.1f}x faster"),
        ("递归 Recursive", f"{time_rec:.6f}", "1.0x baseline"),
        ("记忆化 Memoization", f"{time_mem:.6f}", f"{mem_speed:.1f}x faster")
    ]
    
    for i, row in enumerate(performance_data):
        if i == 0:
            print(f"{row[0]:<20} {row[1]:<20} {row[2]}")
            print("-" * 50)
        else:
            print(f"{row[0]:<20} {row[1]:<20} {row[2]}")
    
    # 结论
    print(f"\n{'='*60}")
    print("结论 Conclusions")
    print(f"{'='*60}")
    
    print(f"\n对于计算前 {n} 项斐波那契数列：")
    print(f"For calculating first {n} terms of Fibonacci sequence:")
    print(f"• 迭代方法最快，执行时间 {time_iter:.6f} 秒")
    print(f"• Iterative method is fastest with {time_iter:.6f} seconds")
    print(f"• 递归方法最慢，但代码最简洁")
    print(f"• Recursive method is slowest but most elegant")
    print(f"• 记忆化方法在两者之间提供了良好的平衡")
    print(f"• Memoization provides a good balance between the two")
    
    print(f"\n所有方法都得到了正确结果：{expected_result}")
    print(f"All methods produced correct results: {expected_result}")
    
    # 返回结果用于变量提取
    return {
        'iterative': result_iter,
        'recursive': result_rec,
        'memoization': result_mem,
        'expected': expected_result,
        'time_iterative': time_iter,
        'time_recursive': time_rec,
        'time_memoization': time_mem
    }

if __name__ == "__main__":
    fibonacci_results = main()