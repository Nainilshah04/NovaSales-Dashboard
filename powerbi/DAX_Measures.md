# Power BI DAX Measures

## Import commission_data.csv into Power BI

## 18 DAX Measures:

Total Commission = SUM(fact_sales[commission_earned])
Total Bonus = SUM(fact_sales[bonus_earned])
Total Payout = SUM(fact_sales[total_payout])
Avg Attainment % = AVERAGE(fact_sales[attainment_pct_display])
Reps Above Quota = CALCULATE(DISTINCTCOUNT(fact_sales[rep_id]), fact_sales[attainment_pct] >= 1.0)
Total Reps = DISTINCTCOUNT(fact_sales[rep_id])
Quota Hit Rate % = DIVIDE([Reps Above Quota], [Total Reps]) * 100
Total Sales Revenue = SUM(fact_sales[actual_sales])
Total Quota = SUM(fact_sales[monthly_target])
Overall Attainment % = DIVIDE([Total Sales Revenue], [Total Quota]) * 100
At Risk Rep Count = CALCULATE(DISTINCTCOUNT(fact_sales[rep_id]), fact_sales[attainment_pct] < 0.60)
Top Performer Count = CALCULATE(COUNTROWS(fact_sales), fact_sales[is_top_performer] = 1)
Commission to Revenue % = DIVIDE([Total Commission], [Total Sales Revenue]) * 100
Avg Deals Per Rep = DIVIDE(SUM(fact_sales[deals_closed]), [Total Reps])
Payout Per Rep = DIVIDE([Total Payout], [Total Reps])
YTD Total Payout = TOTALYTD([Total Payout], dim_date[month])
MoM Payout Change = VAR Curr = [Total Payout] VAR Prev = CALCULATE([Total Payout], PREVIOUSMONTH(dim_date[date_id])) RETURN DIVIDE(Curr - Prev, Prev) * 100
Avg Commission Per Rep = DIVIDE([Total Commission], [Total Reps])