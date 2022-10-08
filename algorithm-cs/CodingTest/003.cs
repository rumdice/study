//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

////문제 설명
////H-Index는 과학자의 생산성과 영향력을 나타내는 지표입니다. 
////어느 과학자의 H-Index를 나타내는 값인 h를 구하려고 합니다. 
////위키백과1에 따르면, H-Index는 다음과 같이 구합니다.

////어떤 과학자가 발표한 논문 n편 중, h번 이상 인용된 논문이 h편 이상이고
////나머지 논문이 h번 이하 인용되었다면 h의 최댓값이 이 과학자의 H-Index입니다.

////어떤 과학자가 발표한 논문의 인용 횟수를 담은 배열 citations가 매개변수로 주어질 때,
////이 과학자의 H-Index를 return 하도록 solution 함수를 작성해주세요.

////제한사항
////과학자가 발표한 논문의 수는 1편 이상 1,000편 이하입니다.
////논문별 인용 횟수는 0회 이상 10,000회 이하입니다.

////입출력 예
////citations	return
////[3, 0, 6, 1, 5] 3

////입출력 예 설명
////이 과학자가 발표한 논문의 수는 5편이고, 그중 3편의 논문은 3회 이상 인용되었습니다.
////그리고 나머지 2편의 논문은 3회 이하 인용되었기 때문에 이 과학자의 H-Index는 3입니다.

//namespace programCS
//{
//    public class Solution
//    {
//        // 오답. (모든 테스크 케이스를 통과 못함)
//        public int solution(int[] citations)
//        {
//            int answer = 0;
//            // 가장 큰 수로 정렬.
//            // h 인덱스가 될수 있는 범위 : 최대 수 논문의 갯수 ~ 0
//            // 해당 인덱스의 수가 입력된 수 보다 크면 +1 (반복)
//            // 5 : 2, 3
//            // 4 : 2, 3
//            // 3 : 3, 2 -> 스톱 (3 == 3) 같음.

//            // 5
//            // 4
//            // 3 ..

//            // linq를 이용?
//            // 자료형에 상관 없이 generic 한 정렬이 하고 싶다.
//            // 어케 접근 하는겨?
//            var asc = citations.OrderBy(i => i);
//            var desc = citations.OrderByDescending(i => i);

//            // linq 안씀
//            Array.Sort(citations, (a, b) => a.CompareTo(b)); // asc
//            Array.Sort(citations, (a, b) => b.CompareTo(a)); // desc


//            Array.Sort(citations, (a, b) => (a < b) ? -1 : 1);
//            for (int i = 0; i < citations.Length; i++) {
//                int hIndex = citations.Length - i;

//                if (citations[i] >= hIndex) {
//                    answer = hIndex;
//                    break;
//                }
//            }

//            return answer;
//        }
//    }
//}