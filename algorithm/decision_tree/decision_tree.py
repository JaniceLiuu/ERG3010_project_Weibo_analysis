# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import sklearn
from sklearn import tree

# Data Preparation
col_names = ['index','likes','comments','reposts','sentiment','cont_len','emo','hotwords','a_ad_per','label_1','label_2','label_3']
pima = pd.read_csv("data_final_labeled.csv", header = None, names=col_names)
pima = pima.dropna()

# feature_cols = ['sentiment','cont_len','hotwords','a_ad_per']
feature_cols = ['sentiment','cont_len','hotwords']

X = pima[feature_cols] # features n*m martices (m features)
y = pima.label_3 # popularity n*1

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7) # 70% training and 30% test
X_train = pd.DataFrame(X_train, columns = ['sentiment','cont_len','hotwords'])
#X_train = X_train.dropna()
# print(X_train.isnull().value_counts())


################################## Decision Tree Implementation #######################################

# Create Decision Tree classifer object
clf = DecisionTreeClassifier(max_depth = 5, min_samples_leaf = 30) 
# optimization: criterion="entropy", max_depth=n, splitter = random, min_samples_leaf = 5

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)
 
# Get trained feature weights
print(dict(zip(X_train.columns, clf.feature_importances_)))

###################################### Pruning ##########################################################
def is_leaf(inner_tree, index):
    # Check whether node is leaf node
    return (inner_tree.children_left[index] == sklearn.tree._tree.TREE_LEAF and 
            inner_tree.children_right[index] == sklearn.tree._tree.TREE_LEAF)

def prune_index(inner_tree, decisions, index=0):
    # Start pruning from the bottom - if we start from the top, we might miss
    # nodes that become leaves during pruning.
    # Do not use this directly - use prune_duplicate_leaves instead.
    if not is_leaf(inner_tree, inner_tree.children_left[index]):
        prune_index(inner_tree, decisions, inner_tree.children_left[index])
    if not is_leaf(inner_tree, inner_tree.children_right[index]):
        prune_index(inner_tree, decisions, inner_tree.children_right[index])

    # Prune children if both children are leaves now and make the same decision:     
    if (is_leaf(inner_tree, inner_tree.children_left[index]) and
        is_leaf(inner_tree, inner_tree.children_right[index]) and
        (decisions[index] == decisions[inner_tree.children_left[index]]) and 
        (decisions[index] == decisions[inner_tree.children_right[index]])):
        # turn node into a leaf by "unlinking" its children
        inner_tree.children_left[index] = sklearn.tree._tree.TREE_LEAF
        inner_tree.children_right[index] = sklearn.tree._tree.TREE_LEAF
        ##print("Pruned {}".format(index))

def prune_duplicate_leaves(mdl):
    # Remove leaves if both 
    decisions = mdl.tree_.value.argmax(axis=2).flatten().tolist() # Decision for each node
    prune_index(mdl.tree_, decisions)

###############################################################################################

#prune_duplicate_leaves(clf)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy of the model using Gini index as measurement and max depth = 5 is :",metrics.accuracy_score(y_test, y_pred))

################################## Visualizing Decision Trees  ########################################

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = feature_cols,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('tree_unpruned.png')
Image(graph.create_png())


###################################### Record ###################################################
#### label = 1,2,3,4
# d = 5 : 0.317
# d = 10 : 0.34
# d = 15 : 0.34245442010111843

#### label = 0,1
# best para: max_depth = 10, min_samples_split = 30 -> 0.58

#### pruning
# not much change

#### CV
# not much change

#### slice the dataset by popularity
# label 1-2: 0.57
# label 3-4: 0.59

#### slice the dataset by number
# 25%: 0.56-0.57
