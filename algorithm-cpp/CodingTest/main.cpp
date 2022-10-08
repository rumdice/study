#include <cstdio>
#include <string>
#include <vector>
#include <iostream>

using namespace std;

vector<int> solution(vector<int> answers) {
    vector<int> answer;
    answer.push_back(1);
    return answer;
}

int main()
{
    vector<int> ans = { 1, 2, 3, 4, 5 };
    vector<int> res = solution(ans);
    //printf("%n", res[0]);
    //std::cout << res << std::end;
    return 0;
}

// 완전 탐색 문제
// 소풍 문제

// 입력
// 테스트 캐이스 수 < 50
