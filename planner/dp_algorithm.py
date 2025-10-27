def study_plan_dp(time_required, importance, total_hours):
    n = len(time_required)
    dp = [[0] * (total_hours + 1) for _ in range(n + 1)]
    
    # Modified logic: consider importance/time ratio for efficiency
    ratio = [importance[i] / time_required[i] for i in range(n)]
    
    for i in range(1, n + 1):
        for t in range(1, total_hours + 1):
            if time_required[i-1] <= t:
                include = importance[i-1] + dp[i-1][t - time_required[i-1]]
                exclude = dp[i-1][t]
                # Ratio acts as tie-breaker for equal importance values
                if include == exclude:
                    dp[i][t] = max(include, exclude, key=lambda x: ratio[i-1])
                else:
                    dp[i][t] = max(include, exclude)
            else:
                dp[i][t] = dp[i-1][t]
    return dp
