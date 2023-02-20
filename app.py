from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import sys
import matplotlib
matplotlib.use('WebAgg')
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from amplitutde_modulation import *
from util import *

app=Flask(__name__,static_url_path='/static')

if __name__ == "__main__":
    app.run(debug=True)


def FM_MAIN(x,inputs):
    [Am,Ac,fm,fc,message_signal,K] = inputs
    if(message_signal=="sin"):
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am/fm)*np.sin(2*np.pi*fm*x))
        y1 = Am*np.sin(2*np.pi*fm*x)#message signal
    else:
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am/fm)*np.sin(2*np.pi*fm*x))
        y1 = Am*np.cos(2*np.pi*fm*x)
    y2 = Ac*np.cos(2*np.pi*fc*x)#carrier signal need to change into scatterplot
        
    plot_graph(x = x, y = y, title = "Modulated wave", name="FM_modulated1.png")
    plot_graph(x = x, y = y1, title = "Message Signal", name="FM_message.png")
    plot_graph(x = x, y = y2, title = "Carrier Signal", name="FM_carrier.png")
    
    
def PHASE_MAIN(x,inputs):
    [Am,Ac,fm,fc,message_signal,K] = inputs
    if(message_signal=="sin"):
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am)*np.cos(2*np.pi*fm*x))
        y1 = Am*np.sin(2*np.pi*fm*x)#message signal
    else:
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am)*np.cos(2*np.pi*fm*x))
        y1 = Am*np.cos(2*np.pi*fm*x)       
    
    y2 = Ac*np.cos(2*np.pi*fc*x)#carrier signal need to change into scatterplot
        
    plot_graph(x = x, y = y, title = "Modulated wave", name="FM_modulated1.png")
    plot_graph(x = x, y = y1, title = "Message Signal", name="FM_message.png")
    plot_graph(x = x, y = y2, title = "Carrier Signal", name="FM_carrier.png")    
    



@app.route('/FM/<index>',methods=['GET','POST'])
def FM(index):
    index = int(index)
    title={1:"Frequency modulation",2:"Phase modulation"}
    if request.method == 'POST':
        fm=int (request.form['fm'])
        fc=int (request.form['fc'])
        Am=int (request.form['Am'])
        Ac=int (request.form['Ac'])
        message_signal = str(request.form['message_signal'])
        K = int(request.form['K'])
        inputs = [Am,Ac,fm,fc,message_signal,K]
        x = np.linspace(-200,200,10000) #domain for the modulated_wave
        s = [1 for i in x]
        if(index==1):
            FM_MAIN(x,inputs)
            
        elif(index==2):
            PHASE_MAIN(x,inputs)   
            
        # elif(index==3):
        #     PULSE_MAIN(x,inputs) 
    return render_template('fm_graphs.html',title=title[index],index=index)






# BASK - Binary Amplitude Shift Key
def BASK(Tb, fc, inputBinarySeq):

  t = np.arange(0, 1+Tb/100, Tb/100)
  c = np.sqrt(2/Tb)*np.sin(2*np.pi*fc*t)  # Equation for the carrier signal as a function of time

  # Generate the message signal
  # N = 8  # Set the number of data elements N
  # m = np.random.rand(N)
  # m = np.array([1,0,1,0,0,1,0])

  m = inputBinarySeq
  N = len(m)

  t1 = 0
  t2 = Tb

  for i in range(N):
      t = np.arange(t1, t2+0.01, 0.01)  # To obtain each data element, generate a random number m in [0,1]
      if m[i] > 0.5:  # If m > 0.5 assign value of m=1, else assign m=0
          m[i] = 1
          m_s = np.ones(len(t))
      else:
          m[i] = 0
          m_s = np.zeros(len(t))

      message = np.zeros((N, len(t)))
      message[i, :] = m_s

      # Product of carrier and message
      ask_sig = c * m_s  # The modulated signal is the product of the message signal level (dc level) and the carrier signal level (analog level)

      t1 = t1 + (Tb + 0.01)
      t2 = t2 + (Tb + 0.01)

      # Plotting the message signal
      plt.subplot(5, 1, 2)
      plt.axis([0, N, -2, 2])
      plt.plot(t, message[i, :], 'r')
      plt.title('message signal')
      plt.xlabel('t')
      plt.ylabel('m(t)')
      plt.grid(True)

      # Plotting the BASK signal (modulated signal)
      plt.subplot(5, 1, 4)
      plt.plot(t, ask_sig)
      plt.title('Amplitude Shift Keying')
      plt.xlabel('t --->')
      plt.ylabel('s(t)')
      plt.grid(True)


  # Save Message & Modulated Signal
  plt.savefig(f'static/results/BASK_msg_mod.png',bbox_inches='tight')

  # Plotting the carrier signal
  plt.figure()
  plt.subplot(5, 1, 3)
  plt.plot(t, c)
  plt.title('carrier signal')
  plt.xlabel('t')
  plt.ylabel('c(t)')
  plt.grid(True)
  plt.savefig(f'static/results/BASK_carrier.png',bbox_inches='tight') # Save
  plt.figure()


  # plt.show()


@app.route('/',methods=['GET'])
def home():
    return redirect(url_for("AM_page"))

@app.route('/AM',methods=['GET'])
def AM_page():
    return render_template('Analog_Modulation.html')

@app.route('/AM/<am_type>',methods=['GET','POST'])
def Amplitutde_Modulation(am_type):  
    root_dir = os.path.dirname(os.getcwd()) 
    res_dir = os.path.join(root_dir,"static","results")
    results = os.listdir('./static/results')
    for images in results:
        if images.endswith(".png"):
            os.remove(os.path.join('./static/results', images))
    
    title = {"MAIN":"Amplitutde Modulation","SSB":"SSB Modulation","DSBSC":"DSB Modulation","QAM":"QAM Modulation"}
    print(am_type)
    if (request.method=='POST'):
        fm=int (request.form['fm'])
        fc=int (request.form['fc'])
        Am=int (request.form['Am'])
        Ac=int (request.form['Ac'])
        message_signal = str(request.form['message_signal'])
        inputs = [Am,Ac,fm,fc,message_signal]
        x = np.linspace(-200,200,10000) #domain for the modulated_wave


        if am_type == "MAIN":
            AM_main_graph(x, inputs)
        elif am_type == "SSB":
            AM_ssb_modulation(x, inputs)
        elif am_type == "DSBSC":
            phi  = float(request.form['phi'])
            inputs.append(phi)
            AM_double_sideband_modulation(x, inputs)
        elif am_type == "QAM":
            message_signal_2 = request.form['message_signal_2']
            inputs.append(message_signal_2)
            AM_QAM(x,inputs) 
    return render_template('AM_graphs.html',am_type=am_type.upper(),title=title[am_type])




@app.route('/DM',methods=['GET'])
def DM_page():
    # return render_template('Digital_Modulation.html')
    return redirect(url_for('DigitalModulation'))


@app.route('/DM/<dmtype>', methods=['GET','POST'])
def DigitalModulation(dmtype):
    print("dmtype == ", dmtype)
    if (request.method=='POST'):
      Tb=int (request.form['Tb'])
      fc=int (request.form['fc'])
      binaryInput = str(request.form['inputBinarySeq'])

      # Change string to array
      inputBinarySeq = np.array(list(binaryInput), dtype=int)

      print("Tb=", Tb)
      print("fc=", fc)
      print("inputBinarySeq=", inputBinarySeq)

      if dmtype.upper() == 'BASK':
          BASK(Tb,fc,inputBinarySeq)

    return render_template('Digital_Modulation.html',dmtype=dmtype.upper())

if __name__ == "__main__":
    app.run(debug=True)
    