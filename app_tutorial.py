import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

### https://www.linkedin.com/learning/python-for-data-science-and-machine-learning-essential-training-part-1/bar-charts-and-pie-charts-in-streamlit?autoSkip=true&resume=false&u=262063330

################################ TUTORIAL 1
st.write("hello world")

################################ TUTORIAL 2

col_names = ['colum1', 'colum2', 'colum3']
data= pd.DataFrame(np.random.randint(30,size=(30,3)),columns=col_names)

'line graph:'
st.line_chart(data)

'bar graph:'
st.bar_chart(data)

animals = ['cat', 'cow','dog']
heights= [30,150,80]

'pie chart:'

fig, ax = plt.subplots()
ax.pie(heights, labels=animals)

st.pyplot(fig)



################################ TUTORIAL 3

rows= np.random.randn(1,1)

'growing line chart:'

chart = st.line_chart(rows)

for i in range(1,100):
    new_rows = rows[0]+ np.random.randn(1,1)
    chart.add_rows(new_rows)
    time.sleep(0.05)
    rows = new_rows

values = np.random.rand(10)
'matplotlibs line chart:'
fig,ax= plt.subplots()
ax.plot(values)

st.pyplot(fig)


################################ TUTORIAL 4

animals = ['cat', 'cow','dog','goat']
heights= [30,150,80,60]
weights= [5,400,40,50]

fig, ax= plt.subplots()

x= np.arange(len(heights))
width=0.4

ax.bar(x-0.2,heights, width, color='red')
ax.bar(x+0.2,weights, width, color='green')

ax.legend(['height', 'weight'])

ax.set_xticks(x)
ax.set_xticklabels(animals)
st.pyplot(fig)


explode = [0.2,0.1,0.1,0.1]

plot_pie,ax= plt.subplots()

ax.pie(heights, explode= explode, labels=animals, autopct='%1.1f%%',shadow=True)

ax.axis('equal')

st.pyplot(plot_pie)

