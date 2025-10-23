from flask import Flask, jsonify, send_from_directory, request  # 导入 Flask 和 jsonify [[1]]
from flask_cors import CORS  # 导入 CORS [[2]]
import os
import frontmatter
from pypinyin import lazy_pinyin
import hashlib

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持 [[2]]

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 简单的用户认证配置（实际项目中应该使用数据库）
USERS = {
    'hector': hash_password('hector0805'),
}

# 定义存放 Markdown 文件和图片的文件夹路径
CONTENT_FOLDER = os.path.join(os.getcwd(), '../content')
MOVIES_FOLDER = os.path.join(CONTENT_FOLDER, 'movies')
ACTORS_FOLDER = os.path.join(CONTENT_FOLDER, 'actors')
POSTS_FOLDER = os.path.join(CONTENT_FOLDER, 'posts')
COVER_FOLDER = 'covers'
MOVIE_COVER_FOLDER = os.path.join(COVER_FOLDER, 'movie-cover')
ACTOR_COVER_FOLDER = os.path.join(COVER_FOLDER, 'actor-cover')
POST_COVER_FOLDER = os.path.join(COVER_FOLDER, 'post-cover')
IMGBED_FOLDER = os.path.join(CONTENT_FOLDER, 'imgbed')

def parse_movie_files():
    """
    解析 content 文件夹中的所有 Markdown 文件，并返回解析后的数据列表。
    """
    movies = []
    for filename in os.listdir(MOVIES_FOLDER):
        if filename.endswith('.md'):
            file_path = os.path.join(MOVIES_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)  # 使用 frontmatter 解析 Markdown 文件 [[3]]
                movie_data = {
                    "id": filename,
                    "title": post.get('title', '未知标题'),
                    "actors": post.get('actors', '未知演员'),
                    "tags": post.get('tags', []),
                    "description": post.get('description', '暂无描述'),
                    "cover": f"/imgs/{MOVIE_COVER_FOLDER}/{post.get('cover')}",
                    "order": post.get('order', float('inf')),
                    "rating": post.get('rating', 0),
                    "body": post.content,  # 只返回原始正文内容
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
                    "favorite": post.get('favorite', 1),  # 默认喜爱度为1
                    "cover": f"/imgs/{ACTOR_COVER_FOLDER}/{post.get('cover')}",
                }
                actors.append(actor_data)
    return actors


def parse_post_files():
    """
    解析 posts 文件夹中的所有 Markdown 文件，并返回解析后的数据列表。
    """
    posts = []
    if not os.path.exists(POSTS_FOLDER):
        return posts
    
    for filename in os.listdir(POSTS_FOLDER):
        if filename.endswith('.md'):
            file_path = os.path.join(POSTS_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                slug = os.path.splitext(filename)[0]  # 去掉.md后缀作为slug
                post_data = {
                    "slug": slug,
                    "title": post.get('title', '未知标题'),
                    "date": post.get('date', ''),
                    "author": post.get('author', '未知作者'),
                    "tags": post.get('tags', []),
                    "excerpt": post.get('excerpt', ''),
                    "content": post.content,
                }
                posts.append(post_data)
    
    # 按日期排序，最新的在前面
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts





def get_post_by_slug(slug):
    """
    根据slug获取特定的博客文章。
    """
    file_path = os.path.join(POSTS_FOLDER, f"{slug}.md")
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        
        post_data = {
            "slug": slug,
            "title": post.get('title', '未知标题'),
            "date": post.get('date', ''),
            "author": post.get('author', '未知作者'),
            "tags": post.get('tags', []),
            "excerpt": post.get('excerpt', ''),
            "content": post.content,
        }
        return post_data

def append_mainwork(actor, movie):
    """
    将演员的主要作品添加到演员数据中，覆盖更新 body 部分，header 不变。
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

        # 拆分正文，定位“主要作品”部分
        mainworks_start = body.find("## 主要作品")
        if mainworks_start != -1:
            before = body[:mainworks_start]
            mainworks_section = body[mainworks_start:]
        else:
            before = body
            mainworks_section = "\n## 主要作品\n"

        # 检查影片是否已存在于"主要作品"部分
        if f"<movie title=\"{movie}\" />" not in mainworks_section:
            # 添加影片到"主要作品"部分，确保有空行间隔
            if not mainworks_section.endswith('\n\n'):
                if mainworks_section.endswith('\n'):
                    mainworks_section += '\n'
                else:
                    mainworks_section += '\n\n'
            mainworks_section += f"<movie title=\"{movie}\" />\n"

        # 组装新的正文
        new_body = before.rstrip('\n') + '\n' + mainworks_section.lstrip('\n')

        # 更新 post.content
        post.content = new_body

        # 写回更新后的内容（只覆盖正文，header 不变）
        f.seek(0)
        f.write(frontmatter.dumps(post))
        f.truncate()
        print(f"Updated {actor}'s main works with {movie}")


@app.route('/imgs/<path:filename>')
def serve_image(filename):
    """
    提供对 imgs 文件夹中图片的访问。
    """
    print(f"Serving image: {filename}")
    search_roots = [
        CONTENT_FOLDER,
        os.path.join(CONTENT_FOLDER, 'imgbed'),
        f'{MOVIES_FOLDER}/imgs',
        f'{ACTORS_FOLDER}/imgs',
        f'{POSTS_FOLDER}/imgs',
    ]

    for root in search_roots:
        if root and os.path.exists(os.path.join(root, filename)):
            return send_from_directory(root, filename)

    # 默认回退到 CONTENT_FOLDER，即使文件不存在也保持原有逻辑
    return send_from_directory(CONTENT_FOLDER, filename)


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
        actor_data = {
            "name": post.get('name'),
            "birth": post.get('birth'),
            "debut": post.get('debut'),
            "favorite": post.get('favorite', 1),  # 默认喜爱度为1
            "cover": f"/imgs/{ACTOR_COVER_FOLDER}/{post.get('cover')}",
            "body": post.content,  # 只返回原始正文内容
        }
        return jsonify(actor_data)
    

@app.route('/api/update-ranking', methods=['POST'])
def update_order():
    try:
        data = request.json
        new_ranking = data.get('ranking')

        for item in new_ranking:
            file_path = os.path.join(MOVIES_FOLDER, item['id'])
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
    API 接口：接收前端发送的影片数据并创建 Markdown 文件，支持图片上传。
    """
    try:
        # 检查是否有文件上传
        has_image = 'image' in request.files and request.files['image'].filename != ''
        
        # 获取表单数据
        title = request.form.get('title', '')
        actors = request.form.get('actors', '')
        tags = request.form.get('tags', '').split(',')  # 将标签字符串转换为列表
        description = request.form.get('description', '')
        order = request.form.get('order', 1)
        rating = request.form.get('rating', 0)

        # 确保内容文件夹存在
        if not os.path.exists(CONTENT_FOLDER):
            os.makedirs(CONTENT_FOLDER)

        # 生成文件名
        filename = f"{title.replace(' ', '_')}.md"
        file_path = os.path.join(MOVIES_FOLDER, filename)

        # 处理封面图片
        cover_filename = f"{title.replace(' ', '_')}.jpg"  # 默认jpg格式
        if has_image:
            file = request.files['image']
            # 检查文件类型
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
                # 使用原始文件的后缀
                file_extension = os.path.splitext(file.filename)[1].lower()
                cover_filename = f"{title.replace(' ', '_')}{file_extension}"
                
                # 保存图片文件
                save_folder = os.path.join(CONTENT_FOLDER, MOVIE_COVER_FOLDER)
                os.makedirs(save_folder, exist_ok=True)
                image_path = os.path.join(save_folder, cover_filename)
                file.save(image_path)
                print(f"影片封面图片保存成功: {image_path}")

        # 构建 Markdown 文件内容
        post = frontmatter.Post("")
        post.metadata = {
            "title": title,
            "actors": actors,
            "tags": [tag.strip() for tag in tags if tag.strip()],
            "description": description,
            "order": int(order),
            "rating": int(rating),
            "cover": cover_filename,
        }

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        for actor in actors.split(','):
            actor = actor.strip()
            if actor:
                append_mainwork(actor, title)

        return jsonify({"success": True, "message": "Movie created successfully"}), 200
        
    except Exception as e:
        print(f"创建影片错误: {str(e)}")
        return jsonify({"success": False, "message": f"创建失败: {str(e)}"}), 500

@app.route('/api/create-actor', methods=['POST'])
def create_actor():
    """
    API 接口：接收前端发送的演员数据并创建 Markdown 文件，支持图片上传。
    """
    try:
        # 检查是否有文件上传
        has_image = 'image' in request.files and request.files['image'].filename != ''
        
        # 获取表单数据
        name = request.form.get('name', '')
        birth = request.form.get('birth', '')
        debut = request.form.get('debut', '')
        favorite = request.form.get('favorite', '1')  # 默认值为1

        # 确保演员文件夹存在
        if not os.path.exists(ACTORS_FOLDER):
            os.makedirs(ACTORS_FOLDER)

        # 生成文件名
        filename = f"{name.replace(' ', '_')}.md"
        file_path = os.path.join(ACTORS_FOLDER, filename)

        # 处理头像图片
        cover_filename = f"{name.replace(' ', '_')}.jpg"  # 默认jpg格式
        if has_image:
            file = request.files['image']
            # 检查文件类型
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
                # 使用原始文件的后缀
                file_extension = os.path.splitext(file.filename)[1].lower()
                cover_filename = f"{name.replace(' ', '_')}{file_extension}"
                
                # 保存图片文件
                save_folder = os.path.join(CONTENT_FOLDER, ACTOR_COVER_FOLDER)
                os.makedirs(save_folder, exist_ok=True)
                image_path = os.path.join(save_folder, cover_filename)
                file.save(image_path)
                print(f"演员头像图片保存成功: {image_path}")

        # 构建 Markdown 文件内容
        post = frontmatter.Post("")
        post.metadata = {
            "name": name,
            "birth": birth,
            "debut": debut,
            "favorite": int(favorite),  # 转换为整数
            "cover": cover_filename,
        }

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        return jsonify({"success": True, "message": "Actor created successfully"}), 200
        
    except Exception as e:
        print(f"创建演员错误: {str(e)}")
        return jsonify({"success": False, "message": f"创建失败: {str(e)}"}), 500


@app.route('/api/create-post', methods=['POST'])
def create_post():
    """
    API 接口：接收前端发送的博客数据并创建 Markdown 文件。
    """
    try:
        # 获取JSON数据
        data = request.get_json()
        
        # 获取表单数据
        slug = data.get('slug', '')
        title = data.get('title', '')
        author = data.get('author', '')
        tags = data.get('tags', [])
        excerpt = data.get('excerpt', '')
        content = data.get('content', '')
        date = data.get('date', '')

        # 确保博客文件夹存在
        if not os.path.exists(POSTS_FOLDER):
            os.makedirs(POSTS_FOLDER)

        # 生成文件名
        filename = f"{slug}.md"
        file_path = os.path.join(POSTS_FOLDER, filename)

        # 构建 Markdown 文件内容
        post = frontmatter.Post(content)
        post.metadata = {
            "title": title,
            "date": date,
            "author": author,
            "tags": tags,
            "excerpt": excerpt,
        }

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        return jsonify({"success": True, "message": "Post created successfully"}), 200
        
    except Exception as e:
        print(f"创建博客错误: {str(e)}")
        return jsonify({"success": False, "message": f"创建失败: {str(e)}"}), 500


@app.route('/api/movie/<movie_name>', methods=['GET'])
def get_movie_by_name(movie_name):
    """
    API 接口：根据电影名称获取影片详细信息 [[3]]。
    """
    for filename in os.listdir(MOVIES_FOLDER):
        if filename.endswith('.md'):
            file_path = os.path.join(MOVIES_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                if post.get('title') == movie_name:  # 匹配电影标题 [[3]]
                    return jsonify({
                        "id": filename,
                        "title": post.get('title'),
                        "actors": post.get('actors', ''),
                        "tags": post.get('tags', []),
                        "description": post.get('description', ''),
                        "cover": f"/imgs/{MOVIE_COVER_FOLDER}/{post.get('cover')}",
                        "rating": post.get('rating', 0),
                        "body": post.content,  # 只返回原始正文内容
                    })
    return jsonify({
        "id": None,
        "title": movie_name,
        "actors": '',
        "tags": [],
        "description": '待观看',
        "cover": '/imgs/default_cover.jpg',
        "rating": 0,
        "body": '',
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
    API 接口：接收前端发送的影片信息，并更新对应的 Markdown 文件，支持图片上传。
    """
    try:
        # 检查是否有文件上传
        has_image = 'image' in request.files and request.files['image'].filename != ''
        
        # 获取表单数据
        title = request.form.get('title', '')
        actors = request.form.get('actors', '')
        tags = request.form.get('tags', '')
        if type(tags) == str:
            tags = tags.split(',')
        description = request.form.get('description', '')
        rating = request.form.get('rating', 0)
        order = request.form.get('order', 1)
        
        file_path = os.path.join(MOVIES_FOLDER, id)

        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "影片文件不存在"}), 404

        # 处理封面图片
        cover_filename = None
        if has_image:
            file = request.files['image']
            # 检查文件类型
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
                # 使用原始文件的后缀
                file_extension = os.path.splitext(file.filename)[1].lower()
                cover_filename = f"{title.replace(' ', '_')}{file_extension}"
                
                # 保存图片文件
                save_folder = os.path.join(CONTENT_FOLDER, MOVIE_COVER_FOLDER)
                os.makedirs(save_folder, exist_ok=True)
                image_path = os.path.join(save_folder, cover_filename)
                file.save(image_path)
                print(f"影片封面图片更新成功: {image_path}")

        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post['title'] = title
            post['actors'] = actors
            post['tags'] = [tag.strip() for tag in tags if tag.strip()]
            if cover_filename:
                post['cover'] = cover_filename
            post['description'] = description
            post['rating'] = int(rating)
            post['order'] = int(order)
            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()

        return jsonify({"success": True, "message": "影片信息更新成功"}), 200
        
    except Exception as e:
        print(f"更新影片错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/update-movie-body/<id>', methods=['PUT'])
def update_movie_body(id):
    """
    API 接口：更新电影的正文内容。
    """
    try:
        data = request.json
        body_content = data.get('body', '')
        
        file_path = os.path.join(MOVIES_FOLDER, id)
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "影片文件不存在"}), 404
        
        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post.content = body_content
            
            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()
        
        return jsonify({"success": True, "message": "正文内容更新成功"}), 200
        
    except Exception as e:
        print(f"更新正文内容错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/update-movie-rating/<id>', methods=['PUT'])
def update_movie_rating(id):
    """
    API 接口：专门用于更新电影的评分，轻量级操作。
    """
    try:
        data = request.json
        rating = data.get('rating', 0)
        
        # 验证评分范围
        if not isinstance(rating, (int, float)) or rating < 0 or rating > 5:
            return jsonify({"success": False, "message": "评分必须在0-5之间"}), 400
        
        file_path = os.path.join(MOVIES_FOLDER, id)
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "影片文件不存在"}), 404
        
        # 只更新评分字段，保持其他字段不变
        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post['rating'] = int(rating)
            
            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()
        
        return jsonify({"success": True, "message": "评分更新成功", "rating": rating}), 200
        
    except Exception as e:
        print(f"更新评分错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/update-actor-body/<actor_name>', methods=['PUT'])
def update_actor_body(actor_name):
    """
    API 接口：更新演员的正文内容。
    """
    try:
        data = request.json
        body_content = data.get('body', '')
        
        file_path = os.path.join(ACTORS_FOLDER, f"{actor_name}.md")
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "演员文件不存在"}), 404
        
        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post.content = body_content
            
            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()
        
        return jsonify({"success": True, "message": "正文内容更新成功"}), 200
        
    except Exception as e:
        print(f"更新演员正文内容错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/update-actor/<actor_name>', methods=['PUT'])
def update_actor(actor_name):
    """
    API 接口：接收前端发送的演员信息，并更新对应的 Markdown 文件，支持图片上传。
    """
    try:
        # 检查是否有文件上传
        has_image = 'image' in request.files and request.files['image'].filename != ''
        
        # 获取表单数据
        name = request.form.get('name', '')
        birth = request.form.get('birth', '')
        debut = request.form.get('debut', '')
        favorite = request.form.get('favorite', '1')  # 默认值为1
        tags = request.form.get('tags', '')
        if type(tags) == str:
            tags = tags.split(',')
        
        file_path = os.path.join(ACTORS_FOLDER, f"{actor_name}.md")

        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "演员文件不存在"}), 404

        # 处理封面图片
        cover_filename = None
        if has_image:
            file = request.files['image']
            # 检查文件类型
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
                # 使用原始文件的后缀
                file_extension = os.path.splitext(file.filename)[1].lower()
                cover_filename = f"{name.replace(' ', '_')}{file_extension}"
                
                # 保存图片文件
                save_folder = os.path.join(CONTENT_FOLDER, ACTOR_COVER_FOLDER)
                os.makedirs(save_folder, exist_ok=True)
                image_path = os.path.join(save_folder, cover_filename)
                file.save(image_path)
                print(f"演员封面图片更新成功: {image_path}")

        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post['name'] = name
            post['birth'] = birth
            post['debut'] = debut
            post['favorite'] = int(favorite)  # 转换为整数
            post['tags'] = [tag.strip() for tag in tags if tag.strip()]
            if cover_filename:
                post['cover'] = cover_filename

            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()

        return jsonify({"success": True, "message": "演员信息更新成功"}), 200
        
    except Exception as e:
        print(f"更新演员错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/update-actor-favorite/<actor_name>', methods=['PUT'])
def update_actor_favorite(actor_name):
    """
    API 接口：更新演员的喜爱度。
    """
    try:
        data = request.json
        favorite = data.get('favorite', 1)
        
        # 验证喜爱度范围
        if not isinstance(favorite, int) or favorite < 1 or favorite > 5:
            return jsonify({"success": False, "message": "喜爱度必须在1-5之间"}), 400
        
        file_path = os.path.join(ACTORS_FOLDER, f"{actor_name}.md")
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "演员文件不存在"}), 404
        
        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post['favorite'] = favorite
            
            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()
        
        return jsonify({"success": True, "message": "喜爱度更新成功"}), 200
        
    except Exception as e:
        print(f"更新演员喜爱度错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/update-post-body/<slug>', methods=['PUT'])
def update_post_body(slug):
    """
    API 接口：更新文章的正文内容。
    """
    try:
        data = request.json
        body_content = data.get('body', '')
        
        file_path = os.path.join(POSTS_FOLDER, f"{slug}.md")
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "文章文件不存在"}), 404
        
        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post.content = body_content
            
            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()
        
        return jsonify({"success": True, "message": "正文内容更新成功"}), 200
        
    except Exception as e:
        print(f"更新文章正文内容错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/update-post/<slug>', methods=['PUT'])
def update_post(slug):
    """
    API 接口：接收前端发送的文章信息，并更新对应的 Markdown 文件，支持图片上传。
    """
    try:
        # 检查是否有文件上传
        has_image = 'image' in request.files and request.files['image'].filename != ''
        
        # 获取表单数据
        title = request.form.get('title', '')
        author = request.form.get('author', '')
        date = request.form.get('date', '')
        excerpt = request.form.get('excerpt', '')
        tags = request.form.get('tags', '')
        if type(tags) == str:
            tags = tags.split(',')
        
        file_path = os.path.join(POSTS_FOLDER, f"{slug}.md")

        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "文章文件不存在"}), 404

        # 处理封面图片
        cover_filename = None
        if has_image:
            file = request.files['image']
            # 检查文件类型
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
                # 使用原始文件的后缀
                file_extension = os.path.splitext(file.filename)[1].lower()
                cover_filename = f"{title.replace(' ', '_')}{file_extension}"
                
                # 保存图片文件
                save_folder = os.path.join(CONTENT_FOLDER, POST_COVER_FOLDER)
                os.makedirs(save_folder, exist_ok=True)
                image_path = os.path.join(save_folder, cover_filename)
                file.save(image_path)
                print(f"文章封面图片更新成功: {image_path}")

        with open(file_path, 'r+', encoding='utf-8') as f:
            post = frontmatter.load(f)
            post['title'] = title
            post['author'] = author
            post['date'] = date
            post['excerpt'] = excerpt
            post['tags'] = [tag.strip() for tag in tags if tag.strip()]
            if cover_filename:
                post['cover'] = cover_filename

            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()

        return jsonify({"success": True, "message": "文章信息更新成功"}), 200
        
    except Exception as e:
        print(f"更新文章错误: {str(e)}")
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """
    API 接口：处理图片上传。
    """
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "没有选择图片文件"}), 400

        file = request.files['image']
        name = request.form.get('name', '')
        image_type = request.form.get('type', '')

        # 验证文件
        if file.filename == '':
            return jsonify({"success": False, "message": "没有选择文件"}), 400

        if not image_type or image_type not in ['actor', 'movie', 'post', 'imgbed']:
            return jsonify({"success": False, "message": "请选择正确的图片类型"}), 400

        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if not file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
            return jsonify({"success": False, "message": "不支持的文件类型"}), 400

        # 生成文件名
        file_extension = os.path.splitext(file.filename)[1].lower()

        # 对于 imgbed 类型，如果没有提供名称则使用原始文件名（不含扩展名）
        if image_type == 'imgbed':
            if not name.strip():
                # 使用原始文件名（不含扩展名）
                name = os.path.splitext(file.filename)[0]
            filename = name + file_extension
        else:
            # 其他类型必须提供名称
            if not name.strip():
                return jsonify({"success": False, "message": "请输入图片名称"}), 400
            filename = name + file_extension

        # 根据类型确定保存路径
        if image_type == 'actor':
            save_folder = os.path.join(CONTENT_FOLDER, ACTOR_COVER_FOLDER)
        elif image_type == 'post':
            save_folder = os.path.join(CONTENT_FOLDER, POST_COVER_FOLDER)
        elif image_type == 'imgbed':
            save_folder = IMGBED_FOLDER
        else:  # movie
            save_folder = os.path.join(CONTENT_FOLDER, MOVIE_COVER_FOLDER)

        # 确保文件夹存在
        os.makedirs(save_folder, exist_ok=True)

        # 保存文件（如果存在同名文件则覆盖）
        file_path = os.path.join(save_folder, filename)
        file.save(file_path)

        print(f"图片上传成功: {file_path}")

        # 确定返回的路径
        if image_type == 'actor':
            return_path = f"/imgs/{ACTOR_COVER_FOLDER}/{filename}"
        elif image_type == 'post':
            return_path = f"/imgs/{POST_COVER_FOLDER}/{filename}"
        elif image_type == 'imgbed':
            return_path = f"/imgs/imgbed/{filename}"
        else:  # movie
            return_path = f"/imgs/{MOVIE_COVER_FOLDER}/{filename}"

        return jsonify({
            "success": True,
            "message": "图片上传成功",
            "filename": filename,
            "path": return_path
        }), 200

    except Exception as e:
        print(f"图片上传错误: {str(e)}")
        return jsonify({"success": False, "message": f"上传失败: {str(e)}"}), 500


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    API 接口：获取所有博客文章列表。
    """
    try:
        posts = parse_post_files()
        return jsonify({
            "success": True,
            "posts": posts
        }), 200
    except Exception as e:
        print(f"获取博客文章列表错误: {str(e)}")
        return jsonify({"success": False, "message": f"获取失败: {str(e)}"}), 500


@app.route('/api/posts/<slug>', methods=['GET'])
def get_post(slug):
    """
    API 接口：根据slug获取特定的博客文章。
    """
    try:
        post = get_post_by_slug(slug)
        if post:
            return jsonify({
                "success": True,
                "post": post
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "文章未找到"
            }), 404
    except Exception as e:
        print(f"获取博客文章错误: {str(e)}")
        return jsonify({"success": False, "message": f"获取失败: {str(e)}"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """
    API 接口：用户登录验证。
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # 验证输入
        if not username or not password:
            return jsonify({
                "success": False,
                "message": "用户名和密码不能为空"
            }), 400
        
        # 验证用户凭据
        if username in USERS:
            # 对输入的密码进行哈希处理
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if USERS[username] == password_hash:
                return jsonify({
                    "success": True,
                    "message": "登录成功",
                    "user": {
                        "username": username,
                        "role": "admin" if username == "admin" else "user"
                    }
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "message": "密码错误"
                }), 401
        else:
            return jsonify({
                "success": False,
                "message": "用户不存在"
            }), 401
            
    except Exception as e:
        print(f"登录错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"登录失败: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
