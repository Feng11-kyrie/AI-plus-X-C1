// 用 macOS 原生 PDFKit 提取 PDF 文本，输出为 Markdown。
//
// 为什么用 JXA 而不是 Python 库：本项目坚持零第三方依赖。
// macOS 自带 PDFKit，通过 osascript 调用无需安装任何东西。
// 代价是这一步不跨平台——非 macOS 环境会明确报错而不是静默产出空文件。
//
// 用法：osascript -l JavaScript pdfkit_dump.js <输入.pdf> <输出.md>

ObjC.import("PDFKit");
ObjC.import("Foundation");

function run(argv) {
  const src = argv[0];
  const dst = argv[1];

  const doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(src));
  if (doc.isNil()) {
    console.log("ERROR: 无法打开 PDF（文件损坏或路径错误）");
    return 1;
  }

  const pc = Number(doc.pageCount);
  const pages = [];
  for (let p = 0; p < pc; p++) {
    const raw = ObjC.unwrap(doc.pageAtIndex(p).string);
    pages.push(raw === undefined ? "" : raw);
  }

  // PDFKit 对设计类 PDF 会把同一行输出两次（描边层 + 填充层），
  // 且两层字距不同，于是出现「近重复」：
  //   Through inter views with our own Claude Code power users, we've gathered insights
  //   Through interviews with our own Claude Code power users, we've gathered insights
  // 只用精确比较去不掉，必须做模糊比较（去掉全部空白后比对）。
  //
  // 两条安全约束：
  //   1. 只合并**相邻**的模糊重复，不跨越中间的其他行；
  //   2. 长度下限 15 字符——短行（代码里的 }、序号）不参与，
  //      否则代码块中相邻的相同行会被误删，破坏代码保真。
  //
  // 保留哪一版：取**字符最短**的那行。断词伪影会给单词插入多余空格，
  // 因此更短的那版通常才是干净的原文。
  //
  // 规范化必须彻底到「只留字母数字」：同一句话的两次绘制不仅字距不同，
  // 标点也常常不同（we’ve 的弯引号 vs we've 的直引号），
  // 只去空白会漏掉这类近重复。
  const out = [];
  const DEDUP_MIN_LEN = 15;
  const norm = function (s) { return s.toLowerCase().replace(/[^a-z0-9]/g, ""); };

  for (let p = 0; p < pages.length; p++) {
    out.push("<!-- page " + (p + 1) + " -->");
    const lines = pages[p].split("\n");
    let i = 0;
    while (i < lines.length) {
      const t = lines[i].trim();
      if (t.length < DEDUP_MIN_LEN) { out.push(lines[i]); i++; continue; }
      const key = norm(t);
      let j = i + 1;
      while (j < lines.length && lines[j].trim().length >= DEDUP_MIN_LEN
             && norm(lines[j].trim()) === key) j++;
      let best = lines[i];
      for (let k = i + 1; k < j; k++) {
        if (lines[k].length < best.length) best = lines[k];
      }
      out.push(best);
      i = j;
    }
    out.push("");
  }

  const text = out.join("\n");
  $(text).writeToFileAtomicallyEncodingError(dst, true, $.NSUTF8StringEncoding, null);
  console.log("OK pages=" + pc + " chars=" + text.length);
  return 0;
}
