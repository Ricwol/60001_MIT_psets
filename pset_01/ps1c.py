# Finding the right amount to save away
#
# Assume the following given:
#   1. Semi-annual raise is 0.07 (7%)
#   2. Investments have an annual return of 0.04 (4%)
#   3. The down payment is 0.25 (25%) of the cost of the house
#   4. The cost of the house is $1M.
#
# Try to find the best rate of savings to achieve a down payment on the house
# within 36 months.
# The savings need to be within 100$ of the required down payment.


# Given values
total_cost = 1000000
semi_annual_raise = 0.07
r = 0.04
epsilon = 100

# Collect the annual salary for our calculation from user input
annual_salary = int(input("Enter the starting salary: "))

# Calculate portion down payment
portion_down_payment = total_cost * 0.25

# Initialize bisection search boundaries from 0 to 10,000 as per assignment
low = 0
high = 10000

# Set steps counter to 1 if first saving rate produces the expected result.
steps = 1

# Search for the best savings rate as long as the difference of the upper and
# lower bound is greater than 1.
# Due to integer division no further progress is possible if high and low are
# only 1 integer apart, e.g.: (3+4) // 2 = 3, resulting in an infinite loop.
while high - low > 1:
    # Reset to initial values
    current_savings = 0
    months = 0
    monthly_salary = annual_salary / 12

    # Calculate new portion_saved
    # Use integer division to cut off decimal places
    # Use float division when dividing by 10,000 to get 4 decimal places
    portion_saved = ((high+low) // 2) / 10000

    # Initial monthly saving portion from salary
    monthly_portion = monthly_salary * portion_saved

    # Calculate savings amount with approximated saving rate for 36 months
    while months < 36:
        # Monthly interest on savings account
        monthly_interest = current_savings * (r/12)

        # Add monthly interest and salary portion to savings
        current_savings += monthly_interest + monthly_portion
        months += 1

        # Every 6 months receive a raise
        if months % 6 == 0:
            # Calculate semi annual salary raise
            monthly_salary += monthly_salary*semi_annual_raise
            # Re-calculate monthly portion after salary raise
            monthly_portion = monthly_salary * portion_saved

    # Break condition if savings is within $100 of the down payment
    if abs(current_savings - portion_down_payment) < epsilon:
        break

    # Eliminate half of the values as per bisection search
    # Convert bound to integer after multiplying by a factor of 10,000
    guess = int(portion_saved * 10000)
    if current_savings < portion_down_payment:
        low = guess
    else:
        high = guess
    # Increment bisection search steps counter
    steps += 1

# Print results if best saving rate was found for a given starter salary
# to afford the down payment with 36 months of saving within $100
if abs(current_savings - portion_down_payment) < epsilon:
    print("Best saving rate:", portion_saved)
    print("Steps in bisection search:", steps)
else:
    print("It is not possible to pay the down payment in three years.")
