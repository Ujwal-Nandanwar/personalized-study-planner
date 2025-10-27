def study_plan_dp(time_required, importance, total_hours):
    n = len(time_required)
    dp = [[0] * (total_hours + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for t in range(1, total_hours + 1):
            if time_required[i-1] <= t:
                dp[i][t] = max(
                    dp[i-1][t],
                    importance[i-1] + dp[i-1][t - time_required[i-1]]
                )
            else:
                dp[i][t] = dp[i-1][t]
    return dp
