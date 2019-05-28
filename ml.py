import numpy as np
# from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from data import Data
from setting import Setting as st
import mongo

flag = True

def predict():
    print(Data.machine_learning_y)
    mongo.get_ml_data()
    #create_data()
    x1 = st.DENSITY_MONSTERS
    x2 = st.DENSITY_SUPERMONSTERS
    x3 = st.DENSITY_MINES
    print(Data.machine_learning_x)
    print(Data.machine_learning_y)
    print(Data.machine_learning_n)
    # model = LinearRegression().fit(Data.machine_learning_x, Data.machine_learning_y)
    # y_pred1 = model.predict(np.array([[x1, x2, x3]]))
    svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
    svr_lin = SVR(kernel='linear', C=100, gamma='auto')

    svr_rbf.fit(Data.machine_learning_x, Data.machine_learning_y)
    svr_lin.fit(Data.machine_learning_x, Data.machine_learning_y)

    pred_rbf = abs(svr_rbf.predict(np.array([[x1, x2, x3]]))%100)
    pred_lin = abs(svr_lin.predict(np.array([[x1, x2, x3]]))%100)

    return pred_rbf, pred_lin

def push(y0):
    y0 = 100 - y0
    x1 = st.DENSITY_MONSTERS
    x2 = st.DENSITY_SUPERMONSTERS
    x3 = st.DENSITY_MINES
    x = Data.machine_learning_x
    y = Data.machine_learning_y
    n = Data.machine_learning_n
    ans=-1
    for i in range(x.shape[0]):
        if x[i][0]==x1 and x[i][1]==x2 and x[i][2]==x3:
            ans = i
            break
    if ans == -1:
        Data.machine_learning_x = np.vstack([x, [x1, x2, x3]])
        Data.machine_learning_y = np.append(y, [y0], axis=0)
        Data.machine_learning_n = np.append(n, [1], axis=0)
    else:
        i = ans
        Data.machine_learning_y[i] = (y[i]*n[i]+y0)/(n[i]+1)
        Data.machine_learning_n[i] += 1
    mongo.create_ml_all_data()
    #mongo.push_ml_one_data([x1,x2,x3], y0)

def create_data():
    # x = [1,99]
    x = np.array([[1, 1, 1],
                  [99, 99, 99]])
    y = np.array([0, 100])
    n = np.array([1, 1])
    Data.machine_learning_x = x
    Data.machine_learning_y = y
    Data.machine_learning_n = n
    mongo.create_ml_all_data()
