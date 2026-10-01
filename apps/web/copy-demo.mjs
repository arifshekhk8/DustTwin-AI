import { cpSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
for (const name of ['demo', 'reports']) {
  cpSync(fileURLToPath(new URL(`../../${name}`, import.meta.url)), fileURLToPath(new URL(`./dist/${name}`, import.meta.url)), { recursive: true });
}
