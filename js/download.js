async function downloadFile(urls, filename) {
    const fileStream = streamSaver.createWriteStream(filename);
    const writer = fileStream.getWriter();


    for (const url of urls) {
        const response = await fetch(url);
        const reader = response.body.getReader();
        const chunks = [];

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            await writer.write(value);
        }
    }

    writer.close();
}
