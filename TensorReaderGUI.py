from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tkinter as tk                
from PIL import Image, ImageFilter

import argparse

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None

####################################################################################################
#Code From: https://github.com/niektemme/tensorflow-mnist-predict/
def imageprepare(argv):
  """
  This function returns the pixel values.
  The imput is a png file location.
  """
  im = Image.open(argv).convert('L')
  width = float(im.size[0])
  height = float(im.size[1])
  newImage = Image.new('L', (28, 28), (255)) #creates white canvas of 28x28 pixels
  
  if width > height: #check which dimension is bigger
    #Width is bigger. Width becomes 20 pixels.
    nheight = int(round((20.0/width*height),0)) #resize height according to ratio width
    if (nheigth == 0): #rare case but minimum is 1 pixel
      nheigth = 1  
    # resize and sharpen
    img = im.resize((20,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
    wtop = int(round(((28 - nheight)/2),0)) #caculate horizontal pozition
    newImage.paste(img, (4, wtop)) #paste resized image on white canvas
  else:
    #Height is bigger. Heigth becomes 20 pixels. 
    nwidth = int(round((20.0/height*width),0)) #resize width according to ratio height
    if (nwidth == 0): #rare case but minimum is 1 pixel
      nwidth = 1
     # resize and sharpen
    img = im.resize((nwidth,20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
    wleft = int(round(((28 - nwidth)/2),0)) #caculate vertical pozition
    newImage.paste(img, (wleft, 4)) #paste resized image on white canvas
  
  #newImage.save("sample.png

  tv = list(newImage.getdata()) #get pixel values
  
  #normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
  tva = [ (255-x)*1.0/255.0 for x in tv] 
  return tva
  ###################################################################################################


class TensorReaderGui(tk.Tk): #GUI using Tkinter for program

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # All frames are stacked on top of eachother using hte container
        container = tk.Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.alphalabels = ["A.png","B.png","C.png"]
        self.diglabels = ["zero_digit.png","one_digit.png","two_digit.png","three_digit.png","four_digit.png","five_digit.png","six_digit.png","seven_digit.png","eight_digit.png","nine_digit.png"]
        self.currentalph = 0
        self.currentdig = 0
        
        for myFrame in (HomePage, AlphaPage, DigitPage, UserPage, HelpPage): #Goes through each page
            page_name = myFrame.__name__
            frame = myFrame(parent=container, controller=self)
            self.frames[page_name] = frame

            # All pages are added in order
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("HomePage")

    def show_frame(self, page_name): #Displays frame for name
        frame = self.frames[page_name]
        frame.tkraise()
        
    def next_dig(self,mylabel): #Goes to the next digit file in the list
        if(self.currentdig == 9):
            self.currentdig = 0
        else:
            self.currentdig = self.currentdig + 1
        mylabel.config(text = self.diglabels[self.currentdig])
            
    def prev_dig(self,mylabel): #Goes to the previous digit file in the list
        if(self.currentdig == 0):
            self.currentdig = 9
        else:
            self.currentdig = self.currentdig - 1
        mylabel.config(text = self.diglabels[self.currentdig])
    
    def dig_results(self,myoutlabel,myinlabel): #Shows results from tensorflow on that digit file
        
        ###Tensorflow Digit Code
        
        #add tensorflow stuff here using the current diglabel
        mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

        # Create the model
        x = tf.placeholder(tf.float32, [None, 784])
        W = tf.Variable(tf.zeros([784, 10]))
        b = tf.Variable(tf.zeros([10]))
        y = tf.matmul(x, W) + b
         
        # Define loss and optimizer
        y_ = tf.placeholder(tf.float32, [None, 10])
        
        # The raw formulation of cross-entropy,
        #
        #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
        #                                 reduction_indices=[1]))
        #
        # can be numerically unstable.
        #
        # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
        # outputs of 'y', and then average across the batch.
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
          
        sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()
        # Train
        for _ in range(1000):
            batch_xs, batch_ys = mnist.train.next_batch(100)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
              
        # Test trained model
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        prediction = tf.argmax(y,1)
        ###Tensorflow Digit Code
        
        #If file path is not working, change to this:
        # mystring = "myfilepath" + mylabel
        mystring = myinlabel #File Path should be updated!
        
        image = imageprepare(mystring)
        pred = prediction.eval(feed_dict = {x: [image]}, session = sess) #Returns what the prediction was, is not 100% accurate
        myoutlabel.config(text = "This is the result from tensorflow on that file: " + str(pred[0]))

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Home",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, expand=YES)
        
        digbutton = tk.Button(self, text="Read a pre-selected Digit", command=lambda: controller.show_frame("DigitPage")) #Opens Digit Page
        digbutton.pack(side=TOP, fill=X, expand=YES)
        
        userbutton = tk.Button(self, text="Read a User File", command=lambda: controller.show_frame("UserPage")) #Opens User Page
        userbutton.pack(side=TOP, fill=X, expand=YES)
        
        helpbutton = tk.Button(self, text="Help", command=lambda: controller.show_frame("HelpPage")) #Opens Help Page
        helpbutton.pack(side=TOP, fill=X, expand=YES)
        

class DigitPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Digit",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, expand=YES)
        
        myresultslabel = tk.Label(self, text="")
        myresultslabel.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        myfilelabel = tk.Label(self, text=controller.diglabels[controller.currentdig]) 
        myfilelabel.pack(side=TOP, fill=X, expand=YES)
        
        backbutton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage")) #Returns to home page
        backbutton.pack(side=BOTTOM, fill=X, expand=YES)
        
        cycleleft = tk.Button(self, text="<", command=lambda: controller.prev_dig(myfilelabel)) #Changes left
        cycleleft.pack(side=LEFT, fill=X, expand=YES)
        
        readbutton = tk.Button(self, text="Read", command=lambda: controller.dig_results(myresultslabel,myfilelabel.cget("text"))) #Runs file thorugh tensorflow
        readbutton.pack(side=LEFT, fill=X, expand=YES)
        
        cycleright = tk.Button(self, text=">", command=lambda: controller.next_dig(myfilelabel)) #Changes right
        cycleright.pack(side=LEFT, fill=X, expand=YES)

class UserPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="User File",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, expand=YES)
        
        label2 = tk.Label(self, text="Please Enter a File Name")
        label2.pack(side=TOP, fill=X, expand=YES)
        
        myresultslabel = tk.Label(self, text="")
        myresultslabel.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        myinput = tk.Entry(self) #User input
        myinput.pack(side=TOP, fill=X, expand=YES)
        
        numbutton = tk.Button(self, text="Read Digit", command=lambda: controller.dig_results(myresultslabel,myinput.get())) #Runs file thorugh tensorflow
        numbutton.pack(side=LEFT, anchor=W, fill=X, expand=YES)
        
        backbutton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage")) #Returns to home page
        backbutton.pack(side=BOTTOM, anchor=W, fill=X, expand=YES)

class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Help",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, expand=YES)
        
        helpmsg = tk.Message(self, text = "If you are having issues using your own images, be sure to use 28x28 pixel png. \n Code is available on Github.")
        helpmsg.pack(side=TOP, fill=X, expand=YES)
        
        backbutton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage")) #Returns to home page 
        backbutton.pack(side=TOP, fill=X, expand=YES)

def main(_):
  # Import data
  mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 784])
  W = tf.Variable(tf.zeros([784, 10]))
  b = tf.Variable(tf.zeros([10]))
  y = tf.matmul(x, W) + b

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 10])

  # The raw formulation of cross-entropy,
  #
  #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
  #                                 reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
  # outputs of 'y', and then average across the batch.
  cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()
  # Train
  for _ in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

  # Test trained model
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(accuracy, feed_dict={x: mnist.test.images,
                                      y_: mnist.test.labels}))
  prediction = tf.argmax(y,1)
  mystring = "D:/School/PythonFinalProj/two_digit.png"
  image = imageprepare(mystring)
  prediction.eval(feed_dict = {x: [image]}, session = sess)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data', help='Directory for storing input data')
    FLAGS, unparsed = parser.parse_known_args()
    app = TensorReaderGui()
    app.mainloop()