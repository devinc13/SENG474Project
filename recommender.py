import csv

likePredictions = []

# CSV file is: inst#,actual,predicted,error,prediction

with open('predictions.csv', 'r') as csvfile:
    predictionReader = csv.reader(csvfile)
    predictionsList = list(predictionReader)

print("Predictions:")
print("inst#,actual,predicted,error,prediction")
for prediction in predictionsList:
    print(prediction)
    if (prediction[2] == '1:like'):
        likePredictions.append(prediction)

sortedLikePredictions = sorted(likePredictions, key=lambda x: x[4], reverse=True)

numRecommendations = 3

recommendations = sortedLikePredictions[0:numRecommendations]
print()
print("Recommending " + str(numRecommendations) + " songs:")
i = 1
for recommendation in recommendations:

    print("Recommendation " + str(i) + " is the song with instance number " + recommendation[0] + " due to its prediction value of " + recommendation[4])
    i += 1