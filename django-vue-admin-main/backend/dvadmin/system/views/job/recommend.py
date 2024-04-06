# -*- coding: utf-8 -*-            
# @Time : 2023/10/27 20:00
#  :name 工作推荐
# @FileName: recommend.py
# @Software: PyCharm
import json
import random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from dvadmin.system.views.evaluate.models import Evaluate
from dvadmin.system.views.job.models import Job
from dvadmin.utils.json_response import ErrorResponse, SuccessResponse
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic


def recommend_content(user):
    skill = user.skill
    user_job_title = user.job_title

    GENDER_CHOICES = {
        0: "木工作业",
        1: "砌筑作业",
        2: "抹灰作业",
        3: "油漆作业",
        4: "脚手架作业",
        5: "焊接作业"
    }
    titles = user_job_title.split(",")

    titles = [GENDER_CHOICES[int(title)] for title in titles]

    jobs = Job.objects.all()
    random_len = min(len(jobs) - 1, 20)
    # 随机获取20条工作信息
    job_list = random.sample(list(jobs), random_len)

    # 假设random_objects包含模型对象，使用values_list获取id值
    ids = [obj.id for obj in job_list]
    # 工作名称标题
    job_names = [obj.job_name for obj in job_list]
    job_types = [GENDER_CHOICES[obj.job_type] for obj in job_list]
    # 工作技能资质要求
    job_demands = [obj.job_demand for obj in job_list]
    # job_descriptions = [obj.description for obj in job_list]
    job_descriptions = [obj.description if obj.description is not None else "" for obj in job_list]

    jobs_data = pd.DataFrame({
        'JobID': ids,
        'Title': job_types,
        'Description': job_descriptions,
        'Skills': job_demands
    })

    # 示例工人的个人偏好
    user_preferences = {
        'Skills': skill,
        'Title': ",".join(titles)
    }

    # 创建TF-IDF向量化器
    tfidf_vectorizer = TfidfVectorizer()

    # 合并工作属性文本
    jobs_data['content'] = jobs_data['Title'] + ' ' + jobs_data['Description'] + ' ' + jobs_data['Skills']

    # 计算TF-IDF矩阵
    tfidf_matrix = tfidf_vectorizer.fit_transform(jobs_data['content'])

    # 计算用户的TF-IDF向量
    user_vector = tfidf_vectorizer.transform([user_preferences['Title'] + ' ' + user_preferences['Skills']])

    # 计算余弦相似度
    cosine_sim = linear_kernel(user_vector, tfidf_matrix)

    # 获取相似工作
    similar_jobs = list(enumerate(cosine_sim[0]))
    similar_jobs = sorted(similar_jobs, key=lambda x: x[1], reverse=True)
    # 输出工作推荐-
    print("工作推荐:")
    recommended_jobs = []  # 存储推荐的工作
    for i in range(len(job_list)):  # 前5个推荐
        job_id, similarity = similar_jobs[i]
        job_title = jobs_data['Title'][job_id]
        JobID = jobs_data['JobID'][job_id]

        # print(f"工作 {job_title} (相似度: {similarity:.2f})")

        for obj in job_list:
            if obj.id == JobID:
                obj.commendation_index = f"{similarity:.2f}"
                obj.dept_name = obj.dept.name
                # 将工作添加到推荐列表
                recommended_jobs.append(obj)
    # 对 job_list 按照 commendation_index 进行排序
    job_list = sorted(recommended_jobs, key=lambda x: x.commendation_index, reverse=True)
    serialized_data = [job.to_dict() for job in job_list]

    return SuccessResponse(data=serialized_data, msg="获取成功",limit=20,total=len(job_list))

    # 导入评估指标
    # from sklearn.metrics import accuracy_score, recall_score, f1_score

    # 划分数据集为训练集和测试集
    # train_data, test_data = train_test_split(jobs_data, test_size=0.2)

    # 在训练集上构建TF-IDF矩阵和用户向量
    # tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_data['content'])
    # user_vector_train = tfidf_vectorizer.transform([user_preferences['Title'] + ' ' + user_preferences['Skills']])

    # 在测试集上构建TF-IDF矩阵和用户向量
    # tfidf_matrix_test = tfidf_vectorizer.transform(test_data['content'])
    # user_vector_test = tfidf_vectorizer.transform([user_preferences['Title'] + ' ' + user_preferences['Skills']])

    # 在训练集上计算余弦相似度
    # cosine_sim_train = linear_kernel(user_vector_train, tfidf_matrix_train)

    # 在测试集上计算余弦相似度
    # cosine_sim_test = linear_kernel(user_vector_test, tfidf_matrix_test)

    # 定义一个阈值，超过该阈值的工作被认为是用户喜欢的
    # threshold = 0.5

    # 在训练集上获取用户喜欢的工作的索引
    # liked_jobs_train = np.where(cosine_sim_train > threshold)[1]

    # 在测试集上获取用户喜欢的工作的索引
    # liked_jobs_test = np.where(cosine_sim_test > threshold)[1]

    # 定义一个函数，判断一个工作是否被用户喜欢
    # def is_liked(job_id, liked_jobs):
    #     return 1 if job_id in liked_jobs else 0

    # 在训练集上获取用户对每个工作的喜好标签
    # y_train = [is_liked(job_id, liked_jobs_train) for job_id in train_data['JobID']]

    # 在测试集上获取用户对每个工作的喜好标签
    # y_test = [is_liked(job_id, liked_jobs_test) for job_id in test_data['JobID']]

    # 计算准确率
    # accuracy = accuracy_score(y_test, y_train)

    # 计算召回率
    # recall = recall_score(y_test, y_train)

    # 计算F1分数
    # f1 = f1_score(y_test, y_train)

    # 打印结果
    # print(f"准确率: {accuracy:.2f}")
    # print(f"召回率: {recall:.2f}")
    # print(f"F1分数: {f1:.2f}")


def recommend_mark(user):

    # 查询不是当前用户并且评分不为空的工作评分
    evaluates = Evaluate.objects.filter(mark__isnull=False).exclude(creator_id=user.id).all()
    # # 清除jod
    # evaluates = evaluates.values_list('job_id', flat=True).distinct()
    # 多获取一下评分数据
    random_len = min(len(evaluates), 30)
    # 随机获取random_len条工作信息
    evaluates = random.sample(list(evaluates), random_len)

    # 查询是当前用户并且评分不为空的工作评分 (recommend_mark当前用户一定有过评分)
    user_evaluates = Evaluate.objects.filter(mark__isnull=False,creator_id=user.id).all()
    user_random_len = min(len(evaluates), 10)
    # 随机获取random_len条工作信息
    user_evaluates = random.sample(list(user_evaluates), user_random_len)
    # 确保评分数据中一定有用户的数据
    evaluates = evaluates + user_evaluates
    # print(evaluates)
    # 工人、工作和评分数据
    # 提取工人和工作数据
    # 创建一个空的数据字典，用于存储评分数据
    data_dict = {
        'Worker': [],
        'Job': [],
        'Score': []
    }

    # 遍历JSON数据并转换为示例格式的评分数据
    for entry in evaluates:
        worker_id = entry.creator.id
        job_id = entry.job.id
        score = entry.mark

        # 将评分添加到数据字典中
        data_dict['Worker'].append(str(worker_id))
        data_dict['Job'].append(str(job_id))
        data_dict['Score'].append(score)
    # 创建DataFrame
    df = pd.DataFrame(data_dict)
    df = df.drop_duplicates(subset=['Worker', 'Job'], keep='last')
    # 打印转换后的数据
    # print(df)
    pivot_df = df.pivot(index='Worker', columns='Job', values='Score').reset_index()
    # pivot_df = df.pivot(index='Job', columns='Worker', values='Score').reset_index()

    pivot_df.fillna(0, inplace=True)

    # pivot_df.columns = ['Worker'] + [f'Job{i}' for i in range(1, len(pivot_df.columns) - 1)]
    pivot_df.columns = [col if col != 'Worker' else 'Worker' for col in pivot_df.columns]
    # pivot_df.columns = [col if col != 'Job' else 'Worker' for col in pivot_df.columns]

    # 使用set_index函数来设置'Worker'列作为索引
    pivot_df.set_index('Worker', inplace=True)

    # 将'Worker'列数据添加到字典中
    result_dict = pivot_df.to_dict(orient='list')
    # result_dict['Worker'] = pivot_df.index.tolist()
    result_dict = {'Worker': pivot_df.index.tolist(), **result_dict}
    df = pd.DataFrame(result_dict)

    # 转换数据为Surprise所需的格式
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(df.melt(id_vars='Worker', var_name='Job', value_name='Rating'), reader)

    # 划分数据集为训练集和测试集
    trainset, testset = train_test_split(data, test_size=0.2)

    # 使用KNNBasic算法进行User-Based协同过滤
    sim_options = {'name': 'cosine', 'user_based': True}
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)

    # 使用模型进行推荐
    worker_name = user.id

    recommendations = []
    for job_id in df.columns[1:]:
        predicted_rating = model.predict(worker_name, job_id)
        recommendations.append({'Job': job_id, 'Predicted_Rating': predicted_rating.est})

    # 根据预测评分降序排序工作推荐
    recommendations = sorted(recommendations, key=lambda x: x['Predicted_Rating'], reverse=True)

    # 存储推荐的工作
    recommended_jobs = []

    # 输出工作推荐
    for recommendation in recommendations:
        job_id = recommendation['Job']
        predicted_rating = recommendation['Predicted_Rating']
        # print(f"Job: {job_id} - Predicted Rating: {predicted_rating :.2f}")
        job = Job.objects.get(id=job_id)
        job.commendation_index = f"{predicted_rating:.2f}"
        job.dept_name = job.dept.name
        # 将工作添加到推荐列表
        recommended_jobs.append(job)
        # 对 job_list 按照 commendation_index 进行排序


    job_list = sorted(recommended_jobs, key=lambda x: x.commendation_index, reverse=True)
    serialized_data = [job.to_dict() for job in job_list]

    return SuccessResponse(data=serialized_data, msg="获取成功", limit=20)

    # 导入评估指标
    # from surprise import accuracy

    # 在测试集上进行预测
    # predictions = model.test(testset)

    # 计算RMSE和MAE
    # rmse = accuracy.rmse(predictions)
    # mae = accuracy.mae(predictions)

    # 打印结果
    # print(f"RMSE: {rmse:.2f}")
    # print(f"MAE: {mae:.2f}")

