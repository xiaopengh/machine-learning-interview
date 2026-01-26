# Chinese to English term translations for ML interview Q&A
# Used to add English translations in parentheses for key terms

TERM_TRANSLATIONS = {
    # Basic concepts
    "损失函数": "Loss Function",
    "过拟合": "Overfitting",
    "欠拟合": "Underfitting",
    "梯度下降": "Gradient Descent",
    "梯度消失": "Vanishing Gradient",
    "梯度爆炸": "Gradient Explosion",
    "正则化": "Regularization",
    "归一化": "Normalization",
    "标准化": "Standardization",
    "泛化": "Generalization",
    "泛化能力": "Generalization Ability",
    "经验风险": "Empirical Risk",
    "结构风险": "Structural Risk",
    "偏差": "Bias",
    "方差": "Variance",
    "奥卡姆剃刀": "Occam's Razor",

    # Evaluation metrics
    "精确率": "Precision",
    "召回率": "Recall",
    "准确率": "Accuracy",
    "混淆矩阵": "Confusion Matrix",
    "交叉验证": "Cross-Validation",
    "真阳性率": "True Positive Rate",
    "假阳性率": "False Positive Rate",

    # Feature engineering
    "特征工程": "Feature Engineering",
    "特征选择": "Feature Selection",
    "缺失值": "Missing Value",
    "异常值": "Outlier",
    "独热编码": "One-Hot Encoding",
    "序号编码": "Ordinal Encoding",
    "二进制编码": "Binary Encoding",
    "特征缩放": "Feature Scaling",
    "降维": "Dimensionality Reduction",
    "主成分分析": "Principal Component Analysis/PCA",
    "维度灾难": "Curse of Dimensionality",

    # Probability and statistics
    "条件概率": "Conditional Probability",
    "联合概率": "Joint Probability",
    "边缘概率": "Marginal Probability",
    "先验概率": "Prior Probability",
    "后验概率": "Posterior Probability",
    "似然函数": "Likelihood Function",
    "极大似然估计": "Maximum Likelihood Estimation/MLE",
    "最大后验概率": "Maximum A Posteriori/MAP",
    "贝叶斯定理": "Bayes' Theorem",
    "贝叶斯估计": "Bayesian Estimation",
    "拉普拉斯平滑": "Laplacian Smoothing",
    "信息熵": "Information Entropy",
    "条件熵": "Conditional Entropy",
    "联合熵": "Joint Entropy",
    "互信息": "Mutual Information",
    "信息增益": "Information Gain",
    "信息增益比": "Information Gain Ratio",
    "基尼系数": "Gini Index",

    # Distance measures
    "欧氏距离": "Euclidean Distance",
    "曼哈顿距离": "Manhattan Distance",
    "切比雪夫距离": "Chebyshev Distance",
    "马氏距离": "Mahalanobis Distance",
    "余弦相似度": "Cosine Similarity",
    "汉明距离": "Hamming Distance",

    # Models
    "决策树": "Decision Tree",
    "随机森林": "Random Forest",
    "支持向量机": "Support Vector Machine/SVM",
    "核函数": "Kernel Function",
    "线性核": "Linear Kernel",
    "多项式核": "Polynomial Kernel",
    "高斯核": "Gaussian Kernel/RBF",
    "朴素贝叶斯": "Naive Bayes",
    "贝叶斯网络": "Bayesian Network",
    "逻辑回归": "Logistic Regression",
    "线性回归": "Linear Regression",
    "广义线性模型": "Generalized Linear Model",
    "梯度提升": "Gradient Boosting",
    "集成学习": "Ensemble Learning",

    # Ensemble methods
    "装袋法": "Bagging",
    "提升法": "Boosting",
    "堆叠法": "Stacking",
    "弱分类器": "Weak Classifier",
    "基分类器": "Base Classifier",

    # Tree-related
    "剪枝": "Pruning",
    "前剪枝": "Pre-pruning",
    "后剪枝": "Post-pruning",
    "叶节点": "Leaf Node",
    "内部节点": "Internal Node",
    "根节点": "Root Node",

    # Neural networks
    "激活函数": "Activation Function",
    "反向传播": "Backpropagation",
    "前向传播": "Forward Propagation",
    "隐藏层": "Hidden Layer",
    "输入层": "Input Layer",
    "输出层": "Output Layer",
    "全连接层": "Fully Connected Layer",
    "权重": "Weight",
    "偏置": "Bias",
    "学习率": "Learning Rate",
    "批量大小": "Batch Size",
    "迭代": "Iteration",
    "轮次": "Epoch",

    # CNN
    "卷积核": "Convolution Kernel",
    "卷积层": "Convolution Layer",
    "池化": "Pooling",
    "池化层": "Pooling Layer",
    "步长": "Stride",
    "填充": "Padding",
    "特征图": "Feature Map",
    "感受野": "Receptive Field",
    "平移不变性": "Translation Invariance",
    "参数共享": "Parameter Sharing",
    "稀疏交互": "Sparse Interaction",

    # RNN/LSTM
    "循环神经网络": "Recurrent Neural Network/RNN",
    "长短期记忆": "Long Short-Term Memory/LSTM",
    "门控循环单元": "Gated Recurrent Unit/GRU",
    "遗忘门": "Forget Gate",
    "输入门": "Input Gate",
    "输出门": "Output Gate",
    "更新门": "Update Gate",
    "重置门": "Reset Gate",
    "细胞状态": "Cell State",
    "隐藏状态": "Hidden State",
    "长期依赖": "Long-term Dependency",
    "序列到序列": "Sequence-to-Sequence/Seq2Seq",
    "编码器": "Encoder",
    "解码器": "Decoder",

    # Attention
    "注意力机制": "Attention Mechanism",
    "自注意力": "Self-Attention",
    "多头注意力": "Multi-Head Attention",

    # Regularization techniques
    "丢弃法": "Dropout",
    "批量归一化": "Batch Normalization",
    "权重衰减": "Weight Decay",
    "早停": "Early Stopping",
    "数据增强": "Data Augmentation",

    # Optimization
    "梯度": "Gradient",
    "随机梯度下降": "Stochastic Gradient Descent/SGD",
    "小批量梯度下降": "Mini-batch Gradient Descent",
    "动量": "Momentum",
    "牛顿法": "Newton's Method",
    "拟牛顿法": "Quasi-Newton Method",
    "凸优化": "Convex Optimization",
    "拉格朗日乘子法": "Lagrange Multiplier Method",
    "对偶问题": "Dual Problem",
    "收敛": "Convergence",

    # Clustering
    "聚类": "Clustering",
    "质心": "Centroid",
    "轮廓系数": "Silhouette Coefficient",

    # Text processing
    "词袋模型": "Bag of Words",
    "词嵌入": "Word Embedding",
    "词向量": "Word Vector",
    "主题模型": "Topic Model",

    # Recommender systems
    "推荐系统": "Recommender System",
    "协同过滤": "Collaborative Filtering",
    "召回": "Recall/Retrieval",
    "精排": "Ranking",
    "粗排": "Pre-ranking",
    "冷启动": "Cold Start",
    "热度穿透": "Popularity Bias",

    # Spark
    "宽依赖": "Wide Dependency",
    "窄依赖": "Narrow Dependency",
    "弹性分布式数据集": "Resilient Distributed Dataset/RDD",

    # Model types
    "生成模型": "Generative Model",
    "判别模型": "Discriminative Model",
    "概率模型": "Probabilistic Model",
    "参数模型": "Parametric Model",
    "非参数模型": "Non-parametric Model",
    "线性模型": "Linear Model",
    "非线性模型": "Nonlinear Model",

    # Sampling
    "过采样": "Oversampling",
    "欠采样": "Undersampling",
    "上采样": "Upsampling",
    "下采样": "Downsampling",
    "类别不平衡": "Class Imbalance",

    # Other
    "特征": "Feature",
    "标签": "Label",
    "样本": "Sample",
    "训练集": "Training Set",
    "测试集": "Test Set",
    "验证集": "Validation Set",
    "超参数": "Hyperparameter",
    "模型选择": "Model Selection",
    "误差分析": "Error Analysis",
}

# Category name translations (for tags)
CATEGORY_TRANSLATIONS = {
    "基本概念": "BasicConcepts",
    "特征工程": "FeatureEngineering",
    "支持向量机": "SVM",
    "朴素贝叶斯": "NaiveBayes",
    "线性回归": "LinearRegression",
    "逻辑回归": "LogisticRegression",
    "决策树": "DecisionTree",
    "随机森林": "RandomForest",
    "深度学习": "DeepLearning",
    "推荐系统": "RecommenderSystem",
    "概率论": "Probability",
    "统计学": "Statistics",
    "最优化": "Optimization",
    "机器学习": "MachineLearning",
    "经典机器学习": "ClassicalML",
    "基础工具": "Tools",
}


def add_translations(text):
    """Add English translations in parentheses after Chinese terms."""
    result = text
    # Sort by length descending to handle longer terms first
    sorted_terms = sorted(TERM_TRANSLATIONS.keys(), key=len, reverse=True)

    for chinese_term in sorted_terms:
        english_term = TERM_TRANSLATIONS[chinese_term]
        # Only add translation if not already present
        if chinese_term in result and f"{chinese_term}({english_term})" not in result and f"{chinese_term}（{english_term}）" not in result:
            # Check if translation is not already there (avoid duplicate)
            pattern_check = f"{chinese_term}\\s*[（(]{english_term}"
            import re
            if not re.search(pattern_check, result, re.IGNORECASE):
                result = result.replace(chinese_term, f"{chinese_term}({english_term})", 1)

    return result


def get_category_tag(chinese_category):
    """Get English tag name for a Chinese category."""
    return CATEGORY_TRANSLATIONS.get(chinese_category, chinese_category)
