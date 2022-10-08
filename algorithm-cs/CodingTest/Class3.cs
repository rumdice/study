//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

//public class Solution
//{
//    List<int> myFriends = new List<int>();
//    public List<int> GetMyFriend(int x, int y, int i)
//    {
//        if (x == i)
//        {
//            myFriends.Add(y);
//        }
//        else if (y == i)
//        {
//            myFriends.Add(x);
//        }

//        return myFriends;
//    }

//    List<int> otherFriends = new List<int>();
//    List<int> getOtherFriends(int[,] relation, List<int> myFriends, int my)
//    {
//        foreach (var myFriend in myFriends)
//        {
//            var idx = relation.Length / relation.Rank;
//            for (int i = 0; i < idx; i++)
//            {
//                var a = relation[i, 0];
//                var b = relation[i, 1];

//                if (a == myFriend)
//                {
//                    if (b != my)
//                    {
//                        otherFriends.Add(b);
//                    }
//                }

//                if (b == myFriend)
//                {
//                    if (a != my)
//                    {
//                        otherFriends.Add(a);
//                    }
//                }
//            }
//        }

//        return otherFriends;
//    }

//    public int[] solution(int N, int[,] relation)
//    {
//        var answerList = new List<int>();
//        for (int n = 1; n <= N; n++)
//        {
//            // 각 관계를 순회 하면서 
//            // 나랑 친구인 경우
//            // 1 : 2,3
//            // 친구의 친구인 경우
//            // 2 의 친구를 구함
//            // 3 의 친구를 구함.

//            // 친구의 친구가 나라면 제외
//            // * 예를들어 2의 친구와 3의 친구가 중복인 경우 제외.

//            // 다 더함.

//            var idx = relation.Length / relation.Rank;
//            for (int i = 0; i < idx; i++)
//            {
//                var a = relation[i, 0];
//                var b = relation[i, 1];
//                GetMyFriend(a, b, n);
//            }
            
//            getOtherFriends(relation, myFriends, n);

//            var TotalFrinds = new List<int>();
//            TotalFrinds.AddRange(myFriends);
//            TotalFrinds.AddRange(otherFriends);

//            TotalFrinds = TotalFrinds.Distinct().ToList();
            
//            answerList.Add(TotalFrinds.Count);
//            myFriends.Clear();
//            otherFriends.Clear();
//        }
//        return answerList.ToArray();
//    }
//}
