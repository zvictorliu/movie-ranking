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
POSTS_FOLDER = os.path.join(CONTENT_FOLDER, 'posts')
COVER_FOLDER = '0_Cover'
MOVIE_COVER_FOLDER = f'{COVER_FOLDER}/movie-cover'
ACTOR_COVER_FOLDER = f'{COVER_FOLDER}/actor-cover'

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
                    "cover": f"/imgs/{MOVIE_COVER_FOLDER}/{post.get('cover')}",
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


def process_shortcodes(content, movies_data):
    """
    处理文章内容中的shortcode，将其替换为HTML。
    """
    import re
    
    # 处理 movie shortcode
    def replace_movie_shortcode(match):
        # 提取title参数
        title_match = re.search(r'title="([^"]+)"', match.group(1))
        
        movie_title = title_match.group(1)
        
        # 在movies_data中查找对应的电影
        movie = None
        for m in movies_data:
            if m['title'] == movie_title:
                movie = m
                break
        
        if not movie:
            return f'<div class="movie-not-found">电影 "{movie_title}" 未找到</div>'
        
        movie_card_html = f'<MoviePreview title="{movie["title"]}" />'
        
        return movie_card_html
    
    # 使用正则表达式查找并替换movie shortcode
    content = re.sub(r'\{\{< movie-preview ([^>]+) >\}\}', replace_movie_shortcode, content)
    
    return content


def get_post_by_slug(slug):
    """
    根据slug获取特定的博客文章。
    """
    file_path = os.path.join(POSTS_FOLDER, f"{slug}.md")
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        
        # 获取电影数据用于处理shortcode
        movies_data = parse_movie_files()
        
        # 处理shortcode
        processed_content = process_shortcodes(post.content, movies_data)
        
        # 替换图片路径
        processed_content = processed_content.replace('src="./imgs', 'src="/imgs')
        
        post_data = {
            "slug": slug,
            "title": post.get('title', '未知标题'),
            "date": post.get('date', ''),
            "author": post.get('author', '未知作者'),
            "tags": post.get('tags', []),
            "excerpt": post.get('excerpt', ''),
            "content": processed_content,
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

        # 检查影片是否已存在于“主要作品”部分
        if f"- {movie}" not in mainworks_section:
            # 添加影片到“主要作品”部分
            if mainworks_section.endswith('\n'):
                mainworks_section += f"- {movie}\n"
            else:
                mainworks_section += f"\n- {movie}\n"

        # 组装新的正文
        new_body = before.rstrip('\n') + '\n' + mainworks_section.lstrip('\n')

        # 更新 post.content
        post.content = new_body

        # 写回更新后的内容（只覆盖正文，header 不变）
        f.seek(0)
        f.write(frontmatter.dumps(post))
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
    if not os.path.exists(os.path.join(imgs_fd, filename)):
        imgs_fd = f'{POSTS_FOLDER}/imgs'
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
            "cover": f"/imgs/{ACTOR_COVER_FOLDER}/{post.get('cover')}",
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
        file_path = os.path.join(CONTENT_FOLDER, filename)

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
                save_folder = os.path.join(IMGS_FOLDER, MOVIE_COVER_FOLDER)
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
                save_folder = os.path.join(IMGS_FOLDER, ACTOR_COVER_FOLDER)
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
            "cover": cover_filename,
        }

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        return jsonify({"success": True, "message": "Actor created successfully"}), 200
        
    except Exception as e:
        print(f"创建演员错误: {str(e)}")
        return jsonify({"success": False, "message": f"创建失败: {str(e)}"}), 500


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
                        "cover": f"/imgs/{MOVIE_COVER_FOLDER}/{post.get('cover')}",
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
        
        file_path = os.path.join(CONTENT_FOLDER, id)

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
                save_folder = os.path.join(IMGS_FOLDER, MOVIE_COVER_FOLDER)
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

            f.seek(0)
            f.write(frontmatter.dumps(post))
            f.truncate()

        return jsonify({"success": True, "message": "影片信息更新成功"}), 200
        
    except Exception as e:
        print(f"更新影片错误: {str(e)}")
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
        
        if not name.strip():
            return jsonify({"success": False, "message": "请输入图片名称"}), 400
        
        if not image_type or image_type not in ['actor', 'movie']:
            return jsonify({"success": False, "message": "请选择正确的图片类型"}), 400
        
        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if not file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
            return jsonify({"success": False, "message": "不支持的文件类型"}), 400
        
        # 生成文件名，保持原始文件的后缀，如果存在同名文件则覆盖
        file_extension = os.path.splitext(file.filename)[1].lower()
        filename = name + file_extension
        
        # 根据类型确定保存路径
        if image_type == 'actor':
            save_folder = os.path.join(IMGS_FOLDER, ACTOR_COVER_FOLDER)
        else:  # movie
            save_folder = os.path.join(IMGS_FOLDER, MOVIE_COVER_FOLDER)
        
        # 确保文件夹存在
        os.makedirs(save_folder, exist_ok=True)
        
        # 保存文件（如果存在同名文件则覆盖）
        file_path = os.path.join(save_folder, filename)
        file.save(file_path)
        
        print(f"图片上传成功: {file_path}")
        
        return jsonify({
            "success": True, 
            "message": "图片上传成功",
            "filename": filename,
            "path": f"/imgs/{ACTOR_COVER_FOLDER if image_type == 'actor' else MOVIE_COVER_FOLDER}/{filename}"
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


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
