using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

public class Solution
{
	public List<Quest> QuestList = new List<Quest>();

	public struct Quest
	{
		public int Id;
		public List<int> subQuests;
	}

	List<int> subQuest = new List<int>();
	public List<int> GetSubQuest(int x, int y, int i)
	{
		if (x != i && y == i)
		{
			subQuest.Add(x);
		}

		return subQuest;
	}

	public int[] solution(int N, int[,] relation)
	{
		// 현재 진행 할 수 있는 퀘스트
		// 12345

		// 연관된 퀘스트가 없으면서 숫자가 가장 작은 퀘스트
		// 1부터 순회

		// 연관된 퀘스트가 있는가?
		// 연관된 퀘스트가 있는 경우 몇개의 퀘스트가 있는가?

		// 1부터 5까지 연관된 선행 퀘스트를 나열 (n)
		// 릴레이션을 순회 하면서
		// 본인이 릴레이션에 포함 되는가?
		// 본인이 릴레이션의 y 자리인가?
		// - 해당 캐이스의 x가 선행 클래스 값이다.

		// 해당 퀘스트를 클리어 하기 전에 선행 해야 하는 퀘스트 목록
		// 1 : 없음
		// 2 : 없음
		// 3 : 1
		// 4 : 1, 5
		// 5 : 3

		// 1부터 순회 하면서
		// 없음
		// 선행 퀘스트 숫자 갯수가 적은 것 부터, 같은 경우 숫자가 작은 것
		// 숫자가 작은 것부터 클리어
		// 1, 2, 3, 5, 4 


		var answerList = new List<int>();

		for (int n = 1; n <= N; n++)
		{
			var idx = relation.Length / relation.Rank;
			for (int i = 0; i < idx; i++)
			{
				var a = relation[i, 0];
				var b = relation[i, 1];
				GetSubQuest(a, b, n);
			}

			var quest = new Quest();
			quest.Id = n;
			quest.subQuests = subQuest.ToList();
			QuestList.Add(quest);

			subQuest.Clear();
		}

		// var result = from i in QuestList orderby i.subQuests.Count, i.Id select i;
		// 선행 퀘스트 갯수가 같은 경우 작은 것부터 해야함.
		var result = QuestList.OrderBy(e => e.subQuests.Count).ThenBy(e => e.Id).ToList();
		
		foreach (var res in result)
		{
			answerList.Add(res.Id);
		}

		return answerList.ToArray();
	}
}
