using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public int solution(int N, int[,] road, int K)
    {
        int answer = 0;
        // 0번 마을에서 각 마을까지 걸리는 가장 최단 시간 목록 구함 - 다익스트라

        int distance = 0; // 거리(비용)
        int town = 1;   // 마을 번호
        List<int> list = new List<int>();
        Queue<(int,int)> queue = new Queue<(int,int)>();
        queue.Enqueue((town, distance));
        
        int[] towns = new int[N];
        for(int i = 0; i < N; i++)
        {
            towns[i] = 999999;
        }

        while(queue.Count > 0)
        {
            (town,distance) = queue.Dequeue();

            if (list.Contains(town) == false)
                list.Add(town);
            towns[town - 1] = distance;

            for (int i = 0; i < road.GetLength(0); i++)
            {
                if(road[i,0] == town && towns[road[i,1]-1] > distance + road[i,2] && distance + road[i,2] <= K)
                    queue.Enqueue((road[i,1], distance + road[i,2]));
                if(road[i,1] == town && towns[road[i,0]-1] > distance + road[i,2] && distance + road[i,2] <= K)
                    queue.Enqueue((road[i,0],distance + road[i,2]));
            }
        }
        
        // 배열을 돌면서 
        answer = list.Count;

        return answer;
    }

    public void dijikstra()
    {

    }

    public void dfs(int now)
    {



    }

    public void bfs()
    {

    }

    static void Main()
    {
        Solution solution = new Solution();
        int n = 5;
        int[,] road = {
            {1,2,1},
            {2,3,3},
            {5,2,2},
            {1,4,2},
            {5,3,1},
            {5,4,2}
        };

        int k = 3;
        solution.solution(n, road, k);

        //Console.WriteLine(solution.solution(n, road, k));
    }
}