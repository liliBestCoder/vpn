function downloadFile(urls, filename) {
  // 1. 立即同步创建文件流，保住用户手势
  const fileStream = streamSaver.createWriteStream(filename);
  const writer     = fileStream.getWriter();

  // 2. 真正干活的部分包成 async，但不影响前面的同步调用
  (async () => {
    try {
      for (const url of urls) {
        const res  = await fetch(url);
        const reader = res.body.getReader();
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          await writer.write(value);   // 逐块写
        }
      }
    } catch (e) {
      console.error(e);
    } finally {
      await writer.close();
    }
  })();
}
