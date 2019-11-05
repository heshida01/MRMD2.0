# https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
# https://blog.csdn.net/hustqb/article/details/80628721

from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler ,StandardScaler
import argparse
import  numpy as np

def tsne_scatter(file,dim,perplexity,early_exaggeration,learning_rate,n_iter):

    df = pd.read_csv(file,engine='python')
    tsne = TSNE(n_components=dim,perplexity=perplexity,early_exaggeration=early_exaggeration,learning_rate=learning_rate,n_iter=n_iter)

    label_name = df.columns.values[0]
    fea_data = df.drop(columns=[label_name])  # 取出所有特征向量用于降维
    redu_fea = tsne.fit_transform(fea_data)  # 将数据降到2维进行后期的可视化处理
    labels = df.iloc[:,0]
    redu_data = np.vstack((redu_fea.T, labels.T)).T  # 将特征向量和正反例标签整合
    tsne_df = pd.DataFrame(
        data=redu_data, columns=['Dimension1', 'Dimension2', "label"])

    scaler = StandardScaler()
    tsne_df[['Dimension1', 'Dimension2']] = scaler.fit_transform(tsne_df[['Dimension1', 'Dimension2']])
    p1 = tsne_df[(tsne_df.iloc[:,2] == 1)]
    p2 = tsne_df[(tsne_df.iloc[:,2] == 0)]
    x1 = p1.values[:, 0]
    y1 = p1.values[:, 1]
    x2 = p2.values[:, 0]
    y2 = p2.values[:, 1]

    # 绘制散点图
    plt.plot(x1, y1, 'o', color="#3dbde2", label='positive',markersize='1')
    plt.plot(x2, y2, 'o', color="#b41f87", label='negative', markersize='1')
    plt.xlabel('Dimension1', fontsize=9)
    plt.ylabel('Dimension2', fontsize=9)

    plt.legend(loc="upper right",fontsize="x-small")
    plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=
        "Visualzes the features based on t-sne in a 2D feature space")
    parser.add_argument(
        '-i',
        '--inputfile',
        help=
        "The input file should be csv format, and multiple file should be separated by commas",
        required=True)
    parser.add_argument(
        '-d', '--d_n_components', help='Dimension of the embedded space.', default=2)
    parser.add_argument(
        '-p',
        '--perplexity',
        help=
        'The perplexity is related to the number of nearest neighbors that is used in other manifold learning algorithms.  ',
        default=30)
    parser.add_argument(
        '-e',
        '--early_exaggeration',
        help='Controls how tight natural clusters in the original space are in the embedded space and how much space will be between them.',
        default=12.0)
    parser.add_argument(
        '-l',
        '--learning_rate',
        help='The learning rate for t-SNE is usually in the range [10.0, 1000.0]. I.',
        default=200)
    parser.add_argument(
        '-n',
        '--n_iter',
        help='Maximum number of iterations for the optimization. Should be at least 250..',
        default=1000)

    args = parser.parse_args()
    tsne_scatter(args.inputfile,args.d_n_components,args.perplexity,args.early_exaggeration,args.learning_rate,args.n_iter)


