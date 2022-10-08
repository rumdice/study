// // 내가 생각한 풀이법
// function solution(begin, target, words) {
//     var answer = 0;
//     return answer;
// }

// 풀이법 (나중에 풀이해보기)
function solution(begin, target, words) {
    const visited = {}
    bfs(begin);
    return visited[target] === undefined ? 0 : visited[target];

    function bfs(node) {
        visited[node] = 0;
        const q = [node];
        while (q.length !== 0) {
            const currentNode = q.shift();
            words.filter(word => canChangeWord(word, currentNode))
                .forEach(movableNode => {
                    if (visited[movableNode] === undefined) {
                        visited[movableNode] = visited[currentNode] + 1;
                        q.push(movableNode)
                    }
                });
        }
    }
}

function canChangeWord(wordOne, wordTwo) {
    let count = 0;
    for (let i = 0; i < wordOne.length; i++) {
        if (wordOne[i] !== wordTwo[i]) count++;
    }
    return count === 1 ? true : false;
}



var begin = "hit"
var target = "cog"
var words = ["hot", "dot", "dog", "lot", "log", "cog"]
console.log(solution(begin, target, words));

// 단어 변환 (level3)

// 문제 설명
// 두 개의 단어 begin, target과 단어의 집합 words가 있습니다. 아래와 같은 규칙을 이용하여 begin에서 target으로 변환하는 가장 짧은 변환 과정을 찾으려고 합니다.

// 1. 한 번에 한 개의 알파벳만 바꿀 수 있습니다.
// 2. words에 있는 단어로만 변환할 수 있습니다.
// 예를 들어 begin이 "hit", target가 "cog", words가 ["hot","dot","dog","lot","log","cog"]라면 "hit" -> "hot" -> "dot" -> "dog" -> "cog"와 같이 4단계를 거쳐 변환할 수 있습니다.

// 두 개의 단어 begin, target과 단어의 집합 words가 매개변수로 주어질 때, 최소 몇 단계의 과정을 거쳐 begin을 target으로 변환할 수 있는지 return 하도록 solution 함수를 작성해주세요.

// 제한사항
// 각 단어는 알파벳 소문자로만 이루어져 있습니다.
// 각 단어의 길이는 3 이상 10 이하이며 모든 단어의 길이는 같습니다.
// words에는 3개 이상 50개 이하의 단어가 있으며 중복되는 단어는 없습니다.
// begin과 target은 같지 않습니다.
// 변환할 수 없는 경우에는 0를 return 합니다.

// 입출력 예
// begin	target	words	                                    return
// "hit"	"cog"	["hot", "dot", "dog", "lot", "log", "cog"]	4
// "hit"	"cog"	["hot", "dot", "dog", "lot", "log"]	        0

// 입출력 예 설명
// 예제 #1
// 문제에 나온 예와 같습니다.

// 예제 #2
// target인 "cog"는 words 안에 없기 때문에 변환할 수 없습니다.




// 문제를 읽고 생각나는 대로 적기
// 정답 풀이법

// 틀려도 좋으니 어떻게 풀어야 할지 생각을 해보기
// 왜 예시에서는 hit가 cog가 되는데 저런 스텝을 걸쳐서 4단계라고 했는가?

// begin 단어를 woad 배열에 0번 인덱스와 비교

// 알파벳이 하나만 다른가? 
// 그렇다면 해당 배열 요소를 사용 
// 아니라면 그 다음 배열 요소로 넘어감
// 변환 시 마다 카운트 증가

// begin 단어가 hot이 되었으므로 검색범위 배열 word에서 제외 하고 검색
// 해당 단어 이전의 것들도 검색 대상이 아님 이후로만 검색하기