const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// 读取 Markdown 文件并解析为 JSON
function loadMovies(folderPath) {
  const files = fs.readdirSync(folderPath); // 获取文件夹中的所有文件
  const movies = [];

  files.forEach((file) => {
    if (path.extname(file) === '.md') {
      const filePath = path.join(folderPath, file);
      const fileContent = fs.readFileSync(filePath, 'utf-8'); // 读取文件内容
      const { data } = matter(fileContent); // 使用 gray-matter 解析 YAML 前置内容 [[6]]
      movies.push({
        id: file, // 使用文件名作为唯一标识
        ...data,
      });
    }
  });

  // 排序规则：按 order 升序排列，如果 order 相同则按 title 排序
  movies.sort((a, b) => {
    if (a.order === b.order) {
      return a.title.localeCompare(b.title); // 按标题字母顺序排序
    }
    return a.order - b.order; // 按序号升序排序
  });

  return movies;
}

// 保存解析后的 JSON 数据到 public 文件夹
const folderPath = './public/movies'; // Markdown 文件所在的文件夹路径
const movies = loadMovies(folderPath);

// 将数据保存为静态文件
fs.writeFileSync('./public/movies.json', JSON.stringify(movies, null, 2));
console.log('Movies data saved to public/movies.json');