const words = require("./words.js");
if (words.length < 2) throw new Error("單字至少要 2 個——抽卡與出題都需要");
const seen = new Set();
for (const w of words){
  if (!w.en || !w.zh) throw new Error("欄位缺漏：" + JSON.stringify(w));
  if (seen.has(w.en)) throw new Error("重複單字：" + w.en);
  seen.add(w.en);
}
console.log("words.js 檢查通過，共 " + words.length + " 字 ✓");
