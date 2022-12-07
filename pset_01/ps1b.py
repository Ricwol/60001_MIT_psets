# House Hunting
# Determine how long it will take you to save enough money to make
# the down payment on your dream house.
#
# Over time, i.e. every six months, you'll receive a pay raise.


# user inputs
annual_salary = int(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = int(input("Enter the cost of your dream home: "))

# Added entry for semi annual pay raise input
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

# Annual return of investment: 4% = 0.04
r = 0.04

# Monthly return of investment rate
monthly_r = r / 12

# Portion of the cost needed for down payment: 25% = 0.25
portion_down_payment = total_cost * 0.25

# Calculate monthly salary
monthly_salary = annual_salary / 12

# Initial monthly salary portion
monthly_portion = monthly_salary * portion_saved

# Initialize savings account
current_savings = 0
months = 0

while current_savings < portion_down_payment:
    # Calculate the monthly interest on savings account
    monthly_interest = current_savings * monthly_r

    # Increase savings by monthly interest and mothly saving rate
    current_savings += monthly_interest + monthly_portion
    months += 1

    # Salary increases after every 6th months
    if months % 6 == 0:
        monthly_salary += monthly_salary * semi_annual_raise
        # Re-calculate the monthly saving rate after pay raise
        monthly_portion = monthly_salary * portion_saved

# Print result of how many months of savings are needed for the down payment
print("Number of months:", months)
