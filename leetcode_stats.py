#!/usr/bin/env python3
import requests

USERNAME = "username"

query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

# Fetch total problems from LeetCode
def get_total_questions():
    resp = requests.get("https://leetcode.com/api/problems/all/")
    if resp.status_code != 200:
        return {"Easy": 0, "Medium": 0, "Hard": 0}
    data = resp.json()
    stats = {"Easy": 0, "Medium": 0, "Hard": 0}
    for q in data["stat_status_pairs"]:
        level = q["difficulty"]["level"]
        if level == 1:
            stats["Easy"] += 1
        elif level == 2:
            stats["Medium"] += 1
        elif level == 3:
            stats["Hard"] += 1
    return stats

# GraphQL user stats
variables = {"username": USERNAME}
headers = {
    "Content-Type": "application/json",
    "Referer": f"https://leetcode.com/u/{USERNAME}/",
    "User-Agent": "Mozilla/5.0"
}

resp = requests.post("https://leetcode.com/graphql", json={"query": query, "variables": variables}, headers=headers)
user_data = resp.json()

try:
    ac_data = user_data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
    ac_map = {item["difficulty"]: item["count"] for item in ac_data}
except KeyError:
    print("Error fetching user data.")
    exit(1)

# Data
total_map = get_total_questions()
easy = ac_map.get("Easy", 0)
medium = ac_map.get("Medium", 0)
hard = ac_map.get("Hard", 0)
total_solved = ac_map.get("All", 0)
total_all = total_map["Easy"] + total_map["Medium"] + total_map["Hard"]

# Colors
RESET = "\033[0m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"

# Output
print()
print("      ╭───────────── LeetCode Progress ─────────────╮")
print("      │                                              │")
print("      │               ◜■■■■■■■■◝                    │")
print(f"      │            ◟■■  {BOLD}{total_solved}/{total_all}{RESET}  ■■◞                 │")
print("      │               ◝■■■■■■■■◞                    │")
print("      │                                              │")
print(f"      │               {BOLD}✓ Solved{RESET}                             │")
print("      │                                              │")
print(f"      │   {CYAN}🟦 Easy     {easy:<3} / {total_map['Easy']:<4}{RESET}                      │")
print(f"      │   {YELLOW}🟨 Medium   {medium:<3} / {total_map['Medium']:<4}{RESET}                      │")
print(f"      │   {RED}🟥 Hard     {hard:<3} / {total_map['Hard']:<4}{RESET}                      │")
print("      ╰──────────────────────────────────────────────╯")
print()
