from flask import Flask, jsonify, send_from_directory, request  # 导入 Flask 和 jsonify [[1]]
from flask_cors import CORS  # 导入 CORS [[2]]
import os
import frontmatter
import markdown

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持 [[2]]

# 定义存放 Markdown 文件和图片的文件夹路径
CONTENT_FOLDER = os.path.join(os.getcwd(), '../content')
IMGS_FOLDER = os.path.join(CONTENT_FOLDER, 'imgs')
ACTORS_FOLDER = os.path.join(CONTENT_FOLDER, 'actors')

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

def parse_markdown_files():
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
                    "cover": f"/imgs/{post.get('cover')}",
                    "order": post.get('order', float('inf')),
                    "body_html": body_html,  # 添加正文 HTML 字段
                }
                movies.append(movie_data)
    movies.sort(key=lambda x: (x['order'], x['title']))
    return movies

# @app.route('/api/movie/<movie_id>', methods=['GET'])
# def get_movie(movie_id):
#     """
#     API 接口：获取指定影片的详细信息。
#     """
#     print(f"获取影片信息：{movie_id}")
#     movies = parse_markdown_files()
#     movie = next((m for m in movies if m['id'] == movie_id), None)
#     if movie:
#         return jsonify(movie)
#     return jsonify({"error": "Movie not found"}), 404

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """
    API 接口：获取所有影片信息。
    """
    movies = parse_markdown_files()
    
    print(f"获取所有影片信息：{len(movies)} movies")
#    for movie in movies:
#        print(movie)

    return jsonify(movies)


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
            "cover": f"/imgs/{post.get('cover')}",
            "body_html": body_html,
        }
        return jsonify(actor_data)
    

@app.route('/api/update-order', methods=['POST'])
def update_order():
    try:
        data = request.json
        new_order = data.get('order')

        for item in new_order:
            file_path = os.path.join(CONTENT_FOLDER, item['id'])
            if not os.path.exists(file_path):
                return jsonify({"error": f"File not found: {item['id']}"}), 404

            with open(file_path, 'r+', encoding='utf-8') as f:
                post = frontmatter.load(f)
                post['order'] = item['order']
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
        "cover": f"{title.replace(' ', '_')}.jpg",  # 默认封面图片名
    }

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

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
    bio = data.get('bio', '')
    cover = data.get('cover', '')

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
