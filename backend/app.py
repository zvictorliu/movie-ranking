from flask import Flask, jsonify, send_from_directory, request  # 导入 Flask 和 jsonify [[1]]
from flask_cors import CORS  # 导入 CORS [[2]]
import os
import frontmatter
import markdown
from pypinyin import lazy_pinyin

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持 [[2]]

# 定义存放 Markdown 文件和图片的文件夹路径
CONTENT_FOLDER = os.path.join(os.getcwd(), '../content')
IMGS_FOLDER = os.path.join(CONTENT_FOLDER, 'imgs')
ACTORS_FOLDER = os.path.join(CONTENT_FOLDER, 'actors')

def parse_movie_files():
    """
    解析 content 文件夹中的所有 Markdown 文件，并返回解析后的数据列表。
    """
    movies = []
    for filename in os.listdir(CONTENT_FOLDER):
        if filename.endswith('.md'):
            file_path = os.path.join(CONTENT_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)  # 使用 frontmatter 解析 Markdown 文件 [[3]]
                body_html = markdown.markdown(post.content)  # 将正文转换为 HTML [[3]]
                body_html = body_html.replace('src="./imgs', 'src="/imgs')  # 替换为绝对路径
                movie_data = {
                    "id": filename,
                    "title": post.get('title', '未知标题'),
                    "actors": post.get('actors', '未知演员'),
                    "tags": post.get('tags', []),
                    "description": post.get('description', '暂无描述'),
                    "cover": f"/imgs/movie-cover/{post.get('cover')}",
                    "order": post.get('order', float('inf')),
                    "rating": post.get('rating', 0),
                    "body_html": body_html,  # 添加正文 HTML 字段
                }
                movies.append(movie_data)
    movies.sort(key=lambda x: (x['order'], x['title']))
    return movies


def parse_actor_files():
    """
    解析 actors 文件夹中的所有 Markdown 文件，并返回解析后的数据列表。
    """
    actors = []
    for filename in os.listdir(ACTORS_FOLDER):
        if filename.endswith('.md'):
            file_path = os.path.join(ACTORS_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                actor_data = {
                    "name": post.get('name', '未知演员'),
                    "birth": post.get('birth', '未知出生日期'),
                    "debut": post.get('debut', '未知出道日期'),
                    "cover": f"/imgs/actor-cover/{post.get('cover')}",
                }
                actors.append(actor_data)
    return actors

def append_mainwork(actor, movie):
    """
    将演员的主要作品添加到演员数据中。
    """
    actor_file = os.path.join(ACTORS_FOLDER, f"{actor}.md")
    if not os.path.exists(actor_file):
        return
    with open(actor_file, 'r+', encoding='utf-8') as f:
        post = frontmatter.load(f)
        body = post.content

        # 查找“主要作品”部分，如果不存在则创建
        if "## 主要作品" not in body:
            body += "\n## 主要作品\n"

        # 检查影片是否已存在于“主要作品”部分
        mainworks_start = body.find("## 主要作品")
        mainworks_section = body[mainworks_start:] if mainworks_start != -1 else ""
        if f"- {movie}" not in mainworks_section:
            body += f"\n- {movie}\n"

        # 写回更新后的内容
        f.seek(0)
        f.write(frontmatter.dumps(post))
        f.write(body)
        f.truncate()
        print(f"Updated {actor}'s main works with {movie}")


# 静态资源路由：提供 imgs 文件夹中的图片
@app.route('/imgs/<path:filename>')
def serve_image(filename):
    """
    提供对 imgs 文件夹中图片的访问。
    """
    print(f"Serving image: {filename}")
    imgs_fd = IMGS_FOLDER
    if not os.path.exists(os.path.join(imgs_fd, filename)):
        imgs_fd = f'{ACTORS_FOLDER}/imgs'
    return send_from_directory(imgs_fd, filename)


@app.route('/api/movies', methods=['GET'])
def get_movies():
    """
    API 接口：获取所有影片信息。
    """
    movies = parse_movie_files()
    
    print(f"获取所有影片信息：{len(movies)} movies")

    return jsonify(movies)

@app.route('/api/actors', methods=['GET'])
def get_actors():
    """
    API 接口：获取所有演员的数据，包括封面路径。
    """
    actors = parse_actor_files()
    print(f"获取所有演员信息：{len(actors)} actors")
    # 姓名的拼音排序
    actors = sorted(actors, key=lambda actor: ''.join(lazy_pinyin(actor['name'])))
    return jsonify(actors), 200

@app.route('/api/tags', methods=['GET'])
def get_tags():
    """
    API 接口：获取所有标签。
    """
    movies = parse_movie_files()
    # 统计标签出现次数
    tag_counts = {}
    for movie in movies:
        tags = movie.get('tags', [])
        for tag in tags:
            if tag not in tag_counts:
                tag_counts[tag] = 0
            tag_counts[tag] += 1

    # 转换为字典列表格式
    tags_list = [{"tag": tag, "count": count} for tag, count in tag_counts.items()]
    
    # 按标签名称排序
    tags_list.sort(key=lambda x: x['tag'])

    print(f"获取所有标签信息：{len(tags_list)} tags")

    return jsonify(tags_list), 200


@app.route('/api/actor/<actor_name>', methods=['GET'])
def get_actor(actor_name):
    """
    API 接口：获取指定演员的详细信息。
    """
    file_path = os.path.join(ACTORS_FOLDER, f"{actor_name}.md")
    if not os.path.exists(file_path):
        return jsonify({"error": "Actor not found"}), 404

    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        body_html = markdown.markdown(post.content)  # 将正文转换为 HTML
        body_html = body_html.replace('src="./imgs', 'src="/imgs')
        actor_data = {
            "name": post.get('name'),
            "birth": post.get('birth'),
            "debut": post.get('debut'),
            "cover": f"/imgs/actor-cover/{post.get('cover')}",
            "body_html": body_html,
        }
        return jsonify(actor_data)
    

@app.route('/api/update-ranking', methods=['POST'])
def update_order():
    try:
        data = request.json
        new_ranking = data.get('ranking')

        for item in new_ranking:
            file_path = os.path.join(CONTENT_FOLDER, item['id'])
            if not os.path.exists(file_path):
                return jsonify({"error": f"File not found: {item['id']}"}), 404

            with open(file_path, 'r+', encoding='utf-8') as f:
                post = frontmatter.load(f)
                post['order'] = item['order']
                post['rating'] = item['rating']
                f.seek(0)
                f.write(frontmatter.dumps(post))
                f.truncate()

        return jsonify({"message": "Order updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/create-movie', methods=['POST'])
def create_movie():
    """
    API 接口：接收前端发送的影片数据并创建 Markdown 文件 [[3]]。
    """
    data = request.json
    title = data.get('title')
    actors = data.get('actors', '')
    tags = data.get('tags', '').split(',')  # 将标签字符串转换为列表
    description = data.get('description', '')
    order = data.get('order', 1)
    rating = data.get('rating', 0)

    # 确保内容文件夹存在
    if not os.path.exists(CONTENT_FOLDER):
        os.makedirs(CONTENT_FOLDER)

    # 生成文件名
    filename = f"{title.replace(' ', '_')}.md"
    file_path = os.path.join(CONTENT_FOLDER, filename)

    # 构建 Markdown 文件内容
    post = frontmatter.Post("")
    post.metadata = {
        "title": title,
        "actors": actors,
        "tags": [tag.strip() for tag in tags if tag.strip()],
        "description": description,
        "order": int(order),  # 默认顺序值为无穷大
        "rating": int(rating),  # 默认评分值为 0
        "cover": f"{title.replace(' ', '_')}.jpg",  # 默认封面图片名
    }

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    for actor in actors.split(','):
        actor = actor.strip()
        if actor:
            append_mainwork(actor, title)

    return jsonify({"success": True, "message": "Movie created successfully"}), 200

@app.route('/api/create-actor', methods=['POST'])
def create_actor():
    """
    API 接口：接收前端发送的演员数据并创建 Markdown 文件 [[1]]。
    """
    data = request.json
    name = data.get('name')
    birth = data.get('birth')
    debut = data.get('debut')
    # bio = data.get('bio', '')
    # cover = data.get('cover', '')

    # 确保演员文件夹存在
    if not os.path.exists(ACTORS_FOLDER):
        os.makedirs(ACTORS_FOLDER)

    # 生成文件名
    filename = f"{name.replace(' ', '_')}.md"
    file_path = os.path.join(ACTORS_FOLDER, filename)

    # 构建 Markdown 文件内容
    post = frontmatter.Post("")
    post.metadata = {
        "name": name,
        "birth": birth,
        "debut": debut,
        "cover": f"{name.replace(' ', '_')}.jpg",  # 默认封面图片名
    }

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    return jsonify({"success": True, "message": "Actor created successfully"}), 200


@app.route('/api/movie/<movie_name>', methods=['GET'])
def get_movie_by_name(movie_name):
    """
    API 接口：根据电影名称获取影片详细信息 [[3]]。
    """
    for filename in os.listdir(CONTENT_FOLDER):
        if filename.endswith('.md'):
            file_path = os.path.join(CONTENT_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                if post.get('title') == movie_name:  # 匹配电影标题 [[3]]
                    body_html = markdown.markdown(post.content)
                    return jsonify({
                        "id": filename,
                        "title": post.get('title'),
                        "actors": post.get('actors', ''),
                        "tags": post.get('tags', []),
                        "description": post.get('description', ''),
                        "cover": f"/imgs/movie-cover/{post.get('cover')}",
                        "rating": post.get('rating', 0),
                        "body_html": body_html,
                    })
    return jsonify({
        "id": None,
        "title": movie_name,
        "actors": '',
        "tags": [],
        "description": '待观看',
        "cover": '/imgs/default_cover.jpg',
        "rating": 0,
        "body_html": '',
    })

@app.route('/api/tags/<tag_name>', methods=['GET'])
def get_movies_by_tag(tag_name):
    """
    API 接口：获取包含指定标签的所有影片。
    """
    movies = parse_movie_files()
    
    # 筛选包含指定标签的影片
    filtered_movies = [movie for movie in movies if tag_name in movie.get('tags', [])]
    
    print(f"获取包含标签 '{tag_name}' 的影片：{len(filtered_movies)} movies")

    return jsonify(filtered_movies), 200

@app.route('/api/update-movie/<id>', methods=['PUT'])
def update_movie(id):
    """
    API 接口：接收前端发送的影片信息，并更新对应的 Markdown 文件。
    """
    data = request.json
    title = data.get('title')
    actors = data.get('actors', '')
    tags = data.get('tags', '').split(',')  # 将标签字符串转换为列表
    description = data.get('description', '')
    rating = data.get('rating', 0)
    file_path = os.path.join(CONTENT_FOLDER, id)

    if not os.path.exists(file_path):
        return jsonify({"success": False, "message": "影片文件不存在"}), 404

    with open(file_path, 'r+', encoding='utf-8') as f:
        post = frontmatter.load(f)
        post['title'] = title
        post['actors'] = actors
        post['tags'] = [tag.strip() for tag in tags if tag.strip()]
        # post['cover'] = data.get('cover', post.get('cover', ''))
        post['description'] = description
        post['rating'] = int(rating)

        f.seek(0)
        f.write(frontmatter.dumps(post))
        f.truncate()

    return jsonify({"success": True, "message": "影片信息更新成功"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
