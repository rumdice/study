//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

//public class Team
//{
//    public int Id = 0;
//    public List<int> Member { get; set; } = new List<int>();
//}

//public class Solution
//{
//    List<Team> teams = new List<Team>();
//    int teamId = 1;

//    public void CreateTeam(int i)
//    {
//        var team = new Team();
//        team.Id = teamId++;
//        team.Member.Add(i);
//        teams.Add(team);
//    }

//    int SelectTeam(int i)
//    {
//        var yourTeamId = 0;
//        foreach (var team in teams)
//        {
//            if (!team.Member.Exists(e => e > i))
//            {
//                yourTeamId = team.Id;
//                team.Member.Add(i);
//                return yourTeamId;
//            }
//        }

//        return 0;
//    }

//    public int solution(int[] stats)
//    {
//        foreach (int i in stats)
//        {
//            if (teams.Count == 0)
//            {
//                CreateTeam(i);
//                continue;
//            }

//            var result = SelectTeam(i);
//            if (result == 0)
//            {
//                CreateTeam(i);
//                continue;
//            }
//        }
//        return teams.Count;
//    }
//}