//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;


//namespace programCS
//{
//    public class Solution
//    {
//        int hitCount = 0;
//        List<MonsterStatus> monstatusList = new List<MonsterStatus>();
//        List<BulletStatus> bulletStatusList = new List<BulletStatus>();


//        public double GetBulletDegree(int bx, int by)
//        {
//            var bulletDegree = Math.Atan2((0 - bx), (0 - by));
//            return bulletDegree;
//        }

//        public class MonsterStatus
//        {
//            public int x = 0;
//            public int y = 0;

//            public bool isHit = false;
//        }

//        public class BulletStatus
//        {
//            public int x = 0;
//            public int y = 0;

//            public bool isOut = false;
//        }

//        public void OnHit(List<MonsterStatus> monsters, List<BulletStatus> bullets)
//        {
//            foreach (var b in bullets)
//            {
//                var bulletDegree = Math.Atan2((0 - b.x), (0 - b.y));

//                foreach (var m in monsters)
//                {
//                    var monsterDegree = Math.Atan2((0 - m.x), (0 - m.y));
//                    if (monsterDegree == bulletDegree)
//                    {
//                        if (m.isHit == false && b.isOut == false)
//                        {
//                            m.isHit = true;
//                            b.isOut = true;
//                            hitCount++;
//                        }
//                    }
//                }
//            }
//        }

//        public List<MonsterStatus> GetMonster(int [,] monster)
//        {
//            var idx = monster.Length / monster.Rank;
//            for (int i = 0; i < idx; i++)
//            {
//                var x = monster[i, 0];
//                var y = monster[i, 1];

//                var monsterPos = new MonsterStatus();
//                monsterPos.x = x;
//                monsterPos.y = y;
//                monsterPos.isHit = false;

//                monstatusList.Add(monsterPos);
//            }

//            return monstatusList;
//        }

//        public List<BulletStatus> GetBullet(int[,] bullet)
//        {
//            var idx = bullet.Length / bullet.Rank;
//            for (int i = 0; i < idx; i++)
//            {
//                var x = bullet[i, 0];
//                var y = bullet[i, 1];

//                var bulletStatus = new BulletStatus();
//                bulletStatus.x = x;
//                bulletStatus.y = y;
//                bulletStatus.isOut = false;

//                bulletStatusList.Add(bulletStatus);
//            }

//            return bulletStatusList;
//        }


//        public int solution(int[,]monster, int[,] bullet)
//        {
//            var answer = 0;

//            var mList = GetMonster(monster);
//            var bList = GetBullet(bullet);
          

//            OnHit(mList, bList);


//            answer = hitCount;
//            if (answer == 0)
//                return -1;

//            return answer;
//        }
//    }
//}

// 슈퍼캣 문제4 좌표 총알 맞추는 문제.
