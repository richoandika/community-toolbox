const test = require('node:test');
const assert = require('node:assert');
const crypto = require('node:crypto');

const {
  DEFAULT_LENGTH,
  parseArgs,
  generatePassword,
  buildCharacterSet,
} = require('..');

test('parseArgs uses defaults when no arguments provided', () => {
  const options = parseArgs(['node', 'index.js']);
  assert.strictEqual(options.length, DEFAULT_LENGTH);
  assert.strictEqual(options.useNumbers, false);
  assert.strictEqual(options.useSymbols, false);
});

test('parseArgs parses length, numbers, and symbols flags', () => {
  const options = parseArgs(['node', 'index.js', '--length', '16', '--numbers', '--symbols']);
  assert.strictEqual(options.length, 16);
  assert.strictEqual(options.useNumbers, true);
  assert.strictEqual(options.useSymbols, true);
});

test('parseArgs throws for invalid length', () => {
  assert.throws(
    () => parseArgs(['node', 'index.js', '--length', 'nope']),
    /length must be a positive integer/,
  );
});

test('generatePassword produces expected length', () => {
  const original = crypto.randomFillSync;
  crypto.randomFillSync = (array) => {
    for (let i = 0; i < array.length; i += 1) {
      array[i] = i;
    }
    return array;
  };

  try {
    const password = generatePassword({ length: 8, useNumbers: false, useSymbols: false });
    assert.strictEqual(password.length, 8);
  } finally {
    crypto.randomFillSync = original;
  }
});

test('buildCharacterSet includes symbols when requested', () => {
  const charset = buildCharacterSet({ useNumbers: false, useSymbols: true });
  assert.match(charset, /[!@#$%^&*()\-_=+\[\]{};:,.<>?/]/);
});
