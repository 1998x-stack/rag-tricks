// Generate with Xmind's official SDK. Post-processing adds native navigation/layout metadata.
const fs = require('node:fs');
const path = require('node:path');
const {Topic, RootTopic, Workbook, writeLocalFile} = require('xmind-generator');
const root = path.resolve(__dirname, '../..');
const outlines = JSON.parse(fs.readFileSync(path.join(root, '.build/outline.json'), 'utf8'));
function build(data, isRoot = false) {
  const topic = isRoot ? RootTopic(data.title).sheetTitle(data.title) : Topic(data.title);
  if (data.note) topic.note(data.note);
  if (data.labels) topic.labels(data.labels);
  if (data.children?.length) topic.children(data.children.map(n => build(n)));
  return topic;
}
(async () => {
  await writeLocalFile(Workbook(outlines.map(n => build(n, true))), path.join(root, 'downloads/rag-tricks-detailed.xmind'));
})().catch(e => { console.error(e); process.exitCode = 1; });
