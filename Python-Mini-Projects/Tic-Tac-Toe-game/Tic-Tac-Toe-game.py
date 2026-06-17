import tkinter as tk
from tkinter import messagebox 

def check_winner():
    global winner 
    for combo in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]['text'] != "":
            winner = True
            winning_indices = set(combo)
            
            
            for i, cell in enumerate(cells):
                if cell["text"] != "":  
                    if i in winning_indices:
                        cell.config(bg="green", fg="white")   
                    else:
                        cell.config(bg="red", fg="white")    

            root.update()
            root.after(300, lambda p=buttons[combo[0]]["text"]: show_winner(p))
            return
        
def show_winner(player):
    messagebox.showinfo("Tic-Tac-Toe", f"Player {player} wins!")
    root.quit()

def cell_click(index):
    if cells[index]["text"] == "" and not winner:
        cells[index].config(text=current_player, bg="#d0f0d0" if current_player == "X" else "#f0d0d0")
        check_winner()
        if not winner:
            toggle_player()




def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")

root = tk.Tk()
root.title("Tic-Tac-Toe")

cells = []
for i in range(9):
    lbl = tk.Label(
        root,
        text="",
        font=("normal", 25),
        width=20,
        height=6,
        relief="groove",
        bg="#eeeeee",
        cursor="hand2"
    )
    lbl.grid(row=i // 3, column=i % 3, padx=2, pady=2)
    lbl.bind("<Button-1>", lambda e, idx=i: cell_click(idx))
    cells.append(lbl)

buttons = cells  

current_player = "X"
winner = False

label = tk.Label(root, text=f"Player {current_player}'s turn", font=("normal", 16))
label.grid(row=3, column=0, columnspan=3)

root.mainloop()





