async function downloadFile(urls, filename) {
    const fileStream = streamSaver.createWriteStream(filename);
    const writer = fileStream.getWriter();

    for (const url of urls) {
        const response = await fetch(url);
        const reader = response.body.getReader();
        const chunks = [];
        let firstChunk;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            if(!firstChunk){
                firstChunk = value;
                await writer.write(firstChunk);
            }
        }

        for (const chunk of chunks) {
            if(chunk !== firstChunk){
                await writer.write(chunk);
            }
        }
    }

    writer.close();
}