//// k 번째 수
//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;
//namespace programCS
//{
//    public class Solution
//    {
//        // 해결 함수
//        public string solution(int[] numbers)
//        {
//            //string answer = "";
//            //return answer;

//            Array.Sort(numbers, (x, y) => {
//                string xy = x.ToString() + y.ToString();
//                string yx = y.ToString() + x.ToString();
//                return yx.CompareTo(xy);
//            });

//            if (numbers.Where(x => x == 0).Count() == numbers.Length)
//                return "0";
//            else
//                return string.Join("", numbers);
//        }

//        static void Main(string[] args)
//        {
//            var nums = new[] { 6, 10, 2};
            
//            var sol2 = new Solution();
//            var a = sol2.solution(nums);

//            Console.WriteLine();
//        }
//    }
//}