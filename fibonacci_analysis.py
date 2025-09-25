#!/usr/bin/env python3
"""
斐波那契数列计算算法分析与性能比较
Fibonacci Sequence Calculation: Algorithm Analysis and Performance Comparison
"""

import time
import sys
import math
from functools import lru_cache
from typing import Dict, List, Tuple, Callable

class FibonacciAnalyzer:
    """斐波那契数列计算器与分析器"""
    
    def __init__(self):
        self.performance_data = {}
        self.complexity_data = {}
        
    def recursive_naive(self, n: int) -> int:
        """朴素递归实现 - O(2^n) 时间复杂度"""
        if n <= 1:
            return n
        return self.recursive_naive(n - 1) + self.recursive_naive(n - 2)
    
    @lru_cache(maxsize=None)
    def recursive_memoized(self, n: int) -> int:
        """记忆化递归实现 - O(n) 时间复杂度"""
        if n <= 1:
            return n
        return self.recursive_memoized(n - 1) + self.recursive_memoized(n - 2)
    
    def iterative(self, n: int) -> int:
        """迭代实现 - O(n) 时间复杂度, O(1) 空间复杂度"""
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def dynamic_programming(self, n: int) -> int:
        """动态规划实现 - O(n) 时间复杂度, O(n) 空间复杂度"""
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[0], dp[1] = 0, 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
    
    def matrix_exponentiation(self, n: int) -> int:
        """矩阵快速幂实现 - O(log n) 时间复杂度"""
        if n <= 1:
            return n
        
        def matrix_multiply(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
            """2x2 矩阵乘法"""
            return [
                [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
            ]
        
        def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
            """矩阵快速幂"""
            result = [[1, 0], [0, 1]]  # 单位矩阵
            
            while power > 0:
                if power % 2 == 1:
                    result = matrix_multiply(result, matrix)
                matrix = matrix_multiply(matrix, matrix)
                power //= 2
            
            return result
        
        # 转换矩阵 [[1, 1], [1, 0]]
        transformation_matrix = [[1, 1], [1, 0]]
        result_matrix = matrix_power(transformation_matrix, n - 1)
        
        return result_matrix[0][0]
    
    def binet_formula(self, n: int) -> int:
        """Binet公式实现 - O(1) 时间复杂度"""
        if n <= 1:
            return n
        
        sqrt5 = math.sqrt(5)
        phi = (1 + sqrt5) / 2  # 黄金比例
        
        # Binet公式: F(n) = (φ^n - (-φ)^(-n)) / √5
        fib = (phi**n - (-phi)**(-n)) / sqrt5
        
        return int(round(fib))
    
    def measure_performance(self, func: Callable, n: int, max_time: float = 10.0) -> Tuple[float, int]:
        """测量函数执行时间和结果"""
        start_time = time.time()
        result = None
        execution_time = 0
        
        try:
            result = func(n)
            execution_time = time.time() - start_time
        except (RecursionError, OverflowError, KeyboardInterrupt):
            execution_time = float('inf')
        
        return execution_time, result
    
    def compare_algorithms(self, max_n: int = 35) -> Dict[str, List[float]]:
        """比较不同算法的性能"""
        algorithms = {
            'Recursive Naive': self.recursive_naive,
            'Recursive Memoized': self.recursive_memoized,
            'Iterative': self.iterative,
            'Dynamic Programming': self.dynamic_programming,
            'Matrix Exponentiation': self.matrix_exponentiation,
            'Binet Formula': self.binet_formula
        }
        
        performance_results = {name: [] for name in algorithms.keys()}
        
        print("斐波那契算法性能比较")
        print("=" * 80)
        print(f"{'n':<4} {'Recursive':<12} {'Memoized':<12} {'Iterative':<12} {'DP':<12} {'Matrix':<12} {'Binet':<12}")
        print("-" * 80)
        
        for n in range(1, max_n + 1):
            row = [f"{n:<4}"]
            
            for name, func in algorithms.items():
                if name == 'Recursive Naive' and n > 35:  # 朴素递归在n>35时非常慢
                    row.append("TOO_SLOW")
                    performance_results[name].append(float('inf'))
                    continue
                
                execution_time, result = self.measure_performance(func, n)
                performance_results[name].append(execution_time)
                
                if execution_time == float('inf'):
                    row.append("TIMEOUT")
                elif execution_time < 0.001:
                    row.append(f"<0.001s")
                elif execution_time < 0.01:
                    row.append(f"{execution_time:.3f}s")
                else:
                    row.append(f"{execution_time:.2f}s")
            
            print(" ".join(row))
        
        return performance_results
    
    def analyze_complexity(self) -> Dict[str, str]:
        """分析各算法的时间复杂度和空间复杂度"""
        complexity_analysis = {
            'Recursive Naive': {
                'time_complexity': 'O(2^n)',
                'space_complexity': 'O(n)',
                'description': '指数级时间复杂度，适用于教学演示，实际应用不推荐'
            },
            'Recursive Memoized': {
                'time_complexity': 'O(n)',
                'space_complexity': 'O(n)',
                'description': '线性时间复杂度，通过记忆化避免重复计算'
            },
            'Iterative': {
                'time_complexity': 'O(n)',
                'space_complexity': 'O(1)',
                'description': '线性时间常数空间，最优的线性算法'
            },
            'Dynamic Programming': {
                'time_complexity': 'O(n)',
                'space_complexity': 'O(n)',
                'description': '线性时间，存储所有中间结果，适合需要完整序列的场景'
            },
            'Matrix Exponentiation': {
                'time_complexity': 'O(log n)',
                'space_complexity': 'O(1)',
                'description': '对数时间复杂度，适合计算非常大的n值'
            },
            'Binet Formula': {
                'time_complexity': 'O(1)',
                'space_complexity': 'O(1)',
                'description': '常数时间复杂度，但存在浮点精度问题'
            }
        }
        return complexity_analysis
    
    def print_complexity_analysis(self):
        """打印复杂度分析结果"""
        analysis = self.analyze_complexity()
        
        print("\n算法复杂度分析")
        print("=" * 80)
        print(f"{'算法名称':<20} {'时间复杂度':<15} {'空间复杂度':<15} {'描述'}")
        print("-" * 80)
        
        for name, data in analysis.items():
            print(f"{name:<20} {data['time_complexity']:<15} {data['space_complexity']:<15} {data['description']}")
    
    def test_correctness(self, test_range: int = 20) -> bool:
        """测试所有算法的正确性"""
        print(f"\n算法正确性测试 (n = 1 to {test_range})")
        print("=" * 80)
        
        algorithms = {
            'Recursive Memoized': self.recursive_memoized,
            'Iterative': self.iterative,
            'Dynamic Programming': self.dynamic_programming,
            'Matrix Exponentiation': self.matrix_exponentiation,
            'Binet Formula': self.binet_formula
        }
        
        all_correct = True
        
        for n in range(1, test_range + 1):
            # 使用迭代算法作为基准
            expected = self.iterative(n)
            results = {}
            
            for name, func in algorithms.items():
                try:
                    result = func(n)
                    results[name] = result
                except Exception as e:
                    results[name] = f"ERROR: {e}"
                    all_correct = False
            
            # 检查所有结果是否一致
            incorrect = []
            for name, result in results.items():
                if isinstance(result, str) or result != expected:
                    incorrect.append(name)
            
            if incorrect:
                print(f"n = {n:<3}: 期望值 = {expected:<10}, 错误算法: {', '.join(incorrect)}")
                all_correct = False
            else:
                if n <= 10:  # 只显示前10个正确结果
                    print(f"n = {n:<3}: 所有算法结果一致 = {expected}")
        
        if all_correct:
            print("\n✅ 所有算法在测试范围内都正确!")
        else:
            print("\n❌ 发现算法结果不一致!")
        
        return all_correct
    
    def analyze_real_world_applications(self):
        """分析实际应用场景"""
        print("\n斐波那契数列的实际应用场景")
        print("=" * 80)
        
        applications = [
            {
                'category': '计算机科学',
                'applications': [
                    '算法分析：用于分析递归算法的时间复杂度',
                    '数据结构：斐波那契堆的实现',
                    '动态规划：经典的教学案例',
                    '随机数生成：某些伪随机数算法的基础'
                ]
            },
            {
                'category': '数学与自然科学',
                'applications': [
                    '黄金比例：相邻斐波那契数的比值趋近于黄金比例φ ≈ 1.618',
                    '植物生长：叶序、花瓣数量、树枝分叉等自然现象',
                    '晶体学：某些晶体结构的分析',
                    '数论：数论性质研究的基础'
                ]
            },
            {
                'category': '金融与经济',
                'applications': [
                    '技术分析：斐波那契回调线、扩展线在股票交易中的应用',
                    '风险管理：用于计算某些金融衍生品定价',
                    '经济建模：某些经济增长模型的基础'
                ]
            },
            {
                'category': '工程与设计',
                'applications': [
                    '建筑设计：黄金比例在建筑设计中的应用',
                    '用户界面：响应式设计的比例计算',
                    '音乐理论：音阶和节奏的数学基础'
                ]
            }
        ]
        
        for app in applications:
            print(f"\n【{app['category']}】")
            for application in app['applications']:
                print(f"  • {application}")
    
    def provide_best_practices(self):
        """提供最佳实践建议"""
        print("\n斐波那契算法选择的最佳实践")
        print("=" * 80)
        
        best_practices = [
            {
                'scenario': '小规模计算 (n < 30)',
                'recommended': '递归算法',
                'reason': '代码简洁易懂，性能差异不明显',
                'implementation': '使用朴素递归或记忆化递归'
            },
            {
                'scenario': '中等规模计算 (30 ≤ n ≤ 10^6)',
                'recommended': '迭代算法',
                'reason': '线性时间复杂度，常数空间复杂度，实现简单',
                'implementation': '使用循环迭代方法'
            },
            {
                'scenario': '大规模计算 (n > 10^6)',
                'recommended': '矩阵快速幂',
                'reason': '对数时间复杂度，适合极大数值计算',
                'implementation': '使用矩阵幂运算'
            },
            {
                'scenario': '需要完整序列',
                'recommended': '动态规划',
                'reason': '存储所有中间结果，便于后续访问',
                'implementation': '使用数组存储整个序列'
            },
            {
                'scenario': '近似计算',
                'recommended': 'Binet公式',
                'reason': '常数时间复杂度，适合快速估算',
                'implementation': '使用黄金比例公式，注意精度问题'
            },
            {
                'scenario': '并发计算',
                'recommended': '矩阵快速幂或迭代',
                'reason': '避免递归深度问题，适合并行化',
                'implementation': '考虑使用多进程或GPU加速'
            }
        ]
        
        for practice in best_practices:
            print(f"\n场景: {practice['scenario']}")
            print(f"推荐算法: {practice['recommended']}")
            print(f"原因: {practice['reason']}")
            print(f"实现建议: {practice['implementation']}")
    
    def run_comprehensive_analysis(self):
        """运行综合分析"""
        print("斐波那契数列算法综合分析")
        print("=" * 80)
        
        # 性能比较
        performance_data = self.compare_algorithms(35)
        
        # 复杂度分析
        self.print_complexity_analysis()
        
        # 正确性测试
        self.test_correctness(20)
        
        # 实际应用场景
        self.analyze_real_world_applications()
        
        # 最佳实践
        self.provide_best_practices()

def main():
    """主函数"""
    analyzer = FibonacciAnalyzer()
    analyzer.run_comprehensive_analysis()

if __name__ == "__main__":
    main()