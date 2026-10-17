// words.js —— 單字包：全隊共編，進 Git
const WORDS = [
  {en:"algorithm", zh:"演算法"},   {en:"recursion", zh:"遞迴"},
  {en:"vocabulary", zh:"字彙"},    {en:"memorize", zh:"背誦"},
  {en:"efficient", zh:"有效率的"}, {en:"persist", zh:"堅持；持續"},
  {en:"retrieve", zh:"取回；檢索"},{en:"interval", zh:"間隔"},
  {en:"iterate", zh:"迭代；重複"},  {en:"complexity", zh:"複雜度"},
  {en:"optimize", zh:"最佳化"}
];

// 讓 Node（資料檢查）與瀏覽器（App）都能用這個檔案
if (typeof module !== "undefined") module.exports = WORDS;
