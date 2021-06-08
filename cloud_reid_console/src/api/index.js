// eslint-disable-next-line prefer-destructuring
const API_URL = process.env.API_URL;

export const authorize = (username, password) => {
  const url = new URL('/api/v1/authorize', API_URL);

  const form = new FormData();
  form.set('username', username);
  form.set('password', password);

  return fetch(url, {
    method: 'POST',
    body: form,
  })
    .then((resp) => {
      if (!resp.ok) {
        throw new Error(resp.statusText);
      }

      return resp.json();
    })
    .then((resp) => resp.token);
};

export const getGroups = (token) => {
  const url = new URL('/api/v1/groups', API_URL);

  return fetch(url.href, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((resp) => {
      if (!resp.ok) {
        throw new Error(resp.statusText);
      }

      return resp.json();
    })
    .then((resp) => resp.payload);
};

export const getGroup = (token, groupID) => {
  const url = new URL(`/api/v1/groups/${groupID}`, API_URL);

  return fetch(url.href, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((resp) => {
      if (!resp.ok) {
        throw new Error(resp.statusText);
      }

      return resp.json();
    })
    .then((resp) => resp.payload);
};

export const getComments = (token, groupID) => {
  const url = new URL(`/api/v1/groups/${groupID}/comments`, API_URL);

  return fetch(url.href, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((resp) => {
      if (!resp.ok) {
        throw new Error(resp.statusText);
      }

      return resp.json();
    })
    .then((resp) => resp.payload);
};

export const getComment = (token, groupID, commentID) => {
  const url = new URL(`/api/v1/groups/${groupID}/comments/${commentID}`, API_URL);

  return fetch(url.href, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((resp) => {
      if (!resp.ok) {
        throw new Error(resp.statusText);
      }

      return resp.json();
    })
    .then((resp) => resp.payload);
};

export const rateComment = (token, groupID, commentID, rate) => {
  const url = new URL(`/api/v1/groups/${groupID}/comments/${commentID}/rate`, API_URL);

  return fetch(url.href, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ rate }),
  })
    .then((resp) => {
      if (!resp.ok) {
        throw new Error(resp.statusText);
      }

      return resp.json();
    })
    .then((resp) => resp.payload);
};
