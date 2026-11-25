'use strict';

// Every sentence a customer can see lives here.
module.exports = {
  slipTitle: 'Packing slip',
  slipThanks: 'Thank you for your order. Every piece is made by hand, so small differences are part of it.',
  slipNoteLabel: 'Your note to us',
  packedSubject: 'Your order is packed',
  packedBody: (name, orderId) =>
    `Hello ${name},\n\nyour order ${orderId} is packed and leaves the studio today.\n\nThe studio`,
};
