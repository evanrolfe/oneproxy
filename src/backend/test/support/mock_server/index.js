const path = require('path');
const express = require('express');

const server = express();
const port = 3000;

const POSTS = [
  {id:1, title:"Hello", body:"World", user_id:1, created_at:"2020-02-05T10:02:49.612Z", updated_at:"2020-02-05T10:02:49.612Z", url:"http://localhost/api/posts/1.json"},
  {id:2, title:"Bye", body:"World", user_id:1, created_at:"2020-02-05T10:02:49.623Z", updated_at:"2020-02-05T10:02:49.623Z", url:"http://localhost/api/posts/2.json"},
  {id:3, title:"Hello", body:"Just a greeting from Bob.", user_id:2, created_at:"2020-02-05T10:02:49.633Z", updated_at:"2020-02-05T10:02:49.633Z", url:"http://localhost/api/posts/3.json"},
  {id:4, title:"Hey", body:"Hey Bob,  how are you?", user_id:3, created_at:"2020-02-05T10:02:49.648Z", updated_at:"2020-02-05T10:02:49.648Z", url:"http://localhost/api/posts/4.json"}
];

const USERS = [
  {id:1, firstName:"Evan", lastName: "Rolfe", email: "evan@gmail.com"},
  {id:2, firstName:"Alice", lastName: "Smith", email: "alice@gmail.com"},
  {id:3, firstName:"Bob", lastName: "Johnson", email: "bob@gmail.com"},
];

server.use('/', express.static(path.join(__dirname, 'frontend')))
server.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});
server.use(express.json());

server.get('/api/posts.json',  (req, res) => {
  res.json(POSTS)
});

server.get('/api/users.json',  (req, res) => {
  res.json(USERS)
});

server.post('/api/posts.json', (req, res) => {
  console.log(`Received POST request with payload: ${JSON.stringify(req.body)}`)
  res.json({message: `Hello, you told us your name is: ${req.body.name}`})
});

server.get('/api/posts/:postId.json',  (req, res) => {
  const { postId } = req.params;
  const post = POSTS.find(p => p.id === parseInt(postId));
  res.json(post)
});

server.get('/api/users/:userId.json',  (req, res) => {
  const { userId } = req.params;
  const user = USERS.find(p => p.id === parseInt(userId));
  res.json(user)
});

server.listen(port, () => console.log(`[MockServer] listening at http://localhost:${port}`));

