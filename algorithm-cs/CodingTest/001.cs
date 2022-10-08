//// k 번째 수

//using System;
//using System.Collections.Generic;

//namespace programCS
//{
//    public class Solution
//    {
//        // 해결 함수
//        public int[] solution(int[] array, int[,] commands)
//        {
//            int[] answer = new int[] { };

//            for (var i = 0; i < commands.Length; i++) {
//                var start = commands[i, 0] - 1;
//                var end = commands[i, 1];
//                var idx = commands[i, 2] - 1;

//                List<int> data = new List<int>();
//                for (var j = start; j < end; j++) {
//                    data.Add(array[j]);
//                }

//                data.Sort();
//                answer[i] = data[idx];
//            }

//            return answer;
//        }

//        static void Main(string[] args)
//        {
//            var arr = new[] { 1, 5, 2, 6, 3, 7, 4 };
//            var cmd = new[,] { { 2, 5, 3 }, { 4, 4, 1 }, { 1, 7, 3 } };

//            Solution sol = new Solution();
//            var a = sol.solution(arr, cmd);
            
//            Console.WriteLine();
//        }
//    }
//}