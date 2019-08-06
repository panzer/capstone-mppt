import tkinter as tk


class Application:
    def __init__(self):
        self.top = tk.Tk()
        self.top.title("Capstone GUI")
        self.top.minsize(300, 300)

        self.hello_world = tk.Label(self.top, text="Hello World!")

        self.hello_world.pack()

    def run(self):
        self.top.mainloop()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()