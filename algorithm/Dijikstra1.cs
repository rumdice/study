
public class Dijikstra
{
    public int solution(int N, int[,] road, int K)
    {
        int answer = 0;
        // 1번 마을에서 각 마을까지 걸리는 가장 최단 시간 목록 구함 - 다익스트라

        // 모든 경로 초기화, 1번 부터 시작하므로 자기자신은 0
        int[] result = new int[N + 1];
        for (int i = 0; i < result.Length; i++)
        {
            result[i] = int.MaxValue;
        }
        result[1] = 0;

        for (int i = 1; i <= N; i++) // 모든 마을을 순회 1 ~ 5 i : 목적지 마을 번호
        {
            for (int j = 0; j < road.GetLength(0); j++) // 0 ~ 6 들어온 경로를 순차적으로 체크 
            {
                if (road[j, 0] == i) // 첫번째 노드(마을)이 목적지 인가?
                {
                    if (result[road[j, 1]] > result[road[j, 0]] + road[j, 2]) // 2번째 노드의 비용이 (자신에게 가는 비용 + 두 노드의 비용) 보다 비싼가 
                    {
                        result[road[j, 1]] = result[road[j, 0]] + road[j, 2]; // 3번째에 명시된 비용이 더 싸므로 교체
                    }
                    //else
                    //    result[road[j, 1]] = result[road[j, 1]]; // 기존의 비용이 더 저렴하므로 바꾸지 않음.
                }
                else if (road[j, 1] == i)  // 두번째 노드가 목적지 인가?
                {
                    if (result[road[j, 0]] > result[road[j, 1]] + road[j, 2]) // 1번째 노드의 비용이 (자기 자신에게 가는 비용 + 두 노드의 비용)보다 비싼가?
                    {
                        result[road[j, 0]] = result[road[j, 1]] + road[j, 2];
                    }
                    //else
                    //    result[road[j, 0]] = result[road[j, 0]];
                }
            }
        }


        // 경로중에서 K길이보다 작은경우만 늘려줌
        foreach (var res in result)
        {
            if (res <= K)
                answer++;
        }

        return answer;
    }
}

