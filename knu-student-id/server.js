const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.use((req, res) => {
  res.status(404).send('<h1>404 - 페이지를 찾을 수 없습니다</h1>');
});

app.listen(PORT, () => {
  console.log(`🚀 서버가 실행 중입니다! → http://localhost:${PORT}`);
  console.log(`   학생증 페이지: http://localhost:${PORT}`);
});