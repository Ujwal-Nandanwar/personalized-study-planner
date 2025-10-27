def backtrack_solution(dp, time_required, importance, total_hours):
    selected = []
    i, t = len(time_required), total_hours

    while i > 0 and t > 0:
        if dp[i][t] != dp[i-1][t]:
            selected.append(i-1)
            t -= time_required[i-1]
        i -= 1

    selected.reverse()
    return selected
