//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Numerics;
//using System.Text;
//using System.Threading.Tasks;

//public class Solution
//{

//    public double GetDistance(double x, double y)
//    {
//        double distance;
//        distance = Math.Sqrt(Math.Pow(x, 2) + Math.Pow(y, 2));
//        return distance;
//    }

//    public double GetVectorSize(double A1, double A2)
//    {
//        return Math.Sqrt(Math.Pow(A1, 2) + Math.Pow(A2, 2));
//    }

//    public double GetInner(double x, double y, double x1, double y1)
//    {
//        return (x * x1) + (y * y1);
//    }

//    public int solution(int x, int y, int r, int d, int[,] target)
//    {
//        var inTarget = new List<List<int>>();
//        var idx = target.Length / target.Rank;
//        for (int i = 0; i < idx; i++)
//        {
//            var a = target[i, 0];
//            var b = target[i, 1];
//            if (GetDistance(a, b) <= r)
//            {
//                var targetPoint = new List<int>();
//                targetPoint.Add(a);
//                targetPoint.Add(b);
//                inTarget.Add(targetPoint);
//            }
//        }

//        int count = 0;
//        double u, v, inner, degree = 0.0f;

//        for (int i = 0; i < inTarget.Count; i++)
//        {
//            u = GetVectorSize(x, y);
//            v = GetVectorSize(inTarget[i][0], inTarget[i][1]);

//            inner = GetInner(x, y, inTarget[i][0], inTarget[i][1]);

//            degree = Math.Acos(inner / (u * v));
//            degree = degree * 180 / 3.141592654;

//            if (degree <= d)
//            {
//                count++;
//            }
//        }

//        int answer = count;
//        return answer;
//    }
//}

// 슈퍼캣 문제2 부채꼴 범위에 적이 충돌되는지 여부 
// https://rangsub.tistory.com/15