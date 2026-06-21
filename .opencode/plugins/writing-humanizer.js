/**
 * Writing Humanizer plugin for OpenCode.ai
 *
 * Registers the shared skills/ directory so OpenCode discovers the
 * writing-humanizer skill — no symlinks or manual config edits needed.
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const WritingHumanizerPlugin = async () => {
  // .opencode/plugins/ -> ../../ is the repo root, where the shared skills/ live.
  const skillsDir = path.resolve(__dirname, '../../skills');

  return {
    // Inject the skills path into live config so OpenCode discovers the skill
    // from the shared skills/ dir. Config.get() returns a cached singleton, so
    // this mutation is visible when skills are lazily discovered later.
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) {
        config.skills.paths.push(skillsDir);
      }
    },
  };
};
