// #1
//var nums = new[] { 5, 3, 4, 6, 2, 1 };
//// var nums = new[] { 6, 2, 3, 4, 1, 5 };
//var sol = new Solution();
//var ans = sol.solution(nums);
//Console.WriteLine(ans);


// #2
//var targets = new int[,]
//{
//    { 0, 1 },
//    { -1, 1 },
//    { 1, 0 },
//    { -2, 2 }
//};

//var sol = new Solution();
//var ans = sol.solution(-1, 2, 2, 60, targets);
//Console.WriteLine(ans);


// #3
//var relation = new int[,]
//{
//    { 1, 2 },
//    { 4, 2 },
//    { 3, 1 },
//    { 4, 5 }
//};

//var sol = new Solution();
//var ans = sol.solution(5, relation);
//foreach (var x in ans)
//{
//    Console.WriteLine(x);
//}


//// #4
//var monster = new int[,]
//{
//	{2,3},
//	{4,5},
//	{3,-3},
//	{2,-4},
//	{3,-6},
//	{-3,-3},
//	{-5,0},
//	{-4,4}
//};

//var bullet = new int[,]
//{
//	{4,1},
//	{4,6},
//	{1,-2},
//	{-4,-4},
//	{-3,0},
//	{-4,4}
//};

//var sol = new Solution();
//var ans = sol.solution(monster, bullet);



//// #5
var relation = new int[,]
{
    { 1, 3 },
    { 1, 4 },
    { 3, 5 },
    { 5, 4 }
};

var sol = new Solution();
var ans = sol.solution(5, relation);
foreach (var x in ans)
{
    Console.WriteLine(x);
}