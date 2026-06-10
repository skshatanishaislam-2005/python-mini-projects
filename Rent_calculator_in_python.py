rent = int(input("Enter the monthly rent: "))
months = int(input("Enter the number of months: "))
person = int(input("Eneter the number of people sharing the rent: "))
food = int(input("Enter the monthly food expenses: "))
electricity_spend = int(input("Enter the total electricity spend: "))
charge_per_unit = int(input("enter the charge per unit: "))


total_bill = (rent * months) + food + (electricity_spend * charge_per_unit)
bill_per_person = total_bill / person

print("Total bill per person in one month is: ", bill_per_person)
