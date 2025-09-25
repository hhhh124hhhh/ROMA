#!/usr/bin/env python3
"""
斐波那契数列优化实现与性能测试
Optimized Fibonacci Sequence Implementation and Performance Testing
"""

import time
import math
from functools import lru_cache
from typing import List, Tuple, Dict, Optional
import sys

class OptimizedFibonacci:
    """优化后的斐波那契数列计算器"""
    
    def __init__(self):
        self.cache = {}
        self.performance_stats = {}
    
    def iterative_optimized(self, n: int) -> int:
        """优化的迭代实现 - 最优的线性算法"""
        if n <= 1:
            return n
        
        a, b = 0, 1
        # 使用位运算优化循环
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    def iterative_with_mod(self, n: int, mod: Optional[int] = None) -> int:
        """支持模运算的迭代实现"""
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, (a + b) % mod if mod else a + b
        
        return b
    
    def matrix_exponentiation_optimized(self, n: int) -> int:
        """优化的矩阵快速幂实现"""
        if n <= 1:
            return n
        
        def multiply_2x2(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
            """优化的2x2矩阵乘法"""
            return (
                a[0]*b[0] + a[1]*b[2],  # c00
                a[0]*b[1] + a[1]*b[3],  # c01
                a[2]*b[0] + a[3]*b[2],  # c10
                a[2]*b[1] + a[3]*b[3]   # c11
            )
        
        def matrix_power_optimized(matrix: Tuple[int, int, int, int], power: int) -> Tuple[int, int, int, int]:
            """优化的矩阵快速幂"""
            result = (1, 0, 0, 1)  # 单位矩阵
            
            while power > 0:
                if power & 1:  # 使用位运算代替模运算
                    result = multiply_2x2(result, matrix)
                matrix = multiply_2x2(matrix, matrix)
                power >>= 1  # 使用位运算代替除法
            
            return result
        
        # 转换矩阵 [[1, 1], [1, 0]] 表示为 (1, 1, 1, 0)
        transformation_matrix = (1, 1, 1, 0)
        result_matrix = matrix_power_optimized(transformation_matrix, n - 1)
        
        return result_matrix[0]  # F(n) = result[0][0]
    
    def fast_doubling(self, n: int) -> int:
        """快速加倍算法 - O(log n) 时间复杂度"""
        def fast_doubling_helper(k: int) -> Tuple[int, int]:
            """返回 (F(k), F(k+1))"""
            if k == 0:
                return (0, 1)
            
            a, b = fast_doubling_helper(k >> 1)  # k // 2
            c = a * (2 * b - a)
            d = a * a + b * b
            
            if k & 1:  # k 是奇数
                return (d, c + d)
            else:  # k 是偶数
                return (c, d)
        
        return fast_doubling_helper(n)[0]
    
    def fast_doubling_with_mod(self, n: int, mod: Optional[int] = None) -> int:
        """支持模运算的快速加倍算法"""
        def fast_doubling_mod_helper(k: int, m: Optional[int] = None) -> Tuple[int, int]:
            """返回 (F(k), F(k+1)) mod m"""
            if k == 0:
                return (0, 1)
            
            a, b = fast_doubling_mod_helper(k >> 1, m)
            c = a * (2 * b - a)
            d = a * a + b * b
            
            if m:
                c %= m
                d %= m
            
            if k & 1:
                return (d, (c + d) % m if m else c + d)
            else:
                return (c, d)
        
        return fast_doubling_mod_helper(n, mod)[0]
    
    def binet_optimized(self, n: int) -> int:
        """优化的Binet公式实现"""
        if n <= 1:
            return n
        
        # 预计算常量
        sqrt5 = math.sqrt(5)
        phi = (1 + sqrt5) / 2
        
        # 使用对数来避免大数溢出
        log_phi = math.log(phi)
        log_fib = n * log_phi - 0.5 * math.log(5)
        
        # 对于大n，使用对数方法计算
        if n > 70:  # 避免浮点精度问题
            return int(round(math.exp(log_fib)))
        else:
            fib = (phi**n - (-phi)**(-n)) / sqrt5
            return int(round(fib))
    
    def generate_sequence(self, n: int) -> List[int]:
        """生成斐波那契数列的前n项"""
        if n <= 0:
            return []
        if n == 1:
            return [0]
        if n == 2:
            return [0, 1]
        
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        
        return sequence
    
    def is_fibonacci(self, num: int) -> bool:
        """判断一个数是否为斐波那契数"""
        if num < 0:
            return False
        if num == 0 or num == 1:
            return True
        
        # 使用性质：一个数是斐波那契数当且仅当 5*n^2 ± 4 是完全平方数
        test1 = 5 * num * num + 4
        test2 = 5 * num * num - 4
        
        return self._is_perfect_square(test1) or self._is_perfect_square(test2)
    
    def _is_perfect_square(self, n: int) -> bool:
        """判断是否为完全平方数"""
        if n < 0:
            return False
        
        root = int(math.sqrt(n))
        return root * root == n
    
    def benchmark_algorithms(self, max_n: int = 50) -> Dict[str, List[float]]:
        """性能基准测试"""
        algorithms = {
            'Iterative Optimized': self.iterative_optimized,
            'Matrix Exponentiation': self.matrix_exponentiation_optimized,
            'Fast Doubling': self.fast_doubling,
            'Binet Optimized': self.binet_optimized
        }
        
        results = {name: [] for name in algorithms.keys()}
        
        print("优化算法性能基准测试")
        print("=" * 80)
        print(f"{'n':<6} {'Iterative':<15} {'Matrix':<15} {'FastDoubling':<15} {'Binet':<15}")
        print("-" * 80)
        
        test_values = [10, 20, 30, 40, 50, 100, 1000, 10000, 100000]
        
        for n in test_values:
            if n > max_n:
                continue
                
            row = [f"{n:<6}"]
            
            for name, func in algorithms.items():
                start_time = time.time()
                
                try:
                    result = func(n)
                    execution_time = time.time() - start_time
                    results[name].append(execution_time)
                    
                    if execution_time < 0.0001:
                        row.append(f"<0.0001s")
                    elif execution_time < 0.001:
                        row.append(f"{execution_time:.4f}s")
                    else:
                        row.append(f"{execution_time:.6f}s")
                        
                except Exception as e:
                    row.append("ERROR")
                    results[name].append(float('inf'))
            
            print(" ".join(row))
        
        return results
    
    def stress_test(self, max_n: int = 1000000) -> None:
        """压力测试"""
        print(f"\n压力测试 - 计算F({max_n})")
        print("=" * 80)
        
        algorithms_to_test = {
            'Iterative Optimized': self.iterative_optimized,
            'Matrix Exponentiation': self.matrix_exponentiation_optimized,
            'Fast Doubling': self.fast_doubling
        }
        
        for name, func in algorithms_to_test.items():
            print(f"\n测试 {name}:")
            start_time = time.time()
            
            try:
                result = func(max_n)
                execution_time = time.time() - start_time
                
                # 只显示结果的最后几位，因为数字很大
                result_str = str(result)
                if len(result_str) > 20:
                    result_str = f"...{result_str[-17:]}"
                
                print(f"  结果: {result_str}")
                print(f"  执行时间: {execution_time:.6f} 秒")
                print(f"  结果位数: {len(str(result))}")
                
            except Exception as e:
                print(f"  错误: {e}")
    
    def memory_efficiency_test(self) -> None:
        """内存效率测试"""
        print(f"\n内存效率测试")
        print("=" * 80)
        
        import sys
        
        # 测试不同算法的内存使用
        test_n = 100000
        
        algorithms = {
            'Iterative': self.iterative_optimized,
            'Matrix Exponentiation': self.matrix_exponentiation_optimized,
            'Fast Doubling': self.fast_doubling
        }
        
        for name, func in algorithms.items():
            print(f"\n{name} 算法内存使用:")
            
            # 获取初始内存
            initial_objects = len(gc.get_objects()) if 'gc' in sys.modules else 0
            
            start_time = time.time()
            result = func(test_n)
            execution_time = time.time() - start_time
            
            # 获取结果对象大小
            result_size = sys.getsizeof(result)
            
            print(f"  执行时间: {execution_time:.6f} 秒")
            print(f"  结果对象大小: {result_size} 字节")
            print(f"  结果位数: {len(str(result))}")
    
    def practical_examples(self) -> None:
        """实际应用示例"""
        print(f"\n实际应用示例")
        print("=" * 80)
        
        # 示例1: 生成斐波那契数列
        print("\n1. 生成斐波那契数列前20项:")
        sequence = self.generate_sequence(20)
        print(f"   {sequence}")
        
        # 示例2: 判断是否为斐波那契数
        print("\n2. 判断数字是否为斐波那契数:")
        test_numbers = [0, 1, 2, 3, 4, 5, 8, 13, 21, 34, 55, 100, 144]
        for num in test_numbers:
            is_fib = self.is_fibonacci(num)
            print(f"   {num:3d}: {'是' if is_fib else '否'}")
        
        # 示例3: 大数计算
        print("\n3. 大数计算示例:")
        large_n = 100
        result = self.fast_doubling(large_n)
        print(f"   F({large_n}) = {result}")
        print(f"   位数: {len(str(result))}")
        
        # 示例4: 模运算
        print("\n4. 模运算示例:")
        mod_n = 1000
        mod_result = self.fast_doubling_with_mod(100, mod_n)
        print(f"   F(100) mod {mod_n} = {mod_result}")
    
    def optimization_recommendations(self) -> None:
        """优化建议"""
        print(f"\n算法优化建议")
        print("=" * 80)
        
        recommendations = [
            {
                'optimization': '使用快速加倍算法',
                'benefit': 'O(log n) 时间复杂度，适合极大数值计算',
                'when_to_use': '需要计算非常大的斐波那契数时'
            },
            {
                'optimization': '矩阵快速幂优化',
                'benefit': '使用位运算和元组优化，减少内存分配',
                'when_to_use': '需要平衡性能和代码可读性时'
            },
            {
                'optimization': '迭代算法优化',
                'benefit': 'O(n) 时间复杂度，O(1) 空间复杂度，实现简单',
                'when_to_use': '中小规模计算，需要代码简洁时'
            },
            {
                'optimization': '模运算支持',
                'benefit': '避免大数溢出，提高计算效率',
                'when_to_use': '只需要结果对某个数取模时'
            },
            {
                'optimization': '预计算常量',
                'benefit': '避免重复计算，提高Binet公式性能',
                'when_to_use': '需要快速近似计算时'
            },
            {
                'optimization': '内存优化',
                'benefit': '使用元组代替列表，减少内存分配',
                'when_to_use': '内存受限环境'
            }
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['optimization']}")
            print(f"   优势: {rec['benefit']}")
            print(f"   适用场景: {rec['when_to_use']}")

def main():
    """主函数"""
    fib = OptimizedFibonacci()
    
    # 运行基准测试
    fib.benchmark_algorithms()
    
    # 压力测试
    fib.stress_test(100000)
    
    # 实际应用示例
    fib.practical_examples()
    
    # 优化建议
    fib.optimization_recommendations()

if __name__ == "__main__":
    main()