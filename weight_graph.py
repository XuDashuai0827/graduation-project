import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 处理要展示的部分静态网络图数据
link_weight_csv = pd.read_csv('link_weight_star.csv') ##
weight = link_weight_csv['star_freq'] ##
aver_w = np.percentile(list(weight),95)
link_weight_len = len(link_weight_csv)
visial_num = []
for i in range(link_weight_len):
    if weight[i] > aver_w:
        visial_num.append(i)

csv_filename = 'visual_data/visial_link_weight_star.csv' ##
link_weight = link_weight_csv.iloc[visial_num]
print(link_weight)
with open(csv_filename, 'w', encoding='utf-8') as f:
    for i in visial_num:
        f.write(link_weight['topic1'][i])
        f.write(",")
        f.write(link_weight['topic2'][i])
        f.write(",")
        f.write(str(link_weight['star_freq'][i])) ##
        f.write('\n')
print(f"Data saved to {csv_filename} successfully.")

## 去掉度太小的节点
G = nx.read_weighted_edgelist('visual_data/visial_link_weight_star.csv', delimiter=',', create_using=nx.Graph()) ##
node_sizes = [d * 60 for _, d in G.degree()]
node_degree = []
for i in range(len(G.degree())):
    node_degree.append(list(G.degree())[i][1])
#print(len(node_degree))
aver_n = np.percentile(node_degree,50)
print(aver_n)
visual_node = []
for i in range(len(G.degree())):
    if node_degree[i] >= aver_n:
        visual_node.append(list(G.degree())[i][0])
#print(visual_node)
link_weight_csv2 = pd.read_csv('visual_data/visial_link_weight_star.csv') ##
visual_drop_num = []
for i in range(len(link_weight_csv2)):
    #print(link_weight_csv2['nodejs'][i],link_weight_csv2['javascript'][i] )
    if (link_weight_csv2['nodejs'][i] not in visual_node) or (link_weight_csv2['javascript'][i] not in visual_node):
        visual_drop_num.append(i)
#print(visual_drop_num)

csv_filename = 'visual_data/visial_link_weight2_star.csv' ##
with open(csv_filename, 'w', encoding='utf-8') as f:
    f.write('nodejs,javascript,289.9\n') ##
    for i in range(len(link_weight_csv2)):
        if i not in visual_drop_num:
            f.write(link_weight_csv2['nodejs'][i])
            f.write(",")
            f.write(link_weight_csv2['javascript'][i])
            f.write(",")
            f.write(str(link_weight_csv2['289.9'][i])) ##
            f.write('\n')
print(f"Data saved to {csv_filename} successfully.")
        
G = nx.read_weighted_edgelist('visual_data/visial_link_weight2_star.csv', delimiter=',', create_using=nx.Graph()) ##
node_sizes = [d * 30 for _, d in G.degree()]
print("networkx 对待画图 csv 文件读取完成")
pos = nx.kamada_kawai_layout(G)
print("使用 Kamada-Kawai 布局绘制图形完成")
print('只显示权重大于',aver_w,'的边、去除小边后节点度大等于',aver_n,'的点，共',len(G.degree()),'个节点',len(link_weight)-len(visual_drop_num),'条边')
nx.draw(G, pos, with_labels=True, font_size=7, node_size=node_sizes, node_color='lightblue', edge_color='pink')
# 设置边权
edge_labels = nx.get_edge_attributes(G, 'weight')
print("边权设置完成")
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # 展示边权
# 显示图形
plt.rcParams['figure.figsize']= (100, 100)
#plt.savefig('network_pictures/topic_network_star.png') ##
plt.show()
