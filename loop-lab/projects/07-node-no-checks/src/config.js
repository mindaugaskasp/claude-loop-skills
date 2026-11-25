'use strict';

const path = require('node:path');

// All settings in one place. Everything can be overridden from the environment.
const config = {
  outDir: process.env.KILN_DESK_OUT || path.join(process.cwd(), 'out'),
  mailApiUrl: process.env.KILN_DESK_MAIL_URL || 'https://mail.example.invalid/v1/send',
  mailApiKey: process.env.KILN_DESK_MAIL_KEY || '',
  mailFrom: process.env.KILN_DESK_MAIL_FROM || 'studio@example.invalid',
  // How many shelf units fit into one firing.
  kilnCapacity: Number(process.env.KILN_DESK_CAPACITY || 24),
};

module.exports = config;
