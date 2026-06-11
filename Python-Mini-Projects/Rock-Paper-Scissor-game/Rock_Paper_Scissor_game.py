import random
item_list = ["Rock", "Paper","Scissor"]

user_choice = input("Enter your move = Rock, Paper,Scissor = ")
computer_choice = random.choice(item_list)

print(f"User choice ={user_choice},Computer choice = {computer_choice}")

if user_choice == computer_choice:
    print("Both choose same: = It's a tie!😭")    

elif user_choice == "Rock":
    if computer_choice == "Scissor":
        print("Rock smashes Scissor: = You win!🎊")
    else:
        print("Paper fold Rock: = Computer wins!🤖")
    
elif user_choice == "Paper":
    if computer_choice == "Rock":
        print("Paper fold Rock: = You win!🎊")
    else:
        print("Scissor cut Paper: = Computer win!🤖")

elif user_choice == "Scissor":
    if computer_choice == "Rock":
        print("Rock smashes Scissor: = Computer win🤖")
    else:
        print("Scissor cut Paper: = You win!🎊")






