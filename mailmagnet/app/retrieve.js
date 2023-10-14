import Imap from 'imap';
import { simpleParser } from 'mailparser';
import { inspect } from 'util';

const imap = new Imap({
  user: 'mygmail@gmail.com',
  password: 'mypassword',
  host: 'imap.gmail.com',
  port: 993,
  tls: true
});

const openInbox = (callback) => {
  imap.openBox('INBOX', true, callback);
};

const parse_email = async (body) => {
  let parsed = simpleParser(body);
  // ...............
};

const setupImap = () => {
  imap.once('ready', () => {
    openInbox((err, box) => {
      if (err) throw err;

      imap.search(['UNSEEN', ['SINCE', 'May 20, 2018']], (err, results) => {
        if (err) throw err;
        const f = imap.fetch(results, { bodies: '' });
        f.on('message', (msg, seqno) => {
          console.log('Message #%d', seqno);
          const prefix = '(#' + seqno + ') ';
          msg.on('body', (stream, info) => {
            if (info.which === 'TEXT')
              console.log(prefix + 'Body [%s] found, %d total bytes', inspect(info.which), info.size);
            let buffer = '', count = 0;
            stream.on('data', (chunk) => {
              count += chunk.length;
              buffer += chunk.toString('utf8');
              parse_email(buffer);
              if (info.which === 'TEXT')
                console.log(prefix + 'Body [%s] (%d/%d)', inspect(info.which), count, info.size);
            });
            stream.once('end', () => {
              if (info.which !== 'TEXT')
                console.log(prefix + 'Parsed header: %s', inspect(Imap.parseHeader(buffer)));
              else
                console.log(prefix + 'Body [%s] Finished', inspect(info.which));
            });
          });
          msg.once('attributes', (attrs) => {
            console.log(prefix + 'Attributes: %s', inspect(attrs, false, 8));
          });
          msg.once('end', () => {
            console.log(prefix + 'Finished');
          });
        });

        f.once('error', (err) => {
          console.log('Fetch error: ' + err);
        });

        f.once('end', () => {
          console.log('Done fetching all messages');
          imap.end();
        });
      });
    });
  });

  imap.once('error', (err) => {
    console.log(err);
  });

  imap.once('end', () => {
    console.log('Connection ended');
  });

  imap.connect();
};

export default setupImap;
