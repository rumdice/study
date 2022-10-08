#include <cstdio>
#include <string>
#include <vector>
#include <iostream>

using namespace std;

// p.155 ��ǳ ����
// ���� �ľ�
// n : �л� ��
// m : ģ�� ���� ��
// 2�� ¦ 
// ��� : ¦�� ���� �� �ִ� ����� ���� ��

int n;
bool isFriends[10][10];

// i��° �л��� ¦�� ã���� true, �ƴϸ� false
int countPair(bool taken[10])
{
	// 1. ������� - ��� ¦�� ã���� ��
	bool finished = true;
	for (int i = 0; i < n; i++) 
	{
		if (!taken[i])
			finished = false;
	}
	if (finished)
		return 1;


	int ret = 0;
	// ���� ģ���� �� �л��� ã�� ¦�� �α�
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

// �ڵ����� �� ������ �����ΰ�?
// ��� �� �ڵ带 ������ �� �� �ִ°�?
// �ߺ����� ���� ������ �ذ�


// i��° �л��� ¦�� ã���� true, �ƴϸ� false
int countPair2(bool taken[10])
{
	// 1. ������� - ��� ¦�� ã���� ��
	int firstFree = -1; // ���� �л� �� ���� ��ȣ�� ���� �л��� ã��.
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
	// �� �л�(���� �л� �� ��ȣ�� ���� ���� �л�) �� ¦���� �л� ���ϱ�
	for (int pairWith = firstFree + 1; pairWith < n; pairWith++)
	{
		// ¦�� �ȵ� ���
		if (!taken[pairWith] && isFriends[firstFree][pairWith])
		{
			// �ٽ� ����
			taken[firstFree] = taken[pairWith] = true;
			ret += countPair2(taken);
			taken[firstFree] = taken[pairWith] = false;
		}
	}
	return ret;
}
