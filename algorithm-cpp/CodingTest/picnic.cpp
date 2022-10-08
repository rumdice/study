#include <cstdio>
#include <string>
#include <vector>
#include <iostream>

using namespace std;

// p.155 소풍 문제
// 문제 파악
// n : 학생 수
// m : 친구 쌍의 수
// 2명씩 짝 
// 출력 : 짝을 지을 수 있는 경우의 가짓 수

int n;
bool isFriends[10][10];

// i번째 학생이 짝을 찾으면 true, 아니면 false
int countPair(bool taken[10])
{
	// 1. 기저사례 - 모든 짝을 찾으면 끝
	bool finished = true;
	for (int i = 0; i < n; i++) 
	{
		if (!taken[i])
			finished = false;
	}
	if (finished)
		return 1;


	int ret = 0;
	// 서로 친구인 두 학생을 찾아 짝을 맺기
	for (int i = 0; i < n; i++)
	{
		for (int j = 0; j < n; j++)
		{
			taken[i] = taken[j] = true;
			ret += countPair(taken);
			taken[i] = taken[j] = false;
		}
	}
	return ret;
}

// 코드이해 및 무었이 문제인가?
// 어떻게 이 코드를 도출해 낼 수 있는가?
// 중복으로 세는 문제를 해결


// i번째 학생이 짝을 찾으면 true, 아니면 false
int countPair2(bool taken[10])
{
	// 1. 기저사례 - 모든 짝을 찾으면 끝
	int firstFree = -1; // 남은 학생 중 가장 번호가 빠른 학생을 찾음.
	for (int i = 0; i < n; i++)
	{
		if (!taken[i])
		{
			firstFree = i;
			break;
		}
	}
	if (firstFree == -1)
		return 1;


	int ret = 0;
	// 이 학생(남은 학생 중 번호가 가장 빠른 학생) 과 짝지을 학생 정하기
	for (int pairWith = firstFree + 1; pairWith < n; pairWith++)
	{
		// 짝이 안된 경우
		if (!taken[pairWith] && isFriends[firstFree][pairWith])
		{
			// 다시 돌림
			taken[firstFree] = taken[pairWith] = true;
			ret += countPair2(taken);
			taken[firstFree] = taken[pairWith] = false;
		}
	}
	return ret;
}
