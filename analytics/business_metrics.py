def business_health(revenue, cost):
    if revenue <= 0:
        return "Invalid"

    margin = (revenue - cost) / revenue

    if margin > 0.3:
        return "Strong"
    elif margin > 0.1:
        return "Moderate"
    else:
        return "Weak"
