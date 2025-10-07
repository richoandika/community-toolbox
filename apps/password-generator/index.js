#!/usr/bin/env node

const DEFAULT_LENGTH = 12;
const LETTERS = 'abcdefghijklmnopqrstuvwxyz';
const NUMBERS = '0123456789';
const SYMBOLS = '!@#$%^&*()-_=+[]{};:,.<>?/';

function parseArgs(argv) {
  const options = {
    length: DEFAULT_LENGTH,
    useNumbers: false,
    useSymbols: false,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    switch (arg) {
      case '--length': {
        const value = argv[++i];
        const parsed = Number.parseInt(value, 10);
        if (!Number.isFinite(parsed) || parsed <= 0) {
          throw new Error('length must be a positive integer');
        }
        options.length = parsed;
        break;
      }
      case '--numbers':
        options.useNumbers = true;
        break;
      case '--symbols':
        options.useSymbols = true;
        break;
      case '--help':
      case '-h':
        options.help = true;
        break;
      default:
        throw new Error(`unknown option: ${arg}`);
    }
  }

  return options;
}

function buildCharacterSet({ useNumbers, useSymbols }) {
  let charset = LETTERS + LETTERS.toUpperCase();
  if (useNumbers) {
    charset += NUMBERS;
  }
  if (useSymbols) {
    charset += SYMBOLS;
  }
  return charset;
}

function generatePassword(options) {
  const charset = buildCharacterSet(options);
  if (!charset) {
    throw new Error('no characters available for password generation');
  }

  let password = '';
  const array = new Uint32Array(options.length);
  require('crypto').randomFillSync(array);

  for (let i = 0; i < options.length; i += 1) {
    password += charset[array[i] % charset.length];
  }

  return password;
}

function printHelp() {
  const message = `Usage: password-generator [options]\n\n` +
    `Options:\n` +
    `  --length <n>   Length of the password (default: ${DEFAULT_LENGTH})\n` +
    `  --numbers      Include numeric characters\n` +
    `  --symbols      Include symbol characters\n` +
    `  -h, --help     Show this message`;
  // eslint-disable-next-line no-console
  console.log(message);
}

if (require.main === module) {
  try {
    const options = parseArgs(process.argv);
    if (options.help) {
      printHelp();
      process.exit(0);
    }
    const password = generatePassword(options);
    // eslint-disable-next-line no-console
    console.log(password);
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error(error.message);
    process.exit(1);
  }
}

module.exports = {
  DEFAULT_LENGTH,
  parseArgs,
  generatePassword,
  buildCharacterSet,
};
