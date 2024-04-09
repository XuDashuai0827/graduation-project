import csv
import requests
import time
import base64

# 设置访问令牌和搜索关键词
access_token = '' # github 上找自己的 token
search_keyword = 'stars:2000..2003' # !!!!!!!一轮
per_page = 100  # 每页返回的仓库数量
total_repositories_limit = 100000  # 要获取的仓库数量上限
request_delay = 2  # 请求之间的延迟时间（秒）

# 初始化变量
page = 1 # !!!!!!!!!!
total_repositories = []

# 发起多个 API 请求，获取仓库数据
while len(total_repositories) < total_repositories_limit:
    # 构建 API 请求的 URL
    url = f'https://api.github.com/search/repositories?q={search_keyword}&sort=stars&order=desc&per_page={per_page}&page={page}'

    # 添加请求头部，包括访问令牌
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # 发起 API 请求
    response = requests.get(url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        print(f'************** EPOCH —— star arrange {search_keyword}, page {page} ****************')
        # 解析响应数据
        data = response.json()
        repositories = data['items']
        print(len(repositories))
        for repo in repositories:
            full_name = repo['full_name']
            print(full_name)
            url = f"https://api.github.com/repos/{full_name}/readme"

            # 获取请求该 url 的结果，并转换为 json
            result = requests.get(url, headers=headers)
            readme_data = result.json()
            
            if 'message' in readme_data.keys() and readme_data['message']=="Not Found":
                print("____________notfound____________")
                repository_ids = [[repo['id'],repo['name'],repo['description'],'',repo['stargazers_count'],repo['language'],repo['topics']]]
                total_repositories.extend(repository_ids)
                continue
            
            if ('content' not in readme_data.keys()) and ('message' not in readme_data.keys()):
                print('🎷Notice!!! This project has moved!!!')
                repository_ids = [[repo['id'],repo['name'],repo['description'],'',repo['stargazers_count'],repo['language'],repo['topics']]]
                total_repositories.extend(repository_ids)
                continue

            # 由于 content 内容是 base64 编码过的，所以需要先作解码处理，不然返回的是一堆字母
            # 获取当前页的仓库信息
            repository_ids = [[repo['id'],repo['name'],repo['description'],base64.b64decode(readme_data['content']),repo['stargazers_count'],repo['language'],repo['topics']]]
            total_repositories.extend(repository_ids)
            
        # 检查是否达到了要获取的仓库数量上限
        if len(total_repositories) >= total_repositories_limit:
            break

        # 检查是否还有下一页
        if len(repositories) < per_page:
            break  # 已经获取了所有仓库，退出循环
        else:
            page+=1
            #if page<7:
            #    page += 1  # 继续获取下一页
            #else:
            #    break

        # 延迟暂停
        time.sleep(request_delay)
        
    else:
        print(f"Request failed with status code {response.status_code}")
        break

# 将仓库信息写入 CSV 文件
csv_filename = 'repos_data_2000.csv'
with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    #writer.writerow(['ID','name','description','readme','stars','language','topics'])
    writer.writerows([repo_id for repo_id in total_repositories])

print(f"Data saved to {csv_filename} successfully.")