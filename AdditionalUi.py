from customtkinter import *
import DataHandling


set_appearance_mode("default")



def center_window(window, width, height):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate X and Y coordinates for the top-left corner
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

def delete(window):
    window.withdraw()
    window.quit()
    return

class RateUs:
    def __init__(self):

        root = CTk("black")

        root.overrideredirect(True)
        center_window(root, 300, 340)
        x_button = CTkButton(root, text="X", font=("george", 20), command=lambda: delete(root), width=40, height=40,
                             corner_radius=0, fg_color="red", hover_color="red3")
        x_button.pack(anchor="ne")

        rateus = CTkLabel(root,text="Rate Us",text_color="white",font=("impact",40))
        rateus.pack(pady=(0,0),padx=(0,0))

        star_frame = CTkFrame(root,width=300,height=100,fg_color="black")
        star_frame.pack(pady=(30,0))

        stars = {}

        rating_messages = ["Poor","Not Good","Good !","Fantastic !!!","Loved it !!!!!!"]
        def fill_color(index):

            # Fill first `i` stars
            for star in range(0,index+1):
                stars[star].configure(text_color="yellow")

            # Fill remaining stars
            for star in range(index+1, 5):
                stars[star].configure(text_color="white")

            # Change rating message
            star_message.configure(text = rating_messages[index])

            # Show submit button
            submit.pack_forget()
            submit.configure(command=lambda x = index+1:self.submit(x,root))
            submit.pack()
        star_message = CTkLabel(star_frame,text="",font=("default",20),text_color="white")
        star_message.grid(row=1,columnspan=5,pady=(8,0))
        for i in range(0,5):
            stars[i] = CTkButton(star_frame,text="★",command=lambda x=i:fill_color(x),width=30,height=70,font=("Segoe UI Emoji",30),fg_color="black",hover_color="gray10")
            stars[i].grid(row=0,column=i,padx=2)

        message_text = """
Rating helps us to Improve !
                        """
        submit = CTkButton(root,text="Submit!",font=("default",20),fg_color="green",width=20,corner_radius=5,hover_color="green3")
        submit.pack_forget()

        message = CTkLabel(root,text=message_text,font=("default",20),text_color="white")
        message.pack()
        root.mainloop()
    @staticmethod
    def submit(rating,window):

        DataHandling.update_rating(rating)
        delete(window)
        return


class Feedback:
    def __init__(self):
        root = CTk()
        root.resizable(False,False)
        center_window(root,300,400)
        root.title("Feedback")
        root.configure(fg_color="gray60")
        root.iconbitmap("assets/icon.ico")

        feedback_label = CTkLabel(root,text="Feedback",font=("impact",40))
        feedback_label.pack()

        feedback_entry = CTkTextbox(root,width=280,height=250,font=("default",18),wrap="word",activate_scrollbars=True)
        feedback_entry.pack(pady=(30,0))

        submit = CTkButton(root, text="Submit!", font=("default", 20), fg_color="green", width=40,height=20, corner_radius=5,
                           hover_color="green3", command=lambda : self.submit(root,str(feedback_entry.get("1.0", "end-1c") )))
        submit.pack(pady=(20,0))

        root.mainloop()

    @staticmethod
    def submit(root,feedback):
        DataHandling.add_feedback(feedback)
        delete(root)



class AskName:
    def __init__(self):
        root = CTk()
        root.resizable(False, False)
        center_window(root, 300, 200)
        root.iconbitmap("assets/icon.ico")
        root.title("Name")
        name_label = CTkLabel(root, text="Your Name", font=("impact", 30))
        name_label.pack(pady=(20,0))


        Name_entry = CTkEntry(root, width=250, height=20, font=("default", 20), placeholder_text="Please Enter Your Name")
        Name_entry.pack(pady=(30, 0))

        submit = CTkButton(root, text="Submit", font=("default", 20), fg_color="green", width=40, height=20,corner_radius=5,hover_color="green3",command=lambda: self.submit(root, str(Name_entry.get())))
        submit.pack(pady=(20, 0))
        root.mainloop()

    @staticmethod
    def submit(root, name):
        delete(root)
        DataHandling.Uid(name).make()




