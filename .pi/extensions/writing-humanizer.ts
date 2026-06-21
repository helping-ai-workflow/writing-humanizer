import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

// .pi/extensions/ -> ../.. is the package root, where the shared skills/ live.
const extensionDir = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(extensionDir, "../..");
const skillsDir = resolve(packageRoot, "skills");

// Register the shared skills/ directory so pi discovers the writing-humanizer
// skill on demand — no symlinks, no copies.
export default function writingHumanizerPiExtension(pi: ExtensionAPI) {
	pi.on("resources_discover", async () => ({
		skillPaths: [skillsDir],
	}));
}
