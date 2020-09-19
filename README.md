# Tracking Sleep using Your Phone and Machine Learning

I've always wondered the exact time I actually spend sleeping at night. So when I needed ideas for the final project of my Mobile Health and Sensing class, I knew making a sleep tracking application was on the top of my list. So that is what me and my partner decided to do; to use our Android phone and a bit of machine learning to determine if the user is sleeping or not.

To track our sleep, we used the phone's tri-axial accelerometer to determine the user is sleeping or in a vigil state. The accelerometer serves as an indicator on how much movement there is on the phone. The more movement there is, the more likely the user is not sleeping, and vice versa. We will use hourly intervals and determine how much of that hour is spent sleeping.

## Data Collection
So first of all, we need to collect some data. We used an Android phone to do this, because it is much more easier to use its accelerometer and retrieve its data compared to using an iOS phone.

We used two methods of collecting data; real-time and simulated. We collected our real-time data by putting our phones in our pockets and going to bed as normal. We composed a rough sleeping log in which we tried to write down at what time we would go to bed and when we would wake up.

We wanted to strictly use real-sleep data because we feel it would result in a better activity recognition. However, there are two main problems that came up during this process of collecting data. The first one is the phone stops collecting data after 4 hours and this could be seen when the final timestamp of the generated CSV file was hours before we actually woke up, making us lose half or more than half of our collected data.

Another problem that we encountered is that it becomes increasingly difficult to know the exact time we fall asleep. We knew it wouldn't be precise but more often than not we just end up guessing to estimate the time when we were tossing and turning and when we were falling asleep. We did this process of data collection for 4 or 5 nights before moving on to another method, because of the problems that would require a lot of work to solve.

![One of the real-time sleeping data that we managed to extract](https://miro.medium.com/max/3200/0*S8rGiDT4HCKMLSEx)

We then came up with a solution, we figured it would save a lot of time and be easier if we just simulated the activities. We then performed two different activities, sleep and vigil. Simulating sleep was easier, as you can just lie down and make minimal movement. Simulating a vigilant state however, is more complex. Simply moving a lot would not work as that is not how people sleep, so you had to gauge how much movement we should make that would a) be realistic and b) would be different enough to the sleep data, so our machine can differentiate between the two.


The problem with this approach is obviously the fact that we are not getting ‘real’ data, but we figured it was close enough to the real data and the time it saved was very beneficial for us.


The problem with this approach is obviously the fact that we are not getting ‘real’ data, but we figured it was close enough to the real data and the time it saved was very beneficial for us.

![Simulated sleep data and simulated vigil data](https://miro.medium.com/max/1400/1*Oevm0paEZ3jpepyh2KZLQw.png)

##Machine Learning

So now that we have all our data, it is time to do the fun machine learning stuff and train our model to predict if someone is sleeping or not. But before that, we made sure to remove the noise in our datas by applying a **butter filter**.

First, we need to extract some features from our data, the classifier will be looking at these features to determine the output later on. Those features are; **mean**, **standard deviation**, **peak length**, **magnitude, dominant frequency**, and **entropy**.

We picked these features because we are going to detect the difference in accelerometer movement, so it makes sense to pick features that can represent how ‘great’ the accelerometer movements are. 


Now it is time for us to use a classifier to, well classify the data based on the features we have extracted.
We created a random forest decision tree using a Stratified KFold cross validation across 10 folds in the data. First we split up the data into 5 minutes intervals and randomly split them up into folds of 10 using the stratifiedKFold method from scikit-learn. We then used a Random Forest classifier to generate a random forest decision tree for our model. We found that this approach yields the best result rather than using the model_selection.KFold method and the regular decision tree.

And after exporting the tree file with graphviz, we can actually visualize how the random forest tree looks like after training it.

![The Random Forest Decision Tree](https://miro.medium.com/max/1118/0*c2E_DMZKQO-3Hr7E)

## Final Result
And voila! We are done with our classifier, and the next step is just running the program and the Android app for the full demonstration of the app. For this, I have made a [video demonstration](https://youtu.be/k_wGoRDrBjk) of the program working.

Here are also some of the outputs that is generated by the program;

![What the program outputs when the user is sleeping. It detects in intervals which state the user is in during that time.
](https://miro.medium.com/max/1400/0*WdVZ1k7vvCDww_6C)

![When the script is killed, the program generates a summary of the period.](https://miro.medium.com/max/1400/0*Can8zvMbO8Z1gA2t)


