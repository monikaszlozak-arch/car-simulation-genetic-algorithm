import tkinter as tk
class change_the_values_exactly :
    def __init__(self):
        self.root = tk.Tk()
        self.slider_angle = tk.Scale(self.root, from_=-180, to=180 , length=1000 , resolution=0.25, orient="horizontal" , label="angle")
        self.slider_angle.pack() # ustaiwia
        self.slider_size_x = tk.Scale(self.root,  to=500 , length=1000 , resolution=1, orient="horizontal" , label="size x")
        self.slider_size_x.pack() # ustaiwia
        self.slider_size_y = tk.Scale(self.root,  to=500 , length=1000 , resolution=1, orient="horizontal" , label="size y")
        self.slider_size_y.pack()# ustaiwia
        self.slider_x = tk.Scale(self.root, from_=-50, to=50 , length=1000 , resolution=0.1, orient="horizontal" , label="position x")
        self.slider_x.pack() #dodaje
        self.slider_y = tk.Scale(self.root, from_=-50, to=50 , length=1000 , resolution=0.1, orient="horizontal" , label="position y")
        self.slider_y.pack() #dodaje
        
            
    def update(self):
        self.root.update()
        return  [ self.slider_angle.get() , self.slider_size_x.get() , self.slider_size_y.get() , self.slider_x.get() , self.slider_y.get() ]
class instruction :
    def __init__(self):
        self.root = tk.Tk()
        label = tk.Label(self.root, text="1 - Siatka \n2 - Nagroda\n3 -  blocking\n4 add z blocking\n5 - potwierdzenie dokłaadnego pozycjonowania \n6 - CTR - Z dla blok\n7 - zapis do json \n6 - CTR - Z dla nagród")
        label.pack()
    def update(self):
        self.root.update()