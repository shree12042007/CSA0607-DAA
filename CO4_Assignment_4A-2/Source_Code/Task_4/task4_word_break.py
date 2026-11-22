"""
Task 4: Word Break Problem (Pseudocode Forensics & Repair)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
Strategy: Dynamic Programming (Prefix Validity Check DP[j] AND substring(j, i) in Dictionary)
"""

def word_break_faulty(text, dictionary):
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        dp[i] = False
        for j in range(0, i):
            if text[j:i] in dictionary:
                dp[i] = True
                break
    return dp[n], dp

def word_break_repaired(text, dictionary):
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        dp[i] = False
        for j in range(0, i):
            if dp[j] and (text[j:i] in dictionary):
                dp[i] = True
                break
    return dp[n], dp

if __name__ == "__main__":
    print("=== TASK 4: WORD BREAK FORENSICS ===")
    text_fail = "dogsand"
    dict_fail = {"sand"}
    res_f, dp_f = word_break_faulty(text_fail, dict_fail)
    res_r, dp_r = word_break_repaired(text_fail, dict_fail)
    print(f"\n[Test Case 1: Failing Counterexample] Text='{text_fail}', Dict={dict_fail}")
    print(f"  Faulty Output   : {res_f} | DP={dp_f}")
    print(f"  Repaired Output : {res_r} | DP={dp_r} (Expected: False)")

    text_pass = "applepenapple"
    dict_pass = {"apple", "pen"}
    res_f2, dp_f2 = word_break_faulty(text_pass, dict_pass)
    res_r2, dp_r2 = word_break_repaired(text_pass, dict_pass)
    print(f"\n[Test Case 2: Regression Check] Text='{text_pass}', Dict={dict_pass}")
    print(f"  Faulty Output   : {res_f2} | DP={dp_f2}")
    print(f"  Repaired Output : {res_r2} | DP={dp_r2} (Expected: True)")

    text_trap = "catsanddog"
    dict_trap = {"cats", "sand", "cat", "dog", "and"}
    _, dp_t = word_break_repaired(text_trap, dict_trap)
    print(f"\n[Test Case 3: Multi-split Valid Input] Text='{text_trap}', Dict={dict_trap}")
    print(f"  Repaired Output : {dp_t[-1]} | DP={dp_t} (Expected: True)")
