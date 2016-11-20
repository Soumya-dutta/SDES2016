"""Calculates the transfer function of the system as demanded by user.

If transfer function not a constant displays different plots such as Time
Response, Bode, Nyquist as demanded by the user.
"""
import control
import matplotlib.pyplot as plt
import Tkinter as tk
from Tkinter import Tk, Button, Radiobutton, StringVar


class Options():
    """
    Create GUI window for different control parameters of the system.

    Parameters:

    - numerator: numerator of the transfer function calculated in
      prog_tf.py
    - denominator: denominator of the transfer function calculated in
      prog_tf.py

    Options provided are time response, bode plot and nyquist plot.
    """

    def __init__(self, numerator, denominator):
        """
        Create a GUI window with title Control Parameter Options

        """
        self.n = numerator
        self.d = denominator
        self.root = Tk()
        self.root.title('Control Parameter Options')
        self.displayoptions()
        self.root.mainloop()

    def displayoptions(self):
        """
        Function displays the different options that are given to the user.

        - If the transfer function is constant it is displayed in the terminal
          and the window closes.

        - If the transfer function is not constant three different options
          are provided to the user.

            - time-domain response for which function step is called

            - Bode plot for which function bode is called

            - Nyquist plot for which function nyq is called

        Radio buttons are the input method for the user.
        """
        self.sys = control.tf(self.n, self.d)
        print("The transfer function of the system is: ")
        print(self.sys)
        if len(self.n) == 1 and len(self.d) == 1:
            print("Transfer function constant. Bye!!")
            self.close()
        else:
            self.v = StringVar()
            Radiobutton(self.root, text="Step Response", variable=self.v,
                        value="step", command=self.step).grid(row=3, column=0,
                                                              sticky=tk.W,
                                                              pady=4)
            Radiobutton(self.root, text="Bode Plot", variable=self.v,
                        value="bode", command=self.bode).grid(row=5, column=0,
                                                              sticky=tk.W,
                                                              pady=4)
            Radiobutton(self.root, text="Nyquist Plot", variable=self.v,
                        value="nyquist", command=self.nyq).grid(row=7,
                                                                column=0,
                                                                sticky=tk.W,
                                                                pady=4)
            Button(self.root, text='Exit',
                   command=self.close).grid(row=10, column=2,
                                            sticky=tk.W, pady=4)

    def step(self):
        """
        Display step response of the system.

        Uses the step_response function of control module to get two arrays

        - T: timestamp against the response

        - yout: actual response data

        They are then plotted using matplotlib
        """
        T, yout = control.step_response(self.sys)
        plt.clf()
        plt.figure(1)
        plt.title("Step Response")
        plt.grid()
        plt.plot(T, yout)
        plt.xlabel('Time(s)')
        plt.ylabel('System Response')
        plt.show()

    def bode(self):
        """
        Display bode plot of the system.

        uses the bode module of control.
        Plots **magnitude in dB** and **phase in degrees** with respect to the
        **Frequency in rad/s**.
        """
        mag, phase, omega = control.bode(self.sys, dB=True)
        plt.clf()
        plt.figure(1)
        plt.subplot(2, 1, 1)
        plt.title("Magnitude Response")
        plt.grid()
        plt.plot(omega, mag, color='g')
        plt.ylabel('Magnitude in dB')
        plt.xlabel('Frequency in rad/s')
        plt.subplot(2, 1, 2)
        plt.title("Phase Response")
        plt.plot(omega, phase, color='r')
        plt.ylabel('Phase in degrees')
        plt.xlabel('Frequency in rad/s')
        plt.grid()
        plt.tight_layout()
        plt.show()

    def nyq(self):
        """
        Display Nyquist plot for the system.

        Uses nyquist plotting functionality of the module control.
        """
        plt.clf()
        plt.figure(1)
        real, imag, freq = control.nyquist(self.sys, Plot=True)
        plt.title("Nyquist Plot")
        plt.xlabel("Re($\omega$)")
        plt.ylabel("Im($\omega$)")
        plt.grid()
        plt.show()

    def close(self):
        """
        Close the GUI window.

        Called when Exit button is pressed by user.
        """
        self.root.destroy()
