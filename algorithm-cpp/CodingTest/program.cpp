#include <cstdio>
#include <string>
#include <vector>
#include <iostream>

using namespace std;

// 1.
// 1부터 n까지의 합을 구하는 메서드를 작성하시오.

// 가장 쉬운 완전탐색
int sum(int n)
{
	int ret = 0;
	for (int i = 1; i <= n; i++)
		ret += i;

	return ret;
}

// 동일한 동작을 재귀함수로
int recursiveSum(int n)
{
	// 1. 기저사례를 먼저 만든다. (무한 반복 방지)
	if (n == 1)
		return 1;

	return n + recursiveSum(n - 1);
}



// 모든 반복문은 재귀로 변환이 가능하다.
// 재귀 구조가 가지는 장점은?
// 어떤 경우에는 코딩이 훨씬 간편해진다.


// 2.
// 0번부터 차례대로 번호가 매겨진 n개의 원소 중 4개를 고르는 모든 '경우의 수'
// 반복이 중첩이다
// 0 부터 n, 그리고 4회


// 가장 쉬운 완전탐색?
void pick(int n)
{
	for (int i = 0; i < n; i++)
		for (int j = i + 1; j < n; j++)
			for (int k = j + 1; k < n; k++)
				for (int l = k + 1; l < n; l++)
					cout << i << "" << j << "" << k << "" << l << endl;
}

// 보기에도 좋지 않고 뽑은 원소의 갯수 4회가 정해지지 않고 유동적인 값이라면 구현 불가능함

// 동일한 동작을 재귀함수로
// n개의 원소 중 m개를 고르는 모든 경우의 수를 나열하시오
// 0. 어떤 작업이 반복되는지 구조 파악
// picked : 지금까지 고른 원소 번호
// toPick : 앞으로 더 고를 원소의 수

void printPicked(vector<int>& picked)
{
	for (int i = 0; i < picked.size(); i++)
		cout << picked[i] << " " << endl;
}

void recursivePick(int n, vector<int>& picked, int toPick)
{
	// 1. 기저사례를 생각한다.
	if (toPick == 0)
	{
		printPicked(picked);
		return;
	}

	int smallist = picked.empty() ? 0 : picked.back() + 1; // 고른게 없다면 0. 있다면 고른 것중 가장 앞의 값

	for (int next = smallist; next < n; next++)
	{
		picked.push_back(next);
		recursivePick(n, picked, toPick - 1);
		picked.pop_back();
	}

}
