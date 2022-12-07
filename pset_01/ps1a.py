# House Hunting
# Determine how long it will take you to save enough money to make
# the down payment on your dream house.

# user inputs
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save as adecimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

# annual return of investment: 4%
r = 0.04

# portion of the cost needed for down payment: 25% = 0.25
portion_down_payment = total_cost * 0.25

# Calculate monthly salary
monthly_salary = annual_salary / 12

# Calculate fixed values
monthly_r = r / 12
monthly_portion = monthly_salary * portion_saved

current_savings = 0
months = 0
while current_savings < portion_down_payment:
    # Calculate monthly interest on current savings amount
    monthly_interest = current_savings * monthly_r

    # Increase savings by monthly interest and monthly saved portion of salary
    current_savings += monthly_interest + monthly_portion
    months += 1

# Print result how many months of saving is needed to afford the down payment
print("Number of months:", months)
