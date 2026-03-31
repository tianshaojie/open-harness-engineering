import { readdirSync, statSync, writeFileSync } from "node:fs"
import path from "node:path"

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..")
const repoRoot = path.resolve(root, "..")

const pagesDir = path.join(root, "src/pages")
const componentsDirs = [
  "src/components/ui",
  "src/components/shared",
  "src/components/playground"
]

function listVueFiles(directory) {
  const results = []

  function walk(current) {
    for (const entry of readdirSync(current)) {
      const full = path.join(current, entry)
      const stats = statSync(full)
      if (stats.isDirectory()) {
        walk(full)
      } else if (entry.endsWith(".vue")) {
        results.push(full)
      }
    }
  }

  walk(directory)
  return results.sort()
}

const pages = listVueFiles(pagesDir).map((file) => path.relative(root, file))
const componentFiles = componentsDirs.flatMap((dir) =>
  listVueFiles(path.join(root, dir)).map((file) => path.relative(root, file))
)

const output = [
  "# UI Inventory",
  "",
  `Generated at: \`${new Date().toISOString()}\``,
  "",
  "## Routes",
  "",
  "- `/`",
  "- `/playground`",
  "- `/:pathMatch(.*)*`",
  "",
  "## Pages",
  "",
  ...pages.map((page) => `- \`${page}\``),
  "",
  "## Components",
  "",
  ...componentFiles.map((component) => `- \`${component}\``),
  "",
  "## Notes",
  "",
  "- This inventory is generated and should stay aligned with the scaffold structure.",
  "- Only non-business foundation components are included in this stage."
].join("\n")

const outputPath = path.join(repoRoot, "docs/generated/ui-inventory.md")
writeFileSync(outputPath, `${output}\n`, "utf-8")

console.log(`Generated ${outputPath}`)
